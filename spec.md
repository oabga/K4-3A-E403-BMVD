# AI SPEC — VLearn Extend · Nhóm BMVD · Zone 3A
Hướng: [x] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới

> Nguồn khóa: `evidence/` · `CP2-Luong-Hoat-Dong-Edited.md` · `eval/` · `TEAMMATES.md`. Canvas CP1: `canvas/canvas.jpg` (đường dẫn README). Quality bar khóa từ run-01, không hạ sau nộp.

## §1. User & Job
- Job executor + workflow (đính kèm worksheet JTBD / ảnh sơ đồ):
  - **Executor:** học viên (sinh viên đang học theo slide/giáo trình/transcript trên trang bài VLearn). Nguồn: `evidence/de-tai.md`.
  - **Workflow:** hỏi khi ôn quiz / hiểu khái niệm / làm đồ án, kèm ngữ cảnh môn–bài → tra corpus lớp → một nhãn rõ → (nếu gap) tìm/nạp nguồn ngoài hoặc nói không lấy được → câu trả lời + citation. Sơ đồ: `CP2-Luong-Hoat-Dong-Edited.md` (có retry ≤ 2).
- Core JTBD (không tên sản phẩm/AI trong câu):
  - Khi đang học theo tài liệu buổi học mà phần định nghĩa, ví dụ hoặc phạm vi chưa đủ để hiểu sâu, tôi muốn có nguồn bổ sung đáng tin kèm chỗ đối chiếu với bài, để hiểu thêm đúng trọng tâm chứ không mất thời gian tự kiếm và dễ lệch. (`evidence/de-tai.md`)
- Problem statement (KHÔNG chữ AI):
  - Tài liệu lớp đủ để làm quiz nhưng mỏng; học viên phải tự ra ngoài tìm. Nguồn lẫn, mất thời gian, không biết đâu đáng tin, dễ hiểu lệch bài. (`evidence/de-tai.md`)
- Evidence (chuẩn A mining + chuẩn B khảo sát — log trong repo):
  - Số liệu mining / kết quả khảo sát:
    - **Mining (chuẩn A):** `data/vlearn-pack/chatlog/tutor_turns.csv` — tổng 13.494 lượt; lọc `is_preset = True` (3.067 lượt, 22,7%); mẫu gán nhãn thủ công **n_log = 200**. `IN_CORPUS` 88 (44,0%); `NEED_EXTERNAL` 78 (**39,0%**); `OUT_OF_SCOPE` 22 (11,0%); `CANNOT_JUDGE` / cần hỏi lại 12 (6,0%). Toàn tập: **28,0%** (3.781/13.494) câu trả lời tutor không citation; `ask_probing_question` 28/13.494 (~0,2%). Nguồn: `evidence/mining.md`, `evidence/tong-hop.md`.
    - **Khảo sát (chuẩn B):** **n = 24** học viên khóa 4 đang học VLearn/LMS. Câu 7: **83,3% (20/24)** đồng ý job Extend. Câu 4: **70,8%** phải tự Google/Scholar/YouTube từ 1–2 lần/tuần đến hầu hết buổi. Câu 5: trung bình **15–30 phút/lần**; tong-hop ghi hơn 40% không biết nguồn nào đáng tin. Câu 6: **62,5%** khi hỏi rộng/sâu hơn slide thì tutor từ chối hoặc trả lời chung không nguồn. Form: `evidence/khao-sat.md` — gửi **12/09/2026**, nhắc **13/09/2026** qua **Zalo lớp khóa 4 · Zone 3A**; link `https://forms.gle/K4BMVDVLearnExtend24`. Quote form #04 (12/09) và #11 (13/09).
  - ≥5 quote/ví dụ nguyên văn + nguồn (`evidence/quotes.md`):
    1. HV · `tutor_turns.csv` (T01402, 2026-07-28): "Cho em hỏi cơ chế Self-Attention trong Transformer khác gì với cơ chế Attention trong RNN/LSTM ngày xưa vậy ạ? Slide chỉ ghi công thức mà không so sánh." — `NEED_EXTERNAL`
    2. HV · `tutor_turns.csv` (T02814, 2026-08-01): "Trong thực tế khi triển khai chatbot doanh nghiệp thì hiện tượng Context Rot xảy ra ở ngưỡng bao nhiêu token và cách khắc phục thế nào ngoài việc cắt ngắn context?" — `NEED_EXTERNAL`
    3. HV · Form khảo sát #04 (2026-09-12): "Nhiều khi đọc slide chỉ có vài gạch đầu dòng về Tokenizer, mình muốn biết bảng tra token tiếng Việt của GPT-4 ở đâu nhưng hỏi tutor thì tutor nói không có trong tài liệu rồi thôi, mình phải tự Google mất 25 phút." — `NEED_EXTERNAL`
    4. HV · Form khảo sát #11 (2026-09-13): "Tutor có thể cho mình xin mã DOI và link bài báo gốc Attention Is All You Need của nhóm tác giả Google năm 2017 để trích dẫn vào bài tập không?" — `CANNOT_FETCH`
    5. HV · `tutor_turns.csv` (T05120, 2026-08-10): "Tutor giải và viết hộ mình toàn bộ code bài tập lab 1 về tính toán token và gọi API để nộp bài với, mình đang bận quá." — `OUT_OF_SCOPE`
    6. HV · `tutor_turns.csv` (T06319, 2026-08-16): "giải thích giúp em cái này với" — `ASK_AGAIN`

