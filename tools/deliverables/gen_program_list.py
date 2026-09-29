#!/usr/bin/env python3
"""Spring 컨트롤러에서 프로그램 목록(docs/product/generated/program-list.md)을 생성한다.

입력: <그룹>/api/src/main/java/**/*.java 의 @RestController/@Controller 와 매핑 애너테이션.
docs/product/api.md, interfaces.md 에 같은 메서드·경로가 있는지도 표시한다 (문서 누락 확인용).
사용:
    python3 tools/deliverables/gen_program_list.py          # 생성
    python3 tools/deliverables/gen_program_list.py --check  # 기존 파일과 다르면 exit 1
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/product/generated/program-list.md"
DOCS = [ROOT / "docs/product/api.md", ROOT / "docs/product/interfaces.md"]

MAPPINGS = {"GetMapping": "GET", "PostMapping": "POST", "PutMapping": "PUT",
            "PatchMapping": "PATCH", "DeleteMapping": "DELETE", "RequestMapping": None}
ANNOTATION = re.compile(r"@(\w+)\s*(\((?:[^()]|\([^()]*\))*\))?")


def paths_of(args: str | None) -> list[str]:
    if not args:
        return [""]
    m = re.search(r"(?:value|path)\s*=\s*(\{[^}]*\}|\"[^\"]*\")", args) or re.match(r"\(\s*(\{[^}]*\}|\"[^\"]*\")", args)
    return re.findall(r"\"([^\"]*)\"", m.group(1)) if m else [""]


def http_method_of(name: str, args: str | None) -> str:
    if MAPPINGS[name]:
        return MAPPINGS[name]
    m = re.search(r"RequestMethod\.(\w+)", args or "")
    return m.group(1) if m else "ANY"


def join(base: str, sub: str) -> str:
    path = "/" + "/".join(p.strip("/") for p in (base, sub) if p.strip("/"))
    return path


def parse_controller(src: str) -> tuple[str, list[dict]] | None:
    class_m = re.search(r"\bclass\s+(\w+)", src)
    if not class_m or not re.search(r"@(Rest)?Controller\b", src[: class_m.start()]):
        return None
    base = ""
    for a in ANNOTATION.finditer(src[: class_m.start()]):
        if a.group(1) == "RequestMapping":
            base = paths_of(a.group(2))[0]
    endpoints = []
    body = src[class_m.end():]
    prev_end = 0  # 직전 메서드 본문 시작 위치. 설명(@Operation)은 이 뒤에서만 찾는다
    for a in ANNOTATION.finditer(body):
        if a.group(1) not in MAPPINGS or a.start() < prev_end:
            continue
        after = body[a.end():]
        brace = after.find("{")
        head = after[: brace if brace >= 0 else 600]
        sig = re.search(r"\b(\w+)\s*\(", re.sub(r"@\w+\s*(\((?:[^()]|\([^()]*\))*\))?", "", head))
        summary = re.search(r"@Operation\s*\([^)]*summary\s*=\s*\"([^\"]*)\"", body[prev_end: a.start()] + head)
        prev_end = a.end() + max(brace, 0)
        for p in paths_of(a.group(2)):
            endpoints.append({
                "method": http_method_of(a.group(1), a.group(2)),
                "path": join(base, p),
                "handler": sig.group(1) if sig else "?",
                "summary": summary.group(1) if summary else "",
            })
    return class_m.group(1), endpoints


def documented() -> set[tuple[str, str]]:
    found = set()
    for doc in DOCS:
        if doc.exists():
            text = doc.read_text(encoding="utf-8")
            for m in re.finditer(r"\|\s*(GET|POST|PUT|PATCH|DELETE)\s*\|\s*`([^`]+)`", text):
                found.add((m.group(1), m.group(2)))
            for m in re.finditer(r"`(GET|POST|PUT|PATCH|DELETE)\s+([^`\s]+)`", text):
                found.add((m.group(1), m.group(2)))
    return found


def normalize(path: str) -> str:
    return re.sub(r"\{[^}]*\}", "{}", path.rstrip("/") or "/")


def render() -> str:
    docs = {(m, normalize(p)) for m, p in documented()}
    rows, undocumented = [], 0
    for f in sorted(ROOT.glob("*/api/src/main/java/**/*.java")):
        parsed = parse_controller(f.read_text(encoding="utf-8"))
        if not parsed:
            continue
        cls, endpoints = parsed
        module = "/".join(f.relative_to(ROOT).parts[:2])
        for e in endpoints:
            in_doc = (e["method"], normalize(e["path"])) in docs
            undocumented += not in_doc
            rows.append(f"| {module} | {e['method']} | `{e['path']}` | `{cls}#{e['handler']}` "
                        f"| {e['summary']} | {'Y' if in_doc else '**N**'} |")
    lines = [
        "# 프로그램 목록",
        "",
        "> 자동 생성 문서. 손으로 고치지 않는다. 원본은 `<그룹>/api` 의 컨트롤러다.",
        "> 재생성: `python3 tools/deliverables/gen_program_list.py`",
        "",
        f"엔드포인트 {len(rows)}개, `api.md`/`interfaces.md` 미등록 {undocumented}개.",
        "",
        "| 모듈 | 메서드 | 경로 | 핸들러 | 설명 | 문서 등록 |",
        "|---|---|---|---|---|:---:|",
        *rows,
    ]
    if not rows:
        lines.append("| - | - | - | - | 컨트롤러가 없다 | - |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="생성 결과가 기존 파일과 다르면 exit 1")
    args = parser.parse_args()
    content = render()
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != content:
            print(f"{OUT.relative_to(ROOT)} 가 코드와 다릅니다. 재생성하세요.", file=sys.stderr)
            return 1
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(content, encoding="utf-8")
    print(f"생성: {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
