# Tổng hợp — Mining (chuẩn A) + trạng thái khảo sát

Cập nhật sau khi **đối chiếu CSV** và gỡ số/mining/quote không tái lập được.

---

## 1. Mining chatlog (chuẩn A) — dùng cho spec §1–§2

Nguồn chi tiết: `evidence/mining.md`, `evidence/quotes.md`.

| Tín hiệu | Số | Dùng để chứng minh gì |
|---|---|---|
| Tổng lượt / free-text | 13.494 / 10.427 | Quy mô log thật |
| Không citation | **28,0%** (3.781) | Khó tin / khó đối chiếu bài |
| Gần như không hỏi lại | **28** lượt `ask_probing_question` | Cần nhánh `ASK_AGAIN` |
| Tutor “không tìm thấy / không có trong tài liệu” (heuristic) | **666** (toàn tập) | Gap corpus/retrieval trên trang bài |
| Xin đào sâu / ví dụ thực tế / paper… (heuristic free-text) | **186 (~1,8%)** | Nhu cầu vượt bullet — **có nhưng không phải 39%** |
| Xin paper/DOI/scholar (heuristic) | **8** | Case rõ `NEED_EXTERNAL` / `CANNOT_FETCH` |

**Không còn dùng:** “78/200 = 39% NEED_EXTERNAL” (không có file nhãn mẫu).

---

## 2. Khảo sát form (chuẩn B) — chưa khóa số trong repo

- Draft câu hỏi + link: `evidence/khao-sat.md`
- **Repo chưa có** export phản hồi (CSV/sheet/ảnh) → **không** đưa `n = 24`, 83,3%, 70,8%, quote form #04/#11 vào spec như số đã đo.
- Nếu sau này có sheet: bổ sung vào đây + `quotes.md`, rồi mới cập nhật §1 spec (changelog §9).

---

## 3. Quyết định lát cắt (vẫn giữ VLearn Extend)

Chọn **A — mở nguồn ngoài có điều kiện** vì:

1. Log cho thấy HV **có** hỏi đào sâu / ví dụ thực tế / paper; tutor hiện tại hoặc giảng trong khung slide, hoặc **không tìm thấy trang**, hoặc **không citation**.
2. Canvas CP1 + JTBD trong `de-tai.md` khớp nhãn `IN_CORPUS` / `NEED_EXTERNAL` / `CANNOT_FETCH`.
3. Loại “chỉ bám slide”: đã có sẵn, không xử lý gap khi corpus mỏng hoặc retrieve fail.
4. Loại “làm hộ bài từ web”: cost-of-error cao; golden `OUT_OF_SCOPE` (GS-14/15).

**Phân loại Spec:** [x] Tính năng mới trên chỗ hỏi đáp VLearn (`spec.md`).