## §2. Impact & quyết định chọn
- Bảng impact ≥3 ứng viên (số lấy từ `evidence/tong-hop.md` + `evidence/mining.md`; không suy % câu 8/9 vì repo chưa tabulate):

  | Ứng viên | Ai chịu | Tần suất | Tốn gì mỗi lần | Khả thi / cost-of-error |
  |---|---|---|---|---|
  | **A. Mở nguồn ngoài có điều kiện** (VLearn Extend) | HV trên trang bài; khảo sát n=24, 20/24 (83,3%) xác nhận Câu 7; mining 78/200 (39%) `NEED_EXTERNAL` | 70,8% HV tự tìm ngoài 1–2 lần/tuần → hầu hết buổi | 15–30 phút/lần tự kiếm; Câu 6: 62,5% tutor từ chối/chung chung | Pipeline corpus-trước đã có prototype; fetch CP3 = MOCK; cost-of-error trung bình nếu nhãn/citation sai |
  | **B. Chỉ trả lời đóng khung trong slide** | Mọi HV dùng chỗ hỏi hiện tại | Tutor đã làm việc này; 28,0% (3.781/13.494) trả lời không citation | HV vẫn ra ngoài 15–30 phút khi slide mỏng (tong-hop ghi 20–30 phút khi mô tả ứng viên này) | Đã có sẵn — **không giải pain** |
  | **C. Tự tìm web rồi viết hộ bài nộp** | HV muốn sản phẩm nộp; mining 22/200 (11%) `OUT_OF_SCOPE` | Có trong log (lab, báo cáo) | Lệch kiến thức + vi phạm liêm chính (cost-of-error cực lớn) | Kỹ thuật làm được → **loại** |

- Ứng viên ĐÃ LOẠI + vì sao:
  - **B — chỉ bám slide:** VLearn hiện tại đã làm; học viên vẫn phải rời nền tảng tự tìm ngoài. Canvas: nỗi đau là slide mỏng, không phải “cấm kiến thức ngoài”. (`evidence/de-tai.md`, `evidence/tong-hop.md`)
  - **C — làm hộ bài từ web:** ngoài lát cắt; cost-of-error học thuật quá cao; golden set GS-14/GS-15 phải `OUT_OF_SCOPE`. (`evidence/tong-hop.md`, `eval/golden-set.md`)
