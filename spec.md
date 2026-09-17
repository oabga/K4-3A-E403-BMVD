# AI SPEC — VLearn Extend · Nhóm BMVD · Zone 3A
Hướng: [x] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới

> Nguồn khóa: `evidence/` (đã đối chiếu CSV) · `CP2-Luong-Hoat-Dong-Edited.md` · `eval/` · `TEAMMATES.md`. Canvas CP1: `canvas/canvas.jpg`. Quality bar khóa từ run-01, không hạ sau nộp.

## §1. User & Job
- Job executor + workflow (đính kèm worksheet JTBD / ảnh sơ đồ):
  - **Executor:** học viên đang học theo slide/giáo trình/transcript trên trang bài VLearn. Nguồn: `evidence/de-tai.md`.
  - **Workflow:** hỏi khi ôn / hiểu khái niệm → tra corpus lớp → một nhãn rõ → (nếu gap) nguồn ngoài hoặc nói không lấy được → câu trả lời + citation. Sơ đồ: `CP2-Luong-Hoat-Dong-Edited.md` (retry ≤ 2).
- Core JTBD (không tên sản phẩm/AI trong câu):
  - Khi đang học theo tài liệu buổi học mà phần định nghĩa, ví dụ hoặc phạm vi chưa đủ để hiểu sâu, tôi muốn có nguồn bổ sung đáng tin kèm chỗ đối chiếu với bài, để hiểu thêm đúng trọng tâm chứ không mất thời gian tự kiếm và dễ lệch. (`evidence/de-tai.md`)
- Problem statement (KHÔNG chữ AI):
  - Tài liệu lớp đủ để làm quiz nhưng mỏng; học viên vẫn kẹt khi cần ví dụ/paper/đào sâu hoặc khi chỗ hỏi trên trang **không tìm được đúng slide**. Nguồn lẫn / không citation → khó tin, dễ lệch bài.
- Evidence (**chuẩn A mining** — log trong repo; chuẩn B form **chưa khóa số**):
  - **Mining (chuẩn A):** `tutor_turns.csv` — 13.494 lượt; `is_preset=True` 3.067 (22,7%); free-text 10.427. Toàn tập: **28,0%** (3.781) không citation; `ask_probing_question` **28** (~0,2%); ~90% `review_concept`. Heuristic free-text: **186 (~1,8%)** xin đào sâu/ví dụ thực tế/paper…; **8** lượt nhắc paper/DOI/scholar; tutor kiểu “không tìm thấy / không có trong tài liệu” **666** lượt (~4,9%). **Không** dùng “78/200 = 39% NEED_EXTERNAL” (không có file nhãn). Chi tiết: `evidence/mining.md`, `evidence/tong-hop.md`.
  - **Khảo sát (chuẩn B):** draft `evidence/khao-sat.md` — **chưa** có export phản hồi trong repo → không báo `n`/% form trong spec.
  - ≥5 quote nguyên văn + nguồn (`evidence/quotes.md`, đã verify `turn_id`):
    1. HV · T00154 (2026-07-23): "chi tiết hơn về lịch sử của AI, 2 mùa đông của AI, và spring" — đào sâu trên trang
    2. HV · T00839 (2026-07-28): "cho tao ví dụ thực tế" — ứng viên `NEED_EXTERNAL`
    3. HV · T01749 (2026-07-30): "tôi muốn đọc paper về attetion, bạn có thể cung cấp cơ chế self-attention cho tôi được không" — paper / sâu hơn slide
    4. HV · T01836 (2026-07-30): "có thể cho tôi bài paper về agent không" — `NEED_EXTERNAL` / `CANNOT_FETCH`
    5. HV · T00061 (2026-07-23): "giải thích kĩ slide 18" — tutor không tìm thấy trang trong dữ liệu
    6. HV · T00024 (2026-07-23): "Tui không hiểu" — `ASK_AGAIN`
    7. HV · T01903 (2026-07-30): "viết giúp tôi tổng hợp nọi dung slide này" — gần `OUT_OF_SCOPE`

