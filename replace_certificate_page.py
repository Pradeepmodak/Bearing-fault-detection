from __future__ import annotations

from io import BytesIO
from pathlib import Path
import zipfile

from PIL import Image, ImageDraw, ImageFont


WORKDIR = Path(r"D:\CWRU-bearing-fault-classification-ML-main")
REPORT_DOCX = Path(r"C:\Users\pmins\Downloads\Bearing_Fault_Diagnosis_Full_Report_Final (1).docx")
OUTPUT_DOCX = WORKDIR / "Bearing_Fault_Diagnosis_Full_Report_Final_updated.docx"
PREVIEW_PNG = WORKDIR / "certificate_page_replacement.png"

STUDENTS = [
    "Pradeep Modak (2023UGCM026)",
    "Ashwini Kumar (2023UGCM004)",
]
PROJECT_TITLE = (
    "Intelligent Bearing Fault Diagnosis for Predictive Maintenance "
    "Using Vibration Signal Analysis and Machine Learning"
)
BROAD_AREA = "Machine Learning and Vibration Signal Analysis"
SUPERVISORS = [
    "Dr. Saroj Sarangi",
    "Dr. Abhijit Dey",
]
CERTIFICATE_DATE = "April 2026"

PAGE_SIZE = (1241, 1755)
PAGE_BG = "white"
TEXT_COLOR = "black"
FONT_TIMES = Path(r"C:\Windows\Fonts\times.ttf")
FONT_TIMES_BOLD = Path(r"C:\Windows\Fonts\timesbd.ttf")
FONT_SYMBOL = Path(r"C:\Windows\Fonts\seguisym.ttf")


def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> int:
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left


def draw_centered(draw: ImageDraw.ImageDraw, y: int, text: str, font: ImageFont.FreeTypeFont) -> None:
    width = text_width(draw, text, font)
    x = (PAGE_SIZE[0] - width) // 2
    draw.text((x, y), text, fill=TEXT_COLOR, font=font)


def draw_wrapped_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    x: int,
    y: int,
    max_width: int,
    line_gap: int = 8,
) -> int:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and text_width(draw, candidate, font) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)

    cursor_y = y
    for line in lines:
        draw.text((x, cursor_y), line, fill=TEXT_COLOR, font=font)
        _, _, _, bottom = draw.textbbox((x, cursor_y), line, font=font)
        cursor_y = bottom + line_gap
    return cursor_y


