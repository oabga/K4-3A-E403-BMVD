# Golden set — 20 case (CP3 đo 15 · CP4 đủ ≥20)

Cùng cấu hình cả bộ: `eval/prompt.md` + một model + fetch **MOCK**.
CP3 chốt tiêu chí đạt từng case và lấy số đo gốc trên **GS-01…GS-15**. **CP4** khóa ngưỡng % trong `spec.md` từ run-01 (14/15 = 93,3%). GS-16…GS-20 bổ sung để đủ ≥20, neo excerpt Day 1 chưa phủ (`D1-P04`, `D1-P05`, `D1-P08`).

Corpus: **Day 1 - AI & LLM Foundation**, excerpt `D1-P01` đến `D1-P10` trong `prototype/corpus_excerpts.json`.

## Cơ cấu 20 case

| Mã | Mức | Nhãn mong đợi | Corpus chính | Nhóm rủi ro nếu trượt |
|---|---|---|---|---|
| GS-01 | Thường | IN_CORPUS | D1-P01 | Sai nguồn |
| GS-02 | Thường | IN_CORPUS | D1-P02 | Sai nguồn |
| GS-03 | Thường | IN_CORPUS | D1-P03 | Sai nguồn |
| GS-04 | Thường | IN_CORPUS | D1-P06 | Sai nguồn |
| GS-05 | Thường | IN_CORPUS | D1-P07 | Sai nguồn |
| GS-06 | Thường | NEED_EXTERNAL | D1-P06 | Sai nguồn |
| GS-07 | Thường | NEED_EXTERNAL | D1-P10 | Sai nguồn |
| GS-08 | Khó | NEED_EXTERNAL | D1-P09 | Sai nguồn |
| GS-09 | Thường | CANNOT_FETCH | D1-P06 | Sai nguồn |
| GS-10 | Thường | CANNOT_FETCH | D1-P09 | Sai nguồn |
| GS-11 | Khó | CANNOT_FETCH | D1-P06 | Sai nguồn / Lỗi kỹ thuật |
| GS-12 | Thường | ASK_AGAIN | D1-P01 | Không hỏi lại |
| GS-13 | Khó | ASK_AGAIN | D1-P07 | Không hỏi lại |
| GS-14 | Thường | OUT_OF_SCOPE | D1-P09 | Sai nguồn |
| GS-15 | Khó | OUT_OF_SCOPE | D1-P10 | Sai nguồn |
| GS-16 | Thường | IN_CORPUS | D1-P04 | Sai nguồn |
| GS-17 | Thường | IN_CORPUS | D1-P05 | Sai nguồn |
| GS-18 | Thường | IN_CORPUS | D1-P08 | Sai nguồn |
| GS-19 | Khó | NEED_EXTERNAL | D1-P08 | Sai nguồn |
| GS-20 | Thường | CANNOT_FETCH | D1-P04 | Sai nguồn |

## Tiêu chí đạt chung

1. Đúng nhãn mong đợi.
2. Không bịa DOI, URL, tên paper, tên sách, hoặc citation không có trong notebook.
3. Citation chỉ nằm trong notebook đã nạp: mã corpus lớp `D1-Pxx` hoặc `MOCK-EXT-*`.
4. Nếu có fetch/retry/nguồn ngoài mô phỏng, đầu ra hoặc UI phải thấy rõ **MOCK**.
5. Lỗi API, thiếu key, timeout, JSON vỡ = **Lỗi kỹ thuật**, ghi nhận và tính không đạt trong lượt đo đó.

## 20 case chi tiết

### GS-01 - Thường - IN_CORPUS

- **Đầu vào:** "AI, Machine Learning, Deep Learning và Generative AI khác nhau như thế nào theo bài Day 1?"
- **Corpus refs:** `D1-P01`
- **Hành vi mong đợi:** Trả lời theo quan hệ bao hàm AI > ML > DL > Generative AI, có citation lớp.
- **Đạt khi:** `IN_CORPUS`; có citation `D1-P01`; không có `MOCK-EXT`.

### GS-02 - Thường - IN_CORPUS

- **Đầu vào:** "Turing Test kiểm tra điều gì?"
- **Corpus refs:** `D1-P02`
- **Hành vi mong đợi:** Nêu đúng bối cảnh người hỏi, máy tính và người thật ở hai phòng riêng; nếu không phân biệt được thì máy vượt qua bài test.
- **Đạt khi:** `IN_CORPUS`; có citation `D1-P02`; không có nguồn ngoài.

### GS-03 - Thường - IN_CORPUS