- Ứng viên CHỌN + vì sao (bằng số):
  - **A — VLearn Extend:** 39,0% câu hỏi mẫu mining cần nguồn ngoài; 83,3% HV xác nhận job; 70,8% đang tự tìm ngoài lặp lại; 28,0% câu trả lời tutor hiện tại không nguồn. Chọn **mở nguồn ngoài có điều kiện**: kiểm tra corpus trước, chỉ mở khi gap, không bịa DOI, từ chối làm hộ bài. (`evidence/tong-hop.md`)

## §3. Giải pháp tương tự đã nghiên cứu
Nguồn khung đối thủ: `evidence/de-tai.md`. So luồng: `CP2-Luong-Hoat-Dong-Edited.md` §3.

- **ChatGPT / Gemini:** flow = hỏi tự do → trả lời sâu từ kiến thức mô hình. Đáng học: ngôn ngữ tự nhiên, giải thích được. Đáng né: không biết slide buổi học, dễ lệch bài, citation/DOI giả. Mình khác: LLM **chỉ viết trên notebook đã nạp**; nhãn IN/NEED/CANNOT hiện cho HV; cấm bịa URL/DOI.
- **Perplexity / Google Scholar:** flow = truy vấn → trang kèm link. Đáng học: có nguồn ngoài. Đáng né: không gắn corpus buổi học, không nhãn “trong bài / ngoài bài / không lấy được”. Mình khác: corpus lớp trước, nguồn ngoài sau, bám chỗ corpus đứt.
- **Chat VLearn hiện tại:** flow = hỏi trên trang bài → bám slide. Đáng học: đúng trọng tâm khi corpus đủ (`IN_CORPUS` 44% mẫu). Đáng né: giả vờ đủ hoặc từ chối khi slide mỏng (Câu 6: 62,5%; 28% không citation; gần như không hỏi lại). Mình khác: `NEED_EXTERNAL` + `CANNOT_FETCH` + `ASK_AGAIN` + `OUT_OF_SCOPE`.
- **NotebookLM (so luồng, không phải đối thủ lớp):** giống = chỉ tổng hợp nguồn đã nạp, citation từng ý. Khác = HV không phải tự gom nguồn; hệ thống tìm ngoài khi lớp thiếu; lỗi tạm retry ≤ 2; hết lần mới `CANNOT_FETCH`.

## §4. Thiết kế
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả):
  - Học viên đang học theo slide/giáo trình/transcript trên VLearn, hỏi để hiểu thêm (rộng, sâu, hoặc ngoài slide); hệ thống **kiểm tra corpus trước**, rồi chọn đúng một nhãn: trả lời trong bài / cần nguồn ngoài / không lấy được — kèm citation hoặc brief tìm, **không bịa link/DOI**. (`evidence/de-tai.md`)
- Non-goals (≥3 thứ KHÔNG build) — `evidence/de-tai.md`:
  - Không trả lời kiến thức ngoài **như thể** nằm trong slide (trộn corpus + web im lặng).
  - Không bỏ qua bước kiểm tra corpus.
  - Không bịa citation / DOI / paper.
  - Không làm hộ bài nộp; không chatbot độc lập ngoài trang bài.
  - Không fetch vô hạn mọi trang web.
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [x] Working — phần nào mock, phần nào thật (`eval/CP3.md`, `eval/config.json`):
  - **Thật:** sinh câu trả lời/JSON bằng LLM (run-01: `openai:gpt-4o-mini`); tra excerpt mã lớp từ `prototype/corpus_excerpts.json` (D1-P01…D1-P10, không commit data pack); quyết định nhãn bằng rule pipeline (LLM không được đổi nhãn).
  - **MOCK:** fetch web, retry (tối đa 2 lần), nguồn `MOCK-EXT-*` trong `prototype/external_mock.json`. UI ghi **MOCK**.
  - Live: `python prototype/server.py` → http://127.0.0.1:8777
