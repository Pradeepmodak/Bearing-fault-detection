from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bearing_fault_diagnosis.config import AppConfig
from bearing_fault_diagnosis.data import load_signal_from_csv
from bearing_fault_diagnosis.inference import predict_signal


def main() -> None:
    parser = argparse.ArgumentParser(description="Run CLI inference on a vibration CSV file.")
    parser.add_argument("csv_path", help="Path to the CSV file containing the vibration signal.")
    parser.add_argument(
        "--sampling-rate",
        type=int,
        default=AppConfig().sampling_rate,
        help="Sampling rate in Hz. Defaults to the project configuration.",
    )
    args = parser.parse_args()

    signal = load_signal_from_csv(args.csv_path)
    result = predict_signal(signal=signal, sampling_rate=args.sampling_rate)

    print(f"Predicted fault: {result['predicted_label']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print("\nProbabilities:")
    print(result["confidence_table"].to_string(index=False))
    print("\nTop features:")
    feature_items = sorted(result["feature_map"].items(), key=lambda item: abs(item[1]), reverse=True)[:10]
    for name, value in feature_items:
        print(f"- {name}: {value:.5f}")


if __name__ == "__main__":
    main()
