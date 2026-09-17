# Review A/B + phần C (Bảo) — CP3

Cập nhật: 2026-09-17

## A — Evidence + corpus (Khải Vũ) — ĐỦ cho CP3

| Artifact | Trạng thái |
|---|---|
| `prototype/corpus_excerpts.json` | 10 đoạn Day 1 `D1-P01`…`D1-P10` (transcript + slide) |
| `evidence/mining.md` | Có số + tiêu chí nhãn |
| `evidence/quotes.md` | ≥5 quote / turn_id |

Ghi chú: mining `NEED_EXTERNAL` 39% trên mẫu 200 — nhóm tự chịu trách nhiệm khi bảo vệ; chatlog toàn cục vẫn chủ yếu bôi đen. Corpus prototype **đã neo Day 1**, đủ chạy golden set.

## B — Golden + Eval (Thân Tiến Đạt) — ĐỦ khung; số đo đã có

| Artifact | Trạng thái |
|---|---|
| `eval/golden-set.md` + `.json` | 15 case neo Day 1, đủ nhãn |
| `eval/prompt.md` | Có |
| `eval/runs/run-01.md` | Đã chạy: **14/15 = 93.3%** (GS-07 Sai nguồn) |

GS-07 fail cũ: nhãn `IN_CORPUS` thay vì `NEED_EXTERNAL` + thiếu MOCK-EXT — do pipeline C chưa khớp câu “thực tế / ngoài việc…”.

## C — AI + Prototype (Bảo) — ĐÃ LÀM trong lượt này

| Việc | File |
|---|---|
| Sửa `decide` + MOCK Day 1 | `prototype/extend.py`, `external_mock.json` |
| Truyền `corpus_refs` khi eval | `prototype/run_eval.py` |
| Demo Streamlit | `prototype/streamlit_app.py` |
| Label check không cần API | **15/15** khớp nhãn kỳ vọng |

### Chạy demo

```bash
cd /home/oabga/K4-3A-E403-BMVD
cp .env.example .env   # điền OPENAI_API_KEY hoặc GEMINI_API_KEY
source .venv/bin/activate
streamlit run prototype/streamlit_app.py
```

### Chạy lại eval (sau khi có key) — nên ghi run-02 hoặc ghi đè run-01 nếu nhóm đồng ý

```bash
source .venv/bin/activate
python prototype/run_eval.py
```

## Việc còn lại (không phải C)

- **D (Minh):** live + video 30s dùng Streamlit + màn `run-01.md`
- **B (tuỳ):** chạy lại eval sau fix C → cập nhật % nếu muốn số mới
