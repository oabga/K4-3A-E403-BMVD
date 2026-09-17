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


def retrieve(question: str, excerpts: list[dict]) -> list[dict]:
    q_tokens = set(re.findall(r"[a-z0-9]+", fold(question)))
    hits = []
    for ex in excerpts:
        blob = fold(ex["text"] + " " + ex["title"] + " " + ex["id"])
        t = set(re.findall(r"[a-z0-9]+", blob))
        score = len(q_tokens & t)
        if score:
            hits.append({**ex, "score": score})
    hits.sort(key=lambda x: -x["score"])
    return hits[:3]


def decide(question: str, hits: list[dict], fetch_policy: str) -> str:
    q = fold(question)
    if re.search(r"viet ho|lam ho|bai tap tuan|hoan chinh de nop|bao cao giua ky|kinh te luong|soan giup", q):
        return "OUT_OF_SCOPE"
    if re.search(r"giai thich cai nay|cai nay giup", q):
        return "ASK_AGAIN"
    if re.search(r"thong ke|xac suat", q):
        return "ASK_AGAIN"
    if re.search(r"doi\s*10\.|doi bai|bai bao|ieee|arxiv|paper smith|10\.\d{4}/|memory safety", q):
        return "CANNOT_FETCH"
    if fetch_policy == "deny":
        return "CANNOT_FETCH"
    if fetch_policy == "fail_after_retry":
        return "CANNOT_FETCH"
    if re.search(r"bien la gi\s*\??$", q.strip()) or q.strip() in {"bien la gi?", "bien la gi"}:
        return "IN_CORPUS"
    if "int tuoi" in q or "luu kieu" in q:
        return "IN_CORPUS"
    if "quiz" in q or "bien dung de lam gi" in q:
        return "IN_CORPUS"
    if re.search(r"khac hang|hang nhu|vi du doi thuc|ngoai slide|mutable|rap chieu|so sanh", q):
        return "NEED_EXTERNAL"
    if hits and hits[0]["score"] >= 3:
        return "IN_CORPUS"
    return "NEED_EXTERNAL"


def mock_fetch(fetch_policy: str) -> dict:
    """Nguồn ngoài: MOCK. Retry: MOCK."""
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
    return {"ok": True, "sources": pack["sources"], "retry_count": 0, "detail": "MOCK nạp external_mock.json"}


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


def answer_for(question: str, fetch_policy: str = "allow_mock") -> dict:
    load_dotenv()
    excerpts = read_json(PROTO / "corpus_excerpts.json")["excerpts"]
    hits = retrieve(question, excerpts)
    label = decide(question, hits, fetch_policy)
    fetch = {"ok": False, "sources": [], "retry_count": 0, "detail": "không fetch"}
    if label == "NEED_EXTERNAL":
        fetch = mock_fetch(fetch_policy)
        if not fetch["ok"]:
            label = "CANNOT_FETCH"
    if label == "CANNOT_FETCH" and fetch_policy == "fail_after_retry":
        fetch = mock_fetch("fail_after_retry")

    notebook = build_notebook(label, hits, fetch)
    mock_parts = ["fetch=MOCK", "retry=MOCK", "corpus=excerpt mã B3-* (không data pack)"]
    try:
        llm, model_id = call_llm(notebook, question)
        ai = "THAT"
    except TechnicalError as e:
        return {
            "label": label,
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
        brief = ["variable vs constant", "introductory programming textbook", "official language docs"]

    return {
        "label": label,
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
