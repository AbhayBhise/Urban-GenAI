"""Train the UrbanGenAI class-conditional diffusion generator.

The available UCMerced data has no paired before/after planning labels. The
reproducible training objective therefore learns conditioned reconstruction and
class semantics; future-land-use transformation claims remain out of scope
until paired municipal scenario data is available.
"""

import os
import json
import time
import math
import subprocess
import threading
import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from PIL import Image

from dataset import get_split_dataloaders, URBAN_CLASSES
from models.diffusion import DiffusionUNet, DDPM

OUTPUT_DIR = '../outputs/diffusion_class_conditional'
os.makedirs(OUTPUT_DIR, exist_ok=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class GpuTelemetry:
    """Collect real GPU power samples when nvidia-smi exposes them."""
    def __init__(self, interval_seconds=2.0):
        self.interval_seconds = interval_seconds
        self.samples = []
        self._stop = threading.Event()
        self._thread = None

    @staticmethod
    def read_power_watts():
        try:
            raw = subprocess.check_output(
                ['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'],
                stderr=subprocess.DEVNULL, text=True, timeout=2,
            ).strip().splitlines()[0]
            return float(raw.strip())
        except Exception:
            return None

    def _sample_loop(self):
        started = time.perf_counter()
        while not self._stop.is_set():
            watts = self.read_power_watts()
            if watts is not None:
                self.samples.append({'elapsed_sec': time.perf_counter() - started, 'power_w': watts})
            self._stop.wait(self.interval_seconds)

    def start(self):
        if device.type == 'cuda':
            self._thread = threading.Thread(target=self._sample_loop, daemon=True)
            self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=3)

    def summary(self):
        if len(self.samples) < 2:
            return {'available': False, 'reason': 'nvidia-smi power telemetry unavailable', 'samples': self.samples}
        energy_wh = 0.0
        for previous, current in zip(self.samples, self.samples[1:]):
            dt_hours = (current['elapsed_sec'] - previous['elapsed_sec']) / 3600.0
            energy_wh += ((previous['power_w'] + current['power_w']) / 2.0) * dt_hours
        watts = [s['power_w'] for s in self.samples]
        return {
            'available': True,
            'samples': self.samples,
            'sample_count': len(self.samples),
            'average_power_w': sum(watts) / len(watts),
            'peak_power_w': max(watts),
            'estimated_energy_wh': energy_wh,
        }


