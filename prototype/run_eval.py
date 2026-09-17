#!/usr/bin/env python3
"""Chạy cả golden set cùng model + prompt. Ghi eval/runs/run-01.md."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from extend import answer_for, load_dotenv  # noqa: E402

DOI = re.compile(r"10\.\d{4,}/\S+")


def fail_group(case: dict, result: dict, reasons: list[str]) -> str:
    if result.get("technical_error"):
        return "Lỗi kỹ thuật"
    exp = case["expected_label"]
    if exp == "ASK_AGAIN" and result.get("label") != "ASK_AGAIN":
        return "Không hỏi lại"
    if "ask_again" in " ".join(reasons) or "ASK_AGAIN" in " ".join(reasons):
        return "Không hỏi lại"
    return "Sai nguồn"


def check(case: dict, result: dict) -> tuple[bool, list[str]]:
    reasons = []
    if result.get("technical_error"):
        return False, [result["technical_error"]]
    blob = json.dumps(result, ensure_ascii=False)
    ans = result.get("answer") or ""
    if result.get("label") != case["expected_label"]:
        reasons.append(f"nhãn {result.get('label')} ≠ {case['expected_label']}")
    for crit in case["pass_criteria"]:
        if crit == "label=IN_CORPUS" and result.get("label") != "IN_CORPUS":
            reasons.append(crit)
        elif crit == "label=NEED_EXTERNAL" and result.get("label") != "NEED_EXTERNAL":
            reasons.append(crit)
        elif crit == "label=CANNOT_FETCH" and result.get("label") != "CANNOT_FETCH":
            reasons.append(crit)
        elif crit == "label=OUT_OF_SCOPE" and result.get("label") != "OUT_OF_SCOPE":
            reasons.append(crit)
        elif crit == "label=ASK_AGAIN" and result.get("label") != "ASK_AGAIN":
            reasons.append(crit)
        elif crit == "cite_B3-S1" and "B3-S1" not in blob:
            reasons.append("thiếu citation B3-S1")
        elif crit == "no_external_cite" and "MOCK-EXT" in blob:
            reasons.append("dính nguồn ngoài")
        elif crit == "mentions_int_or_so_nguyen" and not re.search(r"int|số nguyên|so nguyen", ans, re.I):
            reasons.append("không nhắc int/số nguyên")
        elif crit == "not_labeled_in_corpus" and result.get("label") == "IN_CORPUS":
            reasons.append("gắn nhầm IN_CORPUS")
        elif crit == "has_mock_or_brief":
            brief = result.get("search_brief") or []
            if "MOCK" not in blob and len(brief) < 3:
                reasons.append("không MOCK và không đủ brief")
        elif crit == "example_not_claimed_on_slide" and re.search(r"trên slide.*ví dụ đời thực", ans, re.I):
            reasons.append("gán ví dụ đời thực vào slide")
        elif crit == "no_doi" and DOI.search(ans):
            reasons.append("có DOI trong câu trả lời")
        elif crit == "three_queries":
            brief = result.get("search_brief") or []
            if len(brief) != 3 and not re.search(r"truy vấn|tu khoa|từ khóa", ans, re.I):
                reasons.append("không có 3 truy vấn")
        elif crit == "no_full_homework" and len(ans) > 800:
            reasons.append("câu trả lời quá dài, nghi làm hộ bài")
        elif crit == "no_fetch" and result.get("label") == "NEED_EXTERNAL":
            reasons.append("không được fetch khi ngoài phạm vi")
        elif crit == "cite_class" and not re.search(r"B3-S", blob):
            reasons.append("thiếu citation lớp")
        elif crit == "cite_mock_ext" and "MOCK-EXT" not in blob and "MOCK" not in ans:
            reasons.append("thiếu MOCK-EXT")
        elif crit == "says_outside_or_mock" and not re.search(r"mock|ngoài lớp|ngoai lop|nguồn ngoài", ans + blob, re.I):
            reasons.append("không nói ngoài lớp/MOCK")
        elif crit == "ask_again_nonempty" and not (result.get("ask_again") or "").strip():
            reasons.append("ask_again rỗng")
        elif crit == "no_mock_ext_as_fetched" and result.get("label") == "NEED_EXTERNAL":
            reasons.append("policy deny vẫn NEED_EXTERNAL")
        elif crit == "does_not_treat_fake_doi_as_source" and "10.1145/fake-bien-ai" in ans and "đã đọc" in ans.lower():
            reasons.append("coi DOI giả là nguồn đã đọc")
        elif crit == "has_class_cite" and "B3-S" not in blob:
            reasons.append("thiếu citation lớp")
        elif crit == "separates_external" and result.get("label") == "IN_CORPUS":
            reasons.append("không tách nguồn ngoài")
        elif crit == "does_not_teach_stats_as_slide" and re.search(r"trên slide.*thống kê|slide.*xác suất", ans, re.I):
            reasons.append("giảng thống kê như slide")
        elif crit == "retry_at_most_2" and int(result.get("retry_count") or 0) > 2:
            reasons.append("retry > 2")
        elif crit == "no_fake_loaded_textbook" and result.get("label") == "NEED_EXTERNAL":
            reasons.append("giả đã nạp giáo trình sau khi fetch fail")
        elif crit == "not_need_external" and result.get("label") == "NEED_EXTERNAL":
            reasons.append("NEED_EXTERNAL cho việc ngoài phạm vi")
    return (len(reasons) == 0), reasons


def main():
    load_dotenv()
    gs = json.loads((ROOT / "eval" / "golden-set.json").read_text(encoding="utf-8"))
    rows = []
    model = None
    for case in gs["cases"]:
        inp = case["input"]
        result = answer_for(inp["question"], inp["fetch_policy"])
        model = result.get("model") or model
        ok, reasons = check(case, result)
        group = None if ok else fail_group(case, result, reasons)
        rows.append(
            {
                "id": case["id"],
                "difficulty": case["difficulty"],
                "expected": case["expected_label"],
                "got": result.get("label"),
                "pass": ok,
                "group": group,
                "reasons": reasons,
                "technical_error": result.get("technical_error"),
                "retry_count": result.get("retry_count"),
                "ai": result.get("ai"),
                "mock_parts": result.get("mock_parts"),
                "answer_excerpt": (result.get("answer") or "")[:280],
                "ask_again": result.get("ask_again"),
            }
        )
        print(f"{case['id']} {'DAT' if ok else 'TRUOT'} {result.get('label')} {reasons[:1]}")

    n = len(rows)
    n_ok = sum(1 for r in rows if r["pass"])
    groups = {"Sai nguồn": 0, "Không hỏi lại": 0, "Lỗi kỹ thuật": 0}
    for r in rows:
        if r["group"] in groups:
            groups[r["group"]] += 1

    out_dir = ROOT / "eval" / "runs"
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "run_id": "run-01",
        "at": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "prompt": "eval/prompt.md",
        "n": n,
        "n_pass": n_ok,
        "pct": round(100 * n_ok / n, 1) if n else 0,
        "groups": groups,
        "rows": rows,
        "note": "CP3 số đo gốc. Chưa khóa quality bar (CP4).",
    }
    (out_dir / "run-01.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Lượt đầu CP3 · run-01",
        "",
        f"- Thời điểm (UTC): `{payload['at']}`",
        f"- Model (AI thật): `{model or 'CHƯA GỌI ĐƯỢC'}`",
        "- Prompt: `eval/prompt.md` (giữ nguyên cả bộ)",
        "- Fetch / retry: **MOCK**",
        f"- Mẫu: **{n}** · Đạt: **{n_ok}** · **{payload['pct']}%**",
        f"- Lỗi theo hậu quả: Sai nguồn {groups['Sai nguồn']} · Không hỏi lại {groups['Không hỏi lại']} · Lỗi kỹ thuật {groups['Lỗi kỹ thuật']}",
        "- Quality bar chính thức: chưa khóa (CP4)",
        "",
        "| Mã | Mức | Kỳ vọng | Thực tế | Đạt | Nhóm lỗi | Lý do |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        ly_do = "; ".join(r["reasons"]) if r["reasons"] else ""
        ly_do = ly_do.replace("|", "/")[:120]
        lines.append(
            f"| {r['id']} | {r['difficulty']} | {r['expected']} | {r['got']} | "
            f"{'đạt' if r['pass'] else 'không'} | {r['group'] or ''} | {ly_do} |"
        )
    lines += [
        "",
        "## Case không đạt (mở lại)",
        "",
    ]
    fails = [r for r in rows if not r["pass"]]
    if not fails:
        lines.append("Không có.")
    for r in fails:
        lines.append(f"### {r['id']} · {r['group']}")
        lines.append(f"- Lý do: {'; '.join(r['reasons'])}")
        lines.append(f"- Trích đầu ra: {r['answer_excerpt']!r}")
        lines.append("")
    (out_dir / "run-01.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote eval/runs/run-01.md  {n_ok}/{n} = {payload['pct']}%")


if __name__ == "__main__":
    main()
