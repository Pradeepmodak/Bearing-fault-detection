from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .features import FEATURE_COLUMNS, compute_fft


plt.style.use("seaborn-v0_8-whitegrid")


def save_model_comparison_plot(metrics_table: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    melted = metrics_table.melt(id_vars="model", var_name="metric", value_name="score")
    pivot = melted.pivot(index="metric", columns="model", values="score")
    pivot.plot(kind="bar", ax=ax)
    ax.set_ylim(0, 1.05)
    ax.set_title("Model Performance Comparison")
    ax.set_ylabel("Score")
    ax.set_xlabel("")
    plt.xticks(rotation=20)
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def save_confusion_matrix(confusion: np.ndarray, labels: list[str], output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 6))
    image = ax.imshow(confusion, cmap="Blues")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=20, ha="right")
    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels)
    for row in range(confusion.shape[0]):
        for col in range(confusion.shape[1]):
            ax.text(col, row, int(confusion[row, col]), ha="center", va="center", color="black")
    ax.set_title("Confusion Matrix")
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def save_feature_importance_plot(model_pipeline, output_path: Path) -> None:
    classifier = getattr(model_pipeline, "named_steps", {}).get("classifier")
    if classifier is None or not hasattr(classifier, "feature_importances_"):
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, "Feature importance is available for tree-based models only.", ha="center", va="center")
        ax.axis("off")
        fig.tight_layout()
        fig.savefig(output_path, dpi=200)
        plt.close(fig)
        return

    importances = pd.Series(classifier.feature_importances_, index=FEATURE_COLUMNS).sort_values(ascending=False).head(12)
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(importances.index[::-1], importances.values[::-1], color="#0b7285")
    ax.set_title("Top Feature Importances")
    ax.set_xlabel("Importance")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def build_signal_plots(signal: np.ndarray, sampling_rate: int) -> tuple[plt.Figure, plt.Figure]:
    time_axis = np.arange(signal.size) / sampling_rate
    freqs, magnitude = compute_fft(signal, sampling_rate=sampling_rate)

    fig_time, ax_time = plt.subplots(figsize=(10, 4))
    ax_time.plot(time_axis, signal, color="#0b7285", linewidth=1.2)
    ax_time.set_title("Time-Domain Waveform")
    ax_time.set_xlabel("Time (s)")
    ax_time.set_ylabel("Amplitude")
    fig_time.tight_layout()

    fig_fft, ax_fft = plt.subplots(figsize=(10, 4))
    ax_fft.plot(freqs, magnitude, color="#d9480f", linewidth=1.2)
    ax_fft.set_title("Frequency Spectrum (FFT)")
    ax_fft.set_xlabel("Frequency (Hz)")
    ax_fft.set_ylabel("Magnitude")
    fig_fft.tight_layout()

    return fig_time, fig_fft
