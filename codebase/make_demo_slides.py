#!/usr/bin/env python3
"""Generate demo-slides.pdf — đúng 6 trang (landscape)."""
from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "demo-slides.pdf"
FONT = "C:/Windows/Fonts/segoeui.ttf"
FONT_B = "C:/Windows/Fonts/segoeuib.ttf"

pdfmetrics.registerFont(TTFont("VN", FONT))
pdfmetrics.registerFont(TTFont("VN-Bold", FONT_B if Path(FONT_B).exists() else FONT))

PAGE = landscape(A4)
W, H = PAGE

INK = HexColor("#1c1914")
MUTED = HexColor("#5c564c")
LINE = HexColor("#ddd6c8")
PAPER = HexColor("#f6f1e7")
CARD = HexColor("#fffcf7")
ACCENT = HexColor("#2c4a3e")
ACCENT2 = HexColor("#3d6b58")
WARN = HexColor("#8a5a2b")
BAD = HexColor("#7a3030")
OK = HexColor("#1f5c3a")


def bg(c: canvas.Canvas):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # left accent bar
    c.setFillColor(ACCENT)
    c.rect(0, 0, 8 * mm, H, fill=1, stroke=0)
    # footer
    c.setFillColor(MUTED)
    c.setFont("VN", 9)
    c.drawString(18 * mm, 8 * mm, "VLearn Extend · Nhóm BMVD · Zone 3A · Mini Hackathon AI")
    c.drawRightString(W - 14 * mm, 8 * mm, f"{c.getPageNumber()} / 6")


def title(c: canvas.Canvas, text: str, y: float):
    c.setFillColor(ACCENT)
    c.setFont("VN-Bold", 26)
    c.drawString(18 * mm, y, text)


def subtitle(c: canvas.Canvas, text: str, y: float):
    c.setFillColor(MUTED)
    c.setFont("VN", 12)
    c.drawString(18 * mm, y, text)


def card(c: canvas.Canvas, x, y, w, h, fill=CARD):
    c.setFillColor(fill)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)


def bullet(c: canvas.Canvas, x, y, text, size=11, color=INK, bold=False):
    c.setFillColor(color)
    c.setFont("VN-Bold" if bold else "VN", size)
    c.drawString(x, y, text)
    return y - (size + 6)


def wrap(c: canvas.Canvas, text: str, x: float, y: float, max_w: float, size=11, color=INK, leading=None):
    leading = leading or (size + 5)
    c.setFont("VN", size)
    c.setFillColor(color)
    words = text.split()
    line = ""
    for w in words:
        trial = (line + " " + w).strip()
        if c.stringWidth(trial, "VN", size) <= max_w:
            line = trial
        else:
            c.drawString(x, y, line)
            y -= leading
            line = w
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


def pill(c: canvas.Canvas, x, y, text, bgc, fgc=white):
    c.setFont("VN-Bold", 10)
    tw = c.stringWidth(text, "VN-Bold", 10) + 14
    c.setFillColor(bgc)
    c.roundRect(x, y - 3, tw, 16, 8, fill=1, stroke=0)
    c.setFillColor(fgc)
    c.drawString(x + 7, y, text)
    return tw


def page1(c: canvas.Canvas):
    bg(c)
    title(c, "VLearn Extend", H - 28 * mm)
    subtitle(c, "Hướng A — VLearn · Tính năng mới · Nhóm BMVD", H - 36 * mm)

    y = wrap(
        c,
        "Khi tài liệu buổi học đủ làm quiz nhưng mỏng, học viên muốn hiểu sâu hơn mà không mất thời gian tự kiếm nguồn lẫn và lệch bài.",
        18 * mm,
        H - 50 * mm,
        W - 40 * mm,
        size=13,
        color=INK,
        leading=18,
    )

    # evidence cards
    cards = [
        ("28%", "câu trả lời tutor\nkhông có citation", "3.781 / 13.494"),
        ("~5%", "tutor báo không tìm thấy\n/ không có trong tài liệu", "666 lượt"),
        ("~1,8%", "free-text xin đào sâu\n/ ví dụ / paper", "186 lượt"),
    ]
    cw = 55 * mm
    gap = 6 * mm
    x0 = 18 * mm
    for i, (big, mid, small) in enumerate(cards):
        x = x0 + i * (cw + gap)
        card(c, x, 28 * mm, cw, 55 * mm)
        c.setFillColor(ACCENT)
        c.setFont("VN-Bold", 28)
        c.drawString(x + 4 * mm, 68 * mm, big)
        c.setFillColor(INK)
        c.setFont("VN", 10)
        for j, line in enumerate(mid.split("\n")):
            c.drawString(x + 4 * mm, 55 * mm - j * 12, line)
        c.setFillColor(MUTED)
        c.setFont("VN", 9)
        c.drawString(x + 4 * mm, 34 * mm, small)

    c.showPage()


