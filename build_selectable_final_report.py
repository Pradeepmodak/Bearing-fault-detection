from __future__ import annotations

from copy import deepcopy
from io import BytesIO
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET

from PIL import Image


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"
NS = {"w": W_NS}

ET.register_namespace("w", W_NS)

WORKDIR = Path(r"D:\CWRU-bearing-fault-classification-ML-main")
BASE_DOCX = WORKDIR / "Bearing_Fault_Diagnosis_Remaining_Report_Final.docx"
CERT_DOCX = Path(r"C:\Users\pmins\Downloads\2. Certificate Page (2).docx")
OUTPUT_DOCX = WORKDIR / "Bearing_Fault_Diagnosis_Full_Report_Selectable.docx"
IMAGE_REPORT_DOCX = Path(r"C:\Users\pmins\Downloads\Bearing_Fault_Diagnosis_Full_Report_Final (1).docx")
PLAG_IMAGE_NAME = "word/media/plagiarism_verification.png"

STUDENTS = [
    "Pradeep Modak (2023UGCM026)",
    "Ashwini Kumar (2023UGCM004)",
]
PROJECT_TITLE = (
    "Intelligent Bearing Fault Diagnosis for Predictive Maintenance Using "
    "Vibration Signal Analysis and Machine Learning"
)
SUPERVISORS = [
    "Dr. Saroj Sarangi",
    "Dr. Abhijit Dey",
]
BROAD_AREA = "Machine Learning and Vibration Signal Analysis"


def w_tag(name: str) -> str:
    return f"{{{W_NS}}}{name}"


def make_text_run(text: str, *, bold: bool = False, size: int = 24) -> ET.Element:
    r = ET.Element(w_tag("r"))
    rpr = ET.SubElement(r, w_tag("rPr"))
    ET.SubElement(rpr, w_tag("rFonts"), {
        w_tag("ascii"): "Times New Roman",
        w_tag("hAnsi"): "Times New Roman",
        w_tag("cs"): "Times New Roman",
    })
    if bold:
        ET.SubElement(rpr, w_tag("b"))
        ET.SubElement(rpr, w_tag("bCs"))
    ET.SubElement(rpr, w_tag("sz"), {w_tag("val"): str(size)})
    ET.SubElement(rpr, w_tag("szCs"), {w_tag("val"): str(size)})
    t = ET.SubElement(r, w_tag("t"))
    if text.startswith(" ") or text.endswith(" "):
        t.set(f"{{{XML_NS}}}space", "preserve")
    t.text = text
    return r


def make_para(
    text: str = "",
    *,
    bold: bool = False,
    size: int = 24,
    align: str | None = None,
    before: int | None = None,
    after: int | None = None,
    line: int | None = None,
) -> ET.Element:
    p = ET.Element(w_tag("p"))
    ppr = ET.SubElement(p, w_tag("pPr"))
    if align:
        ET.SubElement(ppr, w_tag("jc"), {w_tag("val"): align})
    if before is not None or after is not None or line is not None:
        attrs: dict[str, str] = {}
        if before is not None:
            attrs[w_tag("before")] = str(before)
        if after is not None:
            attrs[w_tag("after")] = str(after)
        if line is not None:
            attrs[w_tag("line")] = str(line)
            attrs[w_tag("lineRule")] = "auto"
        ET.SubElement(ppr, w_tag("spacing"), attrs)
    if text:
        p.append(make_text_run(text, bold=bold, size=size))
    return p


def make_page_break_para() -> ET.Element:
    p = ET.Element(w_tag("p"))
    r = ET.SubElement(p, w_tag("r"))
    ET.SubElement(r, w_tag("br"), {w_tag("type"): "page"})
    return p


