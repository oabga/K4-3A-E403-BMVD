# Lượt đầu CP3 · run-01

- Thời điểm (UTC): `2026-09-17T07:46:00.790983+00:00`
- Model (AI thật): `openai:gpt-4o-mini`
- Prompt: `eval/prompt.md` (giữ nguyên cả bộ)
- Fetch / retry: **MOCK**
- Mẫu: **15** · Đạt: **14** · **93.3%**
- Lỗi theo hậu quả: Sai nguồn 1 · Không hỏi lại 0 · Lỗi kỹ thuật 0
- Quality bar chính thức: chưa khóa (CP4)

| Mã | Mức | Kỳ vọng | Thực tế | Đạt | Nhóm lỗi | Lý do |
|---|---|---|---|---|---|---|
| GS-01 | thuong | IN_CORPUS | IN_CORPUS | đạt |  |  |
| GS-02 | thuong | IN_CORPUS | IN_CORPUS | đạt |  |  |
| GS-03 | thuong | IN_CORPUS | IN_CORPUS | đạt |  |  |
| GS-04 | thuong | IN_CORPUS | IN_CORPUS | đạt |  |  |
| GS-05 | thuong | IN_CORPUS | IN_CORPUS | đạt |  |  |
| GS-06 | thuong | NEED_EXTERNAL | NEED_EXTERNAL | đạt |  |  |
| GS-07 | thuong | NEED_EXTERNAL | IN_CORPUS | không | Sai nguồn | nhãn IN_CORPUS ≠ NEED_EXTERNAL; label=NEED_EXTERNAL; thiếu MOCK-EXT |
| GS-08 | kho | NEED_EXTERNAL | NEED_EXTERNAL | đạt |  |  |
| GS-09 | thuong | CANNOT_FETCH | CANNOT_FETCH | đạt |  |  |
| GS-10 | thuong | CANNOT_FETCH | CANNOT_FETCH | đạt |  |  |
| GS-11 | kho | CANNOT_FETCH | CANNOT_FETCH | đạt |  |  |
| GS-12 | thuong | ASK_AGAIN | ASK_AGAIN | đạt |  |  |
| GS-13 | kho | ASK_AGAIN | ASK_AGAIN | đạt |  |  |
| GS-14 | thuong | OUT_OF_SCOPE | OUT_OF_SCOPE | đạt |  |  |
| GS-15 | kho | OUT_OF_SCOPE | OUT_OF_SCOPE | đạt |  |  |

## Case không đạt (mở lại)

### GS-07 · Sai nguồn
- Lý do: nhãn IN_CORPUS ≠ NEED_EXTERNAL; label=NEED_EXTERNAL; thiếu MOCK-EXT
- Trích đầu ra: 'Trong thực tế triển khai chatbot doanh nghiệp, ngoài việc cắt ngắn context, có thể áp dụng các biện pháp như quản lý context gọn gàng và chất lượng để tránh hiện tượng Context Rot. Việc này giúp mô hình tập trung hơn và duy trì độ chính xác cao hơn khi xử lý thông tin [D1-P10].'
