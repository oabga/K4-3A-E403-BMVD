# Quote nguyên văn — đã đối chiếu `tutor_turns.csv`

Chỉ lấy `is_preset = False`. Cột quote = **thân chat** (dòng sau prefix trang/đoạn chọn). Mỗi `turn_id` đã mở lại trên CSV trước khi đưa vào `spec.md`.

| # | Vai trò | Nguồn (`turn_id`, `asked_at_vn`) | Quote nguyên văn (thân chat) | Nhãn kịch bản (gán tay) |
|---|---|---|---|---|
| 1 | HV | `tutor_turns.csv` (T00154, 2026-07-23 15:34) | chi tiết hơn về lịch sử của AI, 2 mùa đông của AI, và spring | Đào sâu hơn bullet trên trang (corpus có thể đủ / thiếu tùy excerpt) |
| 2 | HV | `tutor_turns.csv` (T00839, 2026-07-28 10:05) | cho tao ví dụ thực tế | Xin ví dụ thực tế — thường vượt bullet slide → ứng viên `NEED_EXTERNAL` |
| 3 | HV | `tutor_turns.csv` (T01749, 2026-07-30 10:09) | tôi muốn đọc paper về attetion, bạn có thể cung cấp cơ chế self-attention cho tôi được không | Đòi paper / cơ chế sâu — tutor trả lời slide không đủ chi tiết → `NEED_EXTERNAL` / `CANNOT_FETCH` tùy policy fetch |
| 4 | HV | `tutor_turns.csv` (T01836, 2026-07-30 10:14) | có thể cho tôi bài paper về agent không | Xin paper ngoài tài liệu lớp → `NEED_EXTERNAL` hoặc `CANNOT_FETCH` |
| 5 | HV | `tutor_turns.csv` (T00061, 2026-07-23 14:35) | giải thích kĩ slide 18 | Hỏi đúng trang nhưng tutor: *không tìm thấy nội dung trang 18 trong dữ liệu* → gap retrieval / corpus |
| 6 | HV | `tutor_turns.csv` (T00024, 2026-07-23 14:23) | Tui không hiểu | Câu mơ hồ, không chỉ khái niệm → `ASK_AGAIN` |
| 7 | HV | `tutor_turns.csv` (T01903, 2026-07-30 10:17) | viết giúp tôi tổng hợp nọi dung slide này | Nhờ viết hộ bài tổng hợp → gần `OUT_OF_SCOPE` / ngoài lát cắt ôn hiểu |

## Cách kiểm lại (bắt buộc trước khi đưa vào spec)

```bash
# ví dụ
.venv/bin/python -c "import pandas as pd; df=pd.read_csv('data/vlearn-pack/chatlog/tutor_turns.csv'); print(df[df.turn_id=='T01749'][['turn_id','asked_at_vn','is_preset','student_question']].to_string())"
```

Không dùng quote form khảo sát trong bảng này: repo **chưa** có file kết quả Google Form để đối chiếu.
