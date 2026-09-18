#!/usr/bin/env python3
"""demo-slides.pdf — 6 trang landscape, layout kiểu Canva + ảnh trang trí."""
from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, Color, white, black
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "demo-slides.pdf"
IMG = ROOT / "assets" / "slides"

pdfmetrics.registerFont(TTFont("VN", "C:/Windows/Fonts/segoeui.ttf"))
pdfmetrics.registerFont(TTFont("VN-Bold", "C:/Windows/Fonts/segoeuib.ttf"))

PAGE = landscape(A4)
W, H = PAGE

INK = HexColor("#14231c")
MUTED = HexColor("#5a635c")
CREAM = HexColor("#f7f3ea")
SAGE = HexColor("#2c4a3e")
SAGE_LIGHT = HexColor("#3f6a57")
LEAF = HexColor("#dfe8e2")
AMBER = HexColor("#c4843a")
SOFT_RED = HexColor("#a84b3d")
SOFT_GREEN = HexColor("#1f6b45")


def img(name: str) -> Path:
    return IMG / name


def draw_image_cover(c: canvas.Canvas, path: Path, x, y, w, h, radius=0):
    """Cover-fit image into box (center crop)."""
    if not path.exists():
        c.setFillColor(LEAF)
        c.rect(x, y, w, h, fill=1, stroke=0)
        return
    ir = ImageReader(str(path))
    iw, ih = ir.getSize()
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    ox = x + (w - dw) / 2
    oy = y + (h - dh) / 2
    c.saveState()
    p = c.beginPath()
    if radius:
        p.roundRect(x, y, w, h, radius)
    else:
        p.rect(x, y, w, h)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(ir, ox, oy, width=dw, height=dh, mask="auto")
    c.restoreState()


def footer(c: canvas.Canvas, page: int, light=False):
    c.setFillColor(white if light else MUTED)
    c.setFont("VN", 9)
    c.drawString(16 * mm, 7 * mm, "VLearn Extend  ·  Nhóm BMVD")
    c.drawRightString(W - 14 * mm, 7 * mm, f"{page} / 6")


def wrap(c, text, x, y, max_w, font="VN", size=14, color=INK, leading=None):
    leading = leading or size + 7
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    line = ""
    for w in words:
        trial = (line + " " + w).strip()
        if c.stringWidth(trial, font, size) <= max_w:
            line = trial
        else:
            c.drawString(x, y, line)
            y -= leading
            line = w
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


def pill(c, x, y, text, bg, fg=white, size=10):
    c.setFont("VN-Bold", size)
    tw = c.stringWidth(text, "VN-Bold", size) + 16
    c.setFillColor(bg)
    c.roundRect(x, y - 4, tw, 18, 9, fill=1, stroke=0)
    c.setFillColor(fg)
    c.drawString(x + 8, y, text)
    return tw


