from __future__ import annotations

import html
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PPT = Path(r"C:\Users\pmins\Downloads\final ppt (1).pptx")
OUTPUT_PPT = ROOT / "Final_Presentation_With_Speaker_Notes.pptx"
OUTPUT_TXT = ROOT / "Presentation_Speaker_Notes_and_Viva_QA.txt"


SLIDE_NOTES = {
    1: {
        "title": "Title Slide",
        "notes": [
            "Start with a short self-introduction and name your teammate clearly. Mention that this is a Project-II presentation from the Department of Mechanical Engineering at NIT Jamshedpur.",
            "State the project title slowly: Intelligent Bearing Fault Diagnosis for Predictive Maintenance Using Vibration Signal Analysis and Machine Learning.",
            "Add one purpose sentence: the project aims to detect bearing faults early from vibration signals and present the result through a working machine-learning based dashboard.",
            "Tell the professors how the talk will flow: background, literature, gaps, methodology, results, conclusion, and future scope.",
            "If asked why this topic was chosen, answer: because it connects mechanical condition monitoring with a practical AI workflow and has strong relevance to predictive maintenance."
        ],
    },
    2: {
        "title": "Outline",
        "notes": [
            "Do not spend much time here. Use this slide only to orient the audience.",
            "Say that the presentation moves from the problem context toward the developed system, and then to the achieved results and final takeaways.",
            "Mention that a live demonstration is possible because the project includes a Streamlit GUI backed by the trained model."
        ],
    },
    3: {
        "title": "Introduction and Technical Background",
        "notes": [
            "Explain the background in mechanical terms first. Bearings support rotating shafts, so any defect in the rolling elements or races changes the vibration response of the machine.",
            "When you mention time-domain analysis, explain it as observing how vibration amplitude changes with time. These values help capture signal spread, impulsive behavior, and abnormal peaks.",
            "When you mention frequency analysis, explain that FFT is used to see which frequencies dominate the signal. Fault conditions produce characteristic frequency signatures, so the frequency view helps separate classes [1].",
            "For machine learning classification, say that both time-domain and frequency-domain descriptors are combined into one feature vector and then used to train classifiers such as SVM and Random Forest.",
            "If a professor asks why both domains are used, answer: time-domain features capture amplitude variation directly, while frequency-domain features capture spectral structure; using both improves discrimination."
        ],
    },
    4: {
        "title": "Problem Statement",
        "notes": [
            "Frame the problem as a scalability issue. Manual interpretation of vibration signals is possible for a few samples but not for large continuous industrial data streams.",
            "State the specific project objective: to create a reliable and interpretable end-to-end workflow that classifies bearing condition into Normal, Ball Fault, Inner Race Fault, or Outer Race Fault.",
            "Mention the dataset-specific numbers from the project: 9,736 labeled windows, 48 kHz sampling, and four bearing conditions.",
            "If asked what exactly is difficult in raw data, answer: a long vibration signal is only a sequence of amplitude values; the challenge is converting that sequence into meaningful features that a classifier can use."
        ],
    },
    5: {
        "title": "Applications",
        "notes": [
            "Present this slide as the relevance slide. Tie the project to real mechanical systems instead of speaking in abstract AI terms.",
            "For smart manufacturing, explain that the same idea can be extended to plant-wide monitoring where multiple machines are tracked continuously.",
            "For the energy sector, mention turbines, generators, and rotating auxiliaries where unscheduled bearing failure is expensive.",
            "For aerospace or safety-critical systems, explain that early indication is valuable because bearing damage can propagate into larger mechanical problems.",
            "If asked whether this project is directly deployable to those sectors, answer honestly: this project is a benchmark-driven academic implementation, but the workflow is relevant and can be adapted to real sensor setups with further validation."
        ],
    },
    6: {
        "title": "Literature Survey",
        "notes": [
            "Explain the literature in comparison style. Do not read the slide word by word.",
            "Say that earlier work can be grouped into three approaches: classical signal analysis, feature-based machine learning, and deep learning-based diagnosis [2]-[4].",
            "Mention that classical methods depend more on domain interpretation of frequency behavior, while feature-based ML uses engineered descriptors with classifiers such as SVM and Random Forest.",
            "Mention that deep learning reduces manual feature design but may require more computation and may be less interpretable for a classroom-style demonstration [4], [5].",
            "If asked why CWRU is used so often, answer: because it is a controlled public benchmark with known fault classes, which makes method comparison easier [1]."
        ],
    },
    7: {
        "title": "Literature Limitations",
        "notes": [
            "Use this slide to justify your project contribution. Say that many works emphasize model performance but do not show a complete reproducible engineering pipeline.",
            "Explain hidden preprocessing as one important issue. If the paper does not make the segmentation rule or feature design clear, reproduction becomes difficult.",
            "Explain lack of accessibility as another issue. Many works stay at paper level and do not provide an interface that can be demonstrated by students or non-specialists.",
            "For the research-practice gap, say that raw signal handling, feature extraction, model training, and application deployment are often separated rather than integrated.",
            "Then clearly say what your project contributes: one repository containing preprocessing, training, evaluation, saved artifacts, and a GUI."
        ],
    },
    8: {
        "title": "Research Gaps and Objectives",
        "notes": [
            "This slide should sound like a transition from literature to your implementation.",
            "State the gap precisely: the need is not only for classification accuracy but for a demonstrable, explainable, and reproducible mechanical engineering tool.",
            "Go through the objectives naturally: preprocess the signals, extract 25 features, compare SVM and Random Forest, evaluate systematically, and deploy the Streamlit dashboard.",
            "If asked why 2048 samples and 50 percent overlap were chosen, answer: that window keeps localized fault information while generating enough training examples; with 48 kHz sampling it corresponds to about 42.67 milliseconds per window."
        ],
    },
    9: {
        "title": "Methodology and System Design",
        "notes": [
            "Walk through the pipeline from left to right as if you are tracing the data flow.",
            "Start from the data source: raw CWRU MAT files representing four bearing conditions.",
            "Then explain preprocessing: each long signal is segmented into 2048-sample windows with 50 percent overlap, producing 9,736 usable training samples.",
            "Next explain feature extraction: the segmented windows are converted into engineered time-domain and frequency-domain descriptors.",
            "Then explain modeling: SVM and Random Forest are trained on the processed feature table using an 80:20 split.",
            "Finally explain deployment: the best saved model is loaded inside the Streamlit dashboard for live inference.",
            "If asked what scripts actually run this pipeline, answer: scripts/build_dataset.py prepares the dataset, scripts/train_model.py trains the models, and the app is in app/streamlit_app.py."
        ],
    },
    10: {
        "title": "Feature Extraction Module",
        "notes": [
            "Explain that feature extraction is the bridge between raw signal and classification.",
            "For time-domain features, give intuitive meanings: mean and standard deviation show central level and spread, RMS reflects energy, kurtosis and crest factor respond to impulsive defects, and impulse/shape/form factors capture waveform characteristics.",
            "For frequency-domain features, explain that FFT transforms the signal into spectral form, then features such as spectral mean, dominant frequency, spectral standard deviation, and frequency variation describe how the energy is distributed.",
            "Point out the dataset summary again: 9,736 windows, 25 features, 4 classes, 48 kHz sampling.",
            "If asked whether the model uses raw amplitude directly, answer: no, the classifier uses the extracted feature vector, not the raw sequence itself."
        ],
    },
    11: {
        "title": "Model Performance",
        "notes": [
            "Present this as measured evidence rather than a claim.",
            "State that both models performed strongly, but Random Forest achieved the best result with 97.59 percent accuracy and 97.59 percent weighted F1-score on the held-out test set.",
            "Mention that SVM with RBF kernel also performed well, which shows that the feature design itself is meaningful.",
            "Explain why Random Forest was finally selected: it slightly outperformed SVM and also provides feature importance, which helps explain the model during demonstration.",
            "If asked what weighted F1-score means, answer: it balances precision and recall across all classes while accounting for class support, making it useful for multiclass evaluation."
        ],
    },
    12: {
        "title": "Confusion Matrix and Feature Importance",
        "notes": [
            "First explain the confusion matrix. Rows are true classes, columns are predicted classes.",
            "Read the key diagonal numbers: Ball Fault 558, Inner Race Fault 606, Normal 187, Outer Race Fault 550. Emphasize that strong diagonal entries mean strong correct classification.",
            "Mention that the off-diagonal values are comparatively low, so class confusion is limited.",
            "Then move to feature importance. Say that the Random Forest model ranks which features contribute more strongly to its decisions.",
            "Call out the most important features shown: Spectral Mean, Impulse Factor, Standard Deviation, Frequency Variation, Maximum Absolute value, and RMS.",
            "If asked why these matter physically, answer: they reflect how rough, impulsive, and spectrally concentrated the vibration becomes under defective bearing conditions."
        ],
    },
    13: {
        "title": "Summary and Conclusion",
        "notes": [
            "Use this as your closing technical slide.",
            "Summarize the major achievement: the project integrates mechanical vibration analysis, feature engineering, machine learning classification, and GUI deployment in one system.",
            "Restate the most important performance number only once: Random Forest reached 97.59 percent accuracy on the CWRU benchmark dataset.",
            "For future scope, mention validation on real industrial signals, comparison with advanced methods like XGBoost or 1D-CNN, fault severity estimation, and deployment to edge or IoT settings.",
            "If asked what next semester work could be, answer: expanding to real sensor data, testing robustness under noise, and moving from fault type classification toward severity or remaining useful life estimation."
        ],
    },
    14: {
        "title": "References",
        "notes": [
            "Keep this slide brief. Mention that the project is grounded in the official CWRU dataset source, key bearing diagnosis papers, and the Streamlit documentation used for the application layer.",
            "If a professor asks which references are most important, point to the CWRU Bearing Data Center first, then Kankar et al. for feature-based bearing fault diagnosis, and Rajeswari et al. for signal-processing plus SVM-based work."
        ],
    },
    15: {
        "title": "Thank You / Discussion",
        "notes": [
            "Close confidently and invite questions. At this point, be ready to switch from presentation mode to explanation mode.",
            "If they ask for a demo, open the Streamlit app and show one test CSV, the waveform, the FFT plot, the predicted class, and the confidence table.",
            "If they ask what is unique about your project, answer: the contribution is the full pipeline from raw vibration signal to deployable diagnosis dashboard, not just a model accuracy experiment."
        ],
    },
}


