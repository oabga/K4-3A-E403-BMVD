# K4-3A-E403-BMVD · Nhóm BMVD · Zone 3A — VLearn Extend

Mini Hackathon AI · Hướng **A — VLearn** · Lát cắt: mở nguồn ngoài có điều kiện khi slide mỏng.

## Cấu trúc nộp (đối chiếu checklist)

| Path | Trạng thái | Ghi chú |
|---|---|---|
| `README.md` | Có | File này |
| `TEAMMATES.md` | Có | Họ tên + vai (MSSV điền đủ trong `TEAMMATES.md`) |
| `spec.md` | Có | AI Spec 8 phần · quality bar khóa ≥ 93,3% (14/15) |
| `demo-slides.pdf` | **Thiếu — nhóm bổ sung** | Đúng 6 trang PDF báo cáo |
| `codebase/` | Có | Prototype AI thật; fetch/retry = **MOCK** |
| `eval/` | Có | Golden set **20** case + `eval/runs/run-01.*` |
| `validation/` | Có | Nhật ký willing users (R6) |
| `reflection/` | Có | Thu hoạch cá nhân (template — từng người điền) |
| `evidence/` | Có (bổ sung) | Mining / quote / khảo sát — không thay `validation/` |

> Alias: thư mục `prototype/` (nếu còn trên máy) = bản cũ; **chạy và nộp theo `codebase/`**.

## Phân công vai trò

| Vai | Thành viên | Artifact chính |
|---|---|---|
| Evidence + corpus | Khải Vũ | `evidence/`, excerpt `D1-P01`…`D1-P10` |
| Golden set + Eval | Thân Tiến Đạt | `eval/golden-set.*`, `eval/runs/` |
| AI thật + Prototype | Bảo | `codebase/`, `eval/prompt.md`, `.env` (không commit) |
| Bằng chứng live + video + Spec | Minh | Live/video CP3 · `spec.md` · điều phối validation |

Chi tiết tên/MSSV: `TEAMMATES.md`.

## Chạy prototype

```bash
cp .env.example .env   # điền OPENAI_API_KEY hoặc GEMINI_API_KEY
python codebase/server.py
# → http://127.0.0.1:8777
```

- Trả lời: **AI thật** (nếu có key)
- Fetch / retry / nguồn ngoài: **MOCK** — UI ghi rõ; HV chọn nguồn rồi **Nhập** (kiểu NotebookLM) khi `NEED_EXTERNAL`
- Corpus: mã `D1-P*` trong `codebase/corpus_excerpts.json` (không commit `data/`)

Eval:

```bash
python codebase/run_eval.py
```

## Tài liệu liên quan

- Spec: `spec.md`
- Luồng CP2: `CP2-Luong-Hoat-Dong-Edited.md`
- CP3: `eval/CP3.md`
- Canvas CP1: `canvas/canvas.jpg` (nếu có trên máy nhóm)

`data/` **không** commit.
