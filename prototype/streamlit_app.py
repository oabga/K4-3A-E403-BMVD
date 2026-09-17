"""
CP3 demo — VLearn Extend (Streamlit)

Luồng mỗi lần bấm Gửi:
  1) Chọn đoạn lớp (corpus D1-P*) khớp câu hỏi
  2) Gắn nhãn: IN_CORPUS / NEED_EXTERNAL / CANNOT_FETCH / ASK_AGAIN / OUT_OF_SCOPE
  3) Nếu NEED_EXTERNAL + allow_mock → nạp thêm MOCK-EXT (không search web thật)
  4) Gọi AI thật chỉ viết từ notebook đó

Chạy:
  source .venv/bin/activate
  streamlit run prototype/streamlit_app.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st

PROTO = Path(__file__).resolve().parent
sys.path.insert(0, str(PROTO))

from extend import answer_for, load_dotenv, read_json  # noqa: E402

st.set_page_config(page_title="VLearn Extend · CP3", page_icon="📘", layout="wide")
load_dotenv()

excerpts = read_json(PROTO / "corpus_excerpts.json")["excerpts"]
by_id = {ex["id"]: ex for ex in excerpts}

# (tên hiển thị, câu hỏi đúng, fetch policy, corpus_refs gợi ý)
PRESETS = [
    (
        "IN_CORPUS · AI / ML / DL là gì",
        "AI, Machine Learning, Deep Learning và Generative AI khác nhau như thế nào theo bài Day 1?",
        "allow_mock",
        ["D1-P01"],
    ),
    (
        "IN_CORPUS · Turing Test",
        "Turing Test kiểm tra điều gì?",
        "allow_mock",
        ["D1-P02"],
    ),
    (
        "NEED_EXTERNAL · ví dụ Self-Attention",
        "Slide có nói Self-Attention, nhưng cho em ví dụ đời thực ngoài slide để hiểu vì sao nó nhìn toàn bộ câu tốt hơn RNN.",
        "allow_mock",
        ["D1-P06"],
    ),
    (
        "CANNOT_FETCH · DOI (deny)",
        "Cho DOI paper Attention Is All You Need để em trích dẫn, nhưng môi trường đang cấm fetch web.",
        "deny",
        ["D1-P06"],
    ),
    (
        "OUT_OF_SCOPE · làm hộ lab",
        "Viết hộ toàn bộ code bài lab 1 tính toán token và gọi API để nộp.",
        "allow_mock",
        ["D1-P09"],
    ),
    (
        "ASK_AGAIN · mơ hồ",
        "Giải thích cái này giúp.",
        "allow_mock",
        ["D1-P01"],
    ),
]

LABEL_COLOR = {
    "IN_CORPUS": "green",
    "NEED_EXTERNAL": "orange",
    "CANNOT_FETCH": "red",
    "ASK_AGAIN": "blue",
    "OUT_OF_SCOPE": "violet",
}

st.title("VLearn Extend · CP3")
st.caption(
    "AI thật chỉ **viết câu trả lời**. Tài liệu lớp = đoạn `D1-P*` bên trái. "
    "Fetch web = **MOCK**. Không phải model tự đọc file PDF."
)

with st.expander("Cách demo này hoạt động (đọc 30 giây)", expanded=True):
    st.markdown(
        """
1. **Gợi ý demo** chỉ là phím tắt: đổ sẵn *một câu hỏi + nhánh kỳ vọng*.  
2. Hệ thống lấy **đoạn chữ trong corpus** (sidebar) đưa vào *notebook*.  
3. Gắn **nhãn** (đủ bài / cần ngoài / không fetch / hỏi lại / ngoài phạm vi).  
4. **Model** chỉ được viết dựa trên notebook — nên nếu notebook sai đoạn, câu trả lời sẽ lệch.

