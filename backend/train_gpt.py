"""Train MiniGPT (models/gpt.py) on the urban-planning corpus.

Char-level, from scratch. Writes:
  ../outputs/gpt/model.pth     model weights
  ../outputs/gpt/meta.json     {config, stoi, itos}
  ../outputs/gpt/history.json  [{"step", "loss", "val_loss"}]

Runs in ~5-10 min on a laptop GPU, longer on CPU.
"""

import os
import json
import time

import torch

from models.gpt import GPTConfig, MiniGPT

CORPUS = os.path.join(os.path.dirname(__file__), "corpus", "urban_planning.txt")
OUT_DIR = "../outputs/gpt"

BLOCK_SIZE = 192
BATCH_SIZE = 64
MAX_STEPS = 3000
EVAL_EVERY = 100
LR = 3e-4


def get_batch(data, device):
    ix = torch.randint(len(data) - BLOCK_SIZE - 1, (BATCH_SIZE,))
    x = torch.stack([data[i:i + BLOCK_SIZE] for i in ix])
    y = torch.stack([data[i + 1:i + 1 + BLOCK_SIZE] for i in ix])
    return x.to(device), y.to(device)


@torch.no_grad()
def estimate_val(model, data, device, iters=20):
    model.eval()
    losses = []
    for _ in range(iters):
        x, y = get_batch(data, device)
        _, loss = model(x, y)
        losses.append(loss.item())
    model.train()
    return sum(losses) / len(losses)


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    os.makedirs(OUT_DIR, exist_ok=True)

    if not os.path.exists(CORPUS):
        raise SystemExit(
            f"Corpus not found at {CORPUS}. Run: python corpus/build_corpus.py"
        )
    text = open(CORPUS, encoding="utf-8").read()
    chars = sorted(set(text))
    stoi = {c: i for i, c in enumerate(chars)}
    itos = {i: c for i, c in enumerate(chars)}
    data = torch.tensor([stoi[c] for c in text], dtype=torch.long)
    n = int(0.9 * len(data))
    train_data, val_data = data[:n], data[n:]
    print(f"Corpus: {len(text):,} chars | vocab {len(chars)}")

    cfg = GPTConfig(vocab_size=len(chars), block_size=BLOCK_SIZE)
    model = MiniGPT(cfg).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"MiniGPT: {n_params/1e6:.2f}M params")

    opt = torch.optim.AdamW(model.parameters(), lr=LR, betas=(0.9, 0.99))

    with open(os.path.join(OUT_DIR, "meta.json"), "w", encoding="utf-8") as f:
        json.dump({"config": cfg.to_dict(), "stoi": stoi,
                   "itos": {str(k): v for k, v in itos.items()}}, f)

    history = []
    model.train()
    start = time.time()
    for step in range(1, MAX_STEPS + 1):
        x, y = get_batch(train_data, device)
        _, loss = model(x, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()

        if step % EVAL_EVERY == 0 or step == 1:
            val_loss = estimate_val(model, val_data, device)
            history.append({"step": step, "loss": loss.item(),
                            "val_loss": val_loss})
            print(f"step {step:4d}/{MAX_STEPS} | train {loss.item():.3f} | "
                  f"val {val_loss:.3f} | {time.time()-start:.0f}s")
            torch.save(model.state_dict(), os.path.join(OUT_DIR, "model.pth"))
            with open(os.path.join(OUT_DIR, "history.json"), "w") as f:
                json.dump(history, f)

    torch.save(model.state_dict(), os.path.join(OUT_DIR, "model.pth"))
    with open(os.path.join(OUT_DIR, "history.json"), "w") as f:
        json.dump(history, f)
    print("MiniGPT training complete.")

    # Quick sample
    prompt = "Context: an IT-corridor ward with about 55% built-up area"
    idx = torch.tensor([[stoi[c] for c in prompt]], dtype=torch.long, device=device)
    out = model.generate(idx, max_new_tokens=300, temperature=0.8, top_k=40)[0]
    print("\n--- sample ---")
    print("".join(itos[i] for i in out.tolist()))


if __name__ == "__main__":
    main()
