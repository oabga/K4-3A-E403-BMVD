# Đề tài đề xuất — Hướng A · VLearn · học viên tự ôn từ slide bài

Hỏi đáp trên trang bài **đã bám slide, không trả lời ngoài bài** → lát cắt “cấm kiến thức ngoài khi chat” **trùng việc đã có, loại**.

Đổi job: sau buổi học, học viên cần **câu hỏi ôn đúng slide vừa học** — khác chat (chat giải thích khi kẹt; ôn là tự kiểm tra hiểu).

## Lát cắt mới (ưu tiên)

**Tên:** Tự luyện câu hỏi ôn từ đúng slide bài vừa học

**Loại (tạm):** tính năng mới — đổi “tối ưu” nếu trang bài đã có tạo quiz/luyện tập từ slide nhưng câu generic / lệch / không chỉ về slide.

**Một câu:** Học viên vừa học xong một bài trên VLearn, cần biết mình hiểu chỗ nào; hệ thống **chỉ được soạn câu hỏi từ slide/tài liệu bài đó**; mỗi câu gắn vị trí slide; không đủ nội dung trên slide thì **không bịa câu**.

| Thành phần | Giá trị |
|---|---|
| 1 user | Học viên |
| 1 việc | Sau buổi học, tự ôn đúng bài vừa học |
| 1 quyết định AI | Câu nào được ra, có nằm trong slide không; không chắc thì bỏ câu đó |
| 1 kết quả | Bộ câu ôn ngắn + đáp án/gợi ý trỏ về slide, không dùng kiến thức ngoài |

**JTBD:** Khi vừa học xong một buổi, tôi muốn có câu hỏi ôn đúng tài liệu vừa học, để biết chỗ nào chưa hiểu chứ không phải đoán đề hoặc ôn lệch bài.

**Problem:** Sau buổi học thường không có đề ôn bám slide, hoặc đề generic; học viên đọc lại slide, hỏi nguồn ngoài, hoặc không luyện — không biết mình đã hiểu bài đó chưa.

**Quy tắc căn cứ:** câu hỏi, đáp án, giải thích **chỉ lấy từ slide/tài liệu bài đang ôn**. Không ra câu “kiến thức liên quan” nếu slide không có. Chat hỏi đáp sẵn có **không đụng**.

**Không làm:** chatbot mới; hỏi đáp (đã có); làm hộ assignment; đề thi cả môn; kiến thức ngoài slide.

## Hai ứng viên để loại (vẫn hỏi form)

1. ~~Tối ưu chat: không trả lời ngoài slide~~ — **dự kiến loại:** VLearn đã làm. Form hỏi ngắn để có số “không còn đau”.
2. (ưu tiên) Tự ôn bằng câu hỏi từ đúng slide bài vừa học
3. Lúc làm assignment, tìm đoạn slide liên quan đề bài

## Việc tối nay

Gửi form `khao-sat.md` cho lớp (≥15–20 HV). Mai: nếu % việc 2 thấp, xét việc 3; việc 1 (chat) chỉ để ghi vào bảng “đã loại”.
