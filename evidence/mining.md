# Mining chuẩn A — log trong `data/`

Canvas CP1: chỉ mining nguồn **được phép**. Không nhét paper/docs ngoài vào `data/`. Không bịa URL/DOI.

## Cần có trong repo

- `data/slides/` hoặc file slide/transcript buổi học (local, được phép)
- `data/logs/` hỏi–đáp trên trang bài (nếu có export)
- File này cập nhật số sau khi đếm

## Cách đếm (mỗi câu hỏi của HV)

Gắn **một** nhãn:

| Nhãn | Khi nào |
|---|---|
| `IN_CORPUS` | Slide/transcript đã đủ trả lời, có chỗ trích |
| `NEED_EXTERNAL` | Thiếu định nghĩa / ví dụ / phạm vi; muốn hiểu rộng-sâu hơn slide |
| `OUT_OF_SCOPE` | Làm hộ bài, hỏi môn khác, không nhằm hiểu slide |
| `CANNOT_JUDGE` | Log không đủ để phân loại |

## Bảng (điền sau khi đếm)

- Tổng câu hỏi đã gắn nhãn (`n_log`):
- `IN_CORPUS`: số · %
- `NEED_EXTERNAL`: số · %  ← đây là **% xác nhận pain** cho spec
- `OUT_OF_SCOPE`: số · %
- ≥5 câu hỏi nguyên văn loại `NEED_EXTERNAL` + nguồn file log → copy sang `quotes.md`

Câu mẫu `NEED_EXTERNAL` (để nhận ra khi đếm): “ví dụ thực tế hơn”, “định nghĩa đầy đủ”, “khác gì với…”, “áp dụng ngoài bài”, “đọc thêm ở đâu” — trong khi slide chỉ có bullet ngắn.
