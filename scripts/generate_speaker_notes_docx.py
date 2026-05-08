from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from add_ppt_speaker_notes import SLIDE_NOTES, VIVA_QA


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DOCX = ROOT / "Speaker_Notes_For_Presentation.docx"


def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def paragraph(
    text: str,
    *,
    bold: bool = False,
    size_half_points: int = 24,
    center: bool = False,
    after: int = 120,
    before: int = 0,
) -> str:
    jc = '<w:jc w:val="center"/>' if center else '<w:jc w:val="both"/>'
    bold_tag = "<w:b/>" if bold else ""
    return f"""
    <w:p>
      <w:pPr>
        {jc}
        <w:spacing w:line="276" w:lineRule="auto" w:before="{before}" w:after="{after}"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
          <w:sz w:val="{size_half_points}"/>
          <w:szCs w:val="{size_half_points}"/>
          {bold_tag}
        </w:rPr>
        <w:t xml:space="preserve">{xml_escape(text)}</w:t>
      </w:r>
    </w:p>
    """


def page_break() -> str:
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def build_document_xml() -> str:
    parts: list[str] = []

    parts.append(paragraph("Speaker Notes For Project Presentation", bold=True, size_half_points=32, center=True, after=180))
    parts.append(paragraph(
        "Project: Intelligent Bearing Fault Diagnosis for Predictive Maintenance Using Vibration Signal Analysis and Machine Learning",
        bold=True,
        size_half_points=26,
        center=True,
        after=120,
    ))
    parts.append(paragraph(
        "Prepared for slide-by-slide speaking support, viva preparation, and question handling during the final presentation.",
        size_half_points=24,
        center=True,
        after=180,
    ))

    for slide_no in range(1, 16):
        slide = SLIDE_NOTES[slide_no]
        parts.append(page_break() if slide_no > 1 else "")
        parts.append(paragraph(f"Slide {slide_no}: {slide['title']}", bold=True, size_half_points=28, after=140))
        parts.append(paragraph("What to say:", bold=True, size_half_points=24, after=100))
        for idx, note in enumerate(slide["notes"], start=1):
            parts.append(paragraph(f"{idx}. {note}", size_half_points=24, after=80))

        parts.append(paragraph("Quick questions you may face on this slide:", bold=True, size_half_points=24, after=100, before=80))

        slide_questions = {
            1: [
                ("Q1", "Why did you choose this topic?", "We chose this topic because it connects a core mechanical engineering problem, bearing condition monitoring, with a practical machine learning implementation. It is also a strong project for demonstration because we can show raw vibration input, feature extraction, prediction, and GUI output in one complete workflow."),
                ("Q2", "What is the main goal of the project?", "The main goal is to detect bearing fault type automatically from vibration data. In this project, that means converting raw vibration signals into engineered features, training classification models, and using the best model inside a dashboard for live diagnosis."),
            ],
            2: [
                ("Q3", "How is the presentation organized?", "The presentation is organized in a logical engineering order. It starts with the problem background, then shows applications and literature, after that explains the methodology and implementation pipeline, and finally presents results, conclusion, and references."),
            ],
            3: [
                ("Q4", "Why is vibration used for bearing diagnosis?", "Vibration is used because bearing defects directly affect the dynamic response of rotating machinery. When a defect appears in the inner race, outer race, or ball element, the vibration waveform and frequency content both change, so vibration becomes a reliable non-invasive indicator of bearing health."),
                ("Q5", "Why are both time-domain and frequency-domain analyses needed?", "Time-domain analysis helps us measure signal spread, peaks, energy, and impulsiveness directly from amplitude variation. Frequency-domain analysis reveals where the vibration energy is concentrated after FFT. Using both gives the model a fuller description of the fault pattern than either domain alone."),
            ],
            4: [
                ("Q6", "What is the exact problem you are solving?", "The exact problem is automatic classification of bearing condition from vibration signal input. More specifically, we are solving a multiclass diagnosis problem in which short vibration windows must be assigned to the correct bearing state by the trained model."),
                ("Q7", "What are the output classes?", "The output classes in this project are Normal, Ball Fault, Inner Race Fault, and Outer Race Fault. These are the four classes used consistently across preprocessing, training, evaluation, and GUI inference."),
            ],
            5: [
                ("Q8", "Where can this system be used in mechanical engineering?", "This type of system can be used in rotating equipment such as motors, pumps, fans, turbines, compressors, and generator systems. In mechanical engineering terms, it supports condition monitoring and predictive maintenance by identifying faults before major failure occurs."),
            ],
            6: [
                ("Q9", "What types of methods already exist in literature?", "The literature mainly contains three groups of methods: classical signal-processing approaches, feature-based machine learning methods, and deep learning methods. Classical methods focus on waveform or transformed signal interpretation, feature-based methods train classifiers on engineered descriptors, and deep learning tries to learn directly from raw or transformed inputs."),
                ("Q10", "Why is the CWRU dataset so commonly used?", "The CWRU dataset is widely used because it is a public benchmark dataset with known fault labels and controlled recording conditions. That makes it suitable for comparing different diagnosis techniques and for building academic prototypes like this project."),
            ],
            7: [
                ("Q11", "What limitations did you identify in earlier work?", "The major limitations we identified were incomplete preprocessing explanation, lack of an accessible user-facing interface, and separation between research accuracy claims and deployable workflows. Many studies show final results, but not all show a reproducible pipeline from raw signal to final prediction."),
            ],
            8: [
                ("Q12", "What research gap does your project address?", "This project addresses the gap between fault-classification research and a demonstration-ready engineering workflow. It combines preprocessing, feature extraction, model comparison, result visualization, and GUI deployment in one consistent system."),
                ("Q13", "What are your main objectives?", "The main objectives are to preprocess the CWRU signal data, extract time-domain and frequency-domain features, train and compare SVM and Random Forest, evaluate performance with proper metrics, and deploy the selected model through a Streamlit application."),
            ],
            9: [
                ("Q14", "Explain your full pipeline from raw data to prediction.", "The pipeline starts from raw MATLAB vibration files in the dataset. These signals are segmented into overlapping windows, each window is converted into an engineered feature vector, the processed dataset is used to train classifiers, and the best saved model is then loaded into the GUI. When a new CSV is uploaded, the same feature extraction path is repeated and the saved model predicts the fault type."),
                ("Q15", "Which scripts or files handle the training workflow?", "In the repository, scripts/build_dataset.py creates the processed dataset, scripts/train_model.py trains and evaluates the models, the main reusable logic is in src/bearing_fault_diagnosis, and app/streamlit_app.py handles the final inference and visualization layer."),
            ],
            10: [
                ("Q16", "What features are extracted?", "The extracted features include time-domain descriptors such as mean, standard deviation, mean absolute deviation, RMS, maximum absolute amplitude, skewness, kurtosis, crest factor, shape factor, form factor, and impulse factor. Frequency-domain descriptors include spectral mean, spectral standard deviation, dominant frequency, centroid-related measures, frequency variance, and variation factor."),
                ("Q17", "Why did you use 2048 samples and 50 percent overlap?", "A 2048-sample window is large enough to retain useful local vibration structure while still producing many training samples from one long signal. A 50 percent overlap helps preserve transient information between adjacent windows and improves sample continuity in the processed dataset."),
            ],
            11: [
                ("Q18", "Which model performed best and why?", "Random Forest performed best in this project. It achieved slightly higher accuracy and weighted F1-score than the SVM model, and it also provided feature importance values that made the final system easier to explain during presentation."),
                ("Q19", "What does weighted F1-score mean?", "Weighted F1-score is a combined performance measure based on precision and recall, with weighting according to class support. In a multiclass problem, it is useful because it reflects overall balance of classification quality across classes instead of looking at accuracy alone."),
            ],
            12: [
                ("Q20", "How do you interpret the confusion matrix?", "The confusion matrix compares true labels with predicted labels. The diagonal values show correct predictions, while off-diagonal values show errors. In our project, strong diagonal counts indicate that the classifier distinguishes the four bearing conditions effectively."),
                ("Q21", "What does feature importance tell you?", "Feature importance tells us which extracted features contribute more strongly to the Random Forest decision process. In this project, high-importance features like spectral mean, impulse factor, standard deviation, and RMS indicate which physical signal characteristics are most helpful for separating fault classes."),
            ],
            13: [
                ("Q22", "What is the final conclusion of the project?", "The final conclusion is that a properly engineered feature-based machine learning pipeline can classify bearing fault conditions effectively on the CWRU dataset, and that the developed dashboard makes the system practical for academic demonstration and condition monitoring explanation."),
                ("Q23", "What can be done in future work?", "Future work can include validation on real industrial vibration signals, testing additional models such as XGBoost or 1D-CNN, moving toward fault severity estimation, and extending the project to remaining useful life prediction or edge deployment."),
            ],
            14: [
                ("Q24", "Which references are most important for this project?", "The most important references are the official CWRU Bearing Data Center because it provides the dataset foundation, and the published bearing diagnosis studies that justify feature-based classification and signal-processing-based fault analysis. The Streamlit documentation is also important for the application layer."),
            ],
            15: [
                ("Q25", "If asked for a demo, what will you show first?", "First I would open the Streamlit application and upload one prepared test CSV. Then I would show the waveform, the FFT plot, the predicted fault class, the confidence values, and the extracted features. This makes the pipeline visible from input signal to final classification."),
            ],
        }

        for qno, qtext, ans in slide_questions.get(slide_no, []):
            parts.append(paragraph(f"{qno}. {qtext}", bold=True, size_half_points=24, after=55))
            parts.append(paragraph(f"Answer: {ans}", size_half_points=24, after=75))

    parts.append(page_break())
    parts.append(paragraph("General Viva Questions And Answers", bold=True, size_half_points=30, center=True, after=160))

    for idx, (question, answer) in enumerate(VIVA_QA, start=1):
        parts.append(paragraph(f"Q{idx}. {question}", bold=True, size_half_points=24, after=80))
        parts.append(paragraph(f"Answer: {answer}", size_half_points=24, after=90))

    body = "".join(p for p in parts if p)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
 xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
 xmlns:v="urn:schemas-microsoft-com:vml"
 xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
 xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
 xmlns:w10="urn:schemas-microsoft-com:office:word"
 xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
 xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
 xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
 xmlns:wne="http://schemas.microsoft.com/office/2006/wordml"
 xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
 mc:Ignorable="w14 wp14">
  <w:body>
    {body}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>
"""


def main() -> None:
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""
    now = datetime.now(timezone.utc).isoformat()
    core = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Speaker Notes For Presentation</dc:title>
  <dc:creator>OpenAI Codex</dc:creator>
  <cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
"""
    app = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft Office Word</Application>
</Properties>
"""

    with ZipFile(OUTPUT_DOCX, "w", compression=ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("docProps/core.xml", core)
        zf.writestr("docProps/app.xml", app)
        zf.writestr("word/document.xml", build_document_xml())

    print(f"Wrote {OUTPUT_DOCX}")


if __name__ == "__main__":
    main()