def make_image_paragraph(rel_id: str, width_emu: int, height_emu: int, docpr_id: int = 1, name: str = "Image") -> ET.Element:
    p = ET.Element(w_tag("p"))
    ppr = ET.SubElement(p, w_tag("pPr"))
    ET.SubElement(ppr, w_tag("jc"), {w_tag("val"): "center"})

    r = ET.SubElement(p, w_tag("r"))
    drawing = ET.SubElement(r, w_tag("drawing"))

    wp_ns = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
    a_ns = "http://schemas.openxmlformats.org/drawingml/2006/main"
    pic_ns = "http://schemas.openxmlformats.org/drawingml/2006/picture"
    r_ns = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

    inline = ET.SubElement(drawing, f"{{{wp_ns}}}inline", {"distT": "0", "distB": "0", "distL": "0", "distR": "0"})
    ET.SubElement(inline, f"{{{wp_ns}}}extent", {"cx": str(width_emu), "cy": str(height_emu)})
    ET.SubElement(inline, f"{{{wp_ns}}}effectExtent", {"l": "0", "t": "0", "r": "0", "b": "0"})
    ET.SubElement(inline, f"{{{wp_ns}}}docPr", {"id": str(docpr_id), "name": name})
    ET.SubElement(inline, f"{{{wp_ns}}}cNvGraphicFramePr")
    graphic = ET.SubElement(inline, f"{{{a_ns}}}graphic")
    graphic_data = ET.SubElement(graphic, f"{{{a_ns}}}graphicData", {"uri": "http://schemas.openxmlformats.org/drawingml/2006/picture"})
    pic = ET.SubElement(graphic_data, f"{{{pic_ns}}}pic")
    nv_pic_pr = ET.SubElement(pic, f"{{{pic_ns}}}nvPicPr")
    ET.SubElement(nv_pic_pr, f"{{{pic_ns}}}cNvPr", {"id": "0", "name": name})
    ET.SubElement(nv_pic_pr, f"{{{pic_ns}}}cNvPicPr")
    blip_fill = ET.SubElement(pic, f"{{{pic_ns}}}blipFill")
    ET.SubElement(blip_fill, f"{{{a_ns}}}blip", {f"{{{r_ns}}}embed": rel_id})
    stretch = ET.SubElement(blip_fill, f"{{{a_ns}}}stretch")
    ET.SubElement(stretch, f"{{{a_ns}}}fillRect")
    sp_pr = ET.SubElement(pic, f"{{{pic_ns}}}spPr")
    xfrm = ET.SubElement(sp_pr, f"{{{a_ns}}}xfrm")
    ET.SubElement(xfrm, f"{{{a_ns}}}off", {"x": "0", "y": "0"})
    ET.SubElement(xfrm, f"{{{a_ns}}}ext", {"cx": str(width_emu), "cy": str(height_emu)})
    prst = ET.SubElement(sp_pr, f"{{{a_ns}}}prstGeom", {"prst": "rect"})
    ET.SubElement(prst, f"{{{a_ns}}}avLst")
    return p


def set_cell_text(tc: ET.Element, lines: list[str], *, bold: bool = False, size: int = 24) -> None:
    for child in list(tc):
        tc.remove(child)
    tc_pr = ET.SubElement(tc, w_tag("tcPr"))
    width = ET.SubElement(tc_pr, w_tag("tcW"))
    width.set(w_tag("w"), "7497")
    width.set(w_tag("type"), "dxa")
    for line in lines:
        tc.append(make_para(line, bold=bold, size=size, line=360))


def set_label_cell(tc: ET.Element, text: str) -> None:
    for child in list(tc):
        tc.remove(child)
    tc_pr = ET.SubElement(tc, w_tag("tcPr"))
    width = ET.SubElement(tc_pr, w_tag("tcW"))
    width.set(w_tag("w"), "2235")
    width.set(w_tag("type"), "dxa")
    tc.append(make_para(text, bold=True, size=24, line=360))