def write_training_graphs(history, telemetry):
    """Persist auditable loss, time, and energy plots beside the checkpoint."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
        epochs = [row['epoch'] for row in history]
        axes[0].plot(epochs, [row['loss'] for row in history], color='#087f8c', linewidth=2)
        axes[0].set_title('Diffusion noise-prediction loss')
        axes[0].set_xlabel('Epoch'); axes[0].set_ylabel('MSE'); axes[0].grid(alpha=0.25)
        axes[1].plot(epochs, [row['elapsed_sec'] / 60.0 for row in history], color='#6941c6', linewidth=2)
        axes[1].set_title('Cumulative wall-clock time')
        axes[1].set_xlabel('Epoch'); axes[1].set_ylabel('Minutes'); axes[1].grid(alpha=0.25)
        if telemetry.get('available'):
            axes[2].plot([s['elapsed_sec'] / 60.0 for s in telemetry['samples']], [s['power_w'] for s in telemetry['samples']], color='#c2185b', linewidth=1.5)
            axes[2].set_title(f"GPU power · {telemetry['estimated_energy_wh']:.2f} Wh")
            axes[2].set_xlabel('Minutes'); axes[2].set_ylabel('Watts')
        else:
            axes[2].text(0.5, 0.5, 'GPU power telemetry unavailable', ha='center', va='center')
            axes[2].set_axis_off()
        axes[2].grid(alpha=0.25)
        fig.tight_layout()
        fig.savefig(os.path.join(OUTPUT_DIR, 'training_metrics.png'), dpi=160)
        plt.close(fig)
    except Exception as exc:
        with open(os.path.join(OUTPUT_DIR, 'graph_error.txt'), 'w', encoding='utf-8') as f:
            f.write(str(exc))


def train_diffusion(epochs: int = 50, batch_size: int = 32, lr: float = 2e-4, fresh: bool = False):
    print(f"--- Starting Urban Scenario DDPM Training on {device} for {epochs} epochs (batch size {batch_size}) ---")
    torch.manual_seed(2026)
    if device.type == 'cuda':
        torch.cuda.manual_seed_all(2026)
        torch.backends.cudnn.benchmark = True
    dataloader, _, _ = get_split_dataloaders(batch_size=batch_size, size=128, num_workers=0, train_aug=True)

    unet = DiffusionUNet(base_ch=32, num_classes=len(URBAN_CLASSES), condition_channels=0).to(device)
    resume_path = os.path.join(OUTPUT_DIR, 'model_best.pth')
    history_path = os.path.join(OUTPUT_DIR, 'history.json')
    history = []

    if fresh:
        print("Fresh training requested: ignoring existing checkpoints and starting from epoch 1.")
    elif os.path.exists(resume_path):
        unet.load_state_dict(torch.load(resume_path, map_location=device, weights_only=True))
        print(f"Resuming class-conditional diffusion weights from {resume_path}")
        if os.path.exists(history_path):
            with open(history_path, encoding='utf-8') as history_file:
                history = json.load(history_file)

    ddpm = DDPM(unet=unet, timesteps=1000).to(device)

    optimizer = torch.optim.AdamW(unet.parameters(), lr=lr, weight_decay=1e-4)
    lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)
    use_amp = device.type == 'cuda'
    scaler = torch.amp.GradScaler('cuda', enabled=use_amp)
    best_loss = min((row.get('loss', math.inf) for row in history), default=math.inf)
    start_epoch = len(history) + 1
    start_time = time.perf_counter()
    telemetry = GpuTelemetry()
    telemetry.start()
    for epoch in range(start_epoch, epochs + 1):
        ddpm.train()
        total_loss = 0.0
        n_batches = 0
        for imgs, labels in dataloader:
            imgs = imgs.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)
            optimizer.zero_grad()
            with torch.autocast(device_type='cuda', dtype=torch.float16, enabled=use_amp):
                loss = ddpm.compute_loss(imgs, labels)
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(unet.parameters(), 1.0)
            scaler.step(optimizer)
            scaler.update()
            total_loss += loss.item()
            n_batches += 1
        lr_scheduler.step()
        avg_loss = total_loss / max(1, n_batches)
        elapsed_sec = time.perf_counter() - start_time
        history.append({
            "epoch": epoch,
            "loss": float(avg_loss),
            "lr": float(optimizer.param_groups[0]['lr']),
            "elapsed_sec": float(elapsed_sec),
            "batches": n_batches,
        })
        if avg_loss < best_loss:
            best_loss = avg_loss
            torch.save(unet.state_dict(), os.path.join(OUTPUT_DIR, 'model_best.pth'))
        if epoch % 5 == 0 or epoch == epochs:
            elapsed = elapsed_sec / 60.0
            print(f"Epoch [{epoch}/{epochs}] - Loss: {avg_loss:.5f} - Elapsed: {elapsed:.1f}m")
            # Save checkpoint
            torch.save(unet.state_dict(), os.path.join(OUTPUT_DIR, 'model.pth'))
            with open(os.path.join(OUTPUT_DIR, 'history.json'), 'w') as f:
                json.dump(history, f, indent=2)
    telemetry.stop()
    telemetry_summary = telemetry.summary()
    write_training_graphs(history, telemetry_summary)
    with open(os.path.join(OUTPUT_DIR, 'telemetry.json'), 'w') as f:
        json.dump(telemetry_summary, f, indent=2)
    with open(os.path.join(OUTPUT_DIR, 'meta.json'), 'w') as f:
        json.dump({
            "model": "urban_landuse_class_conditional_ddpm",
            "dataset": "UCMerced LandUse",
            "split": "stratified train split from backend/splits.py",
            "epochs_trained": epochs,
            "timesteps": 1000,
            "conditioning": "target land-use class only; generation starts from Gaussian noise",
            "sampling": "DDIM",
            "sampling_steps": 20,
            "device": str(device),
            "best_loss": best_loss,
            "final_loss": history[-1]['loss'] if history else None,
            "wall_clock_seconds": history[-1]['elapsed_sec'] if history else None,
            "energy_telemetry": telemetry_summary,
        }, f, indent=2)
    print(f"DDPM Training finished successfully. best_loss={best_loss:.6f} final_loss={history[-1]['loss']:.6f}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Train Urban Scenario DDPM")
    parser.add_argument("--epochs", type=int, default=50, help="Number of epochs (default: 50)")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size (default: 32)")
    parser.add_argument("--lr", type=float, default=2e-4, help="Learning rate (default: 2e-4)")
    parser.add_argument("--fresh", action="store_true", help="Start fresh from epoch 1")
    args = parser.parse_args()
    train_diffusion(epochs=args.epochs, batch_size=args.batch_size, lr=args.lr, fresh=args.fresh)
