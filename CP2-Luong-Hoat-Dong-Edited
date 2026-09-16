# Checkpoint 2 · Luồng hoạt động

**VLearn Extend** — Mini Hackathon AI

Giống NotebookLM: khi nguồn lớp không đủ, hệ thống tìm và nạp nguồn ngoài liên quan đến câu hỏi, rồi tổng hợp để trả lời đúng, có căn cứ.

Cách đọc: dữ liệu đi từ trái sang phải. Ba nhánh là một quyết định rõ — LLM không được bịa nguồn. Nhánh giữa là phần giống NotebookLM. Fetch nguồn ngoài lỗi tạm thì **retry**, hết lần mới `CANNOT_FETCH`.

---

## 1. Luồng dữ liệu

```mermaid
flowchart LR
  Q["01 Câu hỏi<br/>text + môn + bài"] --> H["02 Hits corpus<br/>đoạn lớp + score"]
  H --> D["03 Decision<br/>phủ / gap"]
  D --> N["04 Notebook<br/>lớp + nguồn ngoài"]
  N --> A["05 Câu trả lời<br/>text + citation"]
```

| Bước | Dữ liệu | Nội dung |
| --- | --- | --- |
| 01 | Câu hỏi | text + môn + bài |
| 02 | Hits corpus | đoạn lớp + score |
| 03 | Decision | phủ / gap |
| 04 | Notebook | lớp + nguồn ngoài |
| 05 | Câu trả lời | text + citation |

---

## 2. Luồng hoạt động

```mermaid
flowchart TD
  SV["01 Sinh viên hỏi"] --> CORPUS["02 Tra nguồn lớp"]
  CORPUS --> DEC{"03 Quyết định rõ"}

  DEC -->|"đủ căn cứ"| IN["IN_CORPUS<br/>Nguồn lớp đủ"]
  DEC -->|"thiếu ví dụ / paper / docs"| NEED["NEED_EXTERNAL<br/>Tổng hợp kiểu NotebookLM"]
  DEC -->|"cấm fetch / nguồn đóng"| CANT["CANNOT_FETCH<br/>AI không lấy được nguồn"]

  IN --> OUT["04 Câu trả lời đúng<br/>kèm nguồn đã dùng"]

  NEED --> FIND["Tìm nguồn ngoài liên quan<br/>bám chỗ corpus đứt"]
  FIND -->|lấy được| LOAD["Lọc tin cậy và nạp vào notebook"]
  FIND -->|lỗi tạm| RETRY["RETRY ≤ 2 lần<br/>đổi query / nguồn"]
  RETRY -->|thành công| LOAD
  RETRY -->|hết lần| CANT
  LOAD --> LLM["LLM chỉ đọc nguồn đã nạp<br/>mỗi ý có citation"]
  LLM --> OUT

  CANT --> BRIEF["Nói thẳng + brief 3 truy vấn<br/>không bịa URL / DOI"]
  BRIEF --> OUT
```

### 01 · Sinh viên hỏi

Câu hỏi khi ôn quiz, hiểu khái niệm hoặc làm đồ án. Kèm ngữ cảnh môn / bài đang học.

### 02 · Tra nguồn lớp

Tìm trong `data/` được phép: slide, giáo trình, transcript. Lấy đoạn liên quan và đo độ phủ.

### 03 · Quyết định rõ

- Đủ căn cứ → **IN_CORPUS**
- Thiếu ví dụ / paper / docs → **NEED_EXTERNAL**
- Fetch lỗi tạm → **RETRY** (tối đa 2 lần)
- Hết lần retry, hoặc môi trường cấm fetch / nguồn đóng → **CANNOT_FETCH**

### Ba nhánh + retry

**IN_CORPUS — Nguồn lớp đủ**

Trả lời ngay từ corpus. Kèm tối đa 3 nguồn trong lớp. Không kéo thêm web.

**NEED_EXTERNAL — Tổng hợp kiểu NotebookLM**

Sinh truy vấn bám đúng chỗ corpus đứt — không search lung tung. Lọc nguồn tin cậy (docs chính thức, giáo trình mở, paper), rồi nạp vào notebook phiên hỏi.

LLM chỉ đọc nguồn đã nạp (lớp + ngoài). Mỗi ý có citation. Không bịa URL, DOI hay tên paper.

**RETRY — không lấy được nguồn ngoài thì thử lại**

Retry khi lỗi tạm: timeout, mạng, nguồn rỗng, trang chặn tạm. Mỗi lần đổi query hẹp hơn hoặc đổi ứng viên nguồn. Tối đa 2 lần retry (tổng 3 lần thử). Thành công → nạp notebook, đi tiếp NEED_EXTERNAL.

Không retry khi môi trường cấm fetch, nguồn đóng, hoặc policy chặn.

**CANNOT_FETCH — AI không lấy được nguồn**

Chỉ vào nhánh này sau khi đã retry (hoặc bị cấm fetch). Nói thẳng. Đưa brief 3 truy vấn + tiêu chí tin cậy để sinh viên tự tìm. Không giả vờ đã đọc nguồn ngoài.

### 04 · Đầu ra cho sinh viên

Câu trả lời đúng, kèm nguồn đã dùng.

Học viên nhận câu trả lời + danh sách nguồn (lớp / ngoài) + trạng thái quyết định. Ôn được tại chỗ, không phải nhảy Google một cách mù mờ, và biết rõ câu nào được grounded trên nguồn thật.

---

## 3. So với NotebookLM

| Giống NotebookLM | Khác NotebookLM |
| --- | --- |
| Câu trả lời chỉ được tổng hợp từ nguồn đã nạp vào notebook. Có citation từng ý. Không dùng kiến thức “trôi” để bịa tài liệu. | Sinh viên không phải tự đi gom hết nguồn. Khi lớp thiếu, hệ thống tìm nguồn ngoài liên quan; lỗi tạm thì retry tối đa 2 lần; hết lần mới nói rõ `CANNOT_FETCH`, không giả vờ. |

Sơ đồ này chốt cách dữ liệu chạy: **corpus trước, nguồn ngoài sau, lỗi tạm thì retry, LLM chỉ nói trên nguồn đã nạp**.