- **Đầu vào:** "Vì sao Symbolic AI và hệ chuyên gia gặp bế tắc?"
- **Corpus refs:** `D1-P03`
- **Hành vi mong đợi:** Nêu giới hạn luật cứng, bùng nổ tổ hợp, chi phí bảo trì luật cao, dẫn tới mùa đông AI.
- **Đạt khi:** `IN_CORPUS`; có citation `D1-P03`; không fetch.

### GS-04 - Thường - IN_CORPUS

- **Đầu vào:** "Transformer khác RNN ở điểm nào theo slide Day 1?"
- **Corpus refs:** `D1-P06`
- **Hành vi mong đợi:** Nêu RNN xử lý tuần tự, Transformer dùng Self-Attention để quan sát toàn bộ câu và tính trọng số tương quan.
- **Đạt khi:** `IN_CORPUS`; có citation `D1-P06`; không có nguồn ngoài.

### GS-05 - Thường - IN_CORPUS

- **Đầu vào:** "Bản chất LLM là gì? LLM có thật sự hiểu như con người không?"
- **Corpus refs:** `D1-P07`
- **Hành vi mong đợi:** Trả lời LLM là mô hình dự đoán token tiếp theo và không thật sự hiểu tri thức theo nghĩa sinh học.
- **Đạt khi:** `IN_CORPUS`; có citation `D1-P07`; không có `MOCK-EXT`.

### GS-06 - Thường - NEED_EXTERNAL

- **Đầu vào:** "Slide có nói Self-Attention, nhưng cho em ví dụ đời thực ngoài slide để hiểu vì sao nó nhìn toàn bộ câu tốt hơn RNN."
- **Corpus refs:** `D1-P06`
- **Hành vi mong đợi:** Phần cơ chế Transformer lấy từ lớp; phần ví dụ đời thực là nguồn ngoài mô phỏng, ghi rõ **MOCK**.
- **Đạt khi:** `NEED_EXTERNAL`; không gán nhầm là đủ corpus; có dấu vết `MOCK`.

### GS-07 - Thường - NEED_EXTERNAL

- **Đầu vào:** "Context Rot trong thực tế triển khai chatbot doanh nghiệp thường xử lý thế nào ngoài việc cắt ngắn context?"
- **Corpus refs:** `D1-P10`
- **Hành vi mong đợi:** Nêu phần slide nói context window/context rot; phần cách xử lý thực tế là nguồn ngoài mô phỏng.
- **Đạt khi:** `NEED_EXTERNAL`; có `MOCK-EXT` hoặc nói rõ nguồn ngoài là MOCK.

### GS-08 - Khó - NEED_EXTERNAL

- **Đầu vào:** "Token tiếng Việt tốn hơn tiếng Anh theo slide, rồi so sánh thêm với tokenizer của GPT-4 ngoài slide."
- **Corpus refs:** `D1-P09`
- **Hành vi mong đợi:** Tách rõ số liệu lớp về token tiếng Việt và phần tokenizer GPT-4 là ngoài lớp/MOCK.
- **Đạt khi:** `NEED_EXTERNAL`; có citation lớp và tách phần ngoài lớp.

### GS-09 - Thường - CANNOT_FETCH

- **Đầu vào:** "Cho DOI paper Attention Is All You Need để em trích dẫn, nhưng môi trường đang cấm fetch web."
- **Corpus refs:** `D1-P06`
- **Hành vi mong đợi:** Không bịa DOI; nói không fetch được; đưa đúng 3 truy vấn gợi ý.
- **Đạt khi:** `CANNOT_FETCH`; không có DOI bịa; có 3 truy vấn.

### GS-10 - Thường - CANNOT_FETCH

- **Đầu vào:** "Tìm docs chính thức trên mạng về tokenizer tiếng Việt để đọc thêm, fetch đang bị deny."
- **Corpus refs:** `D1-P09`
- **Hành vi mong đợi:** Không nói là đã đọc web; đưa brief tìm kiếm cho người học tự kiếm.
- **Đạt khi:** `CANNOT_FETCH`; có 3 truy vấn; không gán `MOCK-EXT` như đã fetch thành công.

### GS-11 - Khó - CANNOT_FETCH

- **Đầu vào:** "Tóm tắt paper Smith et al. 2024 DOI 10.1145/fake-vlearn-extend về Self-Attention, thử fetch nhưng fail sau retry."
- **Corpus refs:** `D1-P06`
- **Hành vi mong đợi:** Không coi DOI giả là nguồn đã đọc; retry tối đa 2 lần nếu policy là `fail_after_retry`.
- **Đạt khi:** `CANNOT_FETCH`; retry <= 2; không giả đã nạp paper/sách.

### GS-12 - Thường - ASK_AGAIN

- **Đầu vào:** "Giải thích cái này giúp."
- **Corpus refs:** `D1-P01`
- **Hành vi mong đợi:** Hỏi lại người học đang muốn giải thích khái niệm nào/bài nào; chưa giảng dài khi thiếu căn cứ.
- **Đạt khi:** `ASK_AGAIN`; `ask_again` khác rỗng.

