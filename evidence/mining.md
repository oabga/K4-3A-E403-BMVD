# Mining chuẩn A — Log trong `data/vlearn-pack`

Nguồn: `data/vlearn-pack/chatlog/tutor_turns.csv` (+ số tổng hợp đã công bố trong `data/vlearn-pack/README.md`).  
**Không** dùng bảng “gán nhãn thủ công n=200 → 39% NEED_EXTERNAL” — bản đó không có file nhãn kèm theo và **không tái lập được** trên CSV.

---

## 1. Quy mô & bộ lọc

| Chỉ số | Giá trị | Ghi chú |
|---|---|---|
| Tổng lượt | **13.494** | HV × AI tutor |
| `is_preset = True` | **3.067 (22,7%)** | Câu mẫu bấm sẵn UI — tách khi nói về hành vi tự hỏi |
| `is_preset = False` | **10.427** | Câu tự gửi (có thể kèm đoạn bôi đen) |

---

## 2. Pain đo được trên **toàn tập** (không cần mẫu 200)

Các số này khớp pack README / cột CSV:

| Tín hiệu | Số | Ý nghĩa cho VLearn Extend |
|---|---|---|
| `has_citation = False` | **3.781 / 13.494 (28,0%)** | Tutor trả lời không trích dẫn — khó đối chiếu với bài |
| `move_used = ask_probing_question` | **28 / 13.494 (~0,2%)** | Gần như không hỏi lại khi câu mơ hồ |
| `move_used = review_concept` | **12.127 / 13.494 (~90%)** | Đa số là giảng lại khái niệm, kể cả khi thiếu căn cứ trang |

---

## 3. Heuristic trên câu tự gửi (`is_preset = False`, n = 10.427)

Đây là **lọc từ khóa**, không phải gán nhãn vàng 4 lớp trên 200 dòng. Dùng để chứng minh pain **có mặt trong log**, không để claim “39% NEED_EXTERNAL”.

| Nhóm heuristic | Pattern (tóm tắt) | Số lượt | ~% trên free-text |
|---|---|---|---|
| Đào sâu / so sánh / ví dụ thực tế / paper | `chi tiết hơn\|sâu hơn\|ví dụ thực tế\|paper\|DOI\|scholar\|khác gì\|…` | **186** | **~1,8%** |
| Trong đó nhắc paper / DOI / scholar / bài báo | `paper\|DOI\|scholar\|bài báo` | **8** | hiếm nhưng rõ nhu cầu ngoài slide |
| Tutor báo không tìm thấy / không có trong tài liệu | `không tìm thấy\|không có trong slide\|…` trên `tutor_reply` | **666** toàn tập · **595** khi câu HV free-text | **~4,9%** toàn tập · **~5,7%** free |

**Đọc số đúng:** phần lớn chatlog vẫn là hỏi–giải thích **trên trang/slide**. Pain “cần nguồn ngoài có điều kiện” **không** phải đa số tuyệt đối; nó hiện ở (a) xin đào sâu/ví dụ/paper, (b) tutor **không retrieve được trang**, (c) **28% không citation**, (d) gần như **không ASK_AGAIN**.

---

## 4. Tiêu chí nhãn dùng cho prototype / golden (thiết kế)

| Nhãn | Khi nào dùng (spec / eval) |
|---|---|
| `IN_CORPUS` | Excerpt lớp đủ → trả lời + `D1-Pxx` |
| `NEED_EXTERNAL` | Corpus mỏng / xin ví dụ–paper–thực tế ngoài bài → không giả vờ trong slide |
| `CANNOT_FETCH` | Policy cấm fetch / fail sau retry → nói thẳng, không bịa DOI |
| `ASK_AGAIN` | Câu cộc / không chỉ khái niệm |
| `OUT_OF_SCOPE` | Làm hộ bài nộp, ngoài môn |

---

## 5. Quote nguyên văn

≥5 câu đã verify `turn_id`: [`quotes.md`](quotes.md).
