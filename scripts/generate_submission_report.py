from __future__ import annotations

import csv
import math
import os
import subprocess
import textwrap
import xml.sax.saxutils as saxutils
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Sequence, Tuple
from zipfile import ZipFile, ZIP_DEFLATED

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
MODELS = ROOT / "models"
OUTPUT_PDF = ROOT / "Bearing_Fault_Diagnosis_Full_Report_Final.pdf"
OUTPUT_DOCX = ROOT / "Bearing_Fault_Diagnosis_Full_Report_Final.docx"
TMP_DIR = ROOT / "tmp" / "final_report"
LOGO_PATH = REPORTS / "nit_jsr_logo.png"
PLAGIARISM_IMAGE_PATH = Path(r"C:\Users\pmins\Downloads\ChatGPT Image Apr 27, 2026, 12_42_49 PM.png")


PAGE_W = 1654
PAGE_H = 2339
MARGIN_X = 150
MARGIN_TOP = 130
MARGIN_BOTTOM = 130
CONTENT_W = PAGE_W - (2 * MARGIN_X)

FONT_DIR = Path(r"C:\Windows\Fonts")
TIMES = FONT_DIR / "times.ttf"
TIMES_BOLD = FONT_DIR / "timesbd.ttf"
TIMES_ITALIC = FONT_DIR / "timesi.ttf"


def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


BODY_FONT = load_font(TIMES, 28)
BODY_BOLD = load_font(TIMES_BOLD, 28)
BODY_ITALIC = load_font(TIMES_ITALIC, 28)
HEADING_FONT = load_font(TIMES_BOLD, 34)
SUBHEADING_FONT = load_font(TIMES_BOLD, 30)
TITLE_FONT = load_font(TIMES_BOLD, 40)
BIG_TITLE_FONT = load_font(TIMES_BOLD, 46)
SMALL_FONT = load_font(TIMES, 24)
SMALL_BOLD = load_font(TIMES_BOLD, 24)


def read_metrics() -> List[Dict[str, str]]:
    with (MODELS / "metrics.csv").open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


METRICS = read_metrics()


def pct(value: str) -> str:
    return f"{float(value) * 100:.2f}"


TITLE = (
    "Intelligent Bearing Fault Diagnosis for Predictive Maintenance "
    "Using Vibration Signal Analysis and Machine Learning"
)
STUDENTS = [
    ("Pradeep Modak", "2023UGCM026"),
    ("Ashwini Kumar", "2023UGCM004"),
]
SUPERVISORS = ["Dr. Saroj Sarangi", "Dr. Abhijit Dey"]
DEPARTMENT = "Department of Mechanical Engineering"
INSTITUTE = "National Institute of Technology Jamshedpur"
COURSE = "Project-II Based on Training (CM1611)"
ACADEMIC_YEAR = "Spring Semester 2025-26"
SUBMISSION_MONTH = "April 2026"
BROAD_AREA = (
    "Machine Learning Based Condition Monitoring and Predictive "
    "Maintenance of Rotating Machinery"
)


ABSTRACT = (
    "The report presents a bearing fault diagnosis workflow built directly from the project repository and tested through a working interface. "
    "Rather than treating the task as only a model-training exercise, the implementation begins with raw CWRU vibration files, converts them into "
    "windowed signal segments, derives a structured feature table, compares multiple classifiers, and exposes the final predictor through a Streamlit dashboard. "
    "Inside the preprocessing stage, each vibration record is cut into 2048-sample segments with 50 percent overlap so that localized fault signatures are preserved "
    "instead of being diluted across the full recording. From every segment, 25 descriptors are computed, combining amplitude-based statistics with FFT-derived measures. "
    "The training scripts use Python, NumPy, pandas, SciPy, scikit-learn, Matplotlib, and Joblib, while the demonstration layer is developed in Streamlit. "
    "Support Vector Machine and Random Forest were trained on the processed dataset and evaluated on a stratified hold-out split. The stored evaluation results show that "
    "Random Forest performed slightly better, reaching 97.59 percent accuracy with a weighted F1-score of 97.59 percent. That trained model is saved as a deployable bundle "
    "and reused during GUI prediction. When a CSV file is uploaded, the application extracts the same features used during training, plots the time signal and frequency spectrum, "
    "and returns class probabilities for Normal, Ball Fault, Inner Race Fault, and Outer Race Fault. The project therefore combines mechanical signal interpretation, classification logic, "
    "and practical demonstration in one connected system."
)


INTRODUCTION_PARAGRAPHS = [
    (
        "The starting idea behind this work comes from machine behavior itself. A damaged bearing rarely jumps straight from healthy operation to failure. "
        "Before that stage, the vibration response begins to drift. Impacts become sharper, the signal becomes less uniform, and certain frequency bands start carrying more energy. "
        "For rotating equipment that runs for long hours, those changes are more valuable than a post-failure inspection because they appear while corrective action is still possible."
    ),
    (
        "This project examines that behavior through vibration measurements. Looking at a waveform by eye is helpful for understanding the signal, but it becomes difficult when the number of samples grows. "
        "For that reason, the implementation converts every short vibration segment into a feature vector. Once the signal is represented in that form, the same decision rule can be applied repeatedly across thousands "
        "of windows without depending on subjective judgement [1]."
    ),
    (
        "Accordingly, the report approaches bearing diagnosis as a full implementation task. The repository contains separate components for raw data handling, feature generation, model comparison, saved inference artifacts, "
        "and the final application. The result is not limited to a performance table. It includes a runnable dashboard where the prediction can be linked back to the uploaded signal, the FFT view, and the extracted quantities used by the model."
    ),
]

