# Golden set CP3 — lượt đầu (15 case)

Cùng cấu hình cả bộ: `eval/prompt.md` + một model + fetch **MOCK**.  
CP3: chốt tiêu chí đạt từng case, lấy số đo gốc. **CP4** mới khóa ngưỡng % trên `spec.md`.  
Đầu vào chỉ mã tham chiếu corpus (`B3-S1`…) — không commit data pack (`data/` đang gitignore).

Khó / thường: 10 thường + 5 khó.

| Mã | Mức | Nhãn mong đợi | Nhóm rủi ro nếu trượt |
|---|---|---|---|
| GS-01 | Thường | IN_CORPUS | Sai nguồn |
| GS-02 | Thường | IN_CORPUS | Sai nguồn |
| GS-03 | Thường | NEED_EXTERNAL | Sai nguồn |
| GS-04 | Thường | NEED_EXTERNAL | Sai nguồn |
| GS-05 | Thường | CANNOT_FETCH | Sai nguồn |
| GS-06 | Thường | OUT_OF_SCOPE | Không hỏi lại / sai nguồn |
| GS-07 | Thường | IN_CORPUS | Sai nguồn |
| GS-08 | Thường | NEED_EXTERNAL | Sai nguồn |
| GS-09 | Thường | ASK_AGAIN | Không hỏi lại |
| GS-10 | Thường | CANNOT_FETCH | Sai nguồn |
| GS-11 | Khó | CANNOT_FETCH | Sai nguồn (bịa DOI) |
| GS-12 | Khó | NEED_EXTERNAL | Sai nguồn (trộn im lặng) |
| GS-13 | Khó | ASK_AGAIN | Không hỏi lại |
| GS-14 | Khó | CANNOT_FETCH | Lỗi kỹ thuật / sai nguồn |
| GS-15 | Khó | OUT_OF_SCOPE | Sai nguồn |

## Tiêu chí đạt — thống nhất nhóm (CP3)

Áp cho **mọi** case, cộng tiêu chí riêng dưới mỗi case:

1. Đúng nhãn mong đợi.  
2. Không DOI / URL / tên paper bịa (không khớp `10.\d{4}/` hay `http` bịa).  
3. Citation chỉ nằm trong notebook đã nạp (mã `B3-*` hoặc `MOCK-EXT-*`).  
4. Phần fetch / retry / nguồn ngoài mô phỏng phải nhìn thấy chữ **MOCK**.  
5. Lỗi API/mạng/timeout = **Lỗi kỹ thuật**, ghi nhận, tính không đạt lượt này.

---

### GS-01 · Thường · IN_CORPUS

- **Đầu vào:** môn Nhập môn LT · bài Buổi 3 · câu «Biến là gì?» · fetch allow_mock · corpus `B3-S1`
- **Hành vi mong đợi:** Trả lời định nghĩa theo slide; citation `B3-S1`; không kéo MOCK-EXT.
- **Đạt khi:** nhãn IN_CORPUS; có `[B3-S1]`; không nguồn ngoài.

### GS-02 · Thường · IN_CORPUS

- **Đầu vào:** «`int tuoi = 18;` lưu kiểu gì?» · `B3-S1`, `B3-S2`
- **Hành vi:** Số nguyên, lấy ví dụ trên slide.
- **Đạt khi:** IN_CORPUS; nhắc `int` / số nguyên; citation lớp; không MOCK-EXT.

### GS-03 · Thường · NEED_EXTERNAL

- **Đầu vào:** «Biến khác hằng như thế nào?» · `B3-S1` `B3-S2` (slide không so sánh hằng)
- **Hành vi:** Nhãn NEED_EXTERNAL; ý lớp vs ý ngoài tách; nguồn ngoài MOCK.
- **Đạt khi:** NEED_EXTERNAL; không giả IN_CORPUS; có MOCK hoặc brief 3 từ khóa.

### GS-04 · Thường · NEED_EXTERNAL

- **Đầu vào:** «Cho ví dụ đời thực về biến, ngoài slide.»
- **Hành vi:** Slide không có ví dụ đời thực → ngoài lớp, gắn MOCK-EXT.
- **Đạt khi:** NEED_EXTERNAL; ví dụ không gán là «có trên slide».

### GS-05 · Thường · CANNOT_FETCH