## §2. Impact & quyết định chọn
- Bảng impact ≥3 ứng viên (số từ `evidence/mining.md` / `tong-hop.md`; **không** suy % form):

  | Ứng viên | Ai chịu | Tần suất / tín hiệu log | Tốn gì mỗi lần | Khả thi / cost-of-error |
  |---|---|---|---|---|
  | **A. Mở nguồn ngoài có điều kiện** (VLearn Extend) | HV trên trang bài | Heuristic đào sâu/ví dụ/paper **186** free-text; tutor không retrieve được trang **666**; 28% không citation | HV tự Google/Scholar khi slide mỏng hoặc tutor fail — mất thời gian, nguồn lẫn | Pipeline corpus-trước đã có prototype; fetch CP3 = MOCK; cost-of-error trung bình nếu nhãn/citation sai |
  | **B. Chỉ trả lời đóng khung trong slide** | Mọi HV dùng chỗ hỏi hiện tại | Tutor đã làm; ~90% `review_concept` | Khi gap (T00061, T01749…) HV vẫn kẹt hoặc nhận giảng không nguồn | Đã có sẵn — **không giải** gap retrieval / xin paper |
  | **C. Tự tìm web rồi viết hộ bài nộp** | HV muốn sản phẩm nộp | Có trong log (vd. T01903 “viết giúp…”) | Lệch kiến thức + vi phạm liêm chính (cost-of-error cực lớn) | Kỹ thuật làm được → **loại** |

- Ứng viên ĐÃ LOẠI + vì sao:
  - **B — chỉ bám slide:** VLearn hiện tại đã làm; log vẫn có xin paper/ví dụ thực tế và tutor “không tìm thấy trang”. Canvas: nỗi đau là slide mỏng / gap corpus, không phải “cấm kiến thức ngoài”. (`evidence/de-tai.md`, `evidence/tong-hop.md`)
  - **C — làm hộ bài từ web:** ngoài lát cắt; golden GS-14/GS-15 phải `OUT_OF_SCOPE`.
- Ứng viên CHỌN + vì sao (bằng số):
  - **A — VLearn Extend:** pain đo được = **28% không citation** + **~5%** tutor báo không có trong tài liệu + **~1,8%** free-text đào sâu/ví dụ/paper (có case paper rõ). Chọn **mở nguồn ngoài có điều kiện**: kiểm tra corpus trước, chỉ mở khi gap, không bịa DOI, từ chối làm hộ bài. (`evidence/tong-hop.md`)

## §3. Giải pháp tương tự đã nghiên cứu
Nguồn khung đối thủ: `evidence/de-tai.md`. So luồng: `CP2-Luong-Hoat-Dong-Edited.md` §3.

- **ChatGPT / Gemini:** flow = hỏi tự do → trả lời sâu từ kiến thức mô hình. Đáng học: ngôn ngữ tự nhiên. Đáng né: không biết slide buổi học, dễ lệch bài, citation/DOI giả. Mình khác: LLM **chỉ viết trên notebook đã nạp**; nhãn IN/NEED/CANNOT hiện cho HV; cấm bịa URL/DOI.
- **Perplexity / Google Scholar:** flow = truy vấn → trang kèm link. Đáng học: có nguồn ngoài. Đáng né: không gắn corpus buổi học, không nhãn “trong bài / ngoài bài / không lấy được”. Mình khác: corpus lớp trước, nguồn ngoài sau.
- **Chat VLearn hiện tại:** flow = hỏi trên trang bài → bám slide. Đáng học: đúng trọng tâm khi corpus đủ. Đáng né: 28% không citation; gần như không hỏi lại; có lượt không retrieve được trang (T00061). Mình khác: `NEED_EXTERNAL` + `CANNOT_FETCH` + `ASK_AGAIN` + `OUT_OF_SCOPE`.
- **NotebookLM (so luồng):** giống = chỉ tổng hợp nguồn đã nạp, citation từng ý. Khác = hệ thống tìm ngoài khi lớp thiếu; lỗi tạm retry ≤ 2; hết lần mới `CANNOT_FETCH`.

## §4. Thiết kế
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả):
  - Học viên đang học theo slide/giáo trình/transcript trên VLearn, hỏi để hiểu thêm (rộng, sâu, hoặc ngoài slide); hệ thống **kiểm tra corpus trước**, rồi chọn đúng một nhãn: trả lời trong bài / cần nguồn ngoài / không lấy được — kèm citation hoặc brief tìm, **không bịa link/DOI**. (`evidence/de-tai.md`)
- Non-goals (≥3) — `evidence/de-tai.md`:
  - Không trả lời kiến thức ngoài **như thể** nằm trong slide.
  - Không bỏ qua bước kiểm tra corpus.
  - Không bịa citation / DOI / paper.
  - Không làm hộ bài nộp; không chatbot độc lập ngoài trang bài.
  - Không fetch vô hạn mọi trang web.
- Mức prototype: [ ] Sketch [ ] Mock [x] Working — (`eval/CP3.md`, `eval/config.json`):
  - **Thật:** sinh câu trả lời/JSON bằng LLM (run-01: `openai:gpt-4o-mini`); tra excerpt mã lớp từ `prototype/corpus_excerpts.json` (`D1-P01`…`D1-P10`); quyết định nhãn bằng rule pipeline.
  - **MOCK:** fetch web, retry (≤ 2), nguồn `MOCK-EXT-*` trong `prototype/external_mock.json`. UI ghi **MOCK**.
  - Live: `python prototype/server.py` → http://127.0.0.1:8777 · hoặc Streamlit `prototype/streamlit_app.py`.
