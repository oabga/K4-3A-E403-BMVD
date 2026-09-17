# CP3 — Nối AI thật · Golden set · Đo lượt đầu · Nộp bằng chứng

CP2 (`CP2-Luong-Hoat-Dong-Edited.md`) đã chốt luồng + retry.  
CP3 **không** khóa quality bar — chỉ thống nhất tiêu chí từng case và lấy số gốc. CP4 mới ghi ngưỡng vào `spec.md`.

## 4 việc

1. **Nối AI thật** — LLM viết câu trả lời từ notebook. Fetch / retry / data pack = **MOCK** (ghi rõ trên UI).  
2. **Golden set** — 15 case: `eval/golden-set.md` + `eval/golden-set.json`.  
3. **Đo lượt đầu** — cùng model + `eval/prompt.md` cho cả bộ → `eval/runs/run-01.md`.  
4. **Nộp bằng chứng** — live xác minh AI thật **và** video 30s + số đo + số mẫu.

Không commit `data/` (đã gitignore). Chỉ mã `B3-S1` / trích ngắn trong `prototype/corpus_excerpts.json`.

## Việc nhóm làm trên máy có key

```bash
cp .env.example .env
# điền OPENAI_API_KEY hoặc GEMINI_API_KEY

python3 prototype/run_eval.py          # ghi eval/runs/run-01.md
python3 prototype/server.py            # live http://127.0.0.1:8777
```

Mở case **không đạt**, gắn đúng một nhóm hậu quả:

| Nhóm | Khi nào |
|---|---|
| Sai nguồn | Nhãn sai, citation ngoài notebook, bịa DOI, trộn ngoài lớp như trong bài |
| Không hỏi lại | Đáng ASK_AGAIN mà vẫn giảng |
| Lỗi kỹ thuật | HTTP, timeout, thiếu key, JSON vỡ — vẫn ghi vào bảng, tính không đạt lượt này |

## Hai bằng chứng nộp

**A. Trình bày trực tiếp**  
Chạy `server.py`, mạng DevTools thấy gọi `api.openai.com` hoặc Gemini. Gửi lần lượt: Biến là gì? → khác hằng → DOI giả → viết hộ bài. Chỉ rõ badge **AI THẬT** vs **MOCK** fetch.

**B. Video ~30 giây + số đo + số mẫu**  
Kịch bản:

0–5s: UI + «AI THẬT / fetch MOCK»  
5–20s: 3 câu (IN / NEED / CANNOT)  
20–30s: màn `run-01.md`: **n = 15**, số đạt, %, 3 nhóm lỗi  

Nộp kèm: `eval/golden-set.md`, `eval/runs/run-01.md` (sau khi chạy), `eval/prompt.md`.

## Phần MOCK vs thật

| Thành phần | CP3 |
|---|---|
| Sinh câu trả lời / JSON | **AI thật** |
| Tra excerpt B3-* | Thật (từ file mã, không data pack) |
| Quyết định nhãn | Rule pipeline (không LLM đổi nhãn) |
| Fetch web, retry, nguồn MOCK-EXT | **MOCK** |
| Trang HTML | Prototype working; chỗ giả lập ghi MOCK |
