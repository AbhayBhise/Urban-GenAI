"""
Lightweight Denoising Diffusion Probabilistic Model (DDPM) for 128x128 aerial imagery synthesis.
Designed for consumer-grade GPU execution (e.g. RTX 4050 6GB) with DDIM fast sampling.

The UrbanGenAI scenario variant receives the uploaded source tile as a
spatial condition in addition to the land-use class. This preserves the
scene-conditioned planning objective instead of generating an unrelated tile.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F

def get_timestep_embedding(timesteps: torch.Tensor, embedding_dim: int) -> torch.Tensor:
    """Sinusoidal positional embeddings for diffusion timesteps."""
    half_dim = embedding_dim // 2
    emb = math.log(10000) / (half_dim - 1)
    emb = torch.exp(torch.arange(half_dim, dtype=torch.float32, device=timesteps.device) * -emb)
    emb = timesteps.float()[:, None] * emb[None, :]
    emb = torch.cat([torch.sin(emb), torch.cos(emb)], dim=1)
    if embedding_dim % 2 == 1:
        emb = F.pad(emb, (0, 1))
    return emb

class ResidualBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, time_dim: int, num_classes: int = 21):
        super().__init__()
        self.norm1 = nn.GroupNorm(8, in_channels)
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, padding=1)
        
        self.time_proj = nn.Linear(time_dim, out_channels)
        self.class_emb = nn.Embedding(num_classes, out_channels)
        
        self.norm2 = nn.GroupNorm(8, out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, padding=1)
        
        if in_channels != out_channels:
            self.shortcut = nn.Conv2d(in_channels, out_channels, 1)
        else:
            self.shortcut = nn.Identity()

    def forward(self, x: torch.Tensor, t_emb: torch.Tensor, c_emb: torch.Tensor) -> torch.Tensor:
        h = self.conv1(F.silu(self.norm1(x)))
        cond = self.time_proj(F.silu(t_emb)) + self.class_emb(c_emb)
        h = h + cond[:, :, None, None]
        h = self.conv2(F.silu(self.norm2(h)))
        return h + self.shortcut(x)

class DownBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, time_dim: int):
        super().__init__()
        self.res = ResidualBlock(in_channels, out_channels, time_dim)
        self.down = nn.Conv2d(out_channels, out_channels, 4, stride=2, padding=1)

    def forward(self, x: torch.Tensor, t_emb: torch.Tensor, c_emb: torch.Tensor):
        x = self.res(x, t_emb, c_emb)
        skip = x
        x = self.down(x)
        return x, skip

class UpBlock(nn.Module):
    def __init__(self, in_channels: int, skip_channels: int, out_channels: int, time_dim: int):
        super().__init__()
        self.up = nn.ConvTranspose2d(in_channels, in_channels // 2, 4, stride=2, padding=1)
        self.res = ResidualBlock((in_channels // 2) + skip_channels, out_channels, time_dim)

    def forward(self, x: torch.Tensor, skip: torch.Tensor, t_emb: torch.Tensor, c_emb: torch.Tensor):
        x = self.up(x)
        x = torch.cat([x, skip], dim=1)
        x = self.res(x, t_emb, c_emb)
        return x

class DiffusionUNet(nn.Module):
    """UNet for noise prediction with optional spatial image conditioning."""
    def __init__(self, in_channels: int = 3, out_channels: int = 3, base_ch: int = 64,
                 num_classes: int = 21, condition_channels: int = 0):
        super().__init__()
        time_dim = base_ch * 4
        self.time_mlp = nn.Sequential(
            nn.Linear(base_ch, time_dim),
            nn.SiLU(),
            nn.Linear(time_dim, time_dim)
        )
        self.time_dim = base_ch
        
        self.condition_channels = condition_channels
        self.init_conv = nn.Conv2d(in_channels + condition_channels, base_ch, 3, padding=1)
        
        # 128 -> 64 -> 32 -> 16
        self.down1 = DownBlock(base_ch, base_ch * 2, time_dim)      # skip1: base_ch * 2 (128x128 -> 64x64)
        self.down2 = DownBlock(base_ch * 2, base_ch * 4, time_dim)  # skip2: base_ch * 4 (64x64 -> 32x32)
        self.down3 = DownBlock(base_ch * 4, base_ch * 4, time_dim)  # skip3: base_ch * 4 (32x32 -> 16x16)
        
        self.mid_res1 = ResidualBlock(base_ch * 4, base_ch * 4, time_dim, num_classes=num_classes)
        self.mid_res2 = ResidualBlock(base_ch * 4, base_ch * 4, time_dim, num_classes=num_classes)
        
        # 16 -> 32 -> 64 -> 128
        self.up3 = UpBlock(in_channels=base_ch * 4, skip_channels=base_ch * 4, out_channels=base_ch * 4, time_dim=time_dim) # 16->32: up (4->2), cat skip 4 -> total 6*base_ch -> out 4*base_ch
        self.up2 = UpBlock(in_channels=base_ch * 4, skip_channels=base_ch * 4, out_channels=base_ch * 2, time_dim=time_dim) # 32->64: up (4->2), cat skip 4 -> total 6*base_ch -> out 2*base_ch
        self.up1 = UpBlock(in_channels=base_ch * 2, skip_channels=base_ch * 2, out_channels=base_ch, time_dim=time_dim)     # 64->128: up (2->1), cat skip 2 -> total 3*base_ch -> out 1*base_ch
        
        self.out_norm = nn.GroupNorm(8, base_ch)
        self.out_conv = nn.Conv2d(base_ch, out_channels, 3, padding=1)

    def forward(self, x: torch.Tensor, t: torch.Tensor, c: torch.Tensor,
                condition: torch.Tensor | None = None) -> torch.Tensor:
        t_emb = get_timestep_embedding(t, self.time_dim)
        t_emb = self.time_mlp(t_emb)
        
        if self.condition_channels:
            if condition is None:
                raise ValueError("An image condition is required for the scenario diffusion model")
            if condition.shape[1] != self.condition_channels or condition.shape[-2:] != x.shape[-2:]:
                raise ValueError("Condition must match the configured channels and spatial size")
            x = torch.cat([x, condition], dim=1)
        h = self.init_conv(x)
        h, skip1 = self.down1(h, t_emb, c)
        h, skip2 = self.down2(h, t_emb, c)
        h, skip3 = self.down3(h, t_emb, c)
        
        h = self.mid_res1(h, t_emb, c)
        h = self.mid_res2(h, t_emb, c)
        
        h = self.up3(h, skip3, t_emb, c)
        h = self.up2(h, skip2, t_emb, c)
        h = self.up1(h, skip1, t_emb, c)
        
        out = self.out_conv(F.silu(self.out_norm(h)))
        return out

class DDPM(nn.Module):
    """Gaussian Diffusion process wrapper with DDPM / DDIM sampler."""
    def __init__(self, unet: nn.Module, timesteps: int = 1000, beta_start: float = 1e-4, beta_end: float = 0.02):
        super().__init__()
        self.unet = unet
        self.timesteps = timesteps
        
        betas = torch.linspace(beta_start, beta_end, timesteps)
        alphas = 1.0 - betas
        alphas_cumprod = torch.cumprod(alphas, dim=0)
        alphas_cumprod_prev = F.pad(alphas_cumprod[:-1], (1, 0), value=1.0)
        
        self.register_buffer('betas', betas)
        self.register_buffer('alphas', alphas)
        self.register_buffer('alphas_cumprod', alphas_cumprod)
        self.register_buffer('alphas_cumprod_prev', alphas_cumprod_prev)
        self.register_buffer('sqrt_alphas_cumprod', torch.sqrt(alphas_cumprod))
        self.register_buffer('sqrt_one_minus_alphas_cumprod', torch.sqrt(1.0 - alphas_cumprod))
        
        # Calculations for posterior q(x_{t-1} | x_t, x_0)
        posterior_variance = betas * (1.0 - alphas_cumprod_prev) / (1.0 - alphas_cumprod)
        self.register_buffer('posterior_variance', posterior_variance)

    def q_sample(self, x_start: torch.Tensor, t: torch.Tensor, noise: torch.Tensor = None) -> torch.Tensor:
        if noise is None:
            noise = torch.randn_like(x_start)
        sqrt_alphas = self.sqrt_alphas_cumprod[t].view(-1, 1, 1, 1)
        sqrt_one_minus_alphas = self.sqrt_one_minus_alphas_cumprod[t].view(-1, 1, 1, 1)
        return sqrt_alphas * x_start + sqrt_one_minus_alphas * noise

    def compute_loss(self, x_start: torch.Tensor, c: torch.Tensor,
                     condition: torch.Tensor | None = None) -> torch.Tensor:
        b = x_start.shape[0]
        t = torch.randint(0, self.timesteps, (b,), device=x_start.device).long()
        noise = torch.randn_like(x_start)
        x_noisy = self.q_sample(x_start=x_start, t=t, noise=noise)
        predicted_noise = self.unet(x_noisy, t, c, condition=condition)
        return F.mse_loss(predicted_noise, noise)

    @torch.no_grad()
    def ddim_sample(self, shape, c: torch.Tensor, steps: int = 20, eta: float = 0.0,
                    condition: torch.Tensor | None = None) -> torch.Tensor:
        """Fast deterministic/low-variance sampling (DDIM) for interactive generation."""
        device = self.betas.device
        b = shape[0]
        times = torch.linspace(0, self.timesteps - 1, steps, dtype=torch.long, device=device)
        times = list(reversed(times.tolist()))
        
        img = torch.randn(shape, device=device)
        
        for i, t in enumerate(times):
            t_batch = torch.full((b,), t, device=device, dtype=torch.long)
            eps = self.unet(img, t_batch, c, condition=condition)
            
            alpha_bar = self.alphas_cumprod[t]
            alpha_bar_prev = self.alphas_cumprod[times[i + 1]] if i < len(times) - 1 else torch.tensor(1.0, device=device)
            
            # Predict x_0
            pred_x0 = (img - torch.sqrt(1.0 - alpha_bar) * eps) / torch.sqrt(alpha_bar)
            pred_x0 = pred_x0.clamp(-1.0, 1.0)
            
            # Direction pointing to x_t
            dir_xt = torch.sqrt(1.0 - alpha_bar_prev - eta**2) * eps
            
            # Noise
            noise = torch.randn_like(img) if eta > 0 and i < len(times) - 1 else 0.0
            
            img = torch.sqrt(alpha_bar_prev) * pred_x0 + dir_xt + eta * noise
            
        return img.clamp(-1.0, 1.0)
