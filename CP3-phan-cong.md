# CP3 — Phân công 4 thành viên & việc cần làm

**Đề:** VLearn Extend (canvas CP1 · luồng CP2 đã chốt)  
**Mốc:** Nối AI thật → Golden set → Đo lượt đầu → Nộp bằng chứng  
**Không làm ở CP3:** khóa quality bar trên `spec.md` (để CP4)

Điền tên vào bảng dưới và commit file này + `TEAMMATES.md`.

---

## 0. Hiện trạng repo (review)


| Hạng mục         | Trạng thái    | Ghi chú                                                          |
| ---------------- | ------------- | ---------------------------------------------------------------- |
| CP1 canvas       | Có            | `canvas/canvas.jpg`                                              |
| CP2 luồng        | Xong          | `CP2-Luong-Hoat-Dong-Edited.md` (có retry)                       |
| Pack BTC         | Có local      | `data/vlearn-pack/` — slides Day1/Day2, transcript, chatlog      |
| `data/` trên git | Không commit  | `.gitignore` có `data/` — đúng luật pack                         |
| Khung CP3        | Có sẵn        | `eval/`, `prototype/`                                            |
| Golden set       | **Xong (B)**  | 15 case Day 1 trong `eval/golden-set.*` |
| Corpus prototype | **Xong (A)**  | `D1-P01`–`D1-P10` trong `prototype/corpus_excerpts.json` |
| Run-01           | **Có số (B)** | 14/15 = 93.3%; GS-07 sai nguồn — C đã sửa pipeline |
| Demo Streamlit   | **Xong (C)**  | `prototype/streamlit_app.py` — xem `eval/CP3-review-ABC.md` |
| Spec CP4         | Template      | Không khóa % ở CP3 |

**Kết luận:** A/B đủ corpus + golden + run-01. C: AI pipeline + Streamlit. Còn **D**: live + video 30s.

---



## 1. Nhớ nhanh: CP3 đang kiểm gì?

1. Prototype gọi **AI thật** (không chỉ HTML kịch bản cứng như CP2).
2. Có **10–20 test case** (nhóm đang nhắm **15**): mã, đầu vào, hành vi, tiêu chí đạt.
3. Chạy **cùng 1 model + 1 prompt** → bảng đạt/không; lỗi gắn nhóm: **Sai nguồn / Không hỏi lại / Lỗi kỹ thuật**.
4. Nộp: **live** xác minh AI thật **và** **video ~30s** + số mẫu + số đo.

**PDF / pack:** không phải “model tự hỏi file PDF”. Người/A trích đoạn từ slide hoặc transcript → notebook → model chỉ viết từ notebook. Fetch web = **MOCK**.

**Chatlog:** nhiều môn/bài; không phải mọi `turn_id` đều là 2 PDF d1/d2. Dùng để lấy ý / evidence; golden set nội dung chính neo **Day 1 hoặc Day 2** (+ transcript cùng buổi).

---



## 2. Bốn ghế (điền tên)


| Ghế   | Tên thành viên    | Vai CP3             | File / artifact chịu trách nhiệm                                            |
| ----- | ----------------- | ------------------- | --------------------------------------------------------------------------- |
| **A** | *( Khải Vũ)*      | Evidence + corpus   | `evidence/mining.md`, `evidence/quotes.md`, trích corpus ngắn cho prototype |
| **B** | *(Thân Tiến Đạt)* | Golden set + Eval   | `eval/golden-set.md`, `eval/golden-set.json`, `eval/runs/run-01.`*          |
| **C** | *(Bảo)*           | AI thật + Prototype | `eval/prompt.md`, `prototype/`*, `.env` (không commit)                      |
| **D** | *(Minh)*          | Bằng chứng nộp CP3  | Kịch bản live + video 30s; checklist nộp; điều phối demo                    |


Canvas gốc có 5 vai (Spec / Prototype / Evidence / AI call / Eval+Demo). Với 4 người: **Spec để CP4**; CP3 gộp **Eval + Demo → B đo số, D nộp bằng chứng**.

---



## 3. Thứ tự làm (bắt buộc)

```
A neo pack (Day1 hoặc Day2 + turn_id)
        ↓
B viết / khóa 15 case + tiêu chí đạt  ← họp nhóm 15 phút duyệt
        ↓
C gắn corpus thật + AI thật chạy được 4 nhánh demo
        ↓
B chạy run-01 (cùng model + prompt.md)
        ↓
C (tuỳ) sửa 1 vòng theo case fail — không đổi model giữa chừng trong cùng lượt đo
        ↓
D live + quay video (n=15, số đạt, %, 3 nhóm lỗi)
```

**Song song được:** C dựng server/UI lúc A đọc pack; D soạn kịch bản video sớm.  
**Không làm ngược:** không khóa 15 case “Biến/int”; không quay video trước khi có bảng `run-01`.

---



## 4. Checklist từng người



### A — Evidence + corpus

- [x] Chốt corpus chính: **Day 1** (Day 1 — AI & LLM Foundation: Transformer, Attention, Token, Context Rot).  
- [x] Đọc `slides/d1-…` + transcript khớp (`transcript-04-clean.md` ~ Day 1).  
- [x] Mining chatlog (đọc `DATA_DICTIONARY.md` trước): lọc `is_preset`, ghi số (% NEED_EXTERNAL, % thiếu trích dẫn) vào `evidence/mining.md`.  
- [x] ≥5 quote hoặc `turn_id` (+ 1 dòng ngữ cảnh) vào `evidence/quotes.md` — đã cập nhật 6 quote thực tế.  
- [x] Giao cho B/C: danh sách **10 đoạn text** (mã `D1-P01` đến `D1-P10`) nạp vào `prototype/corpus_excerpts.json`.  
- [x] Nhắc nhóm: không commit nguyên `tutor_turns.csv` / PDF lên remote công khai (đã cấu hình `.gitignore`).