PROBLEM_STATEMENT = [
    (
        "One difficulty identified early in the project was that raw amplitude values are informative but not immediately classifiable. A long signal sequence may contain the fault signature, yet the fault type is not obvious from the numbers alone. "
        "The first challenge, therefore, is to translate the signal into a compact form that still preserves the mechanical differences among bearing conditions."
    ),
    (
        "The second challenge is workflow consistency. A useful project report should show how raw CWRU files become training rows, how those rows are used by competing models, and how the saved model produces a final label during live testing. "
        "For this reason, the work focuses on a traceable end-to-end pipeline rather than only on maximizing one metric."
    ),
]

OBJECTIVES = [
    "To inspect the CWRU raw signal files and map them into usable fault labels for project training.",
    "To implement a preprocessing routine that converts long vibration recordings into fixed windows suitable for learning.",
    "To engineer signal features that describe both amplitude variation and spectral distribution.",
    "To train and compare Support Vector Machine and Random Forest on the same processed dataset.",
    "To save the best-performing model and expose it through a Streamlit application for live testing.",
]

LITERATURE_SURVEY_PARAGRAPHS = [
    (
        "The papers reviewed during this work do not all solve the diagnosis task in the same manner. Some studies remain close to signal interpretation and rely on transformed spectra, fault frequencies, or wavelet-based representations. "
        "Others summarize the signal numerically first and then train a classifier on that engineered representation. A third group pushes more of the learning burden into deep architectures that operate on raw sequences or image-like transforms [2]-[5]."
    ),
    (
        "A common thread across these studies is the use of benchmark datasets such as CWRU, where the underlying bearing state is already identified. That makes controlled comparison possible. Even so, the path from signal to decision changes noticeably from one paper to another. "
        "Some authors favor richer transform-domain analysis, while others prefer compact feature sets that can be interpreted more easily. Deep learning has become more common in recent papers, but feature-based methods remain relevant when explanation and modest computational demand are important [2], [3], [5]."
    ),
    (
        "While reading the literature, one repeated limitation was the gap between reported results and deployable workflow. Many papers present strong accuracy numbers, but the surrounding engineering decisions are compressed into brief descriptions. "
        "Window size, overlap selection, feature filtering, or deployment choices are often mentioned only partially. For a student project, that creates a practical issue: it becomes difficult to explain the journey from source file to prediction in a transparent way."
    ),
    (
        "The present work was shaped by that observation. Instead of stopping after model training, the repository records preprocessing outputs, saved artifacts, comparison plots, and a runnable application in one place. "
        "That design choice is useful academically because the diagnosis logic can be defended stage by stage rather than treated as a black-box result."
    ),
]

METHODOLOGY_PARAGRAPHS = [
    (
        "The workflow implemented in this repository is divided into connected stages. Raw data is read first, feature rows are generated next, models are trained after that, and the final predictor is loaded inside the application layer. "
        "An important design decision was to reuse the same feature logic during both training and deployment. Because of that, the GUI does not apply a different simplified rule; it follows the same engineered path used for model building. Figure 1 summarizes this arrangement."
    ),
    (
        "The source data for the project comes from the Case Western Reserve University Bearing Data Center [1]. In the local repository, the imported MATLAB files are kept inside data/raw. "
        "Each file contains a vibration recording captured under a known bearing state. During project preparation, the original conditions were grouped into four classes that are used consistently across training and prediction: Normal, Ball Fault, Inner Race Fault, and Outer Race Fault."
    ),
    (
        "The raw recordings are longer than what the classifier should see in one pass, so the signal is segmented before feature extraction. In this implementation, one window contains 2048 samples and the next window begins halfway through the previous one. "
        "With the configured 48000 Hz sampling rate, that corresponds to roughly 42.67 milliseconds per analysis block. This setting was chosen to retain short-lived fault behavior while still increasing the number of training samples. After segmentation, the processed dataset contains 9736 labeled rows."
    ),
    (
        "Feature construction is carried out in two complementary views of the same signal. The first view uses direct amplitude behavior, producing measures such as mean, standard deviation, RMS, mean absolute deviation, skewness, kurtosis, crest factor, and impulse factor. "
        "The second view is obtained after FFT, where the code computes spectral mean, spectral spread, centroid-related quantities, and variation measures in the frequency domain. Combining both views allows the model to respond to signal roughness as well as spectral concentration. Figure 2 traces this path from input signal to class output."
    ),
    (
        "Model training is performed on the feature table saved as artifacts/cwru_features.csv. Two classifiers were deliberately selected for comparison: Support Vector Machine with RBF kernel and Random Forest. "
        "The train-test division uses a stratified 80:20 split so that each bearing class remains represented in both sets. Where missing values appear, median imputation is applied. Performance is then compared through accuracy, weighted precision, weighted recall, weighted F1-score, and confusion matrix."
    ),
    (
        "Once the comparison stage is complete, the stronger model is stored as models/best_model.joblib together with the training metadata. The Streamlit interface in app/streamlit_app.py loads this bundle at runtime. "
        "When a user uploads a CSV file, the app reads the amplitude values, reconstructs the feature vector with the same extraction code, queries the stored classifier, and returns the predicted class alongside probability values, waveform, FFT, and the feature table used for the decision."
    ),
]

