from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bearing_fault_diagnosis.config import AppConfig
from bearing_fault_diagnosis.data import load_feature_table


def main() -> None:
    parser = argparse.ArgumentParser(description="Build or refresh the processed CWRU feature dataset.")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild features from MAT files in data/raw.")
    args = parser.parse_args()

    config = AppConfig()
    dataset = load_feature_table(config=config, rebuild=args.rebuild)
    output_path = config.processed_data_dir / "cwru_features.csv"
    print(f"Saved processed dataset to: {output_path}")
    print(f"Shape: {dataset.shape}")
    print(f"Classes: {sorted(dataset['target'].unique().tolist())}")


if __name__ == "__main__":
    main()
