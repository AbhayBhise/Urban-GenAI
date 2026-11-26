# 📦 Dataset Sources — UrbanGen AI

## 1. Vision Dataset: UCMerced LandUse (Used by Denoising AE & Spatial β-VAE)

- **Name:** UC Merced Land Use Dataset (21-class aerial remote sensing imagery)
- **Size:** 2,100 RGB images (100 images per class × 21 classes, originally `256×256`, resized to `128×128`)
- **Official Source:** http://weegee.vision.ucmerced.edu/datasets/UCMerced_LandUse.zip
- **Hugging Face Link:** https://huggingface.co/datasets/MashriqueIslam/UCMerced_LandUse
- **Kaggle Link:** https://www.kaggle.com/datasets/apollo2506/landuse-scene-classification
- **Classes (21):** `agricultural`, `airplane`, `baseballdiamond`, `beach`, `buildings`, `chaparral`, `denseresidential`, `forest`, `freeway`, `golfcourse`, `harbor`, `intersection`, `mediumresidential`, `mobilehomepark`, `overpass`, `parkinglot`, `river`, `runway`, `sparseresidential`, `storagetanks`, `tenniscourt`

---

## 2. Text Corpus: Pune Urban Planning Corpus (Used by MiniGPT Transformer)

- **File Included Locally:** [`urban_planning.txt`](urban_planning.txt) (`241,400` bytes / ~241 KB)
- **GitHub Link:** https://github.com/AbhayBhise/Urban-GenAI/blob/main/backend/corpus/urban_planning.txt
- **Contents:** Domain-curated urban planning contexts and sustainability recommendations (FSI zoning, Transit-Oriented Development, stormwater/SuDS drainage buffers, green cover mandates) paired with Pune GIS land-use statistics.