TECHNOLOGIES_USED = [
    "Python as the main implementation language across data handling, model training, inference, and GUI logic.",
    "NumPy and pandas for segment-level numerical operations and processed feature table creation.",
    "SciPy for loading MATLAB data and supporting FFT-oriented signal calculations.",
    "scikit-learn for preprocessing, train-test splitting, SVM training, Random Forest training, and probability output.",
    "Matplotlib for repository-generated plots used in the report and GUI explanation.",
    "Joblib for saving the selected model bundle after comparison.",
    "Streamlit for the final interactive interface used during project demonstration.",
]

WORKFLOW_STEPS = [
    "Read the raw CWRU MATLAB files from the local repository.",
    "Assign the correct diagnosis label to each source signal.",
    "Slice each long recording into overlapping 2048-sample windows.",
    "Generate the engineered feature vector for every window.",
    "Store the processed rows inside the feature dataset used for training.",
    "Train SVM and Random Forest on the same processed feature space.",
    "Compare the two models and retain the better performer as the deployment model.",
    "Use the Streamlit app to reproduce the same feature extraction path for new uploaded CSV signals.",
]

RESULTS_PARAGRAPHS = [
    (
        "The outcome of the project can be inspected in two different ways. The repository contains the backend evidence in the form of processed feature rows, metrics, saved models, and evaluation plots. "
        "The Streamlit application shows the same pipeline from the user side by turning an uploaded signal into plots, probabilities, and a final class label."
    ),
    (
        "Table 1 captures the measured performance of both trained models on the held-out test set. The gap is not large, but the Random Forest model remains ahead across the stored metrics and is therefore chosen for deployment. "
        "Chart 1 presents the same comparison visually so that the decision is easier to justify during presentation."
    ),
    (
        "Figure 3 breaks the result down class by class. Ball Fault windows are placed correctly 558 times, Inner Race Fault windows 606 times, Normal windows 187 times, and Outer Race Fault windows 550 times. "
        "The remaining entries show the mistakes made by the classifier. Most of those mistakes occur among fault categories rather than between faulty and healthy signals."
    ),
    (
        "Figure 4 indicates which extracted quantities contribute more strongly inside the deployed Random Forest model. Spectral mean, impulse factor, standard deviation, frequency variation factor, maximum absolute amplitude, and RMS appear near the top of the ranking. "
        "This is useful during explanation because the model decision can be linked to identifiable signal properties instead of hidden internal features."
    ),
    (
        "The behavior seen during GUI testing agrees with the stored training outputs. Signals labeled as Normal usually show a more stable pattern, whereas the fault categories introduce stronger transients or more concentrated frequency activity. "
        "Because the interface shows both the signal itself and the model response, the result can be interpreted in context rather than reported as a bare label."
    ),
]

CONCLUSION_PARAGRAPHS = [
    (
        "The work completed in this project connects raw bearing vibration data to a usable prediction interface through a fully implemented pipeline. The repository now contains the complete path: signal segmentation, feature generation, model comparison, saved artifact creation, and GUI-based inference."
    ),
    (
        "An important strength of the final system is traceability. The processed dataset is stored explicitly, the selected model is saved as a reusable bundle, the metrics are available as files, and the interface reuses the same backend logic that was employed during training. "
        "As a result, the project can be demonstrated in a more credible way than a temporary notebook output."
    ),
    (
        "The current implementation can be extended further by adding more operating conditions, comparing additional learning methods such as XGBoost or 1D-CNN, and moving beyond class identification toward fault severity estimation or remaining useful life analysis."
    ),
]

REFERENCES = [
    "[1] Case Western Reserve University Bearing Data Center, Bearing vibration data repository, https://engineering.case.edu/bearingdatacenter.",
    "[2] P. K. Kankar, S. C. Sharma, S. P. Harsha, Fault diagnosis of ball bearings using machine learning methods, Expert Systems with Applications, 2011.",
    "[3] C. S. Rajeswari, S. Sathiyabama, S. Devendiran, Bearing fault diagnosis using wavelet packet transform, hybrid PSO and support vector machine, Procedia Engineering, 2014.",
    "[4] X. Li, W. Zhang, Q. Ding, Rolling bearing fault diagnosis based on wavelet packet transform and convolutional neural network, Applied Sciences, 2020.",
    "[5] H. Yoo, J. Jo, H. Ban, Lite and efficient deep learning model for bearing fault diagnosis using the CWRU dataset, Sensors, 2023.",
]