**Xong:** B đã có căn cứ viết Golden Set; C đã có kho corpus bài học Day 1 trong prototype.

---



### B — Golden set + Eval

- [x] Xóa/thay case “Biến / int / B3-*” — viết lại **15 case** neo buổi A đã chọn.  
- [x] Cơ cấu gợi ý: ~10 thường + ~5 khó; đủ nhãn `IN_CORPUS`, `NEED_EXTERNAL`, `CANNOT_FETCH`, `ASK_AGAIN` / `OUT_OF_SCOPE`.  
- [x] Mỗi case đủ: **Mã · Đầu vào · Hành vi mong đợi · Tiêu chí đạt**.  
- [x] Họp nhóm 15 phút: **thống nhất tiêu chí đạt** (CP3 chưa khóa % spec).  
- [x] Đồng bộ `eval/golden-set.md` ↔ `eval/golden-set.json`.  
- [x] Sau khi C sẵn sàng: một cấu hình duy nhất → `python3 prototype/run_eval.py`.  
- [x] Điền `eval/runs/run-01.md` (+ json nếu có): đạt/không, lý do, **Sai nguồn / Không hỏi lại / Lỗi kỹ thuật**.  
- [x] Lỗi API/thiếu key cũng ghi **Lỗi kỹ thuật**, tính không đạt lượt này.

**Xong:** có bảng run-01 với **n = 15**, **14/15 = 93.3%**, sai nguồn 1, không hỏi lại 0, lỗi kỹ thuật 0.

---



### C — AI thật + Prototype

- [ ] `cp .env.example .env` — điền `OPENAI_API_KEY` hoặc `GEMINI_API_KEY` (**không commit** `.env`).  
- [ ] Thay `prototype/corpus_excerpts.json` bằng đoạn A giao (mã kiểu `D2-P03`, `[T01-012]`… — không data pack đầy đủ).  
- [ ] Giữ fetch/retry/**MOCK-EXT** ghi rõ **MOCK** trên UI.  
- [ ] Không đổi `eval/prompt.md` giữa các case trong **cùng** lượt run-01.  
- [ ] Live: `python3 prototype/server.py` → chứng minh gọi API thật (DevTools).  
- [ ] Demo tối thiểu 4 câu: có trên slide → cần ngoài → không fetch/DOI → ngoài phạm vi / hỏi lại.  
- [ ] Sau run-01: sửa đúng nhóm lỗi B chỉ ra (một vòng), rồi để B chạy lại **chỉ nếu** cả nhóm đồng ý đó vẫn là “lượt đầu” hoặc ghi `run-02` (CP3 ưu tiên có **một** số gốc rõ).

**Xong khi:** live AI thật + B chạy xong bộ golden không kẹt thiếu key.

---



### D — Bằng chứng nộp CP3

- [ ] Checklist nộp: `eval/golden-set.md`, `eval/prompt.md`, `eval/runs/run-01.md`, prototype chạy được.  
- [ ] **Bằng chứng 1 — Live:** điều phối A/B/C; chỉ rõ badge AI THẬT vs MOCK fetch.  
- [ ] **Bằng chứng 2 — Video ~30s:**  
  - 0–5s: UI + AI THẬT / fetch MOCK  
  - 5–20s: ≥3 nhánh nhãn  
  - 20–30s: màn run-01 với **số mẫu**, **số đạt**, **%**, **3 nhóm lỗi**
- [ ] Link video + ghi chú nộp vào chỗ nhóm quy ước (README ngắn hoặc `eval/CP3-nop.md` nếu cần).  
- [ ] Rà git: không có `data/vlearn-pack/**` nặng / CSV đầy đủ trên remote.

**Xong khi:** live xem được + video có số đo.

---



## 5. Họp nhóm (3 mốc, mỗi mốc ≤ 15 phút)


| Mốc | Ai bắt buộc | Nội dung                                                             |
| --- | ----------- | -------------------------------------------------------------------- |
| H1  | A + B (+ C) | Chốt Day 1 hay Day 2; 3 loại case bắt buộc                           |
| H2  | Cả nhóm     | Duyệt 15 case + tiêu chí đạt                                         |
| H3  | B + C + D   | Đọc run-01; quyết định sửa 1 vòng hay chấp nhận số gốc; D quay video |


---



## 6. Định nghĩa “xong CP3”

- [ ] AI thật chạy trên prototype (không chỉ mock HTML CP2).  
- [ ] Golden set 15 case neo `vlearn-pack` (không còn corpus “Biến” giả).  
- [ ] `run-01` đủ: n, đạt, %, nhóm lỗi (kể cả lỗi kỹ thuật).  
- [ ] Live + video 30s có số.  
- [ ] Phần giả lập ghi **MOCK**.  
- [ ] Không commit nguyên data pack.

---



## 7. Lệnh nhanh (người C / B)

```bash
cp .env.example .env          # điền key
python3 prototype/run_eval.py # → eval/runs/run-01.md
python3 prototype/server.py   # → http://127.0.0.1:8777
```

Chi tiết kỹ thuật thêm: `eval/CP3.md`.

---



## 8. Sau CP3 (nhắc một dòng — không phân công ở file này)

CP4: điền `spec.md`, **khóa** “Đạt khi ≥ X%” từ số run-01. Không hạ ngưỡng sau khi nộp.
