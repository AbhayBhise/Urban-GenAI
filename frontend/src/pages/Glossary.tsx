// Glossary component

type Row = { term: string; name: string; meaning: string; model: string; code: string };

function GlossaryTable({ rows }: { rows: Row[] }) {
  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.84rem' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid var(--border)', color: 'var(--muted)', textAlign: 'left' }}>
            <th style={{ padding: '8px 10px', width: '12%' }}>Symbol / Term</th>
            <th style={{ padding: '8px 10px', width: '38%' }}>Full Name &amp; Meaning</th>
            <th style={{ padding: '8px 10px', width: '14%' }}>Used In</th>
            <th style={{ padding: '8px 10px', width: '36%' }}>Where in the Code</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.term} style={{ borderBottom: '1px solid var(--border)', verticalAlign: 'top' }}>
              <td style={{ padding: '10px', fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--accent)', fontSize: '0.95rem' }}>{r.term}</td>
              <td style={{ padding: '10px', color: 'var(--text)' }}>{r.meaning}</td>
              <td style={{ padding: '10px', color: 'var(--accent2)', fontWeight: 600 }}>{r.model}</td>
              <td style={{ padding: '10px', color: 'var(--muted)', fontFamily: 'var(--font-mono)', fontSize: '0.78rem' }}>{r.code}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const LATENT: Row[] = [
  { term: 'μ', name: 'Mean', meaning: 'Mean (mu) — the center of the VAE’s approximate posterior distribution over the latent code. One of two outputs of the encoder.', model: 'VAE', code: 'backend/models/vae.py — mu_head; encode() returns (mu, logvar)' },
  { term: 'σ² / log σ²', name: 'Variance / Log-Variance', meaning: 'Sigma-squared — the variance of the latent posterior. The network predicts log σ² rather than σ² directly, since exp() of any real number is always positive — a standard trick for numerical stability.', model: 'VAE', code: 'backend/models/vae.py — logvar_head; logvar = torch.clamp(logvar, -20, 20)' },
  { term: 'σ', name: 'Standard Deviation', meaning: 'Sigma — the square root of the variance; computed on the fly during sampling as std = exp(0.5 · log σ²).', model: 'VAE', code: 'backend/models/vae.py — reparameterize(): std = torch.exp(0.5*logvar)' },
  { term: 'ε', name: 'Epsilon', meaning: 'A fresh random sample drawn from a standard normal distribution N(0,I) on every forward pass — the actual source of randomness in the reparameterization trick.', model: 'VAE', code: 'backend/models/vae.py — reparameterize(): eps = torch.randn_like(std)' },
  { term: 'z', name: 'Latent Vector / Noise', meaning: 'An overloaded symbol with two different meanings by model: in the VAE, z is the sampled encoding of a specific real image (z = μ + σ⊙ε). In the GAN, z is pure random noise with no relation to any real image — the Generator’s only input alongside the class label.', model: 'VAE + GAN', code: 'backend/models/vae.py (reparameterize); backend/models/gan.py — LATENT_DIM=128, Generator.forward(z, labels)' },
  { term: '⊙', name: 'Hadamard Product', meaning: 'Element-wise multiplication of two vectors/tensors (position-by-position) — not matrix multiplication.', model: 'VAE', code: 'z = μ + σ⊙ε, in reparameterize()' },
  { term: 'β', name: 'Beta (KL weight)', meaning: 'A scalar hyperparameter controlling how strongly the KL-divergence term is weighted in the total loss. Kept near-zero (~1e-4) here after measuring that larger values (β≥0.02) collapse the model on this dataset.', model: 'VAE', code: 'backend/train_vae.py — BETA_TARGET = 0.0001' },
  { term: 'α', name: 'Alpha (blend factor)', meaning: 'A blend weight between 0 and 1 used to linearly interpolate between two latent vectors: (1−α)·μ₀ + α·μ₁.', model: 'VAE', code: 'backend/api.py — infer_vae_interpolate(): alphas = torch.linspace(0,1,8)' },
  { term: 'KL', name: 'Kullback-Leibler Divergence', meaning: 'A measure of how different one probability distribution is from another. Here: how far the encoder’s learned posterior has drifted from the fixed prior.', model: 'VAE', code: 'backend/models/vae.py — kl_divergence()' },
  { term: 'q(z|x)', name: 'Approximate Posterior', meaning: 'The distribution over latent z that the encoder produces for a given input x — approximated as a diagonal Gaussian defined by μ and log σ².', model: 'VAE', code: 'backend/models/vae.py — encode()' },
  { term: 'N(0, I)', name: 'Standard Multivariate Normal', meaning: 'A Gaussian distribution with mean vector 0 and identity covariance — the fixed "prior" the VAE’s posterior is regularized toward.', model: 'VAE', code: 'implicit in the KL-divergence formula' },
];

const LOSSES: Row[] = [
  { term: 'MSE', name: 'Mean Squared Error', meaning: 'Average of squared pixel-wise differences between two images. Penalizes large errors heavily; famously rewards "average" (blurry) predictions.', model: 'AE, VAE, Anomaly', code: 'backend/train_ae.py — F.mse_loss(); backend/api.py — score_anomaly()' },
  { term: 'L1', name: 'L1 Loss (Mean Absolute Error)', meaning: 'Average of absolute pixel-wise differences. Preserves edges/boundaries better than MSE and is less dominated by outliers.', model: 'VAE', code: 'backend/train_vae.py — 0.7·F.l1_loss(recon, imgs)' },
  { term: 'BCE', name: 'Binary Cross-Entropy', meaning: 'A loss function for a yes/no decision — here, "is this image real or fake."', model: 'GAN', code: 'backend/train_gan.py — nn.BCEWithLogitsLoss()' },
  { term: 'PSNR', name: 'Peak Signal-to-Noise Ratio', meaning: 'An image-quality metric in decibels, derived from MSE: 10·log₁₀(peak²/MSE). Higher = closer to the original.', model: 'AE, VAE', code: 'backend/api.py — psnr = 10*math.log10(4.0/mse)' },
  { term: 'SSIM', name: 'Structural Similarity Index Measure', meaning: 'An image-quality metric (0–1) comparing local luminance, contrast, and structure between two images — more perceptually meaningful than raw pixel difference.', model: 'VAE evaluation', code: 'backend/api.py — compute_ssim()' },
  { term: 'z-score', name: 'Standard Score', meaning: 'How many standard deviations a value sits from the mean of a reference distribution. Here: how unusual a tile’s reconstruction error is versus 294 real tiles.', model: 'VAE anomaly detection', code: 'backend/api.py — score_anomaly()' },
];

const ACTIVATIONS: Row[] = [
  { term: 'ReLU', name: 'Rectified Linear Unit', meaning: 'max(0, x) — the most common neural-network activation function.', model: 'AE decoder', code: 'backend/models/autoencoder.py' },
  { term: 'LeakyReLU', name: 'Leaky ReLU', meaning: 'Like ReLU but allows a small negative slope instead of a hard zero, which helps gradients flow through the Discriminator.', model: 'GAN Discriminator', code: 'backend/models/gan.py' },
  { term: 'GELU', name: 'Gaussian Error Linear Unit', meaning: 'A smoother alternative to ReLU used in modern Transformers, including the original GPT.', model: 'MiniGPT', code: 'backend/models/gpt.py — Block.mlp' },
  { term: 'Tanh', name: 'Hyperbolic Tangent', meaning: 'Squashes output to [-1, 1], matching this project’s normalized image range — the final activation of every image-generating decoder.', model: 'AE, VAE, GAN', code: "each model's final decoder layer" },
  { term: 'Softmax', name: 'Softmax', meaning: 'Converts a vector of raw scores (logits) into a probability distribution that sums to 1.', model: 'Classifier, MiniGPT', code: 'backend/api.py — F.softmax(); backend/models/gpt.py — generate()' },
];

const NORMALIZATION: Row[] = [
  { term: 'BatchNorm', name: 'Batch Normalization', meaning: 'Normalizes activations across a training batch, stabilizing and speeding up training.', model: 'AE, GAN Generator', code: 'backend/models/autoencoder.py; backend/models/gan.py' },
  { term: 'LayerNorm', name: 'Layer Normalization', meaning: 'Normalizes activations across the feature dimension for each token independently of batch size — the standard choice in Transformers.', model: 'MiniGPT', code: 'backend/models/gpt.py — Block.ln1, ln2, ln_f' },
  { term: 'Spectral Norm', name: 'Spectral Normalization', meaning: 'Constrains a layer’s weight matrix so its largest singular value is bounded, stabilizing adversarial training and helping prevent mode collapse.', model: 'GAN Discriminator', code: 'backend/models/gan.py — nn.utils.spectral_norm()' },
  { term: 'EMA', name: 'Exponential Moving Average', meaning: 'A running average of a model’s weights over training, updated slightly at every step — smoother and typically higher-quality than the raw weights at any single step.', model: 'GAN', code: 'backend/train_gan.py — EMA class' },
];

const ABBREVIATIONS: Row[] = [
  { term: 'AE', name: 'Autoencoder', meaning: 'An encoder-decoder network trained to reconstruct its own (denoised) input.', model: 'AE', code: 'backend/models/autoencoder.py' },
  { term: 'VAE', name: 'Variational Autoencoder', meaning: 'An autoencoder with a probabilistic latent space, regularized toward a prior distribution via KL divergence.', model: 'VAE', code: 'backend/models/vae.py' },
  { term: 'GAN', name: 'Generative Adversarial Network', meaning: 'Two networks — a Generator and a Discriminator — trained against each other.', model: 'GAN', code: 'backend/models/gan.py' },
  { term: 'DCGAN', name: 'Deep Convolutional GAN', meaning: 'The standard convolutional Generator/Discriminator recipe for GANs (Radford et al., 2015).', model: 'GAN', code: "backend/models/gan.py — module docstring" },
  { term: 'CNN', name: 'Convolutional Neural Network', meaning: 'A network built from convolutional layers — the basis of every encoder/decoder in this project.', model: 'AE, VAE, GAN, Classifier', code: 'throughout backend/models/' },
  { term: 'ResNet18', name: 'Residual Network (18 layers)', meaning: 'A CNN architecture using "skip"/residual connections around each block, pretrained on ImageNet and reused here via transfer learning.', model: 'AE, VAE, Classifier', code: "torchvision.models.resnet18(weights='IMAGENET1K_V1')" },
  { term: 'GPT', name: 'Generative Pre-trained Transformer', meaning: 'The decoder-only, autoregressive Transformer family this project’s MiniGPT is architecturally modeled on.', model: 'MiniGPT', code: 'backend/models/gpt.py' },
  { term: 'LM Head', name: 'Language-Modeling Head', meaning: 'The final linear layer mapping hidden state to vocabulary logits — here, weight-tied to the token-embedding matrix.', model: 'MiniGPT', code: 'backend/models/gpt.py — self.head' },
  { term: 'FC', name: 'Fully Connected (layer)', meaning: 'A dense linear layer connecting every input to every output.', model: 'Classifier', code: 'backend/models/classifier.py — self.model.fc' },
];

const CONCEPTS: Row[] = [
  { term: 'Embedding', name: 'Embedding', meaning: 'A learned lookup table mapping a discrete id (a class label, a character) to a dense vector.', model: 'GAN (class), MiniGPT (token + position)', code: 'backend/models/gan.py — nn.Embedding; backend/models/gpt.py — tok_emb, pos_emb' },
  { term: 'Reparameterization trick', name: 'Reparameterization Trick', meaning: 'Rewriting a random sample as a deterministic function of a fixed-distribution noise input (z = μ + σ⊙ε), so gradients can flow through what would otherwise be a non-differentiable random draw.', model: 'VAE', code: 'backend/models/vae.py — reparameterize()' },
  { term: 'Posterior collapse', name: 'Posterior Collapse', meaning: 'A VAE failure mode where the KL term dominates and the latent z becomes uninformative — the decoder learns to ignore it. Measured here to occur at β≥0.02.', model: 'VAE', code: 'documented in backend/train_vae.py comments' },
  { term: 'Mode collapse', name: 'Mode Collapse', meaning: 'A GAN failure mode where the Generator produces only a limited variety of outputs regardless of input noise.', model: 'GAN', code: 'mitigated via spectral norm + label smoothing, backend/models/gan.py' },
  { term: 'Autoregressive', name: 'Autoregressive Generation', meaning: 'Generating a sequence one element at a time, each new element conditioned on everything generated so far.', model: 'MiniGPT', code: 'backend/models/gpt.py — generate()' },
  { term: 'Causal mask', name: 'Causal (Attention) Mask', meaning: 'A mask preventing a position from attending to future positions, making a Transformer valid for left-to-right generation instead of bidirectional encoding.', model: 'MiniGPT', code: 'backend/models/gpt.py — self.mask = torch.tril(...)' },
  { term: 'Label smoothing', name: 'Label Smoothing', meaning: 'Replacing hard 0/1 training targets with softer values (0.9/0.1 here) to prevent a discriminator from becoming overconfident.', model: 'GAN', code: 'backend/train_gan.py — real_targets=0.9, fake_targets=0.1' },
];

export default function Glossary() {
  return (
    <div>
      <div className="panel-header">
        <h1 className="panel-title">Glossary &amp; Notation Reference</h1>
        <div className="panel-desc">
          Every symbol, formula, and abbreviation used across the four model pages — its full
          name, what it means, which model it belongs to, and exactly where it lives in the code.
          Some symbols (like <code>z</code>) mean different things in different models — that's
          called out explicitly rather than glossed over.
        </div>
      </div>

      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">Latent-Space Notation (μ, σ, z, β, KL…)</div>
        <GlossaryTable rows={LATENT} />
      </div>

      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">Loss Functions &amp; Evaluation Metrics</div>
        <GlossaryTable rows={LOSSES} />
      </div>

      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">Activation Functions</div>
        <GlossaryTable rows={ACTIVATIONS} />
      </div>

      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">Normalization &amp; Training-Stability Techniques</div>
        <GlossaryTable rows={NORMALIZATION} />
      </div>

      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">Model &amp; Architecture Abbreviations</div>
        <GlossaryTable rows={ABBREVIATIONS} />
      </div>

      <div className="card">
        <div className="card-title">Other Concepts &amp; Failure Modes</div>
        <GlossaryTable rows={CONCEPTS} />
      </div>
    </div>
  );
}
