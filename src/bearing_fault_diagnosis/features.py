from __future__ import annotations

from typing import Iterable

import numpy as np


FEATURE_COLUMNS = [
    "mean",
    "std",
    "mean_abs_dev",
    "rms",
    "max_abs",
    "skewness",
    "kurtosis",
    "crest_factor",
    "form_factor",
    "shape_factor",
    "impulse_factor",
    "spectral_mean",
    "spectral_std",
    "spectral_skewness",
    "spectral_kurtosis",
    "mean_frequency",
    "frequency_std",
    "rms_frequency",
    "root_variance_frequency",
    "spectral_centroid_proxy",
    "frequency_variation_factor",
    "frequency_variance",
    "frequency_skewness",
    "dominant_frequency",
    "spectral_energy",
]


def _safe_divide(numerator: float, denominator: float) -> float:
    return float(numerator / denominator) if denominator not in (0, 0.0) else 0.0


def _safe_moment_ratio(values: np.ndarray, centered: np.ndarray, scale: float, power: int) -> float:
    if values.size == 0 or np.isclose(scale, 0.0):
        return 0.0
    return float(np.mean(centered**power) / (scale**power))


def compute_fft(signal: Iterable[float], sampling_rate: int) -> tuple[np.ndarray, np.ndarray]:
    signal_array = np.asarray(signal, dtype=float).ravel()
    fft_values = np.fft.rfft(signal_array)
    magnitude = np.abs(fft_values) / max(signal_array.size, 1)
    freqs = np.fft.rfftfreq(signal_array.size, d=1.0 / sampling_rate)
    return freqs, magnitude


def extract_features(signal: Iterable[float], sampling_rate: int) -> dict[str, float]:
    signal_array = np.asarray(signal, dtype=float).ravel()
    signal_array = signal_array[~np.isnan(signal_array)]
    if signal_array.size == 0:
        raise ValueError("Signal is empty after removing missing values.")

    mean = float(np.mean(signal_array))
    std = float(np.std(signal_array, ddof=1)) if signal_array.size > 1 else 0.0
    mean_abs_dev = float(np.mean(np.abs(signal_array - mean)))
    rms = float(np.sqrt(np.mean(np.square(signal_array))))
    max_abs = float(np.max(np.abs(signal_array)))

    centered = signal_array - mean
    skewness = _safe_moment_ratio(signal_array, centered, std, 3)
    kurtosis = _safe_moment_ratio(signal_array, centered, std, 4)

    freqs, magnitude = compute_fft(signal_array, sampling_rate)
    spectral_mean = float(np.mean(magnitude))
    spectral_std = float(np.std(magnitude, ddof=1)) if magnitude.size > 1 else 0.0
    spectral_centered = magnitude - spectral_mean
    spectral_skewness = _safe_moment_ratio(magnitude, spectral_centered, spectral_std, 3)
    spectral_kurtosis = _safe_moment_ratio(magnitude, spectral_centered, spectral_std, 4)

    spectral_sum = float(np.sum(magnitude))
    if np.isclose(spectral_sum, 0.0):
        mean_frequency = 0.0
        frequency_std = 0.0
        rms_frequency = 0.0
        root_variance_frequency = 0.0
        spectral_centroid_proxy = 0.0
        frequency_variation_factor = 0.0
        frequency_variance = 0.0
        frequency_skewness = 0.0
        dominant_frequency = 0.0
        spectral_energy = 0.0
    else:
        mean_frequency = float(np.sum(freqs * magnitude) / spectral_sum)
        frequency_std = float(np.sqrt(np.sum(np.square(freqs - mean_frequency) * magnitude) / spectral_sum))
        rms_frequency = float(np.sqrt(np.sum(np.square(freqs) * magnitude) / spectral_sum))
        root_variance_frequency = float(
            np.sqrt(np.sum(np.power(freqs, 4) * magnitude) / np.sum(np.square(freqs) * magnitude))
        )
        spectral_centroid_proxy = float(
            np.sqrt(max(np.sum(freqs * magnitude) - spectral_sum * frequency_std, 0.0) / spectral_sum)
        )
        frequency_variation_factor = _safe_divide(frequency_std, mean_frequency)
        frequency_variance = float(np.average(np.square(freqs - mean_frequency), weights=magnitude))
        frequency_skewness = float(
            np.average(np.power(freqs - mean_frequency, 3), weights=magnitude) / (frequency_std**3)
        ) if not np.isclose(frequency_std, 0.0) else 0.0
        dominant_frequency = float(freqs[int(np.argmax(magnitude))])
        spectral_energy = float(np.sum(np.square(magnitude)))

    return {
        "mean": mean,
        "std": std,
        "mean_abs_dev": mean_abs_dev,
        "rms": rms,
        "max_abs": max_abs,
        "skewness": skewness,
        "kurtosis": kurtosis,
        "crest_factor": _safe_divide(max_abs, rms),
        "form_factor": _safe_divide(max_abs, mean_abs_dev),
        "shape_factor": _safe_divide(rms, mean_abs_dev),
        "impulse_factor": _safe_divide(rms**2, float(np.mean(np.abs(signal_array)))),
        "spectral_mean": spectral_mean,
        "spectral_std": spectral_std,
        "spectral_skewness": spectral_skewness,
        "spectral_kurtosis": spectral_kurtosis,
        "mean_frequency": mean_frequency,
        "frequency_std": frequency_std,
        "rms_frequency": rms_frequency,
        "root_variance_frequency": root_variance_frequency,
        "spectral_centroid_proxy": spectral_centroid_proxy,
        "frequency_variation_factor": frequency_variation_factor,
        "frequency_variance": frequency_variance,
        "frequency_skewness": frequency_skewness,
        "dominant_frequency": dominant_frequency,
        "spectral_energy": spectral_energy,
    }
