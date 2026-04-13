from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import joblib

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bearing_fault_diagnosis.config import AppConfig
from bearing_fault_diagnosis.data import load_feature_table
from bearing_fault_diagnosis.modeling import compute_confusion, generate_classification_report, train_and_select_model
from bearing_fault_diagnosis.plots import save_confusion_matrix, save_feature_importance_plot, save_model_comparison_plot


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the bearing fault diagnosis models and save the best artifact.")
    parser.add_argument("--rebuild-data", action="store_true", help="Rebuild the feature table from MAT files before training.")
    args = parser.parse_args()

    config = AppConfig()
    config.ensure_directories()

    dataset = load_feature_table(config=config, rebuild=args.rebuild_data)
    artifacts = train_and_select_model(dataset=dataset, config=config)
    report_df = generate_classification_report(artifacts)
    confusion = compute_confusion(artifacts)

    metrics_path = config.artifacts_dir / "metrics.csv"
    report_path = config.artifacts_dir / "classification_report.csv"
    bundle_path = config.artifacts_dir / "best_model.joblib"
    metadata_path = config.artifacts_dir / "model_metadata.json"

    artifacts.metrics_table.to_csv(metrics_path, index=False)
    report_df.to_csv(report_path)

    bundle = {
        "model": artifacts.best_pipeline,
        "model_name": artifacts.best_model_name,
        "label_encoder": artifacts.label_encoder,
        "feature_columns": artifacts.feature_columns,
        "sampling_rate": config.sampling_rate,
        "frame_size": config.frame_size,
    }
    joblib.dump(bundle, bundle_path)

    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(
            {
                "best_model": artifacts.best_model_name,
                "sampling_rate": config.sampling_rate,
                "frame_size": config.frame_size,
                "dataset_rows": int(dataset.shape[0]),
                "dataset_columns": int(dataset.shape[1]),
                "models_compared": artifacts.metrics_table["model"].tolist(),
                "best_model_f1_weighted": float(
                    artifacts.metrics_table.loc[artifacts.metrics_table["model"] == artifacts.best_model_name, "f1_weighted"].iloc[0]
                ),
            },
            file,
            indent=2,
        )

    save_model_comparison_plot(artifacts.metrics_table, config.reports_dir / "model_comparison.png")
    save_confusion_matrix(
        confusion,
        labels=list(artifacts.label_encoder.classes_),
        output_path=config.reports_dir / "confusion_matrix.png",
    )
    save_feature_importance_plot(
        artifacts.trained_models["random_forest"],
        config.reports_dir / "feature_importance.png",
    )

    print(f"Best model: {artifacts.best_model_name}")
    print(f"Saved bundle: {bundle_path}")
    print(f"Saved metrics: {metrics_path}")
    print(f"Saved report: {report_path}")


if __name__ == "__main__":
    main()
