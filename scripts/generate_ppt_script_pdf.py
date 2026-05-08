from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "Final_PPT_What_To_Say_Script.pdf"
DOC_TITLE = "Final Presentation Speaking Script"


SLIDES = [
    (
        "Slide 1: Title Slide",
        [
            "Good afternoon respected professors and my dear friends. I am Pradeep Modak, and along with my teammate Ashwini Kumar, I am presenting our Project-II work from the Department of Mechanical Engineering, NIT Jamshedpur.",
            "The title of our project is Intelligent Bearing Fault Diagnosis for Predictive Maintenance Using Vibration Signal Analysis and Machine Learning.",
            "In this work, we studied how bearing faults change the vibration behavior of a rotating machine, and then we developed a complete system that can take a vibration signal, process it, classify the bearing condition, and show the result through a graphical dashboard.",
            "During this presentation, I will explain the background, the research gap, our methodology, the results we obtained, and finally the future scope of the project.",
        ],
    ),
    (
        "Slide 2: Outline",
        [
            "This slide shows the overall flow of the presentation.",
            "First, I will explain the engineering background and why bearing fault diagnosis is important. Then I will discuss the literature survey and the limitations of existing work.",
            "After that, I will present our proposed workflow, including data preprocessing, feature extraction, model training, evaluation, and deployment through the Streamlit interface.",
            "Finally, I will summarize the key results and conclude with the future scope.",
        ],
    ),
    (
        "Slide 3: Introduction",
        [
            "Bearings are critical elements in rotating machinery because they support the rotating shaft and help maintain smooth motion.",
            "When a bearing develops defects in the ball element, inner race, or outer race, the vibration pattern of the machine changes. These changes may not be visible directly from outside, but they appear clearly in the vibration signal.",
            "In this project, we use two important views of the signal. The first is the time-domain view, where we observe how amplitude changes with time. The second is the frequency-domain view, where we apply FFT to identify dominant frequency components related to fault behavior.",
            "Instead of relying only on manual interpretation, we convert these signal patterns into numerical features and use machine learning to classify the bearing condition.",
        ],
    ),
    (
        "Slide 4: Problem Statement",
        [
            "The main problem is that manual analysis of vibration signals becomes difficult when the amount of data increases.",
            "In industrial systems, machines may generate continuous streams of vibration data. Checking all of that manually requires domain expertise, a lot of time, and it becomes difficult to maintain consistency.",
            "So our objective was to build an automated and interpretable system that can classify the signal into one of four conditions: Normal, Ball Fault, Inner Race Fault, or Outer Race Fault.",
            "For this purpose, we used the CWRU benchmark dataset and prepared a processed dataset containing 9,736 labeled windows sampled at 48 kilohertz.",
        ],
    ),
    (
        "Slide 5: Applications",
        [
            "This project is important because the same workflow is relevant to many real mechanical systems.",
            "In smart manufacturing, such a system can support continuous monitoring of rotating machines across a production line.",
            "In the energy sector, similar ideas can be extended to turbines, generators, and other rotating equipment where unexpected bearing failure can interrupt operation and increase maintenance burden.",
            "In safety-critical systems, early identification of abnormal vibration is valuable because a small bearing defect can grow into a larger mechanical problem if it is ignored.",
        ],
    ),
    (
        "Slide 6: Literature Survey",
        [
            "The literature in this area can be broadly grouped into three types.",
            "The first group focuses on classical signal-processing techniques such as waveform study, FFT analysis, and wavelet-based interpretation.",
            "The second group uses engineered statistical and spectral features with machine learning models like Support Vector Machine and Random Forest.",
            "The third group applies deep learning methods directly on raw signals or transformed signal images. These methods are powerful, but they are often more computationally expensive and less transparent for demonstration.",
            "From this survey, we observed that feature-based machine learning provides a good balance between performance, interpretability, and implementation simplicity for a project like ours.",
        ],
    ),
    (
        "Slide 7: Literature Limitations",
        [
            "While studying previous work, we found three practical limitations.",
            "First, many papers report final accuracy, but they do not explain preprocessing and feature extraction clearly enough for easy reproduction.",
            "Second, most studies stop at analysis and do not provide a usable interface for demonstration or educational deployment.",
            "Third, raw signal handling, model training, evaluation, and deployment are often treated separately instead of being integrated into one complete system.",
            "Our project addresses these limitations by building a full reproducible workflow, saving the trained model artifacts, generating result plots, and providing a GUI for live testing.",
        ],
    ),
    (
        "Slide 8: Research Gaps and Objectives",
        [
            "Based on the limitations I just discussed, our main research gap was the absence of a complete demonstrable mechanical engineering tool that connects signal processing, machine learning, and user interaction in one pipeline.",
            "So we defined five clear objectives for the project.",
            "First, preprocess the raw vibration data using 2048-sample windows with 50 percent overlap. Second, extract meaningful time-domain and frequency-domain features. Third, train and compare two machine learning models, namely SVM and Random Forest.",
            "Fourth, evaluate the performance using standard classification metrics. Fifth, deploy the best model through a Streamlit dashboard so that the system can be tested directly from uploaded vibration data.",
        ],
    ),
    (
        "Slide 9: Methodology and System Design",
        [
            "This slide explains the end-to-end workflow of our system.",
            "We begin with the raw CWRU MAT files, which contain vibration signals under four bearing conditions. These long signals are segmented into smaller windows of 2048 samples each, with 50 percent overlap. This gives us 9,736 labeled signal windows for training and testing.",
            "After segmentation, each window is passed through the feature extraction module. The extracted feature set becomes the input table for machine learning.",
            "Then we train two models, Support Vector Machine with RBF kernel and Random Forest, using an 80 to 20 train-test split.",
            "Finally, the best saved model is loaded inside the Streamlit application, where a user can upload a vibration CSV, view the waveform and FFT, and get the predicted fault type with confidence.",
        ],
    ),
    (
        "Slide 10: Feature Extraction Module",
        [
            "Feature extraction is the bridge between the raw amplitude sequence and the classifier.",
            "From the time-domain signal, we extract features such as mean, standard deviation, mean absolute deviation, RMS, maximum absolute value, skewness, kurtosis, crest factor, shape factor, form factor, and impulse factor.",
            "From the frequency-domain signal, we apply FFT and derive spectral features such as spectral mean, spectral standard deviation, dominant frequency, frequency variance, and frequency variation related measures.",
            "These features are useful because they summarize the physical behavior of the signal. Some capture energy and spread, while others capture impulsive behavior and frequency concentration caused by defects.",
            "In our project, each segmented window finally becomes one feature vector containing 25 engineered features used for classification.",
        ],
    ),
    (
        "Slide 11: Model Performance",
        [
            "After preparing the feature dataset, we trained and evaluated two machine learning models.",
            "Both SVM and Random Forest performed well, which indicates that the extracted features are informative.",
            "However, Random Forest gave the best result with 97.59 percent accuracy and 97.59 percent weighted F1-score on the held-out test set. SVM also showed strong performance with 97.48 percent accuracy.",
            "We selected Random Forest as the final deployed model because it slightly outperformed SVM and also provides feature-importance information, which improves explainability during demonstration.",
        ],
    ),
    (
        "Slide 12: Confusion Matrix and Feature Importance",
        [
            "This slide shows both the classification behavior and the interpretability of the final model.",
            "On the left, the confusion matrix shows how many samples were correctly classified into each class. The strong diagonal values indicate that most Ball Fault, Inner Race Fault, Normal, and Outer Race Fault samples are correctly identified.",
            "The misclassified cases are comparatively low, which shows that class separation is strong for the selected feature set.",
            "On the right, the feature-importance plot shows which features contribute most to the Random Forest decision-making process. In our case, spectral mean, impulse factor, standard deviation, frequency variation factor, maximum absolute value, and RMS appear among the most influential features.",
            "This is useful because it shows that the model is not acting like a black box only; we can relate its decisions back to meaningful vibration characteristics.",
        ],
    ),
    (
        "Slide 13: Summary and Conclusion",
        [
            "To summarize, this project combines mechanical vibration analysis and machine learning into one complete working system.",
            "We started from raw bearing vibration signals, performed segmentation and preprocessing, extracted 25 engineered features, trained two machine learning models, compared their performance, and deployed the best model in a Streamlit dashboard.",
            "The final Random Forest model achieved 97.59 percent accuracy on the CWRU benchmark dataset, which shows that the developed workflow is effective for bearing fault classification.",
            "The key outcome of the project is not only a strong classification result, but also a usable and explainable demonstration tool suitable for academic presentation and further extension.",
        ],
    ),
    (
        "Slide 14: References",
        [
            "These are the main references used in the project.",
            "The most important source is the Case Western Reserve University Bearing Data Center, which provided the benchmark vibration dataset used for the full workflow.",
            "In addition, we referred to bearing-fault diagnosis literature related to feature-based machine learning and signal-processing-based fault identification, along with the Streamlit documentation for the application layer.",
        ],
    ),
    (
        "Slide 15: Thank You and Discussion",
        [
            "Thank you, respected professors, for your time and attention.",
            "This was our project on intelligent bearing fault diagnosis using vibration signal analysis and machine learning.",
            "We will be happy to answer your questions. If required, we can also demonstrate the Streamlit dashboard by uploading a test vibration signal and showing the prediction, confidence scores, waveform, FFT plot, and extracted features.",
        ],
    ),
]