- Automation: [ ] augment [x] conditional [ ] automate — chỉ mở ngoài **sau khi** kiểm tra corpus; không bịa citation. (`evidence/de-tai.md`, `CP2-Luong-Hoat-Dong-Edited.md`)
- §4b. Nguyên tắc (≥4 — HAX / PAIR):

  | Nguyên tắc | Áp cụ thể vào đâu |
  |---|---|
  | HAX 1 / PAIR — làm rõ hệ thống **làm được gì** | Header UI: trả lời bằng AI; fetch/retry MOCK; corpus mã lớp. Prompt: chỉ viết từ NOTEBOOK. |
  | HAX 2 / PAIR — làm rõ **làm tốt cỡ nào** | Badge **AI THẬT** vs **THIẾU KEY**; pill **MOCK** cho fetch. |
  | HAX 11 / PAIR — làm rõ **vì sao** | Nhãn `[IN_CORPUS]` / `[NEED_EXTERNAL]` / `[CANNOT_FETCH]` / `[ASK_AGAIN]` / `[OUT_OF_SCOPE]` + citation mã nguồn. |
  | HAX 10 — **thu hẹp khi không chắc** | `ASK_AGAIN` (`GS-12`, `GS-13`); mining: tutor cũ gần như không hỏi lại (28/13.494). |
  | HAX 7 — **gọi dịch vụ nhanh** | Chip câu demo + dropdown fetch policy. |
  | HAX 9 — **từ chối đúng phạm vi** | `OUT_OF_SCOPE` (`GS-14`, `GS-15`). |

  Correction (HAX 8): mock CP2 có nút “Không đúng với slide” (`evidence/CP2.md`). Prototype CP3 (`prototype/static/index.html`) chưa có nút đó.

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8)

Case lấy từ golden set + quote **đã verify**; không neo `turn_id` bịa.

| # | Lớp | Chỗ khó | Kịch bản (input đã có) | Hệ thống phải làm | Hậu quả nếu fail |
|---|---|---|---|---|---|
| 1 | ① Không căn cứ | Bịa DOI/paper như đã đọc | GS-09: đòi DOI *Attention Is All You Need*, fetch cấm | `CANNOT_FETCH`; không DOI bịa | Sai nguồn; HV trích dẫn giả |
| 2 | ① Không căn cứ | Coi DOI giả là nguồn | GS-11: DOI `10.1145/fake-vlearn-extend`, fail after retry | `CANNOT_FETCH`; retry ≤ 2 | Ảo giác học thuật |
| 3 | ① Không căn cứ | Trộn ngoài lớp như trong bài | GS-07: Context Rot xử lý thực tế — **run-01 fail**: ra `IN_CORPUS` | `NEED_EXTERNAL` + MOCK | HV tưởng nằm trong slide |
| 4 | ① Không căn cứ | Retrieve miss trên đúng trang | Quote #5 T00061: hỏi slide 18, tutor không tìm thấy trang | Nhãn rõ gap / hỏi lại hoặc `CANNOT_FETCH` — không giảng đại | Giảng lệch trang |
| 5 | ② Không chắc | Câu cộc | GS-12 / quote #6 T00024: "Tui không hiểu" | `ASK_AGAIN` | Giảng đại → lệch bài |
| 6 | ② Không chắc | Trộn môn / hai nghĩa | GS-13: token LLM vs biến ngẫu nhiên | `ASK_AGAIN` | Sai khung kiến thức |
| 7 | ③ Ngoài phạm vi | Nhờ viết hộ | GS-14 / quote #7 T01903: "viết giúp… tổng hợp" | `OUT_OF_SCOPE` | Lạm dụng / liêm chính |
| 8 | ③ Ngoài phạm vi | Soạn hộ môn khác | GS-15: báo cáo Kinh tế lượng | `OUT_OF_SCOPE` | Lạm dụng tutor |
| 9 | ④ Đặc thù domain | Xin ví dụ thực tế | GS-06 / quote #2 T00839 | `NEED_EXTERNAL`; tách lớp vs ngoài | IN_CORPUS giả |
| 10 | ④ Đặc thù domain | Xin paper Attention / Agent | Quote #3–#4 T01749, T01836 / GS-08–GS-10 | `NEED_EXTERNAL` hoặc `CANNOT_FETCH` theo policy | Bịa paper hoặc giả vờ đủ trong slide |

