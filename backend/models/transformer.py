"""Backwards-compatible shim.

Historically this file held a ResNet18 image classifier that the app labelled
a "Transformer". That was inaccurate. The real transformer-based generative
model now lives in models/gpt.py (MiniGPT); the classifier moved to
models/classifier.py. These re-exports keep old imports working.
"""

from models.classifier import UrbanClassifier
from models.gpt import MiniGPT

# Legacy aliases
UrbanViT = UrbanClassifier

__all__ = ["UrbanClassifier", "UrbanViT", "MiniGPT"]