QUESTIONS = [
    (
        "Q1. What is the input to the system?",
        "The input is a vibration signal from the bearing. In the GUI, it is usually provided as a CSV containing amplitude values sampled over time.",
    ),
    (
        "Q2. What is the output of the system?",
        "The output is the predicted bearing condition: Normal, Ball Fault, Inner Race Fault, or Outer Race Fault. The application also shows confidence values, waveform, FFT, and extracted features.",
    ),
    (
        "Q3. From where is the dataset taken?",
        "The dataset is taken from the Case Western Reserve University Bearing Data Center, commonly called the CWRU bearing dataset.",
    ),
    (
        "Q4. Why did you segment the raw signal?",
        "One raw file contains a long continuous vibration recording. We segment it into smaller windows so that each window becomes one training sample and short-term fault characteristics are preserved.",
    ),
    (
        "Q5. Why did you choose 2048 samples per window?",
        "At 48 kilohertz sampling, 2048 samples represent about 42.67 milliseconds. This gives a practical balance between capturing local vibration behavior and generating enough samples for model training.",
    ),
    (
        "Q6. Why did you use 50 percent overlap?",
        "Overlap increases the number of usable windows and reduces the chance that important transient fault information is missed between adjacent windows.",
    ),
    (
        "Q7. Why did you use feature extraction instead of raw signal directly?",
        "Our goal was to build an interpretable feature-based machine learning system. Feature extraction converts the raw amplitude sequence into compact descriptors like RMS, kurtosis, and spectral mean, which are easier for classical classifiers to use and easier to explain.",
    ),
    (
        "Q8. Which algorithms were used in this project?",
        "We trained Support Vector Machine with RBF kernel and Random Forest. After comparison, Random Forest was selected as the final model for deployment.",
    ),
    (
        "Q9. Why was Random Forest selected finally?",
        "Random Forest achieved the best weighted F1-score and also provided feature-importance information, which made the final system more explainable.",
    ),
    (
        "Q10. How did you validate the correctness of the model?",
        "We used a train-test split. The model was trained on the training set and evaluated on unseen test data using accuracy, precision, recall, weighted F1-score, and confusion matrix.",
    ),
    (
        "Q11. What is the practical mechanical use of this project?",
        "It supports vibration-based condition monitoring and predictive maintenance for rotating machinery such as motors, pumps, turbines, compressors, and similar equipment.",
    ),
    (
        "Q12. What is unique about your project?",
        "The contribution is not only model accuracy. We built the full pipeline from raw vibration signal to feature extraction, model training, evaluation, saved model artifacts, and a working GUI for demonstration.",
    ),
]