VIVA_QA = [
    ("What is the input to the system?", "The input is bearing vibration amplitude data, usually given as a time-series signal or CSV containing sampled amplitude values."),
    ("What is the output?", "The output is the predicted bearing condition: Normal, Ball Fault, Inner Race Fault, or Outer Race Fault, along with class confidence and signal visualizations."),
    ("From where is the dataset taken?", "The dataset is taken from the Case Western Reserve University Bearing Data Center, which is a public benchmark dataset for bearing fault diagnosis [1]."),
    ("What type of dataset is it?", "It is a vibration time-series dataset collected from bearings under healthy and faulty operating conditions."),
    ("Why did you segment the data?", "One raw recording is long and contains many local patterns. Segmentation converts it into smaller windows that become training samples while preserving short-term fault signatures."),
    ("Why 2048 samples?", "It provides a practical balance between preserving local vibration structure and generating enough windows for training. At 48 kHz it corresponds to about 42.67 milliseconds."),
    ("Why 50 percent overlap?", "Overlap increases the number of usable samples and reduces the chance of losing important transient information between adjacent windows."),
    ("How many samples did you train on?", "The processed dataset contains 9,736 labeled windows, generated from the raw CWRU signals after segmentation."),
    ("Why use feature extraction instead of raw signals directly?", "Feature extraction compresses the signal into meaningful descriptors such as RMS, kurtosis, and spectral features, making classical ML models more interpretable and efficient."),
    ("Which algorithms were used?", "Support Vector Machine with RBF kernel and Random Forest were trained and compared; Random Forest was selected as the final deployment model."),
    ("Why Random Forest?", "It achieved the best weighted F1-score in this project and also provided feature importance, which helps explain the prediction process."),
    ("How do you validate correctness?", "The dataset was split into training and testing partitions using a stratified 80:20 split. The model was trained on the training set and evaluated on unseen test data through accuracy, weighted F1-score, and confusion matrix."),
    ("What does the confusion matrix show?", "It shows how many samples of each true class were predicted into each class. Strong diagonal values indicate strong correct classification."),
    ("How are confidence values calculated?", "They come from the classifier's predicted class probabilities. The class with the highest probability becomes the final prediction."),
    ("What is the practical mechanical use of this project?", "It supports vibration-based condition monitoring and predictive maintenance for rotating machinery such as motors, pumps, turbines, and compressors."),
]