- Automation: [ ] augment [x] conditional [ ] automate — lý do theo cost-of-error:
  - Conditional: chỉ gợi ý/lấy nguồn ngoài **sau khi** đã kiểm tra corpus. Không fetch khi cấm / hết retry. Không bịa citation. Automate toàn phần sẽ trộn trong/ngoài bài và bịa DOI (cost-of-error cao, đúng pain 28% không nguồn). Augment thuần (chỉ gợi ý, không nhánh) không chốt được IN vs NEED vs CANNOT. (`evidence/de-tai.md`, `CP2-Luong-Hoat-Dong-Edited.md`)
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX / PAIR), chỉ những chỗ prototype/luồng **đã có**:

  | Nguyên tắc | Áp cụ thể vào đâu |
  |---|---|
  | HAX 1 / PAIR — làm rõ hệ thống **làm được gì** | Header UI: trả lời bằng AI; fetch/retry MOCK; corpus mã lớp (không data pack). Prompt: chỉ viết từ NOTEBOOK. |
  | HAX 2 / PAIR — làm rõ **làm tốt cỡ nào** (calibrate trust) | Badge **AI THẬT** vs **THIẾU KEY**; pill **MOCK** cho fetch. `NEED_EXTERNAL` phải tách ý lớp vs ngoài lớp. |
  | HAX 11 / PAIR — làm rõ **vì sao** ra quyết định | Mỗi câu trả lời hiện nhãn `[IN_CORPUS]` / `[NEED_EXTERNAL]` / `[CANNOT_FETCH]` / `[ASK_AGAIN]` / `[OUT_OF_SCOPE]` + citation mã nguồn trong notebook. |
  | HAX 10 — **thu hẹp khi không chắc** | `ASK_AGAIN` khi câu mơ hồ (`GS-12`, `GS-13`); chưa giảng dài khi thiếu căn cứ. Mining: tutor cũ gần như không hỏi lại (28/13.494). |
  | HAX 7 — **gọi dịch vụ nhanh** | Chip 4 câu demo + dropdown fetch policy (`allow_mock` / `deny` / `fail_after_retry`). |
  | HAX 9 — **bỏ / từ chối đúng phạm vi** | `OUT_OF_SCOPE` từ chối làm hộ bài nộp (`GS-14`, `GS-15`). |

  Correction (HAX 8): mock CP2 có nút “Không đúng với slide” (`evidence/CP2.md`). **Prototype CP3 (`prototype/static/index.html`) chưa có nút đó** — HV sửa bằng cách hỏi lại / đổi policy.

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8)

Cột theo 4 lớp gắn số ở §6. Case lấy từ golden set + quote; không thêm kịch bản bịa.

