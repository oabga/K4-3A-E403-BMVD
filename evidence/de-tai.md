# Đề tài đã chốt — CP1 canvas · VLearn Extend

Nguồn: `canvas/canvas.jpg` (Mini Hackathon AI · Checkpoint 1 · Canvas K3).

VLearn **đã** trả lời theo slide và không lấy kiến thức ngoài. Đó đúng là **nỗi đau trên canvas**: slide đủ làm quiz nhưng mỏng — thiếu định nghĩa, ví dụ, hoặc corpus chỉ phủ một phần. Học viên muốn hiểu **rộng / sâu hơn nội dung slide** thì phải ra Google/Scholar; AI trong lớp không được lấy nguồn ngoài thật → trả lời chung, không citation.

**Không làm đề “cấm kiến thức ngoài”.** Đề này là **mở nguồn ngoài có điều kiện**.

## Lát cắt một câu

Học viên đang học theo slide/giáo trình/transcript trên VLearn, hỏi để hiểu thêm (rộng, sâu, hoặc ngoài slide); hệ thống **kiểm tra corpus trước**, rồi chọn đúng một nhãn: trả lời trong bài / cần nguồn ngoài / không lấy được — kèm citation hoặc brief tìm, **không bịa link/DOI**.

| Thành phần | Giá trị |
|---|---|
| 1 user | Học viên (sinh viên đang học theo slide lớp) |
| 1 việc | Hiểu thêm kiến thức trình bày trên slide khi tài liệu lớp chưa đủ |
| 1 quyết định AI | `IN_CORPUS` · `NEED_EXTERNAL` · `CANNOT_FETCH` |
| 1 kết quả | Trả lời + nguồn trong corpus, **hoặc** brief tìm 3 từ khóa + loại nguồn + tiêu chí tin cậy, **hoặc** checklist tự tìm khi AI không fetch được |

**Hướng spec:** A — VLearn (gắn trang bài VLearn). Canvas gọi “Hướng B · VLearn Extend” = tên bài CP1, không phải ô “Trợ lý Học viên”.  
**Loại:** tính năng mới trên chỗ hỏi đáp đã có (extend), không thay chatbot bám-slide.

## Ba nhãn — bắt buộc hiện cho học viên

1. **`IN_CORPUS`** — câu hỏi đã có trong slide/transcript: trả lời ngắn, citation trong corpus (slide/mục nào). Không nhét nguồn ngoài.
2. **`NEED_EXTERNAL`** — corpus không đủ (thiếu định nghĩa, ví dụ, phần chưa phủ): **không giả vờ là trong bài**. Trả brief tìm: 3 từ khóa, loại nguồn (textbook, docs, paper), tiêu chí tin cậy. Nếu prototype **được phép fetch web**: tổng hợp câu trả lời **kèm nguồn**, ghi rõ đây là ngoài lớp.
3. **`CANNOT_FETCH`** — AI không lấy được web / vượt hạn / nguồn không tin: nói thẳng, đưa checklist để sinh viên tự tìm. Không bịa paper, URL, DOI.

**Automation:** conditional — chỉ gợi ý/lấy nguồn ngoài **sau khi** đã kiểm tra corpus. Không fetch khi quá hạn. Không bịa citation.

## JTBD / problem (không chữ AI, không tên sản phẩm)

**JTBD:** Khi đang học theo tài liệu buổi học mà phần định nghĩa, ví dụ hoặc phạm vi chưa đủ để hiểu sâu, tôi muốn có nguồn bổ sung đáng tin kèm chỗ đối chiếu với bài, để hiểu thêm đúng trọng tâm chứ không mất thời gian tự kiếm và dễ lệch.

**Problem:** Tài liệu lớp đủ để làm quiz nhưng mỏng; học viên phải tự ra ngoài tìm. Nguồn lẫn, mất thời gian, không biết đâu đáng tin, dễ hiểu lệch bài.

## Evidence — canvas bắt **chuẩn A (mining)** trước

Thư mục `data/` (slide, log hỏi–đáp **được phép**):

- Đếm câu hỏi mà corpus **không phủ** (học viên phải ra ngoài).
- Không copy paper/docs hay snippet lấy từ ngoài vào `data/`.
- Không bịa URL/DOI làm evidence.
- Quote ≥5: lấy từ log hỏi–đáp thật hoặc khảo sát bổ sung (`khao-sat.md`).

## Non-goals

- Không trả lời kiến thức ngoài **như thể** nằm trong slide (trộn corpus + web im lặng).
- Không bỏ qua bước kiểm tra corpus.
- Không bịa citation / DOI / paper.
- Không làm hộ bài nộp, không chatbot độc lập ngoài trang bài.
- Không fetch vô hạn mọi trang web.

## Đối thủ (gợi ý §3)

- ChatGPT / Gemini: trả lời sâu nhưng không biết slide lớp, dễ lệch, citation giả.
- Perplexity / Scholar: có nguồn ngoài nhưng không gắn corpus buổi học, không nhãn IN/NEED/CANNOT.
- Chat VLearn hiện tại: bám slide — **đáng học** khi đủ corpus; **đáng né** khi giả vờ đủ lúc slide mỏng.

## Việc làm ngay

1. Mining `data/` → số câu `IN_CORPUS` vs `NEED_EXTERNAL` (`evidence/mining.md`).
2. Gửi form `khao-sat.md` cho HV (quote + % xác nhận job này).
3. Mời ≥5 sinh viên ngoài nhóm làm willing users (canvas §04).
4. Điền spec trước 21:00 17/9.
