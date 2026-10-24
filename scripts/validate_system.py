"""
UrbanGenAI Complete System Validation Protocol
Audits environment, dataset, split integrity, model checkpoints, parameters,
test metrics, generation, and telemetry. Exports outputs/system_validation_report.json.
"""

import os
import sys
import json
import time
import math
import subprocess
from pathlib import Path
from typing import Dict, Any, List

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "backend"))

from backend.splits import load_or_build_split, DATASET_ROOT, URBAN_CLASSES
from backend.models.autoencoder import DenoisingAE
from backend.models.vae import VAE, kl_divergence
from backend.models.classifier import UrbanClassifier
from backend.models.gan import Generator as GANGenerator, Discriminator as GANDiscriminator, LATENT_DIM, NUM_CLASSES
from backend.models.diffusion import DiffusionUNet, DDPM
from backend.models.gpt import MiniGPT, GPTConfig


def calculate_psnr(mse: float) -> float:
    if mse <= 0:
        return float('inf')
    return 10.0 * math.log10(1.0 / mse)


def calculate_ssim(img1: torch.Tensor, img2: torch.Tensor) -> float:
    """Computes basic structural similarity between two [0, 1] batches."""
    C1 = (0.01) ** 2
    C2 = (0.03) ** 2
    mu1 = F.avg_pool2d(img1, 3, 1, 1)
    mu2 = F.avg_pool2d(img2, 3, 1, 1)
    mu1_sq = mu1.pow(2)
    mu2_sq = mu2.pow(2)
    mu1_mu2 = mu1 * mu2
    sigma1_sq = F.avg_pool2d(img1 * img1, 3, 1, 1) - mu1_sq
    sigma2_sq = F.avg_pool2d(img2 * img2, 3, 1, 1) - mu2_sq
    sigma12 = F.avg_pool2d(img1 * img2, 3, 1, 1) - mu1_mu2
    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
    return ssim_map.mean().item()


def count_params(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters())