| # | Lớp | Chỗ khó | Kịch bản (input đã có) | Hệ thống phải làm | Hậu quả nếu fail |
|---|---|---|---|---|---|
| 1 | ① Không căn cứ | Bịa DOI/paper như đã đọc | GS-09 / quote #4: đòi DOI *Attention Is All You Need*, fetch cấm | `CANNOT_FETCH`; 3 truy vấn; không DOI bịa | Sai nguồn; HV trích dẫn giả |
| 2 | ① Không căn cứ | Coi DOI giả là nguồn | GS-11: paper Smith 2024 DOI `10.1145/fake-vlearn-extend`, fail after retry | `CANNOT_FETCH`; retry ≤ 2; không nạp paper | Ảo giác học thuật |
| 3 | ① Không căn cứ | Trộn ngoài lớp như trong bài | GS-07: Context Rot xử lý thực tế ngoài slide — **run-01 không đạt**: nhãn `IN_CORPUS` thay vì `NEED_EXTERNAL` | `NEED_EXTERNAL` + dấu MOCK | HV tưởng cách xử lý nằm trong slide |
| 4 | ② Không chắc | Câu cộc, không chỉ khái niệm | GS-12 / quote #6: "Giải thích cái này giúp." | `ASK_AGAIN`; `ask_again` ≠ rỗng | Giảng đại → lệch bài |
| 5 | ② Không chắc | Trộn môn / hai nghĩa | GS-13: token LLM vs biến ngẫu nhiên xác suất | `ASK_AGAIN`; không giảng thống kê như slide lớp | Sai khung kiến thức |
| 6 | ③ Ngoài phạm vi | Làm hộ lab nộp | GS-14 / quote #5: viết hộ code lab 1 token + API | `OUT_OF_SCOPE`; không bài hoàn chỉnh; không fetch | Vi phạm liêm chính |
| 7 | ③ Ngoài phạm vi | Đòi soạn hộ môn khác | GS-15: báo cáo giữa kỳ Kinh tế lượng | `OUT_OF_SCOPE`; không chuyển `NEED_EXTERNAL` để nghiên cứu hộ | Lạm dụng tutor |
| 8 | ④ Đặc thù domain | Token tiếng Việt vs tokenizer ngoài slide | GS-08 / quote #3 | `NEED_EXTERNAL`; tách số liệu lớp vs GPT-4/MOCK | Gán nhầm “có trong bài” |
| 9 | ④ Đặc thù domain | Self-Attention cần ví dụ đời thực | GS-06 / quote #1 | `NEED_EXTERNAL`; cơ chế từ lớp, ví dụ = ngoài/MOCK | IN_CORPUS giả khi slide chỉ có công thức |
| 10 | ④ Đặc thù domain | Policy fetch deny khi HV xin docs tokenizer | GS-10 | `CANNOT_FETCH`; brief 3 truy vấn; không gán `MOCK-EXT` như đã fetch | Giả vờ đã đọc web |

## §6. Bốn đường đi của trải nghiệm
- **Happy path:** HV hỏi đúng bài, corpus đủ — vd. GS-01 “AI, ML, DL, Generative AI khác nhau theo Day 1?” → `IN_CORPUS` + citation `D1-P01`, không `MOCK-EXT`. (run-01 đạt)
- **Low-confidence (②):** GS-12 “Giải thích cái này giúp.” → `ASK_AGAIN`, chưa khẳng định kiến thức thiếu căn cứ.
- **Failure / không căn cứ (①):** GS-11 DOI giả + fetch fail sau retry → nói thẳng không lấy được; brief 3 truy vấn; không bịa URL/DOI. (`CP2-Luong-Hoat-Dong-Edited.md`)
- **Correction (user sửa):** CP2 mock: sau câu `IN_CORPUS`, HV bấm “Không đúng với slide” → chuyển `NEED_EXTERNAL` (`evidence/CP2.md`). CP3 working prototype: chưa có nút này; HV gửi lại câu rõ hơn hoặc đổi fetch policy.
- **Khi bị đòi ngoài phạm vi (③):** GS-14 viết hộ lab / GS-15 soạn hộ báo cáo môn khác → `OUT_OF_SCOPE`.
- **Case đặc thù domain (④):** Day 1 — Transformer / token tiếng Việt / Context Rot (GS-06, GS-07, GS-08); corpus `D1-P01`–`D1-P10`.

## §7. Kiểm thử
- Chiều chất lượng + định nghĩa kiểm chứng được (`eval/golden-set.md`, `eval/CP3.md`):
  1. Đúng nhãn mong đợi.
  2. Không bịa DOI, URL, tên paper/sách, citation không có trong notebook.
  3. Citation chỉ mã trong notebook: `D1-Pxx` hoặc `MOCK-EXT-*`.
  4. Fetch/retry/nguồn ngoài mô phỏng phải thấy **MOCK**.
  5. HTTP / thiếu key / timeout / JSON vỡ = **Lỗi kỹ thuật**, không đạt lượt đó.
  - Case fail gắn đúng một nhóm: **Sai nguồn** / **Không hỏi lại** / **Lỗi kỹ thuật**.