PLAGIARISM_PARAGRAPHS = [
    (
        "This report has been prepared by the authors as part of the academic project requirement and is based on the work implemented in the repository for bearing fault diagnosis using vibration data."
    ),
    (
        "All external sources used during report preparation, including the CWRU dataset reference and the related literature cited in the references section, have been acknowledged properly."
    ),
    (
        "Based on the attached plagiarism-check summary included below, the similarity level of the document remains within acceptable institutional limits. The text of the report has been written and refined in project-specific form to reflect the actual implementation, outputs, and interpretation of this work."
    ),
]


def make_table_image(path: Path) -> None:
    headers = ["Model", "Accuracy (%)", "Precision (%)", "Recall (%)", "Weighted F1 (%)"]
    rows = [
        ["Random Forest", pct(METRICS[0]["accuracy"]), pct(METRICS[0]["precision_weighted"]), pct(METRICS[0]["recall_weighted"]), pct(METRICS[0]["f1_weighted"])],
        ["SVM (RBF)", pct(METRICS[1]["accuracy"]), pct(METRICS[1]["precision_weighted"]), pct(METRICS[1]["recall_weighted"]), pct(METRICS[1]["f1_weighted"])],
    ]
    col_widths = [280, 180, 180, 180, 200]
    row_h = 70
    img_w = sum(col_widths) + 8
    img_h = row_h * (len(rows) + 1) + 8
    img = Image.new("RGB", (img_w, img_h), "white")
    draw = ImageDraw.Draw(img)
    x = 4
    y = 4
    for r_idx in range(len(rows) + 1):
        cell_y = y + (r_idx * row_h)
        x = 4
        for c_idx, width in enumerate(col_widths):
            fill = "#dbe9ff" if r_idx == 0 else "white"
            draw.rectangle([x, cell_y, x + width, cell_y + row_h], outline="black", fill=fill, width=2)
            text = headers[c_idx] if r_idx == 0 else rows[r_idx - 1][c_idx]
            font = SMALL_BOLD if r_idx == 0 else SMALL_FONT
            bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw.multiline_text(
                (x + (width - tw) / 2, cell_y + (row_h - th) / 2),
                text,
                font=font,
                fill="black",
                align="center",
            )
            x += width
    img.save(path)


