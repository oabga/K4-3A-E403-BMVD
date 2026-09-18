"""
VLearn Extend — Streamlit UI (cùng logic server.py)

Luồng NEED_EXTERNAL:
  1) Tra corpus → gắn nhãn
  2) Hiện danh sách nguồn MOCK → HV chọn → Nhập
  3) Gọi AI thật chỉ viết từ notebook (lớp + nguồn đã chọn)

Chạy (từ thư mục repo gốc):
  pip install -r codebase/requirements.txt
  streamlit run codebase/streamlit_app.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st

PROTO = Path(__file__).resolve().parent
sys.path.insert(0, str(PROTO))

from extend import answer_for, load_dotenv, read_json  # noqa: E402

st.set_page_config(page_title="VLearn Extend · CP4", page_icon="📘", layout="wide")
load_dotenv()

excerpts = read_json(PROTO / "corpus_excerpts.json")["excerpts"]
by_id = {ex["id"]: ex for ex in excerpts}
mock_pack = read_json(PROTO / "external_mock.json")
mock_by_id = {s["id"]: s for s in mock_pack.get("sources", [])}

PRESETS = [
    (
        "IN · AI / ML / DL",
        "AI, Machine Learning, Deep Learning và Generative AI khác nhau như thế nào theo bài Day 1?",
        "allow_mock",
    ),
    (
        "IN · Turing Test",
        "Turing Test kiểm tra điều gì?",
        "allow_mock",
    ),
    (
        "IN · LLM là gì",
        "LLM là gì?",
        "allow_mock",
    ),
    (
        "NEED · lịch sử LLM",
        "Lịch sử LLM là gì? Ai là người tạo ra hướng mô hình này?",
        "allow_mock",
    ),
    (
        "NEED · ví dụ ngoài slide",
        "Slide có nói Self-Attention, nhưng cho em ví dụ đời thực ngoài slide để hiểu vì sao nó nhìn toàn bộ câu tốt hơn RNN.",
        "allow_mock",
    ),
    (
        "CANNOT · DOI (deny)",
        "Cho DOI paper Attention Is All You Need để em trích dẫn, nhưng môi trường đang cấm fetch web.",
        "deny",
    ),
    (
        "SCOPE · lệch môn",
        "công thức phương trình bậc 2 là gì?",
        "allow_mock",
    ),
    (
        "SCOPE · làm hộ lab",
        "Viết hộ toàn bộ code bài lab 1 tính toán token và gọi API để nộp.",
        "allow_mock",
    ),
]

LABEL_COLOR = {
    "IN_CORPUS": "green",
    "NEED_EXTERNAL": "orange",
    "CANNOT_FETCH": "red",
    "ASK_AGAIN": "blue",
    "OUT_OF_SCOPE": "violet",
}

# session defaults
for k, v in {
    "pending_q": None,
    "pending_policy": "allow_mock",
    "candidates": [],
    "last_result": None,
    "chat_log": [],
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


def push_log(role: str, text: str):
    st.session_state.chat_log.append({"role": role, "text": text})


def render_answer(result: dict):
    label = result.get("label") or "?"
    st.markdown(
        f"**Nhãn:** :{LABEL_COLOR.get(label, 'gray')}[**{label}**] · "
        f"AI=`{result.get('ai')}` · `{result.get('model') or ''}`"
    )
    st.caption(" · ".join(result.get("mock_parts") or []))
    if result.get("fetch_detail"):
        st.caption(result["fetch_detail"])
    st.markdown("#### Câu trả lời")
    st.write(result.get("answer") or "")
    if result.get("ask_again"):
        st.warning(f"Hỏi lại: {result['ask_again']}")
    if result.get("search_brief"):
        st.markdown("#### Brief 3 truy vấn")
        for i, t in enumerate(result["search_brief"], 1):
            st.write(f"{i}. `{t}`")
    ids = result.get("notebook_ids") or []
    if ids:
        st.markdown("#### Nguồn notebook")
        st.code(", ".join(ids))
        for nid in ids:
            if nid in by_id:
                with st.expander(f"{nid} (lớp) — {by_id[nid]['title']}"):
                    st.write(by_id[nid]["text"])
            elif nid in mock_by_id:
                with st.expander(f"{nid} (ngoài · MOCK) — {mock_by_id[nid]['title']}"):
                    st.write(mock_by_id[nid]["text"])


st.title("VLearn Extend · CP4")
st.caption(
    "Giống `server.py`: AI thật viết câu trả lời · fetch/retry = **MOCK** · "
    "NEED_EXTERNAL → chọn nguồn rồi **Nhập**."
)

# ─── Sidebar: status + corpus ───
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
        st.error("Thiếu key trong `.env` (thư mục gốc repo)")
    st.warning("Fetch = MOCK")
    st.markdown("### Corpus Day 1")
    for ex in excerpts:
        with st.expander(f"{ex['id']}"):
            st.caption(ex["title"])
            st.write(ex["text"])

# ─── Layout: nguồn | hỏi đáp ───
col_src, col_main = st.columns([1.05, 1.2], gap="large")

with col_src:
    st.subheader("Nguồn › Khám phá nguồn")
    st.caption("MOCK — chỉ hiện khi câu hỏi liên quan bài nhưng slide chưa đủ.")
    pending_q = st.session_state.pending_q
    candidates = st.session_state.candidates or []

    if pending_q:
        st.text_input("Truy vấn", value=pending_q, disabled=True, key="discover_q")
        st.caption(f"{len(candidates)} ứng viên MOCK")
        default_ids = [c["id"] for c in candidates[:2]] if candidates else []
        options = {
            f"{c['id']} · {c.get('site', 'mock')} — {c['title']}": c["id"] for c in candidates
        }
        picked_labels = st.multiselect(
            "Chọn nguồn (có thể chọn nhiều)",
            list(options.keys()),
            default=[k for k, v in options.items() if v in default_ids],
            key="picked_labels",
        )
        picked_ids = [options[k] for k in picked_labels]
        st.write(f"Đã chọn **{len(picked_ids)}** nguồn")
        for c in candidates:
            if c["id"] in picked_ids:
                with st.expander(f"✓ {c['id']}", expanded=False):
                    st.caption(c.get("site", "mock"))
                    st.write(c.get("snippet") or c.get("title"))
        import_go = st.button("Nhập", type="primary", use_container_width=True, disabled=not picked_ids)
        if import_go and picked_ids and pending_q:
            push_log("user", f"Nhập {len(picked_ids)} nguồn cho: {pending_q}")
            with st.spinner("Đang tổng hợp từ nguồn đã chọn…"):
                result = answer_for(
                    pending_q,
                    st.session_state.pending_policy,
                    selected_ids=picked_ids,
                    interactive=True,
                )
            st.session_state.last_result = result
            st.session_state.pending_q = None
            st.session_state.candidates = []
            if result.get("technical_error"):
                push_log("bot", "Lỗi kỹ thuật: " + result["technical_error"])
            else:
                push_log(
                    "bot",
                    f"[{result.get('label')}] {result.get('answer') or ''}"
                    + (f"\nHỏi lại: {result['ask_again']}" if result.get("ask_again") else ""),
                )
            st.rerun()
    else:
        st.info("Khi NEED_EXTERNAL, danh sách nguồn MOCK hiện ở đây — chọn rồi bấm **Nhập**.")

with col_main:
    st.subheader("Hỏi đáp")
    names = ["(gõ tay)"] + [p[0] for p in PRESETS]
    preset = st.selectbox("Gợi ý demo", names)
    preset_q, policy = "", "allow_mock"
    if not preset.startswith("(gõ tay"):
        for name, question, pol in PRESETS:
            if name == preset:
                preset_q, policy = question, pol
                break

    if "last_preset" not in st.session_state:
        st.session_state.last_preset = preset
    if preset != st.session_state.last_preset:
        st.session_state.last_preset = preset
        st.session_state.question = preset_q

    if "question" not in st.session_state:
        st.session_state.question = preset_q

    question = st.text_area("Câu hỏi", key="question", height=90)
    policy = st.selectbox(
        "Fetch policy (MOCK)",
        ["allow_mock", "deny", "fail_after_retry"],
        index=["allow_mock", "deny", "fail_after_retry"].index(policy)
        if policy in ("allow_mock", "deny", "fail_after_retry")
        else 0,
    )

    go = st.button("Gửi AI", type="primary", use_container_width=True)
    if go:
        q = (question or "").strip()
        if not q:
            st.warning("Nhập câu hỏi.")
        else:
            push_log("user", q)
            with st.spinner("Tra corpus / tìm nguồn…"):
                result = answer_for(q, policy, interactive=True)
            if result.get("technical_error"):
                st.session_state.last_result = result
                push_log("bot", "Lỗi kỹ thuật: " + result["technical_error"])
            elif result.get("need_selection"):
                st.session_state.pending_q = q
                st.session_state.pending_policy = policy
                st.session_state.candidates = result.get("candidates") or []
                st.session_state.last_result = result
                push_log(
                    "bot",
                    f"[NEED_EXTERNAL] Corpus lớp chưa đủ.\n"
                    f"Đã tìm {len(st.session_state.candidates)} nguồn MOCK (bên trái).\n"
                    f"Chọn nguồn → bấm Nhập → AI mới trả lời.",
                )
            else:
                st.session_state.pending_q = None
                st.session_state.candidates = []
                st.session_state.last_result = result
                push_log(
                    "bot",
                    f"[{result.get('label')}] {result.get('answer') or ''}"
                    + (f"\nHỏi lại: {result['ask_again']}" if result.get("ask_again") else ""),
                )
            st.rerun()

    st.markdown("#### Kết quả mới nhất")
    if st.session_state.last_result:
        if st.session_state.last_result.get("technical_error"):
            st.error(st.session_state.last_result["technical_error"])
        elif st.session_state.last_result.get("need_selection"):
            st.info("Đang chờ chọn nguồn bên trái rồi bấm **Nhập**.")
        else:
            render_answer(st.session_state.last_result)
    else:
        st.caption("Chưa có kết quả — chọn gợi ý hoặc gõ câu hỏi rồi Gửi AI.")

    with st.expander("Nhật ký hội thoại"):
        for row in st.session_state.chat_log[-12:]:
            st.markdown(f"**{row['role']}:** {row['text']}")

st.divider()
st.markdown(
    "Cùng pipeline với `python codebase/server.py`. "
    "Eval: `python codebase/run_eval.py`"
)
