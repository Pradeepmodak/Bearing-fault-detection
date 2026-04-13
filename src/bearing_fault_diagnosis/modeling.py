from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC

from .config import AppConfig
from .features import FEATURE_COLUMNS


@dataclass(slots=True)
class TrainingArtifacts:
    label_encoder: LabelEncoder
    metrics_table: pd.DataFrame
    best_model_name: str
    best_pipeline: Pipeline
    trained_models: dict[str, Pipeline]
    x_test: pd.DataFrame
    y_test_encoded: np.ndarray
    y_pred_encoded: np.ndarray
    feature_columns: list[str]


def build_model_registry(random_state: int) -> dict[str, Pipeline]:
    return {
        "svm_rbf": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("classifier", SVC(kernel="rbf", C=8.0, gamma="scale", probability=True, random_state=random_state)),
            ]
        ),
        "random_forest": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "classifier",
                    RandomForestClassifier(
                        n_estimators=300,
                        max_depth=None,
                        min_samples_split=4,
                        min_samples_leaf=1,
                        random_state=random_state,
                        class_weight="balanced",
                        n_jobs=1,
                    ),
                ),
            ]
        ),
    }


def train_and_select_model(dataset: pd.DataFrame, config: AppConfig) -> TrainingArtifacts:
    X = dataset[FEATURE_COLUMNS].copy()
    y = dataset["target"].copy()

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.2,
        random_state=config.random_state,
        stratify=y_encoded,
    )

    results: list[dict[str, float | str]] = []
    trained_models: dict[str, Pipeline] = {}
    best_name = ""
    best_score = -1.0
    best_predictions: np.ndarray | None = None

    for model_name, pipeline in build_model_registry(config.random_state).items():
        model = clone(pipeline)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        weighted_f1 = f1_score(y_test, predictions, average="weighted")
        precision = precision_score(y_test, predictions, average="weighted", zero_division=0)
        recall = recall_score(y_test, predictions, average="weighted", zero_division=0)

        results.append(
            {
                "model": model_name,
                "accuracy": accuracy,
                "precision_weighted": precision,
                "recall_weighted": recall,
                "f1_weighted": weighted_f1,
            }
        )
        trained_models[model_name] = model

        if weighted_f1 > best_score:
            best_name = model_name
            best_score = weighted_f1
            best_predictions = predictions

    assert best_predictions is not None
    best_pipeline = trained_models[best_name]

    if not hasattr(best_pipeline.named_steps["classifier"], "predict_proba"):
        calibrated = CalibratedClassifierCV(best_pipeline, cv=3)
        calibrated.fit(X_train, y_train)
        best_pipeline = Pipeline([("calibrated_model", calibrated)])

    return TrainingArtifacts(
        label_encoder=label_encoder,
        metrics_table=pd.DataFrame(results).sort_values(by="f1_weighted", ascending=False).reset_index(drop=True),
        best_model_name=best_name,
        best_pipeline=best_pipeline,
        trained_models=trained_models,
        x_test=X_test.reset_index(drop=True),
        y_test_encoded=y_test,
        y_pred_encoded=best_predictions,
        feature_columns=FEATURE_COLUMNS.copy(),
    )


def generate_classification_report(artifacts: TrainingArtifacts) -> pd.DataFrame:
    report = classification_report(
        artifacts.y_test_encoded,
        artifacts.y_pred_encoded,
        target_names=list(artifacts.label_encoder.classes_),
        output_dict=True,
        zero_division=0,
    )
    return pd.DataFrame(report).transpose()


def compute_confusion(artifacts: TrainingArtifacts) -> np.ndarray:
    return confusion_matrix(artifacts.y_test_encoded, artifacts.y_pred_encoded)
