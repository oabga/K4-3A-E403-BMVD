# CP2 — Nộp mock / sơ đồ luồng

Nộp: **mock bấm được** (AI chưa cần chạy thật) hoặc sơ đồ từ đầu đến cuối.

File: `mock/cp2.html` — mở bằng trình duyệt (`file://` hoặc Live Server). Có cả hai:

1. **Mock trang bài** — slide mỏng + ô hỏi, 4 gợi ý bấm được  
2. **Sơ đồ luồng** — nút trên header

## Demo 4 nhánh (bấm lần lượt)

| Gợi ý | Nhãn |
|---|---|
| Biến là gì? | `IN_CORPUS` |
| So sánh biến/hằng + ví dụ ngoài slide | `NEED_EXTERNAL` (Fetch TẮT = brief; BẬT = tổng hợp ngoài lớp, mô phỏng) |
| Đòi DOI IEEE | `CANNOT_FETCH` |
| Viết hộ bài tập | Ngoài phạm vi |
| Nút “Không đúng với slide” sau câu IN | Correction: đổi sang NEED_EXTERNAL |

Không gọi mạng. Nguồn ngoài trên mock ghi rõ là mô phỏng — không bịa DOI.

Evidence mining (`data/`, form) **không phải file nộp CP2**; để dành cho spec CP4.
