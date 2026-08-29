# UrbanGen AI

> **A Multi-Model Generative AI Framework for Sustainable Smart City Planning and Digital Twin Generation**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-orange?logo=pytorch)](https://pytorch.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Phase%201%20%E2%80%94%20Architecture-yellow)]()

---

## Project Vision

**UrbanGen AI** is an open-source, AI-assisted sustainable urban planning platform. It combines real-world geospatial satellite imagery, land-cover maps, elevation data, road networks, and population density to generate data-driven city plans that are both environmentally sustainable and human-centred.

The long-term vision is a fully automated pipeline that ingests real geospatial data, encodes spatial semantics with deep neural networks, and generates, evaluates, and explains candidate city plans — using a multi-model stack of Autoencoders, VAEs, GANs, Prediction Models, Large Language Models, and Diffusion Models.

---

## Current Status

> **⚠️ Phase 1 — Project Architecture & Real Geospatial Data Pipeline**

This repository is currently in **Phase 1**. The project architecture, directory structure, configuration system, and geospatial data pipeline skeleton are being established.

**What exists now:**
- ✅ Full repository structure and Python package skeleton
- ✅ Configuration system (cities, datasets, model defaults)
- ✅ Data pipeline module stubs (HLS, WorldCover, OSM, SRTM, WorldPop)
- ✅ GIS utility stubs (AOI management, CRS handling, raster/vector ops)
- ✅ Preprocessing module stubs
- ✅ Data fusion and patch extraction stubs

**What is NOT yet implemented:**
- ❌ HLS Autoencoder (Phase 9)
- ❌ VAE (Phase 10)
- ❌ GAN (Phase 11)
- ❌ Prediction Models (Phase 12)
- ❌ LLM Planning Engine (Phase 13)
- ❌ Diffusion Visualization (Phase 14)
- ❌ Evaluation Engine (Phase 15)

---

## Planned Architecture

```
Real Geospatial Data
        │
        ├── NASA HLS S30 (Multispectral Satellite Imagery)
        ├── ESA WorldCover (Land-Use / Land-Cover)
        ├── OpenStreetMap (Roads, Buildings, POIs)
        ├── NASA SRTM (Elevation & Terrain)
        └── WorldPop (Population Density)
        │
        ▼
Geospatial Preprocessing & Multi-Source Alignment
        │
        ▼
HLS Multispectral Autoencoder
        │
        ▼
Urban Latent Representation
        │
        ├── VAE → Candidate Urban Plans
        ├── GAN → Urban Structure Generation
        │
        ▼
Prediction Models
        │
        ├── Traffic Prediction
        ├── Air Quality Index (AQI)
        ├── Flood Risk Assessment
        ├── Energy Consumption
        └── Water Resource Estimation
        │
        ▼
Evaluation Engine
        │
        ▼
LLM Planning & Explanation
        │
        ▼
Diffusion Model Visualization
        │
        ▼
Recommended Sustainable City Plan
```

---

## Datasets

| Dataset | Provider | Purpose |
|---|---|---|
| **HLS S30** | NASA | 30m-resolution multispectral satellite imagery — primary Autoencoder input |
| **WorldCover** | ESA | 10m-resolution global land-use / land-cover semantics |
| **OpenStreetMap** | OSM Community | Roads, buildings, hospitals, schools, parks, POIs and public infrastructure |
| **SRTM** | NASA | 30m-resolution elevation and terrain data |
| **WorldPop** | WorldPop / Univ. of Southampton | 100m-resolution population density grids |

---

## Technology Stack

| Category | Tools |
|---|---|
| **Language** | Python 3.10+ |
| **Deep Learning** | PyTorch, torchvision |
| **Remote Sensing** | Google Earth Engine (GEE), Rasterio, GDAL |
| **Geospatial** | GeoPandas, Shapely, PyProj, OSMnx |
| **Data Science** | NumPy, Pandas, Scikit-learn, SciPy |
| **Visualization** | Matplotlib, Seaborn, Folium |
| **Configuration** | PyYAML, python-dotenv |
| **Experiment Tracking** | Weights & Biases (optional) |
| **Testing** | Pytest |
| **Code Quality** | Ruff, Black, MyPy |

---

## Project Structure

```
UrbanGenAI/
│
├── configs/            # YAML configuration files (cities, datasets, models)
├── src/urbangen/       # Main Python package
│   ├── config/         # Settings and config loading
│   ├── data/           # Dataset downloaders and loaders
│   ├── gis/            # GIS utilities (AOI, CRS, raster, vector ops)
│   ├── preprocessing/  # Per-dataset preprocessing pipelines
│   ├── fusion/         # Multi-source data alignment and stacking
│   ├── patches/        # Patch extraction for model training
│   ├── models/         # Neural network models (Autoencoder, VAE, GAN…)
│   ├── evaluation/     # Evaluation metrics
│   └── utils/          # Logging, file I/O, validation helpers
│
├── scripts/            # CLI entry points for each pipeline stage
├── data/               # Local data storage (NEVER committed to GitHub)
│   ├── raw/            # Raw downloaded datasets
│   ├── processed/      # Preprocessed datasets
│   ├── aligned/        # Multi-source aligned data
│   ├── patches/        # Training/validation/test patch datasets
│   └── manifests/      # Dataset metadata and split manifests
├── models/             # Saved model checkpoints (NEVER committed)
├── experiments/        # Training logs, results (NEVER committed)
├── docs/               # Technical documentation
├── tests/              # Automated tests
└── notebooks/          # Optional Jupyter notebooks for exploration
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/disha-satpute/UrbanGenAI.git
cd UrbanGenAI
```

### 2. Create and activate a virtual environment

```bash
# Using venv
python -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate
```

### 3. Install the package in editable mode

```bash
pip install -e ".[dev]"
```

Or install from `requirements.txt` directly:

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your credentials (GEE service account, NASA Earthdata, etc.)
```

### 5. Authenticate Google Earth Engine (first-time only)

```python
import ee
ee.Authenticate()
ee.Initialize(project="your-gee-project-id")
```

---

## Development Roadmap

| Phase | Description | Status |
|---|---|---|
| **Phase 1** | Repository architecture + data pipeline skeleton | ✅ In Progress |
| **Phase 2** | NASA HLS S30 — download, validation, preprocessing | 🔜 Planned |
| **Phase 3** | ESA WorldCover — download and preprocessing | 🔜 Planned |
| **Phase 4** | OpenStreetMap — road network and POI extraction | 🔜 Planned |
| **Phase 5** | NASA SRTM — elevation preprocessing | 🔜 Planned |
| **Phase 6** | WorldPop — population density preprocessing | 🔜 Planned |
| **Phase 7** | Multi-source geospatial data alignment | 🔜 Planned |
| **Phase 8** | Patch dataset creation (train/val/test splits) | 🔜 Planned |
| **Phase 9** | HLS Multispectral Autoencoder | 🔜 Planned |
| **Phase 10** | Variational Autoencoder (VAE) | 🔜 Planned |
| **Phase 11** | Generative Adversarial Network (GAN) | 🔜 Planned |
| **Phase 12** | Prediction Models (Traffic, AQI, Flood, Energy, Water) | 🔜 Planned |
| **Phase 13** | LLM Planning and Natural Language Explanation | 🔜 Planned |
| **Phase 14** | Diffusion Model Visualization | 🔜 Planned |
| **Phase 15** | Evaluation Engine + End-to-End Integration | 🔜 Planned |

---

## Responsible AI

UrbanGen AI is designed with responsible AI principles in mind:

- **Human Oversight**: AI-generated urban plans are recommendations only. All outputs require review and approval by qualified urban planners, architects, and policymakers.
- **Planning Uncertainty**: Model outputs reflect learned statistical patterns from historical data and should not be treated as definitive predictions.
- **Data Quality**: Results are directly affected by the quality, resolution, and coverage of the underlying geospatial datasets.
- **Geospatial Bias**: Training data is limited to specific cities and regions, which may introduce geographic and demographic biases in generated plans.
- **Privacy**: WorldPop and OSM data used in this project are aggregated at the grid/region level. No individual-level personal data is collected or used.
- **Model Limitations**: Deep learning models may fail to generalise across cities with different climatic, cultural, and infrastructural contexts.
- **Non-Authoritative Recommendations**: Outputs from UrbanGen AI are intended to assist human decision-making — not replace it. No output from this system should be directly implemented without proper regulatory and professional review.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Citation

If you use UrbanGen AI in your research, please cite this repository:

```bibtex
@software{UrbanGenAI2026,
  author  = {Satpute, Disha},
  title   = {UrbanGen AI: A Multi-Model Generative AI Framework for Sustainable Smart City Planning},
  year    = {2026},
  url     = {https://github.com/disha-satpute/UrbanGenAI}
}
```

---

*Built with ❤️ for sustainable cities.*