def run_full_validation() -> Dict[str, Any]:
    print("=" * 80)
    print("           UrbanGenAI System & Model Validation Protocol")
    print("=" * 80)

    report: Dict[str, Any] = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "environment": {},
        "dataset": {},
        "models": {},
        "telemetry": {},
        "summary": {},
    }

    # ---------------------------------------------------------
    # A. Environment Audit
    # ---------------------------------------------------------
    print("\n[A] Auditing Environment...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Git commit info
    git_commit = "Unavailable"
    git_branch = "Unavailable"
    try:
        git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT)).decode().strip()
        git_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=str(REPO_ROOT)).decode().strip()
    except Exception as e:
        git_commit = f"Git error: {e}"

    node_version = "Unavailable"
    npm_version = "Unavailable"
    try:
        node_version = subprocess.check_output(["node", "-v"], shell=True).decode().strip()
        npm_version = subprocess.check_output(["npm", "-v"], shell=True).decode().strip()
    except Exception:
        pass

    report["environment"] = {
        "python_version": sys.version.split()[0],
        "pytorch_version": torch.__version__,
        "device": str(device),
        "cuda_available": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None (CPU Execution)",
        "vram_gb": round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2) if torch.cuda.is_available() else 0.0,
        "git_commit": git_commit,
        "git_branch": git_branch,
        "node_version": node_version,
        "npm_version": npm_version,
    }
    print(f"  Python: {report['environment']['python_version']} | PyTorch: {report['environment']['pytorch_version']}")
    print(f"  Device: {device} | CUDA Available: {report['environment']['cuda_available']}")
    print(f"  Git Commit: {git_commit[:7]} (branch: {git_branch})")

    # ---------------------------------------------------------
    # B. Dataset Audit
    # ---------------------------------------------------------
    print("\n[B] Auditing UCMerced Dataset & Stratified Splits...")
    dataset_exists = DATASET_ROOT.exists()
    classes_found = sorted([d.name for d in DATASET_ROOT.iterdir() if d.is_dir()]) if dataset_exists else []
    total_images = sum(len(list((DATASET_ROOT / c).glob("*.tif"))) for c in classes_found) if dataset_exists else 0

    split_manifest = load_or_build_split(seed=42)
    test_rel_paths = split_manifest["splits"]["test"]
    val_rel_paths = split_manifest["splits"]["val"]
    train_rel_paths = split_manifest["splits"]["train"]

    report["dataset"] = {
        "root_path": str(DATASET_ROOT),
        "exists": dataset_exists,
        "num_classes": len(classes_found),
        "total_images": total_images,
        "classes_valid": classes_found == URBAN_CLASSES,
        "split_counts": {
            "train": len(train_rel_paths),
            "val": len(val_rel_paths),
            "test": len(test_rel_paths),
        },
        "split_seed": split_manifest.get("seed", 42),
    }
    print(f"  Dataset path: {DATASET_ROOT}")
    print(f"  Classes: {len(classes_found)}/21 | Total Images: {total_images}/2100")
    print(f"  Splits (Seed 42): Train={len(train_rel_paths)}, Val={len(val_rel_paths)}, Test={len(test_rel_paths)}")

    # Transforms
    eval_transform_128 = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])
    eval_transform_224 = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # ---------------------------------------------------------
    # C. Model Audits
    # ---------------------------------------------------------

    # 1. Denoising Autoencoder
    print("\n[C.1] Auditing Denoising Autoencoder...")
    ae_path = REPO_ROOT / "outputs" / "ae" / "model.pth"
    ae_model = DenoisingAE().to(device)
    ae_metrics: Dict[str, Any] = {"available": ae_path.exists()}
    if ae_path.exists():
        try:
            ae_model.load_state_dict(torch.load(ae_path, map_location=device, weights_only=True))
            ae_model.eval()
            ae_metrics["loaded"] = True
            ae_metrics["parameters"] = count_params(ae_model)

            # Evaluate on 20 test split samples
            test_samples = [DATASET_ROOT / p for p in test_rel_paths[:20]]
            mses, ssims = [], []
            t0 = time.time()
            with torch.no_grad():
                for p in test_samples:
                    img = Image.open(p).convert("RGB")
                    t_img = eval_transform_128(img).unsqueeze(0).to(device)
                    recon = ae_model(t_img)
                    orig_01 = (t_img * 0.5 + 0.5).clamp(0, 1)
                    recon_01 = (recon * 0.5 + 0.5).clamp(0, 1)
                    mse_val = F.mse_loss(recon_01, orig_01).item()
                    mses.append(mse_val)
                    ssims.append(calculate_ssim(recon_01, orig_01))
            latency = (time.time() - t0) / len(test_samples) * 1000.0
            avg_mse = sum(mses) / len(mses)
            ae_metrics["test_sample_mse"] = round(avg_mse, 6)
            ae_metrics["test_sample_psnr_db"] = round(calculate_psnr(avg_mse), 2)
            ae_metrics["test_sample_ssim"] = round(sum(ssims) / len(ssims), 4)
            ae_metrics["latency_ms_per_tile"] = round(latency, 2)
            print(f"  Parameters: {ae_metrics['parameters']:,} | Checkpoint: Loaded")
            print(f"  Test Sample MSE: {ae_metrics['test_sample_mse']} | PSNR: {ae_metrics['test_sample_psnr_db']} dB | SSIM: {ae_metrics['test_sample_ssim']}")
        except Exception as e:
            ae_metrics["error"] = str(e)
            print(f"  Error loading AE: {e}")
    report["models"]["autoencoder"] = ae_metrics

    # 2. Spatial VAE
    print("\n[C.2] Auditing Spatial Variational Autoencoder (VAE)...")
    vae_path = REPO_ROOT / "outputs" / "vae" / "model.pth"
    vae_model = VAE(latent_channels=64, skip_channels=64, skip0_channels=16).to(device)
    vae_metrics: Dict[str, Any] = {"available": vae_path.exists()}
    if vae_path.exists():
        try:
            vae_model.load_state_dict(torch.load(vae_path, map_location=device, weights_only=True))
            vae_model.eval()
            vae_metrics["loaded"] = True
            vae_metrics["parameters"] = count_params(vae_model)
            vae_metrics["latent_spatial_shape"] = [64, 8, 8]
            vae_metrics["latent_dimensions"] = 64 * 8 * 8

            # Evaluate on 20 test split samples
            test_samples = [DATASET_ROOT / p for p in test_rel_paths[:20]]
            mses, ssims, kls = [], [], []
            t0 = time.time()
            with torch.no_grad():
                for p in test_samples:
                    img = Image.open(p).convert("RGB")
                    t_img = eval_transform_128(img).unsqueeze(0).to(device)
                    recon, mu, logvar = vae_model.reconstruct(t_img)
                    orig_01 = (t_img * 0.5 + 0.5).clamp(0, 1)
                    recon_01 = (recon * 0.5 + 0.5).clamp(0, 1)
                    mse_val = F.mse_loss(recon_01, orig_01).item()
                    mses.append(mse_val)
                    ssims.append(calculate_ssim(recon_01, orig_01))
                    kl_mean, _ = kl_divergence(mu, logvar)
                    kls.append(kl_mean)
            latency = (time.time() - t0) / len(test_samples) * 1000.0
            avg_mse = sum(mses) / len(mses)
            vae_metrics["test_recon_mse"] = round(avg_mse, 6)
            vae_metrics["test_recon_psnr_db"] = round(calculate_psnr(avg_mse), 2)
            vae_metrics["test_recon_ssim"] = round(sum(ssims) / len(ssims), 4)
            vae_metrics["test_kl_divergence"] = round(sum(kls) / len(kls), 2)
            vae_metrics["latency_ms_per_tile"] = round(latency, 2)
            print(f"  Parameters: {vae_metrics['parameters']:,} | Checkpoint: Loaded")
            print(f"  Test Recon MSE: {vae_metrics['test_recon_mse']} | PSNR: {vae_metrics['test_recon_psnr_db']} dB | KL: {vae_metrics['test_kl_divergence']}")
        except Exception as e:
            import traceback
            traceback.print_exc()
            vae_metrics["error"] = str(e)
            print(f"  Error loading VAE: {e}")
    report["models"]["spatial_vae"] = vae_metrics

    # 3. Land-Use Classifier
    print("\n[C.3] Auditing Land-Use Classifier (ResNet18)...")
    clf_path = REPO_ROOT / "outputs" / "transformer" / "model.pth"
    clf_model = UrbanClassifier(num_classes=21).to(device)
    clf_metrics: Dict[str, Any] = {"available": clf_path.exists()}
    if clf_path.exists():
        try:
            clf_model.load_state_dict(torch.load(clf_path, map_location=device, weights_only=True))
            clf_model.eval()
            clf_metrics["loaded"] = True
            clf_metrics["parameters"] = count_params(clf_model)

            # Evaluate test split (all 315 test images across 21 classes)
            all_preds, all_targets = [], []
            t0 = time.time()
            with torch.no_grad():
                for p_rel in test_rel_paths:
                    p = DATASET_ROOT / p_rel
                    cls_name = p.parent.name
                    target = URBAN_CLASSES.index(cls_name)
                    img = Image.open(p).convert("RGB")
                    t_img = eval_transform_224(img).unsqueeze(0).to(device)
                    logits = clf_model(t_img)
                    pred = torch.argmax(logits, dim=1).item()
                    all_preds.append(pred)
                    all_targets.append(target)
            latency = (time.time() - t0) / len(test_rel_paths) * 1000.0

            correct = sum(1 for p, t in zip(all_preds, all_targets) if p == t)
            acc = correct / len(all_targets)
            clf_metrics["test_split_accuracy"] = round(acc * 100.0, 2)
            clf_metrics["test_split_size"] = len(all_targets)
            clf_metrics["latency_ms_per_tile"] = round(latency, 2)
            print(f"  Parameters: {clf_metrics['parameters']:,} | Checkpoint: Loaded")
            print(f"  Held-out Test Split Accuracy: {clf_metrics['test_split_accuracy']}% ({correct}/{len(all_targets)})")
        except Exception as e:
            clf_metrics["error"] = str(e)
            print(f"  Error loading Classifier: {e}")
    report["models"]["classifier"] = clf_metrics

    # 4. Conditional DCGAN
    print("\n[C.4] Auditing Conditional DCGAN...")
    gan_path = REPO_ROOT / "outputs" / "gan" / "generator_ema.pth"
    disc_path = REPO_ROOT / "outputs" / "gan" / "discriminator.pth"
    gan_gen = GANGenerator(latent_dim=LATENT_DIM, num_classes=NUM_CLASSES).to(device)
    gan_disc = GANDiscriminator(num_classes=NUM_CLASSES).to(device)
    gan_metrics: Dict[str, Any] = {"available": gan_path.exists()}
    if gan_path.exists():
        try:
            gan_gen.load_state_dict(torch.load(gan_path, map_location=device, weights_only=True))
            gan_gen.eval()
            gan_metrics["generator_loaded"] = True
            gan_metrics["generator_params"] = count_params(gan_gen)
            if disc_path.exists():
                gan_disc.load_state_dict(torch.load(disc_path, map_location=device, weights_only=True))
                gan_metrics["discriminator_params"] = count_params(gan_disc)

            # Test generation of 5 classes
            z = torch.randn(5, LATENT_DIM, device=device)
            labels = torch.tensor([0, 4, 7, 10, 16], device=device)
            with torch.no_grad():
                gen_tiles = gan_gen(z, labels)
            gan_metrics["generation_output_shape"] = list(gen_tiles.shape)
            gan_metrics["generation_nan"] = torch.isnan(gen_tiles).any().item()
            gan_metrics["fid_status"] = "Requires large-sample benchmark run (torch-fidelity)"
            gan_metrics["kid_status"] = "Requires large-sample benchmark run"
            print(f"  Generator Params: {gan_metrics['generator_params']:,} | Discriminator: {gan_metrics.get('discriminator_params', 0):,}")
            print(f"  Sample generation check: NaN={gan_metrics['generation_nan']}, Shape={gan_metrics['generation_output_shape']}")
        except Exception as e:
            gan_metrics["error"] = str(e)
            print(f"  Error loading GAN: {e}")
    report["models"]["conditional_gan"] = gan_metrics

    # 5. Urban Scenario Diffusion
    print("\n[C.5] Auditing Urban Scenario Diffusion...")
    diff_path = REPO_ROOT / "outputs" / "diffusion_scenario" / "model.pth"
    diff_best_path = REPO_ROOT / "outputs" / "diffusion_scenario" / "model_best.pth"
    diff_unet = DiffusionUNet(base_ch=32, num_classes=len(URBAN_CLASSES), condition_channels=3).to(device)
    diff_model = DDPM(diff_unet, timesteps=1000).to(device)
    diff_metrics: Dict[str, Any] = {
        "available": diff_path.exists(),
        "best_checkpoint_available": diff_best_path.exists(),
    }
    if diff_path.exists():
        try:
            diff_unet.load_state_dict(torch.load(diff_path, map_location=device, weights_only=True))
            diff_model.eval()
            diff_metrics["loaded"] = True
            diff_metrics["parameters"] = count_params(diff_unet)

            # Check DDIM sampling for NaNs across multiple etas
            c = torch.tensor([4], device=device)
            dummy_cond = torch.zeros(1, 3, 128, 128, device=device)
            nan_checks = {}
            for eta in [0.0, 0.2, 0.5, 1.0]:
                out = diff_model.ddim_sample((1, 3, 128, 128), c, steps=5, eta=eta, condition=dummy_cond)
                nan_checks[f"eta_{eta}"] = not torch.isnan(out).any().item()
            diff_metrics["ddim_nan_free_checks"] = nan_checks

            # Load actual training telemetry and history
            hist_path = REPO_ROOT / "outputs" / "diffusion_scenario" / "history.json"
            meta_path = REPO_ROOT / "outputs" / "diffusion_scenario" / "meta.json"
            telem_path = REPO_ROOT / "outputs" / "diffusion_scenario" / "telemetry.json"
            if hist_path.exists() and meta_path.exists() and telem_path.exists():
                hist = json.load(open(hist_path))
                meta = json.load(open(meta_path))
                telem = json.load(open(telem_path))
                diff_metrics["measured_initial_mse"] = round(hist[0]["loss"], 5)
                diff_metrics["measured_final_mse"] = round(meta["final_loss"], 5)
                diff_metrics["measured_best_mse"] = round(meta["best_loss"], 5)
                diff_metrics["training_wall_minutes"] = round(meta["wall_clock_seconds"] / 60.0, 2)
                diff_metrics["average_gpu_power_w"] = round(telem["average_power_w"], 2)
                diff_metrics["peak_gpu_power_w"] = round(telem["peak_power_w"], 2)
                diff_metrics["estimated_energy_wh"] = round(telem["estimated_energy_wh"], 2)

            print(f"  Parameters: {diff_metrics['parameters']:,} | Checkpoint: Loaded")
            print(f"  DDIM Sampler NaN-Free Checks: {diff_metrics['ddim_nan_free_checks']}")
            print(f"  Measured MSE: Initial={diff_metrics.get('measured_initial_mse')}, Final={diff_metrics.get('measured_final_mse')}, Best={diff_metrics.get('measured_best_mse')}")
            print(f"  Measured Energy: {diff_metrics.get('estimated_energy_wh')} Wh ({diff_metrics.get('average_gpu_power_w')} W avg, {diff_metrics.get('training_wall_minutes')} min)")
        except Exception as e:
            diff_metrics["error"] = str(e)
            print(f"  Error loading Diffusion: {e}")
    report["models"]["diffusion_scenario"] = diff_metrics

    # 6. MiniGPT Urban Plan Generator
    print("\n[C.6] Auditing MiniGPT Urban Plan Generator...")
    gpt_path = REPO_ROOT / "outputs" / "gpt" / "model.pth"
    gpt_meta_path = REPO_ROOT / "outputs" / "gpt" / "meta.json"
    gpt_metrics: Dict[str, Any] = {"available": gpt_path.exists()}
    if gpt_path.exists() and gpt_meta_path.exists():
        try:
            with open(gpt_meta_path, encoding="utf-8") as f:
                gpt_meta = json.load(f)
            cfg_dict = gpt_meta["config"]
            cfg = GPTConfig(**cfg_dict)
            gpt_model = MiniGPT(cfg).to(device)
            gpt_model.load_state_dict(torch.load(gpt_path, map_location=device, weights_only=True))
            gpt_model.eval()
            gpt_metrics["loaded"] = True
            gpt_metrics["parameters"] = count_params(gpt_model)
            gpt_metrics["vocab_size"] = cfg.vocab_size
            gpt_metrics["block_size"] = cfg.block_size
            gpt_metrics["n_layer"] = cfg.n_layer
            gpt_metrics["n_head"] = cfg.n_head
            gpt_metrics["n_embd"] = cfg.n_embd

            # Load history
            gpt_hist_path = REPO_ROOT / "outputs" / "gpt" / "history.json"
            if gpt_hist_path.exists():
                h = json.load(open(gpt_hist_path))
                last_step = h[-1]
                gpt_metrics["final_training_loss"] = round(last_step["loss"], 4)
                gpt_metrics["held_out_val_loss"] = round(last_step["val_loss"], 4)
                gpt_metrics["held_out_perplexity"] = round(math.exp(last_step["val_loss"]), 3)
                gpt_metrics["bits_per_character"] = round(last_step["val_loss"] / math.log(2), 4)

            print(f"  Parameters: {gpt_metrics['parameters']:,} | Checkpoint: Loaded")
            print(f"  Held-out Val Loss: {gpt_metrics.get('held_out_val_loss')} | Perplexity: {gpt_metrics.get('held_out_perplexity')} | BPC: {gpt_metrics.get('bits_per_character')}")
        except Exception as e:
            gpt_metrics["error"] = str(e)
            print(f"  Error loading MiniGPT: {e}")
    report["models"]["minigpt_planner"] = gpt_metrics

    # ---------------------------------------------------------
    # D. Energy & Carbon Audit
    # ---------------------------------------------------------
    report["telemetry"] = {
        "diffusion_gpu_board_energy_wh": diff_metrics.get("estimated_energy_wh", "Unavailable"),
        "diffusion_average_power_w": diff_metrics.get("average_gpu_power_w", "Unavailable"),
        "diffusion_peak_power_w": diff_metrics.get("peak_gpu_power_w", "Unavailable"),
        "ae_energy": "Not measured",
        "vae_energy": "Not measured",
        "classifier_energy": "Not measured",
        "gan_energy": "Not measured",
        "gpt_energy": "Not measured",
        "note": "Per rule 1 & 2: Only diffusion has genuinely recorded hardware power samples from nvidia-smi. All other models are unmeasured.",
    }

    # Summary
    all_models_loaded = all(
        report["models"].get(m, {}).get("loaded", False) or report["models"].get(m, {}).get("generator_loaded", False)
        for m in ["autoencoder", "spatial_vae", "classifier", "conditional_gan", "diffusion_scenario", "minigpt_planner"]
    )
    report["summary"] = {
        "all_checkpoints_loaded": all_models_loaded,
        "dataset_integrity_verified": report["dataset"]["classes_valid"] and report["dataset"]["total_images"] == 2100,
        "overall_status": "PASS" if all_models_loaded and report["dataset"]["total_images"] == 2100 else "PARTIAL",
    }

    # Save to outputs/system_validation_report.json
    out_file = REPO_ROOT / "outputs" / "system_validation_report.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 80)
    print(f"Validation finished. Overall status: {report['summary']['overall_status']}")
    print(f"Machine-readable report written to: {out_file}")
    print("=" * 80)

    return report


if __name__ == "__main__":
    run_full_validation()
