from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bearing_fault_diagnosis.config import AppConfig
from bearing_fault_diagnosis.data import get_demo_signal_info, save_signal_to_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a built-in demo vibration signal to CSV.")
    parser.add_argument(
        "--output",
        default="artifacts/demo_signal.csv",
        help="Output CSV path for the exported demo signal.",
    )
    args = parser.parse_args()

    config = AppConfig()
    signal, source_name = get_demo_signal_info(config)
    output_path = save_signal_to_csv(signal, Path(args.output))

    print(f"Exported demo signal from: {source_name}")
    print(f"Saved CSV to: {output_path.resolve()}")


if __name__ == "__main__":
    main()
