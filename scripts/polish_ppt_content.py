from __future__ import annotations

import re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PPT = ROOT / "Final_Presentation_With_Speaker_Notes.pptx"
OUTPUT_PPT = ROOT / "Final_Presentation_Polished.pptx"

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}


def set_texts_by_index(xml_bytes: bytes, replacements: dict[int, str]) -> bytes:
    root = ET.fromstring(xml_bytes)
    texts = root.findall(".//a:t", NS)
    for idx, value in replacements.items():
        if 0 <= idx < len(texts):
            texts[idx].text = value
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


SLIDE_INDEX_REPLACEMENTS = {
    "ppt/slides/slide2.xml": {
        12: "Results & Discussion",
        13: "08",
        14: "References",
        15: "",
        16: "07",
        17: "",
        18: "Summary & Conclusion",
    },
    "ppt/slides/slide4.xml": {
        2: (
            "Manual interpretation of vibration signals is time-consuming and requires strong domain expertise. "
            "When machines generate continuous sensor streams, manual screening becomes difficult to maintain "
            "consistently across large industrial systems."
        ),
    },
    "ppt/slides/slide5.xml": {
        5: (
            "Integration with smart factories can support real-time health monitoring across production lines "
            "and help maintenance teams plan action before failure."
        ),
        9: (
            "The same workflow can be adapted for wind turbines, hydroelectric generators, and other rotating "
            "energy assets where early fault detection lowers maintenance burden."
        ),
        13: (
            "Similar vibration-based fault monitoring ideas are relevant for safety-critical aerospace components, "
            "where early warning is more valuable than post-failure diagnosis."
        ),
    },
    "ppt/slides/slide14.xml": {
        1: "[1] Case Western Reserve University Bearing Data Center, \"Bearing Data Center,\" [Online]. Available:",
        2: "",
        3: "",
        4: "https://engineering.case.edu/bearingdatacenter",
        5: "",
        6: "",
        7: "[2] P. K. Kankar, S. C. Sharma, and S. P. Harsha,",
        8: "",
        9: "\"Fault diagnosis of ball bearings using machine learning methods,\" Expert Systems with Applications, 2011.",
        10: "[3] C. S. Rajeswari, S. Sathiyabama, and S. Devendiran, \"Bearing fault diagnosis using wavelet packet transform, hybrid PSO and support vector machine,\" Procedia Engineering, 2014.",
        11: "",
        12: "[4]",
        13: "Streamlit Documentation,",
        14: "[Online]. Available: https://docs.streamlit.io/",
    },
    "ppt/slides/slide15.xml": {
        3: "Supervisors: Dr. Saroj Sarangi  |  Dr. Abhijit Dey",
    },
}


def main() -> None:
    with ZipFile(SOURCE_PPT, "r") as zin, ZipFile(OUTPUT_PPT, "w", compression=ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename in SLIDE_INDEX_REPLACEMENTS:
                data = set_texts_by_index(data, SLIDE_INDEX_REPLACEMENTS[item.filename])
            zout.writestr(item, data)
    print(f"Wrote {OUTPUT_PPT}")


if __name__ == "__main__":
    main()