def page2(c: canvas.Canvas):
    bg(c)
    title(c, "Lát cắt & quyết định", H - 28 * mm)
    subtitle(c, "1 user · 1 việc · 1 quyết định · 1 kết quả", H - 36 * mm)

    card(c, 18 * mm, 95 * mm, W - 36 * mm, 42 * mm)
    wrap(
        c,
        "Học viên hỏi để hiểu thêm theo slide; hệ thống kiểm tra corpus trước, rồi chọn đúng một nhãn: trong bài / cần nguồn ngoài / không lấy được — kèm citation hoặc brief, không bịa DOI.",
        24 * mm,
        125 * mm,
        W - 48 * mm,
        size=12,
        leading=16,
    )

    # 3 candidates
    opts = [
        ("CHỌN", "Mở nguồn ngoài có điều kiện", "Corpus trước → ngoài sau\nKhông bịa DOI · từ chối làm hộ", OK),
        ("LOẠI", "Chỉ bám slide", "Đã có sẵn — không xử lý\ngap khi slide mỏng / retrieve fail", WARN),
        ("LOẠI", "Tìm web + viết hộ bài", "Cost-of-error học thuật cao\nNgoài lát cắt", BAD),
    ]
    cw = 58 * mm
    for i, (tag, head, body, col) in enumerate(opts):
        x = 18 * mm + i * (cw + 5 * mm)
        card(c, x, 28 * mm, cw, 58 * mm)
        pill(c, x + 4 * mm, 74 * mm, tag, col)
        c.setFillColor(INK)
        c.setFont("VN-Bold", 11)
        c.drawString(x + 4 * mm, 62 * mm, head)
        c.setFont("VN", 9)
        c.setFillColor(MUTED)
        for j, line in enumerate(body.split("\n")):
            c.drawString(x + 4 * mm, 50 * mm - j * 12, line)

    c.showPage()


def page3(c: canvas.Canvas):
    bg(c)
    title(c, "Luồng hoạt động", H - 28 * mm)
    subtitle(c, "Corpus trước · nguồn ngoài sau · retry ≤ 2 · LLM chỉ đọc notebook đã nạp", H - 36 * mm)

    steps = [
        ("01", "Hỏi", "Câu hỏi + ngữ cảnh bài"),
        ("02", "Tra lớp", "Hits corpus D1-P*"),
        ("03", "Quyết định", "Một nhãn rõ"),
        ("04", "Notebook", "Lớp ± nguồn ngoài"),
        ("05", "Trả lời", "Text + citation"),
    ]
    for i, (n, h, d) in enumerate(steps):
        x = 16 * mm + i * 55 * mm
        card(c, x, 118 * mm, 50 * mm, 32 * mm)
        c.setFillColor(ACCENT)
        c.setFont("VN-Bold", 10)
        c.drawString(x + 3 * mm, 140 * mm, n)
        c.setFillColor(INK)
        c.setFont("VN-Bold", 12)
        c.drawString(x + 3 * mm, 128 * mm, h)
        c.setFillColor(MUTED)
        c.setFont("VN", 9)
        c.drawString(x + 3 * mm, 118 * mm + 6, d)
        if i < 4:
            c.setFillColor(ACCENT2)
            c.setFont("VN-Bold", 14)
            c.drawString(x + 48 * mm, 130 * mm, "→")

    labels = [
        ("IN_CORPUS", "Đủ slide → trả lời ngay + citation lớp", OK),
        ("NEED_EXTERNAL", "Thiếu nhưng liên quan chủ đề → tìm MOCK, HV chọn + Nhập", ACCENT2),
        ("CANNOT_FETCH", "Cấm fetch / hết retry → brief 3 truy vấn, không bịa DOI", WARN),
        ("ASK_AGAIN / OUT", "Mơ hồ → hỏi lại · Lệch môn / làm hộ → từ chối", BAD),
    ]
    y = 100 * mm
    for lab, desc, col in labels:
        card(c, 18 * mm, y - 14 * mm, W - 36 * mm, 20 * mm)
        pill(c, 24 * mm, y - 4 * mm, lab, col)
        c.setFillColor(INK)
        c.setFont("VN", 11)
        c.drawString(78 * mm, y - 4 * mm, desc)
        y -= 24 * mm

    c.showPage()


