# Validation R6 — Kiểm thử người dùng ngoài nhóm

Nhóm BMVD · VLearn Extend · Prototype `codebase/server.py`  
Willing users (đã ghi trong `spec.md` / `TEAMMATES.md`):

| # | Họ tên | MSSV | Ngày | Hình thức |
|---|---|---|---|---|
| 1 | Trí | 2A202602730 | 2026-09-18 | Live prototype local (http://127.0.0.1:8777) |
| 2 | Trí | 2A202602603 | 2026-09-18 | Live prototype local |

Kịch bản 4 nhánh: IN (có trên slide) · NEED (liên quan nhưng slide thiếu → chọn nguồn MOCK + Nhập) · CANNOT (DOI / cấm fetch) · SCOPE (lệch môn hoặc làm hộ).

## Nhật ký & quote nguyên văn

### User 1 — Trí (2A202602730)

- **IN:** Hỏi khác nhau AI/ML/DL theo Day 1 → thấy nhãn `IN_CORPUS`, có citation `D1-P*`.
- **NEED:** Hỏi lịch sử LLM / ai tạo hướng mô hình → cột trái hiện nguồn MOCK, chọn rồi Nhập mới ra câu trả lời.
- **Quote:** "Cái chỗ chọn nguồn rồi mới trả lời dễ hiểu hơn là AI tự bịa; mình biết đâu là ngoài slide."
- **Lệch môn:** Hỏi công thức PT bậc 2 → bị từ chối ngoài phạm vi buổi học (đúng kỳ vọng).

### User 2 — Trí (2A202602603)

- **CANNOT:** Đòi DOI paper → hệ thống không bịa DOI, đưa brief tìm.
- **SCOPE:** Nhờ viết hộ lab → từ chối làm hộ.
- **Quote:** "Mình hay hỏi thêm lịch sử / người tạo ra khái niệm trên slide; kiểu này hợp hơn Google lung tung."
- **Góp ý:** Muốn nút “không đúng với slide” để sửa nhánh IN → NEED (đã ghi non-goal / backlog HAX 8 trên spec).

## Kết luận vòng R6

- Hai HV ngoài nhóm chạy được 4 nhánh; hiểu badge **AI THẬT** vs **MOCK**.
- Không sửa quality bar (đã khóa 14/15 = 93,3% từ run-01) theo góp ý validation.
- Việc tiếp: bổ sung `demo-slides.pdf` 6 trang; từng TV điền `reflection/`.
