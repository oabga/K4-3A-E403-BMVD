# Tổng hợp — Sau khai phá Mining & Khảo sát Form

---

## 1. Kết quả Mining Chatlog (`evidence/mining.md`)

* **Quy mô mẫu phân tích (`n_log`):** **200** lượt hỏi-đáp thật (đã loại bỏ 22,7% câu hỏi mẫu).
* **% `NEED_EXTERNAL` (Nhu cầu mở rộng nguồn ngoài):** **39.0%** (78/200) — **Con số chứng minh Pain point chính của đề tài.**
* **% `IN_CORPUS` (Đã có trong tài liệu slide):** **44.0%** (88/200).
* **% `OUT_OF_SCOPE` (Ngoài phạm vi / làm hộ bài):** **11.0%** (22/200).
* **% `CANNOT_JUDGE` (Mơ hồ / cần hỏi lại):** **6.0%** (12/200).
* **Tỷ lệ trả lời không nguồn của AI Tutor hiện tại:** **28.0%** (3.781/13.494 lượt).

---

## 2. Kết quả Khảo sát Học viên (`evidence/khao-sat.md`)

* **Quy mô mẫu khảo sát (`n`):** **24** học viên khóa 4 đang học VLearn/LMS.
* **Tỷ lệ xác nhận nhu cầu VLearn Extend (Câu 7):** **83.3% (20/24)** học viên đồng ý rằng: *"Khi tài liệu buổi học chưa đủ để hiểu sâu nội dung trên slide, tôi muốn được chỉ nguồn bổ sung đáng tin và phân biệt rõ đâu là trong bài, đâu là ngoài bài"*.
* **Tần suất phải tự ra ngoài tìm kiếm (Câu 4):** **70.8%** học viên phải tự tìm kiếm Google/Scholar/YouTube từ 1–2 lần/tuần đến hầu hết các buổi học.
* **Thời gian tiêu tốn mỗi lần tự tìm ngoài (Câu 5):** Trung bình **15–30 phút/lần**; hơn 40% cảm thấy bối rối vì không biết nguồn nào đáng tin cậy để đối chiếu với bài học.
* **Trải nghiệm với AI tutor hiện tại (Câu 6):** 62.5% cho biết khi hỏi câu rộng/sâu hơn slide thì tutor hoặc từ chối hoặc trả lời chung chung không có nguồn kiểm chứng.

---

## 3. Quyết định lựa chọn giải pháp & Impact

* **CHỌN: VLearn Extend**
  * Tự động kiểm tra tài liệu bài giảng trước (`IN_CORPUS`).
  * Chỉ mở rộng nguồn ngoài có điều kiện kèm trích dẫn đối chiếu khi tài liệu mỏng (`NEED_EXTERNAL`).
  * Cảnh báo rõ ràng và đưa checklist tự tìm khi không lấy được web/DOI (`CANNOT_FETCH`), tuyệt đối không bịa.
  * Từ chối các yêu cầu giải hộ bài tập (`OUT_OF_SCOPE`).
* **ỨNG VIÊN BỊ LOẠI 1 — "Chỉ trả lời đóng khung trong slide":** VLearn hiện tại đã làm việc này nhưng tạo ra nỗi đau lớn: học viên vẫn phải rời khỏi nền tảng tự tìm ngoài mất 20–30 phút.
* **ỨNG VIÊN BỊ LOẠI 2 — "Tự động làm hộ bài tập từ web":** Chi phí sai lệch kiến thức và vi phạm liêm chính học thuật quá cao (Cost-of-error cực lớn).
* **Phân loại Spec:** [x] Tính năng mới trên nền tảng VLearn Tutor (`spec.md`).
