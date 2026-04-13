from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class AppConfig:
    """Central configuration for paths and signal processing defaults."""

    project_root: Path = field(default_factory=lambda: Path(__file__).resolve().parents[2])
    data_dir: Path = field(init=False)
    raw_data_dir: Path = field(init=False)
    processed_data_dir: Path = field(init=False)
    artifacts_dir: Path = field(init=False)
    reports_dir: Path = field(init=False)
    app_dir: Path = field(init=False)
    sampling_rate: int = 48_000
    frame_size: int = 2_048
    overlap: float = 0.5
    random_state: int = 42

    def __post_init__(self) -> None:
        self.data_dir = self.project_root / "data"
        self.raw_data_dir = self.data_dir / "raw"
        self.processed_data_dir = self.project_root / "artifacts"
        self.artifacts_dir = self.project_root / "models"
        self.reports_dir = self.project_root / "reports"
        self.app_dir = self.project_root / "app"

    def ensure_directories(self) -> None:
        for path in (
            self.processed_data_dir,
            self.artifacts_dir,
            self.reports_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)