def page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Roman", 10)
    canvas.drawCentredString(A4[0] / 2.0, 1.1 * cm, str(doc.page))
    canvas.restoreState()


def build_pdf() -> None:
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=2.0 * cm,
        leftMargin=2.0 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontName="Times-Bold",
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=10,
    )
    sub_style = ParagraphStyle(
        "SubCustom",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=11.5,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#334155"),
        spaceAfter=12,
    )
    heading_style = ParagraphStyle(
        "HeadingCustom",
        parent=styles["Heading1"],
        fontName="Times-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=8,
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "BodyCustom",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=12,
        leading=16,
        alignment=TA_JUSTIFY,
        spaceAfter=7,
    )
    q_style = ParagraphStyle(
        "QuestionCustom",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=12,
        leading=16,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=5,
        spaceAfter=3,
    )

    story = []
    story.append(Paragraph(DOC_TITLE, title_style))
    story.append(Paragraph("Project: Intelligent Bearing Fault Diagnosis for Predictive Maintenance Using Vibration Signal Analysis and Machine Learning", sub_style))
    story.append(Paragraph("This script is prepared for direct speaking during the presentation. The wording below is written in natural order so that the presentation can be delivered clearly from slide to slide.", sub_style))
    story.append(Spacer(1, 0.2 * cm))

    for title, lines in SLIDES:
        story.append(Paragraph(title, heading_style))
        for line in lines:
            story.append(Paragraph(line, body_style))
        story.append(Spacer(1, 0.15 * cm))

    story.append(PageBreak())
    story.append(Paragraph("Questions to Prepare", heading_style))
    story.append(Paragraph("The following questions are likely during the viva or discussion after the presentation. The answers are written in direct form so that they can be used immediately while responding.", body_style))
    for q, a in QUESTIONS:
        story.append(Paragraph(q, q_style))
        story.append(Paragraph(a, body_style))

    doc.build(story, onFirstPage=page_number, onLaterPages=page_number)


if __name__ == "__main__":
    build_pdf()
    print(f"Wrote {PDF_PATH}")
