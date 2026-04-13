# Bearing Fault Diagnosis Using the CWRU Dataset

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-GUI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Dataset](https://img.shields.io/badge/Dataset-CWRU%20Bearing-0B7285?style=for-the-badge)

An end-to-end machine learning project for bearing fault diagnosis using vibration signals from the Case Western Reserve University (CWRU) bearing dataset. The project combines mechanical engineering context, signal processing, classical ML models, explainable visualizations, and a Streamlit GUI suitable for minor project evaluation, interviews, and live demos.

## Why This Project Matters

Rolling element bearings are critical in motors, pumps, turbines, compressors, and other rotating machines. When a bearing develops a defect, the vibration pattern changes. Early fault diagnosis helps:

- reduce downtime
- prevent catastrophic machine failure
- support predictive maintenance
- improve maintenance planning

This project classifies the following health states:

- Normal
- Inner Race Fault
- Outer Race Fault
- Ball Fault

## Project Highlights

- complete ML pipeline from data loading to saved model inference
- feature engineering in both time and frequency domains
- two ML models implemented and compared: SVM and Random Forest
- trained model saved as a reusable artifact
- Streamlit dashboard for upload, visualization, and prediction
- confusion matrix, FFT plots, feature table, and feature importance chart
- presentation-ready documentation and viva preparation
- CLI scripts for building data, training, exporting a demo CSV, and predicting from CSV

## Dataset Information

### Source

This project is based on the Case Western Reserve University Bearing Data Center dataset.

Official source:

- [CWRU Bearing Data Center](https://engineering.case.edu/bearingdatacenter)

### What The Dataset Contains

The original CWRU dataset contains vibration signals measured from bearings under different health conditions and fault sizes. Signals are collected from accelerometers mounted on a bearing test rig.

Typical classes:

- Normal
- Inner race fault
- Outer race fault
- Ball fault

### Files Available In This Repository

This repository already includes:

- sample raw `.mat` files in [data/raw](D:/CWRU-bearing-fault-classification-ML-main/data/raw)
- a legacy feature table in [data/CWRUdataset.csv](D:/CWRU-bearing-fault-classification-ML-main/data/CWRUdataset.csv)

The new pipeline supports either:

1. using the included feature CSV for quick setup
2. rebuilding the features directly from the raw `.mat` files

## End-To-End Pipeline

### 1. Data Loading

- raw `.mat` files are loaded from `data/raw/`
- the drive-end vibration signal is extracted
- the signal is divided into overlapping windows

### 2. Preprocessing

- segmentation increases the number of learning samples
- missing values are handled by median imputation
- scaling is applied for the SVM pipeline

### 3. Feature Extraction

Time-domain features:

- mean
- standard deviation
- RMS
- kurtosis
- skewness
- crest factor
- form factor
- impulse factor

Frequency-domain features:

- FFT magnitude spectrum
- dominant frequency
- mean frequency
- spectral energy
- frequency variance

### 4. Model Training

Two models are trained and compared:

- `svm_rbf`
- `random_forest`

The best model is selected using weighted F1-score and saved for later inference.

### 5. Evaluation

The training workflow generates:

- model comparison table
- classification report
- confusion matrix
- feature importance chart

### 6. GUI Prediction

The Streamlit app lets the user:

- upload a vibration CSV
- use a built-in demo signal
- visualize waveform and FFT
- predict the fault type
- inspect confidence and extracted features

## Project Structure

```text
CWRU-bearing-fault-classification-ML-main/
|-- app/
|   `-- streamlit_app.py
|-- artifacts/
|   |-- cwru_features.csv
|   `-- demo_signal.csv
|-- data/
|   |-- raw/
|   `-- CWRUdataset.csv
|-- docs/
|   `-- project_walkthrough.md
|-- models/
|   |-- best_model.joblib
|   |-- classification_report.csv
|   |-- metrics.csv
|   `-- model_metadata.json
|-- reports/
|   |-- confusion_matrix.png
|   |-- feature_importance.png
|   `-- model_comparison.png
|-- scripts/
|   |-- build_dataset.py
|   |-- export_demo_signal.py
|   |-- predict_signal.py
|   `-- train_model.py
|-- src/
|   `-- bearing_fault_diagnosis/
|       |-- config.py
|       |-- data.py
|       |-- features.py
|       |-- inference.py
|       |-- modeling.py
|       `-- plots.py
|-- pyproject.toml
|-- requirements.txt
`-- README.md
```

## How To Run Locally

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 3. Build the dataset

Use the included feature table:

```bash
python scripts/build_dataset.py
```

Rebuild from raw `.mat` signals:

```bash
python scripts/build_dataset.py --rebuild
```

### 4. Train the models

```bash
python scripts/train_model.py
```

Or rebuild features and train in one step:

```bash
python scripts/train_model.py --rebuild-data
```

This generates:

- [artifacts/cwru_features.csv](D:/CWRU-bearing-fault-classification-ML-main/artifacts/cwru_features.csv)
- [models/best_model.joblib](D:/CWRU-bearing-fault-classification-ML-main/models/best_model.joblib)
- [models/metrics.csv](D:/CWRU-bearing-fault-classification-ML-main/models/metrics.csv)
- [models/classification_report.csv](D:/CWRU-bearing-fault-classification-ML-main/models/classification_report.csv)
- [models/model_metadata.json](D:/CWRU-bearing-fault-classification-ML-main/models/model_metadata.json)
- [reports/confusion_matrix.png](D:/CWRU-bearing-fault-classification-ML-main/reports/confusion_matrix.png)
- [reports/feature_importance.png](D:/CWRU-bearing-fault-classification-ML-main/reports/feature_importance.png)

### 5. Launch the Streamlit app

```bash
streamlit run app/streamlit_app.py
```

### 6. Export a ready-to-use demo CSV

```bash
python scripts/export_demo_signal.py
```

### 7. Run CLI inference

```bash
python scripts/predict_signal.py artifacts/demo_signal.csv
```

## Streamlit GUI Features

- upload vibration CSV
- built-in demo signal
- waveform plot
- FFT plot
- predicted fault class
- confidence score
- fault probability table
- extracted feature values
- confusion matrix display
- feature importance display

## Algorithms Used

### Support Vector Machine

- strong on structured numerical feature sets
- effective when scaled features are used
- useful for nonlinear class separation

### Random Forest

- robust to noise and nonlinear relationships
- provides feature importance
- strong baseline for industrial tabular ML

## Typical Input Format For The GUI

Upload a CSV file with at least one numeric column. The app uses the first numeric column as the vibration amplitude signal.

```csv
amplitude
0.012
0.019
0.004
-0.008
...
```

## Industrial Applications

- predictive maintenance in manufacturing
- motor and pump health monitoring
- condition-based maintenance for rotating equipment
- Industry 4.0 machine health dashboards

## Future Improvements

- add deep learning models such as 1D CNNs
- include more operating loads and speeds
- evaluate with stricter split strategies
- connect the app to live sensors
- deploy the dashboard online

## Presentation Walkthrough

For viva and presentation support, see:

- [docs/project_walkthrough.md](D:/CWRU-bearing-fault-classification-ML-main/docs/project_walkthrough.md)

Short version:

- **Problem statement:** bearing faults change vibration behavior and must be detected early.
- **Approach:** segment the signal, extract time and frequency features, train ML models, compare them, and deploy the best model in a GUI.
- **Result:** the system provides fast and interpretable fault diagnosis with plots, confidence scores, and saved artifacts.

## Important Notes

- the repo includes enough local data to demonstrate the full workflow
- the sample subset is good for project presentation and demo
- for research-grade benchmarking, you should expand the dataset and use stricter evaluation splits

## License

This project is released under the GPL-3.0 license. See [LICENSE](D:/CWRU-bearing-fault-classification-ML-main/LICENSE).
