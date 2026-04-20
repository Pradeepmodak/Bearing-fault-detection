from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bearing_fault_diagnosis.config import AppConfig
from bearing_fault_diagnosis.data import get_demo_signal_info, load_signal_from_csv
from bearing_fault_diagnosis.inference import bundle_ready, predict_signal
from bearing_fault_diagnosis.plots import build_signal_plots


st.set_page_config(
    page_title="Bearing Fault Diagnosis",
    page_icon="AI",
    layout="wide",
)

config = AppConfig()
MODEL_READY = bundle_ready()


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background: radial-gradient(circle at top left, #e6fcf5 0%, #f8f9fa 45%, #fff4e6 100%);
            }
            .hero {
                padding: 1.3rem 1.5rem;
                border-radius: 20px;
                background: linear-gradient(135deg, rgba(8,127,91,0.92), rgba(230,119,0,0.88));
                color: white;
                box-shadow: 0 18px 45px rgba(73, 80, 87, 0.18);
                margin-bottom: 1rem;
            }
            .metric-card {
                padding: 1rem;
                border-radius: 16px;
                background: rgba(255,255,255,0.75);
                border: 1px solid rgba(8,127,91,0.12);
            }
            .info-card {
                padding: 1rem 1.2rem;
                border-radius: 18px;
                background: rgba(255,255,255,0.82);
                border: 1px solid rgba(73,80,87,0.08);
                min-height: 120px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_styles()

st.markdown(
    """
    <div class="hero">
        <h1 style="margin-bottom:0.2rem;">CWRU Bearing Fault Diagnosis Dashboard</h1>
        <p style="font-size:1.05rem;margin:0;">
            Upload a vibration signal, inspect waveform and FFT behavior, and classify the bearing condition into
            Normal, Inner Race Fault, Outer Race Fault, or Ball Fault.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Input Settings")
    sampling_rate = st.number_input("Sampling Rate (Hz)", min_value=1_000, max_value=100_000, value=config.sampling_rate, step=1_000)
    uploaded_file = st.file_uploader("Upload vibration CSV", type=["csv"])
    if st.button("Use Built-In Demo Signal", use_container_width=True):
        demo_signal, source_name = get_demo_signal_info(config)
        st.session_state["demo_signal"] = demo_signal
        st.session_state["demo_signal_source"] = source_name
    st.caption("CSV should contain at least one numeric column with signal amplitude values.")
    st.divider()
    st.markdown("**Expected classes**")
    st.caption("Normal, Inner Race Fault, Outer Race Fault, Ball Fault")
    if MODEL_READY:
        st.success("Trained model bundle found.")
    else:
        st.error("Model bundle missing. Run `python scripts/train_model.py` first.")


signal = None
signal_source = "Uploaded CSV"
if uploaded_file is not None:
    try:
        signal = load_signal_from_csv(uploaded_file)
    except ValueError as exc:
        st.error(str(exc))
elif "demo_signal" in st.session_state:
    signal = st.session_state["demo_signal"]
    signal_source = f"Built-in demo from {st.session_state.get('demo_signal_source', 'data/raw')}"

summary_col1 = st.columns([1])[0]
with summary_col1:
    st.markdown(
        """
        <div class="info-card">
            <h3 style="margin-top:0;">Workflow</h3>
            <p style="margin-bottom:0;">Upload a vibration signal, compute time-domain and FFT-based features, then classify the bearing condition with the trained ML model.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if not MODEL_READY:
    st.warning("The trained model artifact was not found. Train it first with `python scripts/train_model.py`.")
elif signal is None:
    st.info("Upload a CSV signal file to start the diagnosis workflow.")
else:
    prediction = predict_signal(signal=signal, sampling_rate=int(sampling_rate))
    fig_time, fig_fft = build_signal_plots(signal=signal, sampling_rate=int(sampling_rate))

    col1, col2, col3 = st.columns(3)
    col1.metric("Predicted Fault", prediction["predicted_label"])
    col2.metric("Confidence", f"{prediction['confidence']:.2%}")
    col3.metric("Signal Length", f"{len(signal)} samples")
    st.caption(f"Signal source: {signal_source}")

    plot_col1, plot_col2 = st.columns(2)
    with plot_col1:
        st.pyplot(fig_time, use_container_width=True)
    with plot_col2:
        st.pyplot(fig_fft, use_container_width=True)

    st.subheader("Confidence by Fault Type")
    st.dataframe(
        prediction["confidence_table"].style.format({"probability": "{:.2%}"}),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Extracted Features")
    feature_df = pd.DataFrame(
        {"feature": list(prediction["feature_map"].keys()), "value": list(prediction["feature_map"].values())}
    )
    st.dataframe(feature_df.style.format({"value": "{:.5f}"}), use_container_width=True, hide_index=True)

    report_col1, report_col2 = st.columns(2)
    confusion_path = config.reports_dir / "confusion_matrix.png"
    importance_path = config.reports_dir / "feature_importance.png"

    with report_col1:
        st.subheader("Confusion Matrix")
        if confusion_path.exists():
            st.image(str(confusion_path))
        else:
            st.warning("Train the model first to generate the confusion matrix.")

    with report_col2:
        st.subheader("Feature Importance")
        if importance_path.exists():
            st.image(str(importance_path))
        else:
            st.warning("Train the model first to generate the feature importance plot.")
