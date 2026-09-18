"""VLearn Extend pipeline. Fetch/retry = MOCK. Câu trả lời = AI thật (OpenAI hoặc Gemini)."""
from __future__ import annotations

import json
import os
import re
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTO = Path(__file__).resolve().parent


def load_dotenv():
    path = ROOT / ".env"
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fold(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.lower()


def load_prompt() -> str:
    raw = (ROOT / "eval" / "prompt.md").read_text(encoding="utf-8")
    m = re.search(r"```\n(.*)\n```", raw, re.S)
    return m.group(1).strip() if m else raw


STOPWORDS = {
    "la", "gi", "cua", "va", "cac", "mot", "nhung", "cho", "em", "voi", "the",
    "nao", "nhu", "theo", "bai", "slide", "day", "trong", "ngoai", "co", "khong",
    "duoc", "de", "toi", "minh", "ban", "hay", "hoac", "neu", "khi", "thi",
    "rat", "qua", "nay", "do", "ay", "ve", "tu", "len", "xuong", "ra", "vao",
    "what", "is", "the", "a", "an", "of", "to", "in", "on", "for", "and", "or",
    "how", "why", "when", "where", "does", "do", "are", "was", "were", "be",
    "bao", "nhieu", "nam", "goi", "giup", "hoi", "xin", "them", "nguoi",
}

# Khái niệm / thực thể có trong (hoặc neo trực tiếp từ) corpus Day 1
DOMAIN_TERMS = {
    "ai", "ml", "dl", "llm", "machine", "learning", "deep", "generative",
    "turing", "symbolic", "transformer", "attention", "rnn", "lstm",
    "token", "tokenizer", "context", "rot", "window", "hallucination",
    "giac", "alphago", "imagenet", "neuron", "gpt", "rag", "prediction",
    "expert", "winter", "sedol",
}

HOMEWORK_RE = (
    r"viet ho|lam ho|bai tap|lab 1|hoan chinh de nop|bao cao giua ky|"
    r"kinh te luong|soan giup|viet ho toan bo code"
)

# Neo chủ đề buổi học (phải có ít nhất một khi hỏi mở rộng lịch sử / người tạo)
TOPIC_ANCHOR_RE = (
    r"\b(ai|llm|ml|dl|transformer|attention|self-?attention|token|tokenizer|"
    r"alphago|imagenet|gpt|rnn|lstm|hallucin|context\s*rot|symbolic|"
    r"deep\s*learning|machine\s*learning|generative|turing|rag)\b"
)

# Người / tổ chức liên quan trực tiếp nội dung slide (được hỏi mở rộng tiểu sử / lịch sử)
RELATED_PEOPLE_RE = (
    r"turing|fei-?fei|lee\s*sedol|deepmind|vaswani|hinton|lecun|"
    r"openai|google\s*brain|attention is all you need"
)


def content_tokens(text: str) -> set[str]:
    raw = set(re.findall(r"[a-z0-9]+", fold(text)))
    keep = set()
    for t in raw:
        if t in DOMAIN_TERMS:
            keep.add(t)
        elif len(t) >= 3 and t not in STOPWORDS:
            keep.add(t)
    return keep


def is_homework(question: str) -> bool:
    return bool(re.search(HOMEWORK_RE, fold(question)))


def topic_related(question: str) -> bool:
    """Chỉ cho hỏi khi neo được vào chủ đề Day 1 (hoặc mở rộng trực tiếp: lịch sử LLM, người tạo…)."""
    q = fold(question)
    tokens = content_tokens(question)
    if tokens & DOMAIN_TERMS:
        return True
    if re.search(RELATED_PEOPLE_RE, q):
        return True
    expansion = re.search(
        r"lich su|nguoi tao|phat minh|sang lap|inventor|founder|"
        r"ra doi|lan dau|dau tien|ai (da )?(tao|phat minh|viet|cong bo)|"
        r"tieu su|biography|ai sang tao",
        q,
    )
    if expansion and re.search(TOPIC_ANCHOR_RE, q):
        return True
    return False


def asks_beyond_slide(question: str) -> bool:
    """Xin mở rộng ngoài nội dung đã có trên slide (vẫn neo chủ đề)."""
    q = fold(question)
    return bool(
        re.search(
            r"ngoai slide|vi du doi thuc|trong thuc te|ngoai viec|"
            r"chatbot doanh nghiep|tokenizer cua gpt|gpt-4|"
            r"doc them tren mang|tim docs chinh thuc|"
            r"lich su|nguoi tao|phat minh|dau tien|tieu su|ra doi|"
            r"mo rong|dao sau hon|chi tiet hon ve nguoi",
            q,
        )
    )


def corpus_sufficient(question: str, hits: list[dict]) -> bool:
    """
    Corpus đủ khi đoạn lớp phủ được ý hỏi.
    Câu ngắn kiểu "LLM là gì?" / "Turing Test là gì?" chỉ có 1–2 token nội dung
    → không đòi score >= 3 (tránh gán nhầm NEED_EXTERNAL).
    """
    if not hits:
        return False
    q_tokens = content_tokens(question)
    if not q_tokens:
        return False
    top = hits[0]
    blob_tokens = content_tokens(top.get("title", "") + " " + top.get("text", ""))
    covered = q_tokens & blob_tokens
    # Câu ngắn: mọi token nội dung đều nằm trong đoạn hit → đủ slide
    if covered == q_tokens:
        return True
    # Câu dài hơn: cần overlap mạnh
    if top.get("score", 0) >= 3 and len(covered) >= 2:
        return True
    # Một khái niệm miền khớp rõ title (vd. LLM, Turing, Transformer…)
    title_tokens = content_tokens(top.get("title", ""))
    if (q_tokens & DOMAIN_TERMS & title_tokens) and len(covered) >= 1:
        return True
    return False


def rank_mock_sources(question: str, sources: list[dict]) -> list[dict]:
    """Xếp ứng viên MOCK theo câu hỏi — ưu tiên đúng chủ đề, tránh nguồn lạc đề."""
    q = fold(question)
    q_tokens = content_tokens(question)
    weak = {"lich", "su", "nguoi", "tao", "dau", "tien", "them", "doc", "cho", "minh"}
    strong_q = q_tokens - weak

    scored = []
    for s in sources:
        blob = fold(s.get("title", "") + " " + s.get("text", "") + " " + s.get("id", ""))
        blob_t = content_tokens(blob)
        score = 3 * len(strong_q & blob_t) + len(q_tokens & blob_t)

        # Neo đúng nguồn theo chủ đề hỏi (điểm cao)
        topic_rules = (
            (r"turing|alan", "MOCK-EXT-11", 25),
            (r"lich su (cua )?(llm|gpt)|llm ra doi|nguoi tao.*llm|ai tao.*llm", "MOCK-EXT-09", 22),
            (r"vaswani|nguoi tao.*transformer|phat minh.*transformer|cong bo.*transformer", "MOCK-EXT-10", 22),
            (r"fei-?fei|imagenet", "MOCK-EXT-07", 18),
            (r"alphago|lee sedol|deepmind|nuoc (di )?37", "MOCK-EXT-08", 18),
            (r"context rot|chatbot doanh nghiep", "MOCK-EXT-02", 16),
            (r"tokenizer|gpt-4|token tieng viet", "MOCK-EXT-03", 16),
            (r"vi du doi thuc|self-attention.*rnn|rnn.*self-attention", "MOCK-EXT-01", 16),
            (r"hallucin|ao giac|production", "MOCK-EXT-05", 14),
            (r"next.?token|ban chat llm", "MOCK-EXT-04", 12),
            (r"attention is all|transformer paper", "MOCK-EXT-06", 12),
        )
        for pat, sid, boost in topic_rules:
            if re.search(pat, q) and s["id"] == sid:
                score += boost

        # Đang hỏi Turing mà nguồn không nhắc Turing → hạ mạnh (tránh Self-Attention / hallucination)
        if re.search(r"turing|alan", q) and not re.search(r"turing|alan", blob):
            score -= 12
        if re.search(r"\bllm\b", q) and re.search(r"lich su|nguoi tao|ra doi", q):
            if s["id"] not in ("MOCK-EXT-09", "MOCK-EXT-04", "MOCK-EXT-11") and not re.search(
                r"\bllm\b|gpt|ngon ngu", blob
            ):
                score -= 8

        scored.append({**s, "score": score})

    scored.sort(key=lambda x: (-x["score"], x["id"]))
    if not scored:
        return []
    best = scored[0]["score"]
    # Chỉ giữ nguồn thực sự liên quan (không đổ cả 11 cái lạc đề)
    if best >= 10:
        kept = [s for s in scored if s["score"] >= max(4, best * 0.35)]
        return kept[:5]
    return [s for s in scored if s["score"] > 0][:5]


def retrieve(question: str, excerpts: list[dict], corpus_refs: list[str] | None = None) -> list[dict]:
    if corpus_refs:
        by_id = {ex["id"]: ex for ex in excerpts}
        hits = []
        for ref in corpus_refs:
            if ref in by_id:
                hits.append({**by_id[ref], "score": 10})
        if hits:
            return hits[:3]

    q_tokens = content_tokens(question)
    weak = {"lich", "su", "nguoi", "tao", "dau", "tien", "them", "doc", "cho", "minh"}
    strong_q = q_tokens - weak
    hits = []
    for ex in excerpts:
        title_t = content_tokens(ex["title"] + " " + ex["id"])
        body_t = content_tokens(ex["text"])
        blob_t = title_t | body_t
        overlap = q_tokens & blob_t
        strong_overlap = strong_q & blob_t
        if not overlap:
            continue
        # Bỏ hit chỉ vì chữ yếu kiểu "lịch sử" (dễ kéo nhầm AlphaGo)
        if not strong_overlap and not (q_tokens & DOMAIN_TERMS & blob_t):
            continue
        score = len(strong_overlap) * 3 + len(overlap) + 2 * len(q_tokens & title_t)
        hits.append({**ex, "score": score})
    hits.sort(key=lambda x: -x["score"])
    return hits[:3]


def decide(question: str, hits: list[dict], fetch_policy: str) -> str:
    q = fold(question)

    if is_homework(question):
        return "OUT_OF_SCOPE"

    if re.search(r"giai thich cai nay|cai nay giup|giai thich giup em cai nay", q):
        return "ASK_AGAIN"
    if re.search(r"thong ke|xac suat|bien ngau nhien", q):
        return "ASK_AGAIN"

    # Lệch môn hoàn toàn (PT bậc 2, lịch sử VN, …) — không mở nguồn ngoài
    if not topic_related(question):
        return "OUT_OF_SCOPE"

    if re.search(
        r"doi\s*10\.|doi paper|cho doi|ma doi|doi bai|paper smith|10\.\d{4}/|"
        r"(doi|link|pdf).{0,40}(arxiv|ieee)|(arxiv|ieee).{0,40}(doi|link|pdf)",
        q,
    ):
        return "CANNOT_FETCH"
    if fetch_policy == "deny":
        return "CANNOT_FETCH"
    if fetch_policy == "fail_after_retry":
        return "CANNOT_FETCH"

    # Xin mở rộng ngoài slide → NEED_EXTERNAL (dù corpus có khái niệm nền)
    if asks_beyond_slide(question):
        return "NEED_EXTERNAL"

    # Định nghĩa / hỏi đúng nội dung đã có trên slide → IN_CORPUS
    if corpus_sufficient(question, hits):
        return "IN_CORPUS"
    return "NEED_EXTERNAL"


def mock_fetch(
    fetch_policy: str,
    question: str = "",
    selected_ids: list[str] | None = None,
    all_candidates: bool = False,
) -> dict:
    """Nguồn ngoài: MOCK. Retry: MOCK. all_candidates=True → trả list để HV chọn."""
    if fetch_policy == "deny":
        return {"ok": False, "sources": [], "retry_count": 0, "detail": "MOCK policy deny — không fetch"}
    if fetch_policy == "fail_after_retry":
        return {
            "ok": False,
            "sources": [],
            "retry_count": 2,
            "detail": "MOCK timeout ×2 rồi hết lần retry",
        }
    pack = read_json(PROTO / "external_mock.json")
    ranked = rank_mock_sources(question, pack["sources"])
    if all_candidates:
        return {
            "ok": True,
            "sources": ranked,
            "retry_count": 0,
            "detail": "MOCK đề xuất nguồn — chờ HV chọn và Nhập",
        }
    if selected_ids:
        by_id = {s["id"]: s for s in pack["sources"]}
        picked = [by_id[i] for i in selected_ids if i in by_id]
        if not picked:
            picked = ranked[:1]
        return {
            "ok": True,
            "sources": picked,
            "retry_count": 0,
            "detail": f"MOCK nạp {len(picked)} nguồn HV đã chọn",
        }
    # Eval / non-interactive: auto lấy 1 nguồn xếp hạng cao nhất
    picked = ranked[:1] if ranked else []
    return {"ok": True, "sources": picked, "retry_count": 0, "detail": "MOCK auto-nạp (không interactive)"}


def build_notebook(label: str, hits: list[dict], fetch: dict) -> str:
    lines = [f"LABEL={label}", "NOTEBOOK_LOP:"]
    for h in hits:
        lines.append(f"[{h['id']}] {h['title']}: {h['text']}")
    if not hits:
        lines.append("(khong co hit)")
    lines.append("NOTEBOOK_NGOAI:")
    if label == "NEED_EXTERNAL" and fetch.get("ok"):
        for s in fetch["sources"]:
            lines.append(f"[{s['id']}] {s['title']}: {s['text']}")
    else:
        lines.append("(khong nap nguon ngoai)")
    return "\n".join(lines)


class TechnicalError(Exception):
    pass


def _http_json(url: str, payload: dict, headers: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise TechnicalError(f"HTTP {e.code}: {body[:400]}") from e
    except urllib.error.URLError as e:
        raise TechnicalError(f"Mạng/timeout: {e}") from e


def call_llm(notebook: str, question: str) -> tuple[dict, str]:
    prompt = load_prompt()
    user = f"{prompt}\n\nCAU_HOI:\n{question}\n\n{notebook}\n"
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip() or os.environ.get("GOOGLE_API_KEY", "").strip()

    if openai_key:
        model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"
        base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        data = _http_json(
            f"{base}/chat/completions",
            {
                "model": model,
                "temperature": 0,
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user},
                ],
            },
            {"Authorization": f"Bearer {openai_key}"},
        )
        content = data["choices"][0]["message"]["content"]
        return json.loads(content), f"openai:{model}"

    if gemini_key:
        model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash").strip() or "gemini-2.0-flash"
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            f"?key={gemini_key}"
        )
        data = _http_json(
            url,
            {
                "contents": [{"parts": [{"text": user}]}],
                "generationConfig": {"temperature": 0, "responseMimeType": "application/json"},
            },
            {},
        )
        content = data["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(content), f"gemini:{model}"

    raise TechnicalError("Thiếu OPENAI_API_KEY hoặc GEMINI_API_KEY trong .env — chưa nối được AI thật")


def answer_for(
    question: str,
    fetch_policy: str = "allow_mock",
    corpus_refs: list[str] | None = None,
    selected_ids: list[str] | None = None,
    interactive: bool = False,
) -> dict:
    load_dotenv()
    excerpts = read_json(PROTO / "corpus_excerpts.json")["excerpts"]
    hits = retrieve(question, excerpts, corpus_refs=corpus_refs)
    label = decide(question, hits, fetch_policy)
    fetch = {"ok": False, "sources": [], "retry_count": 0, "detail": "không fetch"}
    mock_parts = ["fetch=MOCK", "retry=MOCK", "corpus=excerpt mã D1-P* (không commit data pack)"]

    # Ngoài chủ đề buổi học (không phải làm hộ bài) — từ chối sớm, không mở nguồn
    if label == "OUT_OF_SCOPE" and not is_homework(question):
        return {
            "label": "OUT_OF_SCOPE",
            "need_selection": False,
            "candidates": [],
            "answer": (
                "Câu hỏi không liên quan chủ đề buổi học Day 1 (AI & LLM Foundation).\n"
                "Bạn có thể hỏi nội dung trên slide, hoặc mở rộng trực tiếp từ đó "
                "(ví dụ: lịch sử LLM, ai công bố Transformer, tiểu sử Alan Turing / Fei-Fei Li…).\n"
                "Không trả lời các chủ đề lệch môn (toán phổ thông, lịch sử chung, môn khác…)."
            ),
            "ask_again": "Bạn muốn hỏi khái niệm nào trên slide Day 1, hay mở rộng lịch sử/người liên quan đến khái niệm đó?",
            "citations": [],
            "search_brief": None,
            "retry_count": 0,
            "notebook_ids": [h["id"] for h in hits],
            "fetch_detail": "không fetch — ngoài phạm vi chủ đề bài",
            "mock_parts": mock_parts,
            "model": None,
            "technical_error": None,
            "ai": "RULE",
        }

    if label == "NEED_EXTERNAL":
        # Bước 1 (UI): đề xuất list nguồn, chờ HV chọn + Nhập — chưa gọi LLM
        if interactive and not selected_ids:
            propose = mock_fetch(fetch_policy, question, all_candidates=True)
            if not propose["ok"]:
                label = "CANNOT_FETCH"
                fetch = propose
            else:
                return {
                    "label": "NEED_EXTERNAL",
                    "need_selection": True,
                    "candidates": [
                        {
                            "id": s["id"],
                            "site": s.get("site", "mock"),
                            "title": s["title"],
                            "snippet": (s["text"][:160] + "…") if len(s["text"]) > 160 else s["text"],
                            "score": s.get("score", 0),
                        }
                        for s in propose["sources"]
                    ],
                    "answer": "",
                    "ask_again": None,
                    "citations": [],
                    "search_brief": None,
                    "retry_count": propose.get("retry_count", 0),
                    "notebook_ids": [h["id"] for h in hits],
                    "fetch_detail": propose.get("detail"),
                    "mock_parts": mock_parts + ["ui=chọn nguồn kiểu NotebookLM"],
                    "model": None,
                    "technical_error": None,
                    "ai": "CHO_NGUON",
                }
        fetch = mock_fetch(fetch_policy, question, selected_ids=selected_ids)
        if not fetch["ok"]:
            label = "CANNOT_FETCH"
    if label == "CANNOT_FETCH" and fetch_policy == "fail_after_retry":
        fetch = mock_fetch("fail_after_retry", question)

    notebook = build_notebook(label, hits, fetch)
    try:
        llm, model_id = call_llm(notebook, question)
        ai = "THAT"
    except TechnicalError as e:
        return {
            "label": label,
            "need_selection": False,
            "candidates": [],
            "answer": "",
            "ask_again": None,
            "citations": [],
            "search_brief": None,
            "retry_count": fetch.get("retry_count", 0),
            "notebook_ids": [h["id"] for h in hits],
            "fetch_detail": fetch.get("detail"),
            "mock_parts": mock_parts,
            "model": None,
            "technical_error": str(e),
            "ai": "LOI",
        }

    brief = None
    if label == "CANNOT_FETCH":
        brief = [
            "Attention Is All You Need Google 2017",
            "official tokenizer documentation Vietnamese",
            "context window management RAG chatbot",
        ]

    return {
        "label": label,
        "need_selection": False,
        "candidates": [],
        "answer": llm.get("answer", ""),
        "ask_again": llm.get("ask_again"),
        "citations": llm.get("citations_used") or [],
        "search_brief": brief,
        "retry_count": fetch.get("retry_count", 0),
        "notebook_ids": [h["id"] for h in hits]
        + ([s["id"] for s in fetch.get("sources", [])] if label == "NEED_EXTERNAL" else []),
        "fetch_detail": fetch.get("detail"),
        "mock_parts": mock_parts,
        "model": model_id,
        "technical_error": None,
        "ai": ai,
    }