def draw_certificate_page() -> Image.Image:
    img = Image.new("RGB", PAGE_SIZE, PAGE_BG)
    draw = ImageDraw.Draw(img)

    title_font = load_font(FONT_TIMES_BOLD, 36)
    subtitle_font = load_font(FONT_TIMES_BOLD, 24)
    body_font = load_font(FONT_TIMES, 24)
    body_bold = load_font(FONT_TIMES_BOLD, 24)
    label_font = load_font(FONT_TIMES_BOLD, 20)
    body_small = load_font(FONT_TIMES, 21)
    symbol_font = load_font(FONT_SYMBOL, 24)

    # Header
    title = "Certificate"
    title_y = 120
    draw_centered(draw, title_y, title, title_font)
    title_w = text_width(draw, title, title_font)
    title_x = (PAGE_SIZE[0] - title_w) // 2
    draw.line((title_x, title_y + 40, title_x + title_w, title_y + 40), fill=TEXT_COLOR, width=1)

    draw_centered(draw, 175, "CM1611 Project-II (Based on Training)", subtitle_font)

    # Main table
    table_x = 127
    table_y = 255
    left_col_w = 227
    right_col_w = 760
    table_w = left_col_w + right_col_w
    row_heights = [82, 130, 82, 100, 152]
    table_h = sum(row_heights)

    draw.rectangle((table_x, table_y, table_x + table_w, table_y + table_h), outline=TEXT_COLOR, width=1)
    draw.line((table_x + left_col_w, table_y, table_x + left_col_w, table_y + table_h), fill=TEXT_COLOR, width=1)

    current_y = table_y
    for height in row_heights[:-1]:
        current_y += height
        draw.line((table_x, current_y, table_x + table_w, current_y), fill=TEXT_COLOR, width=1)

    labels = [
        "Name and Reg No. of Student(s)",
        "Title of the Project",
        "Nature of Project",
        "Broad Area of Project",
        "Name of Supervisor(s)",
    ]

    current_y = table_y
    for label, height in zip(labels, row_heights):
        draw_wrapped_text(
            draw,
            label,
            label_font,
            table_x + 10,
            current_y + 16,
            left_col_w - 20,
            line_gap=2,
        )
        current_y += height

    # Right-side table content
    right_x = table_x + left_col_w + 18

    # Filled student names
    student_y = table_y + 16
    for student in STUDENTS:
        draw.text((right_x, student_y), student, fill=TEXT_COLOR, font=body_small)
        student_y += 32

    # Filled project title
    draw_wrapped_text(
        draw,
        PROJECT_TITLE,
        body_small,
        right_x,
        table_y + row_heights[0] + 16,
        right_col_w - 36,
        line_gap=5,
    )

    nature_y = table_y + row_heights[0] + row_heights[1] + 18
    x = table_x + left_col_w + 18
    pieces = [
        ("\u2612", symbol_font),
        (" Experimental ", body_font),
        ("\u2610", symbol_font),
        (" Simulation ", body_font),
        ("\u2610", symbol_font),
        (" Both", body_font),
    ]
    for text, font in pieces:
        draw.text((x, nature_y), text, fill=TEXT_COLOR, font=font)
        x += text_width(draw, text, font)

    # Broad area
    draw_wrapped_text(
        draw,
        BROAD_AREA,
        body_small,
        right_x,
        table_y + row_heights[0] + row_heights[1] + row_heights[2] + 16,
        right_col_w - 36,
        line_gap=5,
    )

    sup_base_y = table_y + sum(row_heights[:-1]) + 32
    draw.text((right_x, sup_base_y), f"1. {SUPERVISORS[0]}", fill=TEXT_COLOR, font=body_small)
    draw.text((right_x, sup_base_y + 62), f"2. {SUPERVISORS[1]}", fill=TEXT_COLOR, font=body_small)

    # Lower signature section
    divider_x1 = 128
    divider_x2 = 1114
    top_divider_y = table_y + table_h + 96
    draw.line((divider_x1, top_divider_y, divider_x2, top_divider_y), fill=TEXT_COLOR, width=1)

    draw.text((divider_x1, top_divider_y + 28), "Name and Signature of Supervisor(s):", fill=TEXT_COLOR, font=body_font)

    line1_y = top_divider_y + 108
    line2_y = line1_y + 88
    draw.text((divider_x1, line1_y), f"{SUPERVISORS[0]}  _________________________", fill=TEXT_COLOR, font=body_small)
    draw.text((divider_x1, line2_y), f"{SUPERVISORS[1]}  _________________________", fill=TEXT_COLOR, font=body_small)

    date_y = line2_y + 52
    draw.text((divider_x1, date_y), f"Date: {CERTIFICATE_DATE}", fill=TEXT_COLOR, font=body_font)

    bottom_divider_y = date_y + 54
    draw.line((divider_x1, bottom_divider_y, divider_x2, bottom_divider_y), fill=TEXT_COLOR, width=1)

    footer_y = bottom_divider_y + 28
    draw.text((divider_x1, footer_y), "Faculty Advisor", fill=TEXT_COLOR, font=body_font)
    hod_text = "HoD"
    hod_w = text_width(draw, hod_text, body_font)
    draw.text((divider_x2 - hod_w, footer_y), hod_text, fill=TEXT_COLOR, font=body_font)

    return img


def replace_page(report_docx: Path, output_docx: Path, replacement_png_bytes: bytes) -> None:
    with zipfile.ZipFile(report_docx, "r") as src, zipfile.ZipFile(output_docx, "w", compression=zipfile.ZIP_DEFLATED) as dst:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "word/media/page-02.png":
                data = replacement_png_bytes
            dst.writestr(info, data)


def main() -> None:
    replacement = draw_certificate_page()
    replacement.save(PREVIEW_PNG, format="PNG")

    buffer = BytesIO()
    replacement.save(buffer, format="PNG")
    replace_page(REPORT_DOCX, OUTPUT_DOCX, buffer.getvalue())

    print(PREVIEW_PNG)
    print(OUTPUT_DOCX)


if __name__ == "__main__":
    main()