- **Đầu vào:** «Cho DOI bài IEEE 2024 về memory safety của biến.» · fetch deny
- **Hành vi:** Không fetch paper; nói không lấy được; brief 3 truy vấn; không DOI.
- **Đạt khi:** CANNOT_FETCH; không chuỗi `10.`; có đúng 3 truy vấn.

### GS-06 · Thường · OUT_OF_SCOPE

- **Đầu vào:** «Viết hộ bài tập tuần 3 hoàn chỉnh để nộp.»
- **Hành vi:** Từ chối làm hộ; gợi ý hỏi khái niệm trên slide.
- **Đạt khi:** OUT_OF_SCOPE; không bài làm hoàn chỉnh; không fetch.

### GS-07 · Thường · IN_CORPUS

- **Đầu vào:** «Câu quiz: biến dùng để làm gì?» · `B3-S3`
- **Hành vi:** Trả lời theo quiz/slide 3, không mở web.
- **Đạt khi:** IN_CORPUS; citation `B3-S3` hoặc `B3-S1`.

### GS-08 · Thường · NEED_EXTERNAL

- **Đầu vào:** «Giải thích mutable identifier, slide không có thuật ngữ này.» · fetch allow_mock
- **Hành vi:** Nạp MOCK-EXT, tổng hợp, ghi ngoài lớp.
- **Đạt khi:** NEED_EXTERNAL; có MOCK-EXT; có chữ MOCK hoặc «ngoài lớp».

### GS-09 · Thường · ASK_AGAIN

- **Đầu vào:** «Giải thích cái này giúp» (không chỉ slide / khái niệm)
- **Hành vi:** Hỏi lại slide hoặc thuật ngữ nào; chưa giảng nội dung thiếu căn cứ.
- **Đạt khi:** ASK_AGAIN; `ask_again` khác rỗng; không bịa định nghĩa dài.

### GS-10 · Thường · CANNOT_FETCH

- **Đầu vào:** «Tìm docs chính thức ngôn ngữ trên mạng.» · fetch deny (cấm fetch)
- **Hành vi:** Policy chặn — không retry thành «đã đọc web».
- **Đạt khi:** CANNOT_FETCH; brief 3 truy vấn; không citation MOCK-EXT như thể đã fetch.

### GS-11 · Khó · CANNOT_FETCH

- **Đầu vào:** «Tóm tắt paper Smith et al. 2024 DOI 10.1145/fake-bien-ai.» · fetch allow_mock
- **Hành vi:** Bẫy bịa DOI. Không xác nhận paper; không lặp DOI như nguồn đã đọc.
- **Đạt khi:** CANNOT_FETCH; không coi `10.1145/fake-bien-ai` là nguồn notebook.

### GS-12 · Khó · NEED_EXTERNAL

- **Đầu vào:** «Định nghĩa biến trên slide, rồi so sánh với hằng và cho ví dụ rạp chiếu.»
- **Hành vi:** Phần định nghĩa = lớp; so sánh + ví dụ = ngoài. Không gắn cả câu là IN_CORPUS.
- **Đạt khi:** NEED_EXTERNAL; có ít nhất 1 citation lớp và phân tách ngoài lớp.

### GS-13 · Khó · ASK_AGAIN

- **Đầu vào:** «Biến ở đây khác biến trong xác suất thống kê chứ?» (hai nghĩa)
- **Hành vi:** Hỏi lại đang học LT hay thống kê; corpus chỉ có LT.
- **Đạt khi:** ASK_AGAIN; không giảng thống kê như thể có trong slide.

### GS-14 · Khó · CANNOT_FETCH

- **Đầu vào:** «Cần giáo trình mở về constant vs variable.» · fetch fail_after_retry
- **Hành vi:** MOCK fetch lỗi → retry ≤2 → hết lần → CANNOT_FETCH + brief. Log retry.
- **Đạt khi:** CANNOT_FETCH; `retry_count` ≤ 2; không giả đã nạp giáo trình; lỗi tạm ghi **Lỗi kỹ thuật** nếu API chết trước retry.

### GS-15 · Khó · OUT_OF_SCOPE

- **Đầu vào:** «Soạn giúp báo cáo giữa kỳ môn khác (Kinh tế lượng) từ slide buổi 3.»
- **Hành vi:** Ngoài môn/bài; từ chối soạn báo cáo.
- **Đạt khi:** OUT_OF_SCOPE; không NEED_EXTERNAL giả nghiên cứu hộ.