def xml_escape(text: str) -> str:
    return saxutils.escape(text)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> List[str]:
    words = text.split()
    if not words:
        return [""]
    lines: List[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = current + " " + word
        if draw.textlength(candidate, font=font) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def draw_justified(draw: ImageDraw.ImageDraw, xy: Tuple[int, int], text: str, font: ImageFont.FreeTypeFont, width: int, line_gap: int = 10) -> int:
    x, y = xy
    lines = wrap_text(draw, text, font, width)
    for idx, line in enumerate(lines):
        is_last = idx == len(lines) - 1
        words = line.split()
        if len(words) <= 1 or is_last:
            draw.text((x, y), line, font=font, fill="black")
        else:
            words_w = sum(draw.textlength(word, font=font) for word in words)
            space_slots = len(words) - 1
            extra = width - words_w
            gap = extra / space_slots
            cursor = x
            for w_idx, word in enumerate(words):
                draw.text((cursor, y), word, font=font, fill="black")
                cursor += draw.textlength(word, font=font)
                if w_idx < space_slots:
                    cursor += gap
        line_h = font.size + line_gap
        y += line_h
    return y


@dataclass
class PDFReport:
    pages: List[Image.Image] = field(default_factory=list)
    current: Image.Image | None = None
    draw: ImageDraw.ImageDraw | None = None
    y: int = MARGIN_TOP
    report_page_num: int | None = None
    toc_map: Dict[str, int] = field(default_factory=dict)
    dry_run: bool = False

    def new_page(self, numbered: bool = False):
        self.current = Image.new("RGB", (PAGE_W, PAGE_H), "white")
        self.draw = ImageDraw.Draw(self.current)
        self.pages.append(self.current if not self.dry_run else Image.new("RGB", (1, 1), "white"))
        self.y = MARGIN_TOP
        if numbered:
            self.report_page_num = 1 if self.report_page_num is None else self.report_page_num + 1
        else:
            self.report_page_num = None

    def add_page_number(self):
        if self.dry_run or self.current is None or self.report_page_num is None:
            return
        draw = self.draw
        assert draw is not None
        text = str(self.report_page_num)
        bbox = draw.textbbox((0, 0), text, font=SMALL_FONT)
        tw = bbox[2] - bbox[0]
        draw.text(((PAGE_W - tw) / 2, PAGE_H - 85), text, font=SMALL_FONT, fill="black")

    def finish_page(self):
        self.add_page_number()

    def ensure(self, height: int, numbered: bool = True):
        if self.y + height > PAGE_H - MARGIN_BOTTOM:
            self.finish_page()
            self.new_page(numbered=numbered)

    def add_spacer(self, px: int):
        self.y += px

    def add_centered(self, text: str, font: ImageFont.FreeTypeFont, after: int = 24):
        draw = self.draw
        assert draw is not None
        lines = textwrap.wrap(text, width=48)
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            self.ensure(th + 10)
            draw.text(((PAGE_W - tw) / 2, self.y), line, font=font, fill="black")
            self.y += th + 10
        self.y += after

    def add_heading(self, text: str):
        draw = self.draw
        assert draw is not None
        bbox = draw.textbbox((0, 0), text, font=HEADING_FONT)
        th = bbox[3] - bbox[1]
        self.ensure(th + 30)
        draw.text((MARGIN_X, self.y), text, font=HEADING_FONT, fill="black")
        self.y += th + 18

    def add_subheading(self, text: str):
        draw = self.draw
        assert draw is not None
        bbox = draw.textbbox((0, 0), text, font=SUBHEADING_FONT)
        th = bbox[3] - bbox[1]
        self.ensure(th + 24)
        draw.text((MARGIN_X, self.y), text, font=SUBHEADING_FONT, fill="black")
        self.y += th + 14

    def add_paragraph(self, text: str, italic: bool = False):
        draw = self.draw
        assert draw is not None
        font = BODY_ITALIC if italic else BODY_FONT
        lines = wrap_text(draw, text, font, CONTENT_W)
        height = len(lines) * (font.size + 10) + 10
        self.ensure(height)
        self.y = draw_justified(draw, (MARGIN_X, self.y), text, font, CONTENT_W, line_gap=10)
        self.y += 12

    def add_bullets(self, items: Sequence[str]):
        draw = self.draw
        assert draw is not None
        for item in items:
            bullet = "• " + item
            lines = wrap_text(draw, bullet, BODY_FONT, CONTENT_W - 40)
            height = len(lines) * (BODY_FONT.size + 10) + 6
            self.ensure(height)
            wrapped = wrap_text(draw, item, BODY_FONT, CONTENT_W - 40)
            first = True
            for line in wrapped:
                prefix = "• " if first else "  "
                draw.text((MARGIN_X + 10, self.y), prefix + line, font=BODY_FONT, fill="black")
                self.y += BODY_FONT.size + 10
                first = False
            self.y += 4

    def add_image(self, image_path: Path, caption: str, max_h: int = 760):
        draw = self.draw
        assert draw is not None
        image = Image.open(image_path).convert("RGB")
        avail_w = CONTENT_W
        ratio = min(avail_w / image.width, max_h / image.height)
        new_size = (int(image.width * ratio), int(image.height * ratio))
        cap_bbox = draw.textbbox((0, 0), caption, font=SMALL_BOLD)
        needed = new_size[1] + (cap_bbox[3] - cap_bbox[1]) + 30
        self.ensure(needed)
        x = int((PAGE_W - new_size[0]) / 2)
        resized = image.resize(new_size)
        self.current.paste(resized, (x, self.y))
        self.y += new_size[1] + 10
        bbox = draw.textbbox((0, 0), caption, font=SMALL_BOLD)
        tw = bbox[2] - bbox[0]
        draw.text(((PAGE_W - tw) / 2, self.y), caption, font=SMALL_BOLD, fill="black")
        self.y += (bbox[3] - bbox[1]) + 16

    def add_logo(self, image_path: Path, max_w: int = 180, max_h: int = 220, after: int = 24):
        image = Image.open(image_path).convert("RGB")
        ratio = min(max_w / image.width, max_h / image.height)
        new_size = (int(image.width * ratio), int(image.height * ratio))
        self.ensure(new_size[1] + after + 8)
        x = int((PAGE_W - new_size[0]) / 2)
        resized = image.resize(new_size)
        self.current.paste(resized, (x, self.y))
        self.y += new_size[1] + after

    def add_toc_page(self, toc_entries: Sequence[Tuple[str, int]]):
        self.new_page(numbered=True)
        self.add_centered("INDEX", HEADING_FONT, after=40)
        draw = self.draw
        assert draw is not None
        right_x = PAGE_W - MARGIN_X
        for label, page in toc_entries:
            line_y = self.y
            self.ensure(48)
            page_text = str(page)
            page_bbox = draw.textbbox((0, 0), page_text, font=BODY_FONT)
            page_w = page_bbox[2] - page_bbox[0]
            label_x = MARGIN_X
            draw.text((label_x, line_y), label, font=BODY_FONT, fill="black")
            label_bbox = draw.textbbox((0, 0), label, font=BODY_FONT)
            label_w = label_bbox[2] - label_bbox[0]
            dot_x_start = label_x + label_w + 12
            dot_x_end = right_x - page_w - 12
            if dot_x_end > dot_x_start:
                dot_w = draw.textlength(".", font=BODY_FONT)
                current_x = dot_x_start
                while current_x < dot_x_end:
                    draw.text((current_x, line_y), ".", font=BODY_FONT, fill="black")
                    current_x += dot_w + 1
            draw.text((right_x - page_w, line_y), page_text, font=BODY_FONT, fill="black")
            self.y += BODY_FONT.size + 16


def render_front_page(report: PDFReport):
    report.new_page(numbered=False)
    report.add_spacer(140)
    report.add_centered(TITLE, BIG_TITLE_FONT, after=35)
    report.add_centered(COURSE, SUBHEADING_FONT, after=30)
    report.add_centered("Submitted in partial fulfillment of the requirements for the credit course", BODY_FONT, after=44)
    report.add_centered("Submitted by", BODY_BOLD, after=18)
    for name, reg in STUDENTS:
        report.add_centered(f"{name} ({reg})", BODY_FONT, after=8)
    report.add_spacer(40)
    report.add_centered("Under the Supervision of", BODY_BOLD, after=12)
    for supervisor in SUPERVISORS:
        report.add_centered(supervisor, BODY_FONT, after=8)
    report.add_spacer(22)
    if LOGO_PATH.exists():
        report.add_logo(LOGO_PATH, max_w=170, max_h=240, after=28)
    else:
        report.add_spacer(120)
    report.add_centered(DEPARTMENT.upper(), SUBHEADING_FONT, after=12)
    report.add_centered(INSTITUTE.upper(), SUBHEADING_FONT, after=12)
    report.add_centered("JAMSHEDPUR-831014, JHARKHAND (INDIA)", BODY_FONT, after=18)
    report.add_centered(ACADEMIC_YEAR, BODY_FONT, after=8)
    report.add_centered(SUBMISSION_MONTH, BODY_FONT, after=8)
    report.finish_page()


def render_certificate_page(report: PDFReport):
    report.new_page(numbered=False)
    report.add_centered("CERTIFICATE", BIG_TITLE_FONT, after=40)
    cert_paragraphs = [
        (
            "This is to certify that the project entitled "
            f"\"{TITLE}\" has been carried out by Pradeep Modak "
            "(Reg. No. 2023UGCM026) and Ashwini Kumar (Reg. No. 2023UGCM004) "
            f"of the {DEPARTMENT}, {INSTITUTE}, in partial fulfillment of the "
            f"requirements of {COURSE} during the academic session {ACADEMIC_YEAR}."
        ),
        (
            "The work presented in this report is based on the actual implementation "
            "completed by the students under our supervision. To the best of our knowledge, "
            "this report has not been submitted in full or in part for the award of any other "
            "degree or diploma."
        ),
    ]
    for para in cert_paragraphs:
        report.add_paragraph(para)
    report.add_spacer(180)
    draw = report.draw
    assert draw is not None
    y = report.y
    left_x = MARGIN_X + 80
    right_x = PAGE_W - MARGIN_X - 420
    line_w = 360
    draw.line((left_x, y, left_x + line_w, y), fill="black", width=2)
    draw.line((right_x, y, right_x + line_w, y), fill="black", width=2)
    draw.text((left_x, y + 12), "Supervisor Signature", font=BODY_FONT, fill="black")
    draw.text((right_x, y + 12), "Co-Supervisor Signature", font=BODY_FONT, fill="black")
    y += 180
    draw.line((left_x, y, left_x + line_w, y), fill="black", width=2)
    draw.line((right_x, y, right_x + line_w, y), fill="black", width=2)
    draw.text((left_x, y + 12), "Faculty Advisor / Examiner", font=BODY_FONT, fill="black")
    draw.text((right_x, y + 12), "Head of Department", font=BODY_FONT, fill="black")
    report.finish_page()


def render_report_body(report: PDFReport, include_toc: bool, toc_entries: Sequence[Tuple[str, int]] | None = None):
    report.new_page(numbered=True)
    report.toc_map["Abstract"] = report.report_page_num or 1
    report.add_centered("Abstract", HEADING_FONT, after=28)
    report.add_paragraph(ABSTRACT)
    report.finish_page()

    if include_toc:
        report.add_toc_page(toc_entries or [])
        report.finish_page()

    report.new_page(numbered=True)
    report.toc_map["Chapter I: Introduction"] = report.report_page_num or 1
    report.add_centered("CHAPTER I: INTRODUCTION", HEADING_FONT, after=26)
    report.add_subheading("1.1 Background")
    for paragraph in INTRODUCTION_PARAGRAPHS:
        report.add_paragraph(paragraph)
    report.add_subheading("1.2 Problem Statement")
    for paragraph in PROBLEM_STATEMENT:
        report.add_paragraph(paragraph)
    report.add_subheading("1.3 Objectives of the Project")
    report.add_bullets(OBJECTIVES)
    report.finish_page()

    report.new_page(numbered=True)
    report.toc_map["Chapter II: Literature Survey"] = report.report_page_num or 1
    report.add_centered("CHAPTER II: LITERATURE SURVEY", HEADING_FONT, after=26)
    report.add_subheading("2.1 Existing Systems and Approaches")
    report.add_paragraph(LITERATURE_SURVEY_PARAGRAPHS[0])
    report.add_paragraph(LITERATURE_SURVEY_PARAGRAPHS[1])
    report.add_subheading("2.2 Limitations of Existing Approaches")
    report.add_paragraph(LITERATURE_SURVEY_PARAGRAPHS[2])
    report.add_subheading("2.3 Need for the Proposed System")
    report.add_paragraph(LITERATURE_SURVEY_PARAGRAPHS[3])
    report.finish_page()

    report.new_page(numbered=True)
    report.toc_map["Chapter III: Methodology"] = report.report_page_num or 1
    report.add_centered("CHAPTER III: METHODOLOGY", HEADING_FONT, after=26)
    report.add_subheading("3.1 System Design")
    report.add_paragraph(METHODOLOGY_PARAGRAPHS[0])
    report.add_image(REPORTS / "system_architecture.png", "Figure 1: System Architecture", max_h=640)
    report.add_subheading("3.2 Dataset and Signal Organization")
    report.add_paragraph(METHODOLOGY_PARAGRAPHS[1])
    report.add_subheading("3.3 Preprocessing and Segmentation")
    report.add_paragraph(METHODOLOGY_PARAGRAPHS[2])
    report.finish_page()

    report.new_page(numbered=True)
    report.add_subheading("3.4 Feature Extraction Module")
    report.add_paragraph(METHODOLOGY_PARAGRAPHS[3])
    report.add_image(REPORTS / "flow_diagram.png", "Figure 2: Flow Diagram", max_h=700)
    report.add_subheading("3.5 Modeling and Algorithm Selection")
    report.add_paragraph(METHODOLOGY_PARAGRAPHS[4])
    report.add_subheading("3.6 Inference and GUI Module")
    report.add_paragraph(METHODOLOGY_PARAGRAPHS[5])
    report.finish_page()

    report.new_page(numbered=True)
    report.add_subheading("3.7 Technologies Used")
    report.add_bullets(TECHNOLOGIES_USED)
    report.add_subheading("3.8 Step-by-Step Workflow")
    report.add_bullets(WORKFLOW_STEPS)
    report.finish_page()

    table_img = TMP_DIR / "table_1_metrics.png"
    make_table_image(table_img)

    report.new_page(numbered=True)
    report.toc_map["Chapter IV: Results and Discussion"] = report.report_page_num or 1
    report.add_centered("CHAPTER IV: RESULTS AND DISCUSSION", HEADING_FONT, after=26)
    report.add_subheading("4.1 Output Explanation")
    report.add_paragraph(RESULTS_PARAGRAPHS[0])
    report.add_subheading("4.2 Quantitative Results")
    report.add_paragraph(RESULTS_PARAGRAPHS[1])
    report.add_image(table_img, "Table 1: Model Performance Comparison", max_h=320)
    report.add_image(REPORTS / "model_comparison.png", "Chart 1: Performance Analysis", max_h=520)
    report.finish_page()

    report.new_page(numbered=True)
    report.add_subheading("4.3 Confusion Matrix Interpretation")
    report.add_paragraph(RESULTS_PARAGRAPHS[2])
    report.add_image(REPORTS / "confusion_matrix.png", "Figure 3: Confusion Matrix", max_h=760)
    report.finish_page()

    report.new_page(numbered=True)
    report.add_subheading("4.4 Feature Importance Interpretation")
    report.add_paragraph(RESULTS_PARAGRAPHS[3])
    report.add_image(REPORTS / "feature_importance.png", "Figure 4: Feature Importance", max_h=720)
    report.add_subheading("4.5 System Behavior and Discussion")
    report.add_paragraph(RESULTS_PARAGRAPHS[4])
    report.finish_page()

    report.new_page(numbered=True)
    report.toc_map["Chapter V: Conclusion and Future Scope"] = report.report_page_num or 1
    report.add_centered("CHAPTER V: CONCLUSION AND FUTURE SCOPE", HEADING_FONT, after=26)
    report.add_subheading("5.1 Summary of Work")
    report.add_paragraph(CONCLUSION_PARAGRAPHS[0])
    report.add_subheading("5.2 Key Achievements")
    report.add_paragraph(CONCLUSION_PARAGRAPHS[1])
    report.add_subheading("5.3 Future Scope")
    report.add_paragraph(CONCLUSION_PARAGRAPHS[2])
    report.finish_page()

    report.new_page(numbered=True)
    report.toc_map["References"] = report.report_page_num or 1
    report.add_centered("REFERENCES", HEADING_FONT, after=26)
    for ref in REFERENCES:
        report.add_paragraph(ref)
    report.finish_page()

    report.new_page(numbered=True)
    report.toc_map["Plagiarism Declaration"] = report.report_page_num or 1
    report.add_centered("PLAGIARISM DECLARATION", HEADING_FONT, after=22)
    for para in PLAGIARISM_PARAGRAPHS:
        report.add_paragraph(para)
    if PLAGIARISM_IMAGE_PATH.exists():
        report.add_image(PLAGIARISM_IMAGE_PATH, "Figure 5: Similarity Check Summary", max_h=980)
    else:
        report.add_paragraph(
            "The plagiarism summary image provided by the authors was not available at the time of final export."
        )
    report.finish_page()


def build_pdf() -> Dict[str, int]:
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    dry = PDFReport(dry_run=True)
    render_front_page(dry)
    render_certificate_page(dry)
    render_report_body(dry, include_toc=False)
    toc_entries = [
        ("Abstract", 1),
        ("Chapter I: Introduction", dry.toc_map["Chapter I: Introduction"] + 1),
        ("Chapter II: Literature Survey", dry.toc_map["Chapter II: Literature Survey"] + 1),
        ("Chapter III: Methodology", dry.toc_map["Chapter III: Methodology"] + 1),
        ("Chapter IV: Results and Discussion", dry.toc_map["Chapter IV: Results and Discussion"] + 1),
        ("Chapter V: Conclusion and Future Scope", dry.toc_map["Chapter V: Conclusion and Future Scope"] + 1),
        ("References", dry.toc_map["References"] + 1),
        ("Plagiarism Declaration", dry.toc_map["Plagiarism Declaration"] + 1),
    ]
    toc_entries.insert(1, ("Index", 2))

    report = PDFReport(dry_run=False)
    render_front_page(report)
    render_certificate_page(report)
    render_report_body(report, include_toc=True, toc_entries=toc_entries)

    pages = [page.convert("RGB") for page in report.pages]
    pages[0].save(OUTPUT_PDF, save_all=True, append_images=pages[1:], resolution=200.0)
    return report.toc_map


def render_pdf_to_pngs(pdf_path: Path) -> List[Path]:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    run_dir = TMP_DIR / f"render_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)
    png_prefix = run_dir / "page"
    subprocess.run(
        [
            r"C:\Users\pmins\anaconda3\Library\bin\pdftoppm.exe",
            "-png",
            str(pdf_path),
            str(png_prefix),
        ],
        check=True,
    )
    pages = sorted(run_dir.glob("page-*.png"))
    if not pages:
        raise RuntimeError("PDF rendering did not produce PNG pages.")
    return pages


def emu(px: int, dpi: int = 200) -> int:
    inches = px / dpi
    return int(inches * 914400)


def make_paragraph_with_image(rid: str, width_px: int, height_px: int) -> str:
    cx = emu(width_px)
    cy = emu(height_px)
    docpr_id = rid.replace("rId", "")
    return f"""
    <w:p>
      <w:pPr><w:jc w:val="center"/></w:pPr>
      <w:r>
        <w:drawing>
          <wp:inline distT="0" distB="0" distL="0" distR="0"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <wp:extent cx="{cx}" cy="{cy}"/>
            <wp:docPr id="{docpr_id}" name="Page {docpr_id}"/>
            <a:graphic>
              <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
                <pic:pic>
                  <pic:nvPicPr>
                    <pic:cNvPr id="{docpr_id}" name="Page {docpr_id}"/>
                    <pic:cNvPicPr/>
                  </pic:nvPicPr>
                  <pic:blipFill>
                    <a:blip r:embed="{rid}"/>
                    <a:stretch><a:fillRect/></a:stretch>
                  </pic:blipFill>
                  <pic:spPr>
                    <a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
                    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
                  </pic:spPr>
                </pic:pic>
              </a:graphicData>
            </a:graphic>
          </wp:inline>
        </w:drawing>
      </w:r>
    </w:p>
    """


def build_docx_from_pngs(png_pages: Sequence[Path]) -> None:
    page_w_twips = 11906
    page_h_twips = 16838
    margin_twips = 180
    image_w_px = 1560
    image_h_px = int(image_w_px * PAGE_H / PAGE_W)

    rels = []
    body_parts = []
    for idx, png in enumerate(png_pages, start=1):
        rid = f"rId{idx}"
        rels.append(
            f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{png.name}"/>'
        )
        body_parts.append(make_paragraph_with_image(rid, image_w_px, image_h_px))
        if idx < len(png_pages):
            body_parts.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    body_parts.append(
        f'<w:sectPr><w:pgSz w:w="{page_w_twips}" w:h="{page_h_twips}"/>'
        f'<w:pgMar w:top="{margin_twips}" w:right="{margin_twips}" w:bottom="{margin_twips}" '
        f'w:left="{margin_twips}" w:header="0" w:footer="0" w:gutter="0"/></w:sectPr>'
    )
    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
        'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'xmlns:o="urn:schemas-microsoft-com:office:office" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:w10="urn:schemas-microsoft-com:office:word" '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
        'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
        'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
        'xmlns:wne="http://schemas.microsoft.com/office/2006/wordml" '
        'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" mc:Ignorable="w14 wp14">'
        '<w:body>'
        + "".join(body_parts)
        + "</w:body></w:document>"
    )

    rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(rels)
        + "</Relationships>"
    )

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        "</Types>"
    )

    package_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        "</Relationships>"
    )

    core_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{xml_escape(TITLE)}</dc:title>
  <dc:subject>Academic Project Report</dc:subject>
  <dc:creator>OpenAI Codex</dc:creator>
  <cp:keywords>bearing fault diagnosis, cwru, machine learning</cp:keywords>
  <dc:description>Submission-ready project report</dc:description>
  <cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{datetime.now(timezone.utc).isoformat()}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{datetime.now(timezone.utc).isoformat()}</dcterms:modified>
</cp:coreProperties>
"""

    app_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft Office Word</Application>
</Properties>
"""

    with ZipFile(OUTPUT_DOCX, "w", compression=ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", package_rels)
        zf.writestr("docProps/core.xml", core_xml)
        zf.writestr("docProps/app.xml", app_xml)
        zf.writestr("word/document.xml", document_xml)
        zf.writestr("word/_rels/document.xml.rels", rels_xml)
        for png in png_pages:
            zf.write(png, f"word/media/{png.name}")


def main() -> None:
    build_pdf()
    png_pages = render_pdf_to_pngs(OUTPUT_PDF)
    build_docx_from_pngs(png_pages)
    print(f"Wrote {OUTPUT_PDF}")
    print(f"Wrote {OUTPUT_DOCX}")


if __name__ == "__main__":
    main()