**Lỗi hay gặp:** chọn gợi ý “Turing Test” rồi sửa ô thành “AI là gì” → trước đây vẫn khóa `D1-P02` → trả lời Turing.  
**Đã sửa:** chỉ khóa đoạn corpus khi câu hỏi **còn đúng** như gợi ý; nếu bạn sửa câu → tự tìm đoạn theo nội dung hỏi.
        """
    )

with st.sidebar:
    st.header("Trạng thái")
    has_openai = bool(os.environ.get("OPENAI_API_KEY", "").strip())
    has_gemini = bool(
        os.environ.get("GEMINI_API_KEY", "").strip() or os.environ.get("GOOGLE_API_KEY", "").strip()
    )
    if has_openai or has_gemini:
        st.success("AI THẬT — có API key")
        st.write(os.environ.get("OPENAI_MODEL") or os.environ.get("GEMINI_MODEL") or "default")
    else:
        st.error("Thiếu key trong `.env`")
    st.warning("Fetch = MOCK (không Google/Scholar thật)")
    st.markdown("### Corpus Day 1 — đây mới là “slide” của demo")
    for ex in excerpts:
        with st.expander(f"{ex['id']} · {ex['title'][:40]}…"):
            st.write(ex["text"])

col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.subheader("1. Chọn tình huống hoặc gõ tay")
    names = ["(gõ tay — tự tìm đoạn theo câu hỏi)"] + [p[0] for p in PRESETS]
    preset = st.selectbox("Gợi ý demo", names)

    preset_q = ""
    policy = "allow_mock"
    pinned_refs = None
    if not preset.startswith("(gõ tay"):
        for name, question, pol, r in PRESETS:
            if name == preset:
                preset_q, policy, pinned_refs = question, pol, r
                break

    # Giữ câu hỏi theo preset khi đổi selectbox
    if "last_preset" not in st.session_state:
        st.session_state.last_preset = preset
    if preset != st.session_state.last_preset:
        st.session_state.last_preset = preset
        st.session_state.question = preset_q if preset_q else ""

    if "question" not in st.session_state:
        st.session_state.question = preset_q

    question = st.text_area("2. Câu hỏi", key="question", height=110)

    # Chỉ pin corpus khi user chưa sửa lệch preset
    use_pin = bool(pinned_refs) and question.strip() == (preset_q or "").strip()
    if pinned_refs and not use_pin:
        st.info(
            "Bạn đã sửa câu hỏi khác gợi ý → **không** khóa đoạn cũ; "
            "hệ thống sẽ tự chọn `D1-P*` theo nội dung câu hỏi."
        )
        refs = None
    else:
        refs = pinned_refs

    policy = st.selectbox(
        "3. Fetch policy (MOCK)",
        ["allow_mock", "deny", "fail_after_retry"],
        index=["allow_mock", "deny", "fail_after_retry"].index(policy)
        if policy in ("allow_mock", "deny", "fail_after_retry")
        else 0,
        help="allow_mock = được nạp MOCK-EXT khi NEED_EXTERNAL · deny = cấm fetch → CANNOT_FETCH",
    )

    if use_pin and refs:
        st.caption("Đoạn lớp sẽ dùng (khóa theo gợi ý): " + ", ".join(refs))
        for rid in refs:
            if rid in by_id:
                st.code(f"{rid}: {by_id[rid]['text'][:180]}…")

    go = st.button("4. Gửi AI", type="primary", use_container_width=True)

with col_right:
    st.subheader("Kết quả")
    if go:
        if not question.strip():
            st.warning("Nhập câu hỏi.")
        else:
            with st.spinner("Tra corpus → gắn nhãn → (MOCK nếu cần) → gọi AI…"):
                result = answer_for(question.strip(), policy, corpus_refs=refs)
            if result.get("technical_error"):
                st.error(f"Lỗi kỹ thuật: {result['technical_error']}")
            else:
                label = result.get("label") or "?"
                st.markdown(
                    f"**Nhãn:** :{LABEL_COLOR.get(label, 'gray')}[**{label}**] · "
                    f"AI=`{result.get('ai')}` · `{result.get('model')}`"
                )
                st.caption(" · ".join(result.get("mock_parts") or []))
                st.markdown("#### Câu trả lời (do model viết từ notebook)")
                st.write(result.get("answer") or "")
                if result.get("ask_again"):
                    st.warning(f"Hỏi lại: {result['ask_again']}")
                if result.get("search_brief"):
                    st.markdown("#### Brief 3 truy vấn")
                    for i, t in enumerate(result["search_brief"], 1):
                        st.write(f"{i}. `{t}`")
                st.markdown("#### Notebook đã đưa cho model")
                ids = result.get("notebook_ids") or []
                st.code(", ".join(ids) or "(trống)")
                for nid in ids:
                    if nid in by_id:
                        st.markdown(f"**{nid} (lớp)** — {by_id[nid]['title']}")
                        st.write(by_id[nid]["text"])
                    elif str(nid).startswith("MOCK"):
                        st.markdown(f"**{nid} (ngoài lớp · MOCK)**")
                st.caption(result.get("fetch_detail") or "")
                with st.expander("JSON đầy đủ"):
                    st.json(result)
    else:
        st.info(
            "**Cách test nhanh:** chọn lần lượt 4–5 gợi ý, **đừng sửa câu**, bấm Gửi. "
            "Muốn hỏi “AI là gì” → chọn gợi ý **AI / ML / DL** hoặc chọn “gõ tay” rồi gõ đúng câu đó."
        )

st.divider()
st.markdown(
    "**Video 30s:** gợi ý IN → NEED → CANNOT → SCOPE · rồi mở `eval/runs/run-01.md`. "
    "Eval cả bộ: `python prototype/run_eval.py`"
)