# ─── SLIDE 1: Tên nhóm ───────────────────────────────────────────
def page_team(c: canvas.Canvas):
    # full-bleed image
    draw_image_cover(c, img("slide-01-team.png"), 0, 0, W, H)
    # dark soft overlay left for readability
    c.setFillColor(Color(0.08, 0.14, 0.11, alpha=0.55))
    c.rect(0, 0, W * 0.52, H, fill=1, stroke=0)

    c.setFillColor(HexColor("#d8e6dc"))
    c.setFont("VN", 12)
    c.drawString(22 * mm, H - 28 * mm, "MINI HACKATHON AI  ·  ZONE 3A")

    c.setFillColor(white)
    c.setFont("VN-Bold", 54)
    c.drawString(22 * mm, H - 55 * mm, "BMVD")

    c.setFont("VN-Bold", 22)
    c.drawString(22 * mm, H - 70 * mm, "VLearn Extend")

    y = wrap(
        c,
        "Khi slide lớp mỏng, học viên vẫn hiểu sâu — có nguồn, có phân biệt trong bài / ngoài bài.",
        22 * mm,
        H - 88 * mm,
        W * 0.42,
        size=13,
        color=HexColor("#e8f0eb"),
        leading=18,
    )

    members = [
        "Khải Vũ — Evidence",
        "Thân Tiến Đạt — Eval",
        "Bảo — Prototype",
        "Minh — Spec & Demo",
    ]
    y = 48 * mm
    for m in members:
        c.setFillColor(Color(1, 1, 1, alpha=0.18))
        c.roundRect(22 * mm, y - 3, 78 * mm, 11 * mm, 5, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("VN", 11)
        c.drawString(26 * mm, y, m)
        y -= 14 * mm

    footer(c, 1, light=True)
    c.showPage()


# ─── SLIDE 2: Pain ───────────────────────────────────────────────
def page_pain(c: canvas.Canvas):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # image right panel
    draw_image_cover(c, img("slide-02-pain.png"), W * 0.48, 0, W * 0.52, H)

    c.setFillColor(SAGE)
    c.rect(0, 0, 6 * mm, H, fill=1, stroke=0)

    pill(c, 18 * mm, H - 24 * mm, "VẤN ĐỀ", SOFT_RED)
    c.setFillColor(INK)
    c.setFont("VN-Bold", 28)
    c.drawString(18 * mm, H - 42 * mm, "Slide đủ làm quiz…")
    c.drawString(18 * mm, H - 54 * mm, "nhưng chưa đủ để hiểu.")

    pains = [
        ("1", "Slide chỉ vài gạch đầu dòng", "Muốn ví dụ / đào sâu thì… hết."),
        ("2", "Phải tự Google / Scholar", "Mất 15–30 phút, nguồn lẫn."),
        ("3", "Tutor trong lớp hay chung chung", "28% câu trả lời không có nguồn."),
    ]
    y = H - 78 * mm
    for num, title, sub in pains:
        c.setFillColor(white)
        c.setStrokeColor(HexColor("#e4ddd0"))
        c.setLineWidth(1)
        c.roundRect(18 * mm, y - 8 * mm, W * 0.40, 28 * mm, 8, fill=1, stroke=1)
        c.setFillColor(SAGE)
        c.circle(28 * mm, y + 6 * mm, 7, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("VN-Bold", 12)
        c.drawCentredString(28 * mm, y + 3 * mm, num)
        c.setFillColor(INK)
        c.setFont("VN-Bold", 13)
        c.drawString(40 * mm, y + 8 * mm, title)
        c.setFillColor(MUTED)
        c.setFont("VN", 11)
        c.drawString(40 * mm, y - 2 * mm, sub)
        y -= 34 * mm

    footer(c, 2)
    c.showPage()


# ─── SLIDE 3: Solution ───────────────────────────────────────────
def page_solution(c: canvas.Canvas):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    draw_image_cover(c, img("slide-03-solution.png"), 0, 0, W * 0.46, H)

    # cream panel right
    c.setFillColor(CREAM)
    c.rect(W * 0.44, 0, W * 0.56, H, fill=1, stroke=0)
    # soft fade strip
    c.setFillColor(Color(0.97, 0.95, 0.92, alpha=0.85))
    c.rect(W * 0.42, 0, W * 0.04, H, fill=1, stroke=0)

    pill(c, W * 0.48, H - 24 * mm, "GIẢI PHÁP", SOFT_GREEN)
    c.setFillColor(INK)
    c.setFont("VN-Bold", 26)
    c.drawString(W * 0.48, H - 42 * mm, "VLearn Extend")
    wrap(
        c,
        "Trợ lý trên trang bài: đọc slide trước, chỉ mở nguồn ngoài khi cần — và để bạn chọn nguồn trước khi trả lời.",
        W * 0.48,
        H - 56 * mm,
        W * 0.44,
        size=13,
        color=MUTED,
        leading=17,
    )

    steps = [
        ("Trong bài", "Có trên slide → trả lời ngay, kèm mã nguồn lớp."),
        ("Thiếu nhưng liên quan", "Hiện danh sách nguồn MOCK → bạn chọn → Nhập → mới trả lời."),
        ("Không lấy được / lệch môn", "Nói thẳng, gợi ý tìm; hoặc từ chối làm hộ / hỏi lệch đề."),
    ]
    y = H - 95 * mm
    for title, body in steps:
        c.setFillColor(white)
        c.roundRect(W * 0.48, y - 6 * mm, W * 0.44, 26 * mm, 8, fill=1, stroke=0)
        c.setFillColor(SAGE)
        c.setFont("VN-Bold", 12)
        c.drawString(W * 0.48 + 5 * mm, y + 10 * mm, title)
        c.setFillColor(MUTED)
        c.setFont("VN", 10)
        wrap(c, body, W * 0.48 + 5 * mm, y + 1 * mm, W * 0.40, size=10, color=MUTED, leading=13)
        y -= 32 * mm

    footer(c, 3)
    c.showPage()


# ─── SLIDE 4: Flow (dễ hiểu) ─────────────────────────────────────
def page_flow(c: canvas.Canvas):
    c.setFillColor(HexColor("#eef3f0"))
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # top banner image strip
    draw_image_cover(c, img("slide-04-flow.png"), 0, H * 0.42, W, H * 0.58)
    c.setFillColor(Color(0.08, 0.14, 0.11, alpha=0.45))
    c.rect(0, H * 0.42, W, H * 0.58, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("VN-Bold", 28)
    c.drawString(18 * mm, H - 28 * mm, "Chạy thế nào?")
    c.setFont("VN", 13)
    c.drawString(18 * mm, H - 40 * mm, "Năm bước — học viên thấy rõ mỗi lần hỏi")

    # bottom cream cards
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H * 0.48, fill=1, stroke=0)

    cards = [
        ("1", "Hỏi", "Câu hỏi trên trang bài"),
        ("2", "Đọc slide", "Tra corpus lớp trước"),
        ("3", "Gắn nhãn", "Trong bài / cần ngoài / không lấy được"),
        ("4", "Chọn nguồn", "Nếu thiếu: tick + Nhập"),
        ("5", "Trả lời", "Có citation, không bịa DOI"),
    ]
    cw = 48 * mm
    gap = 4 * mm
    total = 5 * cw + 4 * gap
    x0 = (W - total) / 2
    for i, (n, t, d) in enumerate(cards):
        x = x0 + i * (cw + gap)
        c.setFillColor(white)
        c.setStrokeColor(HexColor("#d5e0d9"))
        c.roundRect(x, 22 * mm, cw, 58 * mm, 10, fill=1, stroke=1)
        c.setFillColor(SAGE)
        c.circle(x + 10 * mm, 68 * mm, 6, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("VN-Bold", 11)
        c.drawCentredString(x + 10 * mm, 65.5 * mm, n)
        c.setFillColor(INK)
        c.setFont("VN-Bold", 12)
        c.drawString(x + 4 * mm, 52 * mm, t)
        wrap(c, d, x + 4 * mm, 42 * mm, cw - 8 * mm, size=9, color=MUTED, leading=12)

    footer(c, 4)
    c.showPage()


# ─── SLIDE 5: Proof ──────────────────────────────────────────────
def page_proof(c: canvas.Canvas):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    draw_image_cover(c, img("slide-05-proof.png"), W * 0.55, 18 * mm, W * 0.40, H - 36 * mm, radius=14)

    pill(c, 18 * mm, H - 24 * mm, "BẰNG CHỨNG", SAGE)
    c.setFillColor(INK)
    c.setFont("VN-Bold", 26)
    c.drawString(18 * mm, H - 42 * mm, "Đã đo, đã khóa.")

    # big metric
    c.setFillColor(white)
    c.roundRect(18 * mm, H - 95 * mm, 70 * mm, 42 * mm, 12, fill=1, stroke=0)
    c.setFillColor(SOFT_GREEN)
    c.setFont("VN-Bold", 40)
    c.drawString(26 * mm, H - 72 * mm, "93,3%")
    c.setFillColor(MUTED)
    c.setFont("VN", 11)
    c.drawString(26 * mm, H - 86 * mm, "14/15 case lượt đầu")

    bullets = [
        "Golden set 20 case (Day 1 AI & LLM)",
        "Quality bar khóa ≥ 93,3% — không hạ sau nộp",
        "AI thật viết câu trả lời · fetch = MOCK",
        "Validation R6: 2 HV ngoài nhóm",
    ]
    y = H - 112 * mm
    for b in bullets:
        c.setFillColor(SAGE)
        c.circle(22 * mm, y + 2, 2.2, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("VN", 12)
        c.drawString(28 * mm, y, b)
        y -= 12 * mm

    footer(c, 5)
    c.showPage()


# ─── SLIDE 6: Ending ─────────────────────────────────────────────
def page_ending(c: canvas.Canvas):
    draw_image_cover(c, img("slide-06-ending.png"), 0, 0, W, H)
    c.setFillColor(Color(0.07, 0.12, 0.10, alpha=0.50))
    c.rect(0, 0, W, H, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("VN-Bold", 42)
    c.drawCentredString(W / 2, H * 0.58, "Cảm ơn đã lắng nghe")

    c.setFont("VN", 16)
    c.drawCentredString(W / 2, H * 0.48, "Nhóm BMVD  ·  VLearn Extend")

    c.setFillColor(HexColor("#d5e4db"))
    c.setFont("VN", 12)
    c.drawCentredString(W / 2, H * 0.38, "Hỏi trên trang bài  →  nguồn rõ  →  hiểu sâu, không lệch đề")

    # decorative line
    c.setStrokeColor(HexColor("#9bb5a6"))
    c.setLineWidth(1.2)
    c.line(W / 2 - 40 * mm, H * 0.33, W / 2 + 40 * mm, H * 0.33)

    c.setFillColor(white)
    c.setFont("VN", 11)
    c.drawCentredString(W / 2, H * 0.26, "Live demo: python codebase/server.py  →  http://127.0.0.1:8777")

    footer(c, 6, light=True)
    c.showPage()


def main():
    c = canvas.Canvas(str(OUT), pagesize=PAGE)
    c.setTitle("VLearn Extend — BMVD Demo")
    c.setAuthor("Nhóm BMVD")
    page_team(c)
    page_pain(c)
    page_solution(c)
    page_flow(c)
    page_proof(c)
    page_ending(c)
    c.save()
    from pypdf import PdfReader

    n = len(PdfReader(str(OUT)).pages)
    print(f"Wrote {OUT} · pages={n} · {OUT.stat().st_size} bytes")
    if n != 6:
        raise SystemExit(f"Expected 6 pages, got {n}")


if __name__ == "__main__":
    main()