def page4(c: canvas.Canvas):
    bg(c)
    title(c, "Prototype · Demo", H - 28 * mm)
    subtitle(c, "AI thật viết câu trả lời · Fetch/retry = MOCK · Chọn nguồn kiểu NotebookLM", H - 36 * mm)

    # left panel mock
    card(c, 18 * mm, 30 * mm, 85 * mm, 105 * mm)
    c.setFillColor(ACCENT)
    c.setFont("VN-Bold", 12)
    c.drawString(24 * mm, 122 * mm, "Nguồn › Khám phá")
    pill(c, 70 * mm, 122 * mm, "MOCK", WARN)
    c.setFillColor(MUTED)
    c.setFont("VN", 9)
    c.drawString(24 * mm, 110 * mm, "Câu hỏi ngoài slide nhưng liên quan LLM…")

    for i, (site, tit) in enumerate(
        [
            ("history.llm.mock", "[MOCK] Lược sử LLM → GPT"),
            ("history.transformer.mock", "[MOCK] Vaswani et al. 2017"),
            ("history.turing.mock", "[MOCK] Alan Turing & Test"),
        ]
    ):
        yy = 92 * mm - i * 20 * mm
        c.setFillColor(LINE)
        c.roundRect(24 * mm, yy, 73 * mm, 17 * mm, 4, fill=1, stroke=0)
        c.setFillColor(MUTED)
        c.setFont("VN", 8)
        c.drawString(28 * mm, yy + 10, site)
        c.setFillColor(INK)
        c.setFont("VN", 9)
        c.drawString(28 * mm, yy + 2, tit)

    c.setFillColor(HexColor("#1a73e8"))
    c.roundRect(55 * mm, 36 * mm, 28 * mm, 10 * mm, 5, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("VN-Bold", 10)
    c.drawCentredString(69 * mm, 39 * mm, "Nhập")

    # right points
    pts = [
        "Chạy: python codebase/server.py → :8777",
        "Badge: AI THẬT · fetch MOCK",
        "Corpus: mã D1-P* (không commit data pack)",
        "Chỉ mở nguồn khi neo chủ đề Day 1",
        "Lệch môn (PT bậc 2, LS chung…) → từ chối",
        "Làm hộ bài → OUT_OF_SCOPE",
    ]
    y = 125 * mm
    for p in pts:
        card(c, 110 * mm, y - 8 * mm, W - 128 * mm, 16 * mm)
        y = bullet(c, 116 * mm, y - 2 * mm, "•  " + p, size=11)
        y -= 6

    c.showPage()


def page5(c: canvas.Canvas):
    bg(c)
    title(c, "Kiểm thử & quality bar", H - 28 * mm)
    subtitle(c, "Golden set 20 case · Đo lượt đầu run-01 · Bar khóa từ CP4", H - 36 * mm)

    # big number
    card(c, 18 * mm, 95 * mm, 70 * mm, 50 * mm)
    c.setFillColor(OK)
    c.setFont("VN-Bold", 42)
    c.drawCentredString(53 * mm, 122 * mm, "93,3%")
    c.setFillColor(INK)
    c.setFont("VN", 11)
    c.drawCentredString(53 * mm, 108 * mm, "14 / 15 đạt · run-01")
    c.setFillColor(MUTED)
    c.setFont("VN", 9)
    c.drawCentredString(53 * mm, 98 * mm, "openai:gpt-4o-mini")

    card(c, 95 * mm, 95 * mm, W - 113 * mm, 50 * mm)
    rows = [
        "Quality bar (khóa): ≥ 93,3% trên GS-01…15",
        "0 bịa DOI / URL / paper ngoài notebook",
        "ASK_AGAIN phải có ask_again ≠ rỗng",
        "Lỗi API / thiếu key = không đạt",
        "GS-16…20 bổ sung ≥20 — không hạ bar",
    ]
    y = 135 * mm
    for r in rows:
        y = bullet(c, 102 * mm, y, "•  " + r, size=11)
        y -= 2

    # error groups
    groups = [
        ("Sai nguồn", "1", "GS-07 Context Rot"),
        ("Không hỏi lại", "0", "—"),
        ("Lỗi kỹ thuật", "0", "—"),
    ]
    for i, (name, n, note) in enumerate(groups):
        x = 18 * mm + i * 62 * mm
        card(c, x, 30 * mm, 58 * mm, 50 * mm)
        c.setFillColor(ACCENT)
        c.setFont("VN-Bold", 12)
        c.drawString(x + 4 * mm, 68 * mm, name)
        c.setFont("VN-Bold", 28)
        c.setFillColor(BAD if n != "0" else OK)
        c.drawString(x + 4 * mm, 50 * mm, n)
        c.setFillColor(MUTED)
        c.setFont("VN", 9)
        c.drawString(x + 4 * mm, 38 * mm, note)

    c.showPage()


def page6(c: canvas.Canvas):
    bg(c)
    title(c, "Nhóm & validation", H - 28 * mm)
    subtitle(c, "Phân công · Willing users R6 · Repo nộp", H - 36 * mm)

    team = [
        ("Khải Vũ", "Evidence + corpus"),
        ("Thân Tiến Đạt", "Golden set + Eval"),
        ("Bảo", "AI thật + Prototype"),
        ("Minh", "Bằng chứng + Spec"),
    ]
    for i, (name, role) in enumerate(team):
        x = 18 * mm + (i % 2) * 95 * mm
        y = 115 * mm - (i // 2) * 28 * mm
        card(c, x, y, 90 * mm, 24 * mm)
        c.setFillColor(INK)
        c.setFont("VN-Bold", 12)
        c.drawString(x + 4 * mm, y + 12 * mm, name)
        c.setFillColor(MUTED)
        c.setFont("VN", 10)
        c.drawString(x + 4 * mm, y + 4 * mm, role)

    card(c, 18 * mm, 28 * mm, W - 36 * mm, 48 * mm)
    c.setFillColor(ACCENT)
    c.setFont("VN-Bold", 12)
    c.drawString(24 * mm, 64 * mm, "Validation R6 (ngoài nhóm)")
    c.setFillColor(INK)
    c.setFont("VN", 11)
    c.drawString(24 * mm, 50 * mm, "Trí — 2A202602730   ·   Trí — 2A202602603")
    wrap(
        c,
        "Chạy 4 nhánh IN / NEED (chọn nguồn) / CANNOT / SCOPE. Quote: dễ hiểu hơn khi biết đâu là ngoài slide; hợp hỏi lịch sử / người tạo khái niệm trên bài.",
        24 * mm,
        40 * mm,
        W - 48 * mm,
        size=10,
        color=MUTED,
        leading=13,
    )

    c.setFillColor(MUTED)
    c.setFont("VN", 9)
    c.drawString(18 * mm, 18 * mm, "Repo: github.com/oabga/K4-3A-E403-BMVD  ·  Branch CP04  ·  Live: codebase/server.py")

    c.showPage()


def main():
    c = canvas.Canvas(str(OUT), pagesize=PAGE)
    c.setTitle("VLearn Extend — Demo slides · BMVD")
    c.setAuthor("Nhóm BMVD")
    for fn in (page1, page2, page3, page4, page5, page6):
        fn(c)
    c.save()
    # verify page count
    from reportlab.lib.pagesizes import landscape  # noqa: F401
    from reportlab.pdfbase.pdfdoc import PDFDocument  # noqa: F401

    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
