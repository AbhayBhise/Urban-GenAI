"""Reproducible, class-stratified UCMerced split shared by training and evaluation."""

from __future__ import annotations

import json
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_ROOT = PROJECT_ROOT / "UCMerced_LandUse" / "UCMerced_LandUse" / "Images"
SPLIT_PATH = PROJECT_ROOT / "outputs" / "splits" / "ucmerced_seed42.json"

URBAN_CLASSES = [
    "agricultural", "airplane", "baseballdiamond", "beach",
    "buildings", "chaparral", "denseresidential", "forest",
    "freeway", "golfcourse", "harbor", "intersection",
    "mediumresidential", "mobilehomepark", "overpass",
    "parkinglot", "river", "runway", "sparseresidential",
    "storagetanks", "tenniscourt",
]

TRAIN_FRACTION = 0.70
VAL_FRACTION = 0.15
TEST_FRACTION = 0.15


def _relative(path: Path) -> str:
    return path.relative_to(DATASET_ROOT).as_posix()


def build_split(seed: int = 42) -> dict:
    if not DATASET_ROOT.exists():
        raise FileNotFoundError(f"UCMerced dataset not found at {DATASET_ROOT}")

    rng = random.Random(seed)
    split = {"train": [], "val": [], "test": []}

    for cls in URBAN_CLASSES:
        paths = sorted((DATASET_ROOT / cls).glob("*.tif"))
        if not paths:
            continue
        rng.shuffle(paths)

        n = len(paths)
        n_train = int(n * TRAIN_FRACTION)
        n_val = int(n * VAL_FRACTION)
        split["train"].extend(_relative(p) for p in paths[:n_train])
        split["val"].extend(_relative(p) for p in paths[n_train:n_train + n_val])
        split["test"].extend(_relative(p) for p in paths[n_train + n_val:])

    for key in split:
        split[key].sort()

    return {
        "dataset": "UCMerced_LandUse",
        "seed": seed,
        "classes": URBAN_CLASSES,
        "fractions": {
            "train": TRAIN_FRACTION,
            "val": VAL_FRACTION,
            "test": TEST_FRACTION,
        },
        "counts": {key: len(value) for key, value in split.items()},
        "splits": split,
    }


def load_or_build_split(seed: int = 42, rebuild: bool = False) -> dict:
    if not rebuild and SPLIT_PATH.exists():
        with open(SPLIT_PATH, encoding="utf-8") as f:
            manifest = json.load(f)
        if manifest.get("seed") == seed and manifest.get("dataset") == "UCMerced_LandUse":
            return manifest

    manifest = build_split(seed=seed)
    SPLIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SPLIT_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    return manifest


def split_paths(split: str, seed: int = 42) -> list[Path]:
    manifest = load_or_build_split(seed=seed)
    return [DATASET_ROOT / rel for rel in manifest["splits"][split]]


if __name__ == "__main__":
    manifest = load_or_build_split(rebuild=True)
    print(json.dumps(manifest["counts"], indent=2))