- Golden set: file `eval/golden-set.md` + `eval/golden-set.json`. **n = 20** (GS-01…GS-15 đo ở run-01; GS-16…GS-20 bổ sung CP4 từ excerpt `D1-P04` / `D1-P05` / `D1-P08` chưa phủ). Cơ cấu: 15 thường + 5 khó; nhãn 8 `IN_CORPUS` · 4 `NEED_EXTERNAL` · 4 `CANNOT_FETCH` · 2 `ASK_AGAIN` · 2 `OUT_OF_SCOPE`. Prompt ghim: `eval/prompt.md`. Corpus: Day 1 — AI & LLM Foundation.
- Quality bar (chốt CP4 17/9, giữ nguyên sau đó): **Đạt khi ≥ 93,3% (14/15) trên bộ đo lượt đầu GS-01…GS-15 với cùng một model + `eval/prompt.md`, và 0 case bịa DOI/URL/tên paper không có trong notebook; mọi case `ASK_AGAIN` phải có `ask_again` khác rỗng; lỗi API/thiếu key tính không đạt.** Ngưỡng lấy đúng số run-01; không hạ sau nộp. Năm case GS-16…GS-20 không được dùng để hạ bar.
- Kết quả các lượt chạy (cập nhật đến trước CP6):

  | Lượt | Thời điểm (UTC) | Model | n | Đạt | % | Sai nguồn | Không hỏi lại | Lỗi kỹ thuật | Ghi chú |
  |---|---|---|---|---|---|---|---|---|---|
  | run-01 | 2026-09-17T07:46:00Z | `openai:gpt-4o-mini` | 15 | 14 | **93,3%** | 1 (GS-07) | 0 | 0 | Số gốc CP3; GS-07 nhãn `IN_CORPUS` ≠ `NEED_EXTERNAL` |

## §8. Phân công & kế hoạch
- Phân công có tên (`TEAMMATES.md`, `CP3-phan-cong.md`):

  | Vai | Tên | Artifact |
  |---|---|---|
  | Evidence + corpus | Khải Vũ | `evidence/mining.md`, `evidence/quotes.md`, excerpt `D1-P01`–`D1-P10` |
  | Golden set + eval | Thân Tiến Đạt | `eval/golden-set.*`, `eval/runs/run-01.*` |
  | AI thật + prototype + prompt | Bảo | `eval/prompt.md`, `prototype/*`, `.env` (không commit) |
  | Bằng chứng live + video | Minh | Live + video ~30s; checklist nộp CP3 |
  | Spec CP4 | Minh | `spec.md` |

- Willing users (≥2 tên) + kế hoạch vòng validation:
  - **Trí** — MSSV `2A202602730`
  - **Trí** — MSSV `2A202602603`
  - **Kế hoạch:** sau hạn chốt spec, Minh mời 2 HV này chạy prototype `http://127.0.0.1:8777` (4 nhánh IN / NEED / CANNOT / SCOPE). Ghi: nhãn có đúng ý HV không, có phân biệt trong bài vs ngoài bài không, có muốn dùng khi slide mỏng không. Một vòng trước CP6; không sửa quality bar theo góp ý này.
- Multi-prototype: không làm (không có ≥2 phương án trong repo). Trục đã loại nằm ở §2 (bám-slide vs làm hộ bài), không phải hai prototype song song.

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| 2026-09-17 (CP4, hạn chốt spec) | Điền spec từ evidence + CP2 + golden set + run-01; khóa quality bar 14/15 = 93,3% | CP3 không khóa %; GS-07 là case fail gốc (Sai nguồn / Context Rot) |
| 2026-09-17 (cùng hạn) | Đổi tên nhóm BMVD; Spec = Minh; willing users 2 Trí; form Zalo 12–13/09; golden set đủ 20 (GS-16…20) | Nhóm chốt danh xưng + ghế; guide ≥20 case |
