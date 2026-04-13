from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import scipy.io

from .config import AppConfig
from .features import FEATURE_COLUMNS, extract_features


CLASS_NAME_MAP = {
    "Normal": "Normal",
    "IR": "Inner Race Fault",
    "OR": "Outer Race Fault",
    "B": "Ball Fault",
}


def load_signal_from_csv(file_like: str | Path | Iterable[bytes]) -> np.ndarray:
    data = pd.read_csv(file_like)
    numeric = data.select_dtypes(include=["number"])
    if numeric.empty:
        raise ValueError("Uploaded CSV must contain at least one numeric column.")
    return numeric.iloc[:, 0].dropna().to_numpy(dtype=float)


def parse_fault_metadata(file_name: str) -> tuple[str, str]:
    stem = Path(file_name).stem
    if "Normal" in stem:
        return "Normal", "0"

    match = re.match(r"([A-Za-z]+)(\d+)", stem)
    if not match:
        return "Unknown", "Unknown"
    return match.group(1), match.group(2)


def load_drive_end_signal(mat_path: Path) -> np.ndarray:
    mat_data = scipy.io.loadmat(mat_path)
    matching_keys = [key for key in mat_data.keys() if key.endswith("DE_time")]
    if not matching_keys:
        raise ValueError(f"No drive-end signal found in {mat_path.name}.")
    return np.asarray(mat_data[matching_keys[0]]).ravel().astype(float)


def segment_signal(signal: np.ndarray, frame_size: int, overlap: float) -> list[np.ndarray]:
    step_size = max(int(frame_size * (1 - overlap)), 1)
    if signal.size < frame_size:
        return []
    return [signal[start : start + frame_size] for start in range(0, signal.size - frame_size + 1, step_size)]


def load_demo_signal(config: AppConfig) -> np.ndarray:
    for mat_file in sorted(config.raw_data_dir.glob("*.mat")):
        signal = load_drive_end_signal(mat_file)
        segments = segment_signal(signal, frame_size=config.frame_size, overlap=config.overlap)
        if segments:
            return segments[0]
    raise FileNotFoundError("No demo signal is available in data/raw.")


def get_demo_signal_info(config: AppConfig) -> tuple[np.ndarray, str]:
    for mat_file in sorted(config.raw_data_dir.glob("*.mat")):
        signal = load_drive_end_signal(mat_file)
        segments = segment_signal(signal, frame_size=config.frame_size, overlap=config.overlap)
        if segments:
            return segments[0], mat_file.name
    raise FileNotFoundError("No demo signal is available in data/raw.")


def save_signal_to_csv(signal: np.ndarray, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"amplitude": np.asarray(signal, dtype=float)}).to_csv(output_path, index=False)
    return output_path


def build_feature_dataset(
    raw_dir: Path,
    frame_size: int,
    overlap: float,
    sampling_rate: int,
) -> pd.DataFrame:
    rows: list[dict[str, float | str | int]] = []

    for mat_file in sorted(raw_dir.glob("*.mat")):
        health_state, damage_size = parse_fault_metadata(mat_file.name)
        target_label = CLASS_NAME_MAP.get(health_state, health_state)
        signal = load_drive_end_signal(mat_file)
        segments = segment_signal(signal, frame_size=frame_size, overlap=overlap)

        for segment_id, segment in enumerate(segments):
            feature_row = extract_features(segment, sampling_rate=sampling_rate)
            rows.append(
                {
                    "source_file": mat_file.name,
                    "segment_id": segment_id,
                    "health_state_code": health_state,
                    "damage_size_mils": damage_size,
                    "target": target_label,
                    **feature_row,
                }
            )

    if not rows:
        raise FileNotFoundError(f"No usable MAT files found in {raw_dir}.")

    return pd.DataFrame(rows)


def load_feature_table(config: AppConfig, rebuild: bool = False) -> pd.DataFrame:
    config.ensure_directories()
    processed_path = config.processed_data_dir / "cwru_features.csv"
    legacy_path = config.data_dir / "CWRUdataset.csv"

    if rebuild and config.raw_data_dir.exists():
        dataset = build_feature_dataset(
            raw_dir=config.raw_data_dir,
            frame_size=config.frame_size,
            overlap=config.overlap,
            sampling_rate=config.sampling_rate,
        )
        dataset.to_csv(processed_path, index=False)
        return dataset

    if processed_path.exists():
        return pd.read_csv(processed_path)

    if legacy_path.exists():
        legacy = pd.read_csv(legacy_path)
        renamed = legacy.rename(
            columns={
                "Specific Label": "source_file",
                "Health State": "health_state_code",
                "Damage Size": "damage_size_mils",
                "Mean": "mean",
                "Standard deviation": "std",
                "Mean absolute deviation": "mean_abs_dev",
                "Root mean square": "rms",
                "Maximum absolute value": "max_abs",
                "Skewness": "skewness",
                "Kurtosis": "kurtosis",
                "Crest factor": "crest_factor",
                "Form factor": "form_factor",
                "Shape factor": "shape_factor",
                "Impulse factor": "impulse_factor",
                "Mean of power spectrum": "spectral_mean",
                "Standard deviation of power spectrum": "spectral_std",
                "Skewness of power spectrum": "spectral_skewness",
                "Kurtosis of power spectrum": "spectral_kurtosis",
                "Mean frequency": "mean_frequency",
                "Standard deviation of frequency": "frequency_std",
                "Root mean square frequency": "rms_frequency",
                "Root variance frequency": "root_variance_frequency",
                "Frequency centroid": "spectral_centroid_proxy",
                "Frequency variation factor": "frequency_variation_factor",
                "Frequency variance": "frequency_variance",
                "Frequency skewness": "frequency_skewness",
            }
        )
        renamed["target"] = renamed["health_state_code"].map(CLASS_NAME_MAP).fillna(renamed["health_state_code"])
        renamed["segment_id"] = np.arange(len(renamed))
        for column in FEATURE_COLUMNS:
            if column not in renamed.columns:
                renamed[column] = 0.0
        renamed = renamed[
            ["source_file", "segment_id", "health_state_code", "damage_size_mils", "target", *FEATURE_COLUMNS]
        ].copy()
        renamed.to_csv(processed_path, index=False)
        return renamed

    if config.raw_data_dir.exists():
        dataset = build_feature_dataset(
            raw_dir=config.raw_data_dir,
            frame_size=config.frame_size,
            overlap=config.overlap,
            sampling_rate=config.sampling_rate,
        )
        dataset.to_csv(processed_path, index=False)
        return dataset

    raise FileNotFoundError(
        "No feature dataset or raw MAT files were found. Add files to data/raw/ or provide data/CWRUdataset.csv."
    )