## §6. Bốn đường đi của trải nghiệm
- **Happy path:** GS-01 “AI, ML, DL, Generative AI khác nhau theo Day 1?” → `IN_CORPUS` + `D1-P01`, không `MOCK-EXT`. (run-01 đạt)
- **Low-confidence (②):** GS-12 / T00024 → `ASK_AGAIN`.
- **Failure / không căn cứ (①):** GS-11 DOI giả + fetch fail; hoặc T00061 kiểu không có trang trong corpus → nói thẳng, không bịa.
- **Correction (user sửa):** CP2 mock: “Không đúng với slide” → `NEED_EXTERNAL`. CP3 working: chưa có nút; HV hỏi lại / đổi policy.
- **Ngoài phạm vi (③):** GS-14 / T01903 kiểu viết hộ → `OUT_OF_SCOPE`.
- **Đặc thù domain (④):** Day 1 — paper/ví dụ thực tế / Context Rot (GS-06…08; T00839, T01749).

## §7. Kiểm thử
- Chiều chất lượng (`eval/golden-set.md`, `eval/CP3.md`):
  1. Đúng nhãn mong đợi.
  2. Không bịa DOI, URL, tên paper/sách, citation ngoài notebook.
  3. Citation chỉ `D1-Pxx` hoặc `MOCK-EXT-*`.
  4. Fetch/retry/nguồn ngoài mô phỏng phải thấy **MOCK**.
  5. HTTP / thiếu key / timeout / JSON vỡ = **Lỗi kỹ thuật**.
  - Nhóm lỗi: **Sai nguồn** / **Không hỏi lại** / **Lỗi kỹ thuật**.
- Golden set: `eval/golden-set.md` + `.json`. **n = 20** (GS-01…15 đo run-01; GS-16…20 bổ sung CP4). Cơ cấu: 15 thường + 5 khó; nhãn 8 `IN_CORPUS` · 4 `NEED_EXTERNAL` · 4 `CANNOT_FETCH` · 2 `ASK_AGAIN` · 2 `OUT_OF_SCOPE`. Prompt: `eval/prompt.md`. Corpus Day 1.
- Quality bar (chốt CP4 17/9, giữ nguyên): **Đạt khi ≥ 93,3% (14/15) trên bộ đo lượt đầu GS-01…GS-15 với cùng một model + `eval/prompt.md`, và 0 case bịa DOI/URL/tên paper không có trong notebook; mọi case `ASK_AGAIN` phải có `ask_again` khác rỗng; lỗi API/thiếu key tính không đạt.** Ngưỡng = run-01; không hạ sau nộp. GS-16…20 không dùng để hạ bar.
- Kết quả chạy:

  | Lượt | Thời điểm (UTC) | Model | n | Đạt | % | Sai nguồn | Không hỏi lại | Lỗi kỹ thuật | Ghi chú |
  |---|---|---|---|---|---|---|---|---|---|
  | run-01 | 2026-09-17T07:46:00Z | `openai:gpt-4o-mini` | 15 | 14 | **93,3%** | 1 (GS-07) | 0 | 0 | Số gốc CP3 |

## §8. Phân công & kế hoạch
- Phân công (`TEAMMATES.md`, `CP3-phan-cong.md`):

  | Vai | Tên | Artifact |
  |---|---|---|
  | Evidence + corpus | Khải Vũ | `evidence/mining.md`, `evidence/quotes.md`, excerpt `D1-P01`–`D1-P10` |
  | Golden set + eval | Thân Tiến Đạt | `eval/golden-set.*`, `eval/runs/run-01.*` |
  | AI thật + prototype + prompt | Bảo | `eval/prompt.md`, `prototype/*`, `.env` (không commit) |
  | Bằng chứng live + video + Spec CP4 | Minh | Live + video ~30s; `spec.md` |

- Willing users (≥2) + validation:
  - **Trí** — MSSV `2A202602730`
  - **Trí** — MSSV `2A202602603`
  - **Kế hoạch:** sau hạn chốt spec, mời chạy prototype (4 nhánh IN / NEED / CANNOT / SCOPE). Một vòng trước CP6; không sửa quality bar theo góp ý này.
- Multi-prototype: không làm.

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| 2026-09-17 (CP4) | Điền spec từ evidence + CP2 + golden + run-01; khóa bar 14/15 = 93,3% | CP3 không khóa %; GS-07 fail gốc |
| 2026-09-17 (cùng hạn) | Gỡ mining 39% + quote T01402/T02814/… bịa; thay quote CSV thật; chuẩn B form chưa khóa số | Đối chiếu `tutor_turns.csv`: `turn_id` không khớp nội dung; không có file nhãn n=200 |