def xml_escape(text: str) -> str:
    return (
        html.escape(text, quote=False)
        .replace("'", "&apos;")
        .replace('"', "&quot;")
    )


def build_notes_paragraphs(lines: list[str]) -> str:
    paragraphs = []
    for line in lines:
        paragraphs.append(
            "<a:p>"
            '<a:pPr lvl="0"/>'
            '<a:r><a:rPr lang="en-US" sz="1200"/><a:t>'
            + xml_escape(line)
            + "</a:t></a:r>"
            '<a:endParaRPr lang="en-US" sz="1200"/>'
            "</a:p>"
        )
    return "".join(paragraphs)


def replace_notes_body(xml: str, lines: list[str]) -> str:
    new_body = (
        "<p:txBody><a:bodyPr/><a:lstStyle/>"
        + build_notes_paragraphs(lines)
        + "</p:txBody>"
    )
    pattern = (
        r'(<p:sp><p:nvSpPr><p:cNvPr id="3" name="Notes Placeholder 2"/>'
        r'.*?<p:spPr/>)<p:txBody>.*?</p:txBody>(</p:sp>)'
    )
    return re.sub(pattern, r"\1" + new_body + r"\2", xml, flags=re.DOTALL)


def create_updated_ppt() -> None:
    with ZipFile(SOURCE_PPT, "r") as zin, ZipFile(OUTPUT_PPT, "w", compression=ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", item.filename):
                slide_num = int(re.search(r"(\d+)", item.filename).group(1))
                if slide_num in SLIDE_NOTES:
                    xml = data.decode("utf-8", errors="ignore")
                    title = SLIDE_NOTES[slide_num]["title"]
                    bullets = SLIDE_NOTES[slide_num]["notes"]
                    full_lines = [f"Slide {slide_num}: {title}"] + bullets
                    updated = replace_notes_body(xml, full_lines)
                    data = updated.encode("utf-8")
            zout.writestr(item, data)


def create_notes_text() -> None:
    lines: list[str] = []
    lines.append("SPEAKER NOTES FOR FINAL PPT")
    lines.append("=" * 80)
    lines.append("")
    for slide_num in range(1, 16):
        block = SLIDE_NOTES[slide_num]
        lines.append(f"SLIDE {slide_num}: {block['title']}")
        lines.append("-" * 80)
        for idx, note in enumerate(block["notes"], start=1):
            lines.append(f"{idx}. {note}")
        lines.append("")
    lines.append("LIKELY PROFESSOR / VIVA QUESTIONS")
    lines.append("=" * 80)
    lines.append("")
    for idx, (q, a) in enumerate(VIVA_QA, start=1):
        lines.append(f"{idx}. Q: {q}")
        lines.append(f"   A: {a}")
        lines.append("")
    OUTPUT_TXT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    create_updated_ppt()
    create_notes_text()
    print(f"Wrote {OUTPUT_PPT}")
    print(f"Wrote {OUTPUT_TXT}")


if __name__ == "__main__":
    main()