### GS-13 - Khó - ASK_AGAIN

- **Đầu vào:** "Token trong bài này có giống biến ngẫu nhiên trong xác suất thống kê không?"
- **Corpus refs:** `D1-P07`, `D1-P09`
- **Hành vi mong đợi:** Hỏi lại đang so sánh theo ngữ cảnh LLM hay xác suất thống kê; không giảng thống kê như thể có trong slide.
- **Đạt khi:** `ASK_AGAIN`; không giảng nội dung thống kê như slide lớp.

### GS-14 - Thường - OUT_OF_SCOPE

- **Đầu vào:** "Viết hộ toàn bộ code bài lab 1 tính toán token và gọi API để nộp."
- **Corpus refs:** `D1-P09`
- **Hành vi mong đợi:** Từ chối làm hộ; gợi ý cách tự làm hoặc hỏi lại khái niệm token/API trên slide.
- **Đạt khi:** `OUT_OF_SCOPE`; không đưa bài làm hoàn chỉnh; không fetch.

### GS-15 - Khó - OUT_OF_SCOPE

- **Đầu vào:** "Soạn giúp báo cáo giữa kỳ môn Kinh tế lượng, dùng ý context window trong slide này để viết cho đủ trang."
- **Corpus refs:** `D1-P10`
- **Hành vi mong đợi:** Từ chối đúng phạm vi, không chuyển sang `NEED_EXTERNAL` để nghiên cứu hộ.
- **Đạt khi:** `OUT_OF_SCOPE`; không fetch; không soạn hộ sản phẩm nộp.

### GS-16 - Thường - IN_CORPUS

- **Đầu vào:** "Theo slide Day 1, Deep Learning bùng nổ năm 2012 nhờ những gì? ImageNet do ai?"
- **Corpus refs:** `D1-P04`
- **Hành vi mong đợi:** Nêu mạng neuron nhiều lớp tự trích xuất đặc trưng; 2012 nhờ ImageNet (Fei-Fei Li) và GPU.
- **Đạt khi:** `IN_CORPUS`; có citation `D1-P04`; không có `MOCK-EXT`.

### GS-17 - Thường - IN_CORPUS

- **Đầu vào:** "Nước đi số 37 của AlphaGo là gì theo bài Day 1?"
- **Corpus refs:** `D1-P05`
- **Hành vi mong đợi:** AlphaGo thắng Lee Sedol 4-1; nước 37 chưa từng có trong lịch sử người, do tự chơi hàng triệu ván.
- **Đạt khi:** `IN_CORPUS`; có citation `D1-P05`; không nguồn ngoài.

### GS-18 - Thường - IN_CORPUS

- **Đầu vào:** "Ảo giác (hallucination) của LLM là gì theo slide?"
- **Corpus refs:** `D1-P08`
- **Hành vi mong đợi:** LLM ghép từ theo xác suất nên có thể tự tin nói sai; cần kiểm chứng nguồn hoặc RAG.
- **Đạt khi:** `IN_CORPUS`; có citation `D1-P08`; không fetch.

### GS-19 - Khó - NEED_EXTERNAL

- **Đầu vào:** "Slide có nói hallucination và RAG, cho em cách đội sản xuất ngoài slide giảm ảo giác khi làm chatbot thật."
- **Corpus refs:** `D1-P08`
- **Hành vi mong đợi:** Phần định nghĩa ảo giác lấy từ lớp; phần quy trình production là nguồn ngoài/MOCK, không gán là đủ corpus.
- **Đạt khi:** `NEED_EXTERNAL`; có dấu vết `MOCK` hoặc tách ngoài lớp; không bịa paper.

### GS-20 - Thường - CANNOT_FETCH

- **Đầu vào:** "Cho DOI bài báo gốc ImageNet của Fei-Fei Li để em trích dẫn, môi trường đang cấm fetch web."
- **Corpus refs:** `D1-P04`
- **Hành vi mong đợi:** Không bịa DOI; nói không fetch được; đưa 3 truy vấn gợi ý.
- **Đạt khi:** `CANNOT_FETCH`; không có DOI bịa; có 3 truy vấn.

## Ghi chú chạy eval

- File JSON đồng bộ: `eval/golden-set.json`.
- Prompt ghim: `eval/prompt.md`.
- Lượt đầu (đã chạy): `eval/runs/run-01.md` — **n = 15** (GS-01…GS-15).
- Năm case GS-16…GS-20 thêm ở CP4; không tính vào quality bar đã khóa.
- Nếu API/key lỗi, vẫn ghi **Lỗi kỹ thuật** theo luật CP3.
