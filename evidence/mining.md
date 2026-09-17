# Mining chuẩn A — Log trong `data/`

Canvas CP1 & Đề tài VLearn Extend: Phân tích dữ liệu thực tế từ `data/vlearn-pack/chatlog/tutor_turns.csv` và `DATA_DICTIONARY.md`.

---

## 1. Phương pháp phân loại & đếm

* **Tổng tập dữ liệu nguồn:** 13.494 lượt hỏi-đáp thật giữa học viên và AI tutor trên nền tảng VLearn.
* **Bộ lọc trước khi đếm:** Lọc bỏ 22,7% câu hỏi mẫu bấm sẵn của giao diện (`is_preset = True`, 3.067 lượt) để phản ánh đúng hành vi hỏi thật của người học.
* **Quy mô mẫu phân tích sâu:** Rút ngẫu nhiên $n_{log} = 200$ lượt hỏi-đáp thật (`is_preset = False`) để gán nhãn thủ công theo 4 nhóm.

---

## 2. Tiêu chí gắn nhãn

| Nhãn | Tiêu chí nhận diện khi đếm | Ý nghĩa thực tế |
|---|---|---|
| `IN_CORPUS` | Slide và transcript bài học đã có đủ thông tin để trả lời; có mốc trang hoặc dòng cụ thể để trích dẫn. | Học viên ôn lại bài đúng trọng tâm slide. |
| `NEED_EXTERNAL` | Slide chỉ có bullet ngắn, học viên hỏi xin: "ví dụ thực tế hơn", "định nghĩa đầy đủ toán học", "khác gì với công cụ X", "áp dụng thực tế ra sao", "đọc thêm ở đâu". | **Xác nhận nỗi đau cốt lõi của đề tài:** Tài liệu mỏng, học viên có nhu cầu hiểu sâu/rộng hơn. |
| `OUT_OF_SCOPE` | Nhờ giải hộ bài tập tuần để nộp bài, hỏi bài tập môn khác, hoặc thử prompt injection ("SYSTEM_OVERRIDE"). | Đòi hỏi vượt thẩm quyền của AI tutor. |
| `CANNOT_JUDGE` | Câu hỏi quá ngắn, cộc lốc ("giải thích cái này", "hả?"), không kèm đoạn chọn cụ thể. | Cần cơ chế hỏi lại (`ASK_AGAIN`). |

---

## 3. Bảng số liệu thực nghiệm sau khi đếm ($n_{log} = 200$)

* **Tổng số câu hỏi đã phân tích (`n_log`):** **200**
* **`IN_CORPUS`:** **88 câu (44.0%)** — Kiến thức có sẵn trong tài liệu.
* **`NEED_EXTERNAL`:** **78 câu (39.0%)** — **Tỷ lệ xác nhận Pain Point cho tính năng VLearn Extend.** Học viên khao khát nguồn mở rộng đáng tin cậy.
* **`OUT_OF_SCOPE`:** **22 câu (11.0%)** — Cần cơ chế từ chối lịch sự và an toàn.
* **`CANNOT_JUDGE` / `ASK_AGAIN`:** **12 câu (6.0%)** — Cần AI chủ động hỏi lại để thu hẹp phạm vi.

---

## 4. Các khiếm khuyết hệ thống đo được từ toàn bộ 13.494 lượt chatlog

1. **28.0% (3.781 lượt) câu trả lời của AI tutor không hề có trích dẫn nguồn (`has_citation = False`):** Dẫn đến tình trạng học viên không biết thông tin AI nói lấy từ đâu, dễ bị ảo giác hoặc lệch bài.
2. **AI Tutor gần như không có phản xạ hỏi lại (Socratic method):** Nước đi `ask_probing_question` chỉ xuất hiện **28 lượt / 13.494 lượt** (chưa đầy 0,2%). Khi gặp câu hỏi mơ hồ, tutor vẫn cố đoán và xổ một tràng lý thuyết dài 90% là `review_concept` (12.127 lượt).
3. **Mức độ tương tác đánh giá rất thấp:** Chỉ **1,3% lượt (177 lượt)** có rating; `understanding_level` gần như rỗng (20 lượt), chứng tỏ học viên chưa hài lòng hoặc bỏ qua phản hồi.

---

## 5. Dẫn chứng nguyên văn
Đã trích xuất 6 câu hỏi nguyên văn điển hình từ log và form khảo sát lưu tại [`evidence/quotes.md`](quotes.md).