def build_certificate_section() -> list[ET.Element]:
    with zipfile.ZipFile(CERT_DOCX) as z:
        cert_root = ET.fromstring(z.read("word/document.xml"))
    cert_body = cert_root.find("w:body", NS)
    assert cert_body is not None
    cert_table = deepcopy(cert_body.find("w:tbl", NS))
    assert cert_table is not None

    tbl_pr = cert_table.find("w:tblPr", NS)
    if tbl_pr is not None:
        existing_borders = tbl_pr.find("w:tblBorders", NS)
        if existing_borders is not None:
            tbl_pr.remove(existing_borders)
        borders = ET.SubElement(tbl_pr, w_tag("tblBorders"))
        for side in ["top", "left", "bottom", "right", "insideH", "insideV"]:
            ET.SubElement(
                borders,
                w_tag(side),
                {
                    w_tag("val"): "single",
                    w_tag("sz"): "8",
                    w_tag("space"): "0",
                    w_tag("color"): "000000",
                },
            )

    rows = cert_table.findall("w:tr", NS)
    set_label_cell(rows[0].findall("w:tc", NS)[0], "Name and Reg No. of Student(s)")
    set_cell_text(rows[0].findall("w:tc", NS)[1], STUDENTS)

    set_label_cell(rows[1].findall("w:tc", NS)[0], "Title of the Project")
    set_cell_text(
        rows[1].findall("w:tc", NS)[1],
        [
            "Intelligent Bearing Fault Diagnosis for Predictive Maintenance Using",
            "Vibration Signal Analysis and Machine Learning",
        ],
        size=22,
    )

    set_label_cell(rows[2].findall("w:tc", NS)[0], "Nature of Project")
    set_cell_text(rows[2].findall("w:tc", NS)[1], ["☒ Experimental   ☐ Simulation   ☐ Both"])

    set_label_cell(rows[3].findall("w:tc", NS)[0], "Broad Area of Project")
    set_cell_text(rows[3].findall("w:tc", NS)[1], [BROAD_AREA], size=22)

    set_label_cell(rows[4].findall("w:tc", NS)[0], "Name of Supervisor(s)")
    set_cell_text(rows[4].findall("w:tc", NS)[1], [f"1. {SUPERVISORS[0]}", f"2. {SUPERVISORS[1]}"])

    elements: list[ET.Element] = [
        make_para("Certificate", bold=True, size=32, align="center", after=0),
        make_para("CM1611 Project-II (Based on Training)", bold=True, size=24, align="center", after=160),
        make_para("", after=160),
        cert_table,
        make_para("", after=120),
        make_para("Name and Signature of Supervisor(s):", size=24),
        make_para("", after=120),
        make_para(f"{SUPERVISORS[0]}  _________________________________", size=24),
        make_para("", after=80),
        make_para(f"{SUPERVISORS[1]}  _________________________________", size=24),
        make_para("Date: April 2026", size=24, after=40),
        make_para("Faculty Advisor                                                                                                          HoD", size=24),
    ]
    return elements


def build_plagiarism_image() -> bytes:
    with zipfile.ZipFile(IMAGE_REPORT_DOCX) as z:
        raw = z.read("word/media/page-15.png")
    with Image.open(BytesIO(raw)) as img:
        crop = img.crop((120, 360, 1120, 1020))
        out = BytesIO()
        crop.save(out, format="PNG")
        return out.getvalue()


def build_plagiarism_section(rel_id: str) -> list[ET.Element]:
    width_px, height_px = 1000, 660
    width_emu = 6_000_000
    height_emu = int(width_emu * height_px / width_px)
    return [
        make_para("PLAGIARISM DECLARATION", bold=True, size=30, align="center", after=120),
        make_para(
            "This report has been prepared by the authors as part of the academic project requirement and is based on the work implemented in the repository for bearing fault diagnosis using vibration data.",
            size=24,
            line=320,
            after=80,
        ),
        make_para(
            "All external sources used during report preparation, including the CWRU dataset reference and the related literature cited in the references section, have been acknowledged properly.",
            size=24,
            line=320,
            after=80,
        ),
        make_para(
            "Based on the attached plagiarism-check summary included below, the similarity level of the document remains within acceptable institutional limits. The text of the report has been written and refined in project-specific form to reflect the actual implementation, outputs, and interpretation of this work.",
            size=24,
            line=320,
            after=120,
        ),
        make_image_paragraph(rel_id, width_emu, height_emu, docpr_id=77, name="PlagiarismVerification"),
    ]


