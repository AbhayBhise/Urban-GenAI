# outputs/gan/

This directory stores all GAN training outputs:

| File | Description |
|---|---|
| `generator.pth` | Raw Generator checkpoint (saved every 10 epochs) |
| `discriminator.pth` | Discriminator checkpoint |
| `generator_ema.pth` | **EMA-smoothed Generator** — used by `/infer/gan` API |
| `history.json` | Per-epoch D-loss and G-loss for the training dashboard |
| `meta.json` | Hyperparameters: latent_dim, num_classes, epochs_trained, etc. |
| `samples/epoch_XXXX.png` | Sample grids saved every N epochs during training |

## Train the GAN

```bash
cd backend
python train_gan.py --epochs 100 --batch-size 32
```

Options:
- `--epochs`       — total training epochs (default: 100)
- `--batch-size`   — batch size (default: 32)
- `--lr`           — learning rate (default: 2e-4)
- `--d-steps`      — discriminator updates per G update (default: 2)
- `--save-every`   — save sample grid every N epochs (default: 10)
- `--resume`       — resume from existing checkpoints

Requires: `../UCMerced_LandUse/` dataset to be present.
