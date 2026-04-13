from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from .config import AppConfig
from .features import FEATURE_COLUMNS, extract_features


def load_bundle(bundle_path: Path | None = None) -> dict:
    config = AppConfig()
    path = bundle_path or (config.artifacts_dir / "best_model.joblib")
    if not path.exists():
        raise FileNotFoundError("Model bundle not found. Train the project first with the training script.")
    return joblib.load(path)


def predict_signal(signal, sampling_rate: int, bundle_path: Path | None = None) -> dict:
    bundle = load_bundle(bundle_path)
    feature_map = extract_features(signal, sampling_rate=sampling_rate)
    feature_frame = pd.DataFrame([[feature_map[column] for column in FEATURE_COLUMNS]], columns=FEATURE_COLUMNS)

    pipeline = bundle["model"]
    label_encoder = bundle["label_encoder"]

    predicted_encoded = pipeline.predict(feature_frame)[0]
    probabilities = pipeline.predict_proba(feature_frame)[0]
    predicted_label = label_encoder.inverse_transform([predicted_encoded])[0]

    confidence_table = (
        pd.DataFrame(
            {
                "fault_type": label_encoder.classes_,
                "probability": probabilities,
            }
        )
        .sort_values(by="probability", ascending=False)
        .reset_index(drop=True)
    )

    return {
        "predicted_label": predicted_label,
        "confidence": float(confidence_table.loc[0, "probability"]),
        "feature_map": feature_map,
        "confidence_table": confidence_table,
        "feature_frame": feature_frame,
        "bundle": bundle,
    }


def bundle_ready(bundle_path: Path | None = None) -> bool:
    config = AppConfig()
    path = bundle_path or (config.artifacts_dir / "best_model.joblib")
    return path.exists()