def build_front_page_section() -> list[ET.Element]:
    return [
        make_para("", before=400),
        make_para(
            "Intelligent Bearing Fault Diagnosis for",
            bold=True,
            size=34,
            align="center",
            line=360,
        ),
        make_para(
            "Predictive Maintenance Using Vibration Signal",
            bold=True,
            size=34,
            align="center",
            line=360,
        ),
        make_para(
            "Analysis and Machine Learning",
            bold=True,
            size=34,
            align="center",
            line=360,
            after=200,
        ),
        make_para("Project-II Based on Training (CM1611)", bold=True, size=28, align="center", after=220),
        make_para("Submitted in partial fulfillment of the", size=24, align="center", line=320),
        make_para("requirements for the credit course", size=24, align="center", line=320, after=220),
        make_para("Submitted by", bold=True, size=26, align="center", after=120),
        make_para(STUDENTS[0], size=24, align="center", line=320),
        make_para(STUDENTS[1], size=24, align="center", line=320, after=220),
        make_para("Under the Supervision of", bold=True, size=26, align="center", after=120),
        make_para(SUPERVISORS[0], size=24, align="center", line=320),
        make_para(SUPERVISORS[1], size=24, align="center", line=320, after=300),
        make_para("DEPARTMENT OF MECHANICAL ENGINEERING", bold=True, size=26, align="center", line=320),
        make_para("NATIONAL INSTITUTE OF TECHNOLOGY JAMSHEDPUR", bold=True, size=24, align="center", line=320),
        make_para("JAMSHEDPUR-831014, JHARKHAND (INDIA)", size=22, align="center", line=320, after=160),
        make_para("Spring Semester 2025-26", size=22, align="center", line=320),
        make_para("April 2026", size=22, align="center", line=320),
    ]


def build_output() -> None:
    with zipfile.ZipFile(BASE_DOCX) as zin:
        files = {name: zin.read(name) for name in zin.namelist()}

    files[PLAG_IMAGE_NAME] = build_plagiarism_image()

    root = ET.fromstring(files["word/document.xml"])
    body = root.find("w:body", NS)
    assert body is not None

    sect_pr = None
    if len(body) and body[-1].tag == w_tag("sectPr"):
        sect_pr = deepcopy(body[-1])
        body.remove(body[-1])

    original_children = [deepcopy(child) for child in list(body)]
    filtered_children: list[ET.Element] = []
    for child in original_children:
        text = "".join(t.text or "" for t in child.findall(".//w:t", NS)).strip()
        if text in {
            "Plagiarism Report",
            "This report has been checked for plagiarism and is within acceptable limits.",
        }:
            continue
        filtered_children.append(child)
    for child in list(body):
        body.remove(child)

    rels_root = ET.fromstring(files["word/_rels/document.xml.rels"])
    rel_ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    rel_ids = [rel.get("Id", "") for rel in rels_root.findall(f"{{{rel_ns}}}Relationship")]
    next_num = max([int(r[3:]) for r in rel_ids if r.startswith("rId") and r[3:].isdigit()] or [0]) + 1
    plag_rel_id = f"rId{next_num}"
    ET.SubElement(
        rels_root,
        f"{{{rel_ns}}}Relationship",
        {
            "Id": plag_rel_id,
            "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image",
            "Target": "media/plagiarism_verification.png",
        },
    )
    files["word/_rels/document.xml.rels"] = ET.tostring(rels_root, encoding="utf-8", xml_declaration=True)

    prepend = []
    prepend.extend(build_front_page_section())
    prepend.append(make_page_break_para())
    prepend.extend(build_certificate_section())
    prepend.append(make_page_break_para())
    append = [
        make_page_break_para(),
        *build_plagiarism_section(plag_rel_id),
    ]

    for el in prepend + filtered_children + append:
        body.append(el)
    if sect_pr is not None:
        body.append(sect_pr)

    files["word/document.xml"] = ET.tostring(root, encoding="utf-8", xml_declaration=True)

    with zipfile.ZipFile(OUTPUT_DOCX, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for name, data in files.items():
            zout.writestr(name, data)


if __name__ == "__main__":
    build_output()
    print(OUTPUT_DOCX)
