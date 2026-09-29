#!/usr/bin/env python3
"""DDL 에서 테이블 정의서(docs/product/generated/table-spec.md)를 생성한다.

입력: <그룹>/docs/database/**/*.sql 의 create table 과 comment on.
사용:
    python3 tools/deliverables/gen_table_spec.py          # 생성
    python3 tools/deliverables/gen_table_spec.py --check  # 기존 파일과 다르면 exit 1
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/product/generated/table-spec.md"

CONSTRAINT_PREFIXES = ("constraint", "primary key", "foreign key", "unique", "check", "exclude")
TYPE_STOP = re.compile(
    r"\s+(not\s+null|null|default|primary\s+key|references|constraint|check|unique|generated|collate)\b",
    re.I,
)


def strip_comments(sql: str) -> str:
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.S)
    return re.sub(r"--[^\n]*", "", sql)


def split_top_level(body: str) -> list[str]:
    parts, depth, cur, quote = [], 0, [], False
    for ch in body:
        if ch == "'":
            quote = not quote
        elif not quote and ch == "(":
            depth += 1
        elif not quote and ch == ")":
            depth -= 1
        elif not quote and ch == "," and depth == 0:
            parts.append("".join(cur).strip())
            cur = []
            continue
        cur.append(ch)
    if "".join(cur).strip():
        parts.append("".join(cur).strip())
    return parts


def unquote(literal: str) -> str:
    return literal[1:-1].replace("''", "'")


def parse_sql(sql: str) -> tuple[dict, dict, dict]:
    """(tables, table_comments, column_comments) 를 돌려준다."""
    sql = strip_comments(sql)
    tables: dict[str, list[dict]] = {}
    for m in re.finditer(r"create\s+table\s+(?:if\s+not\s+exists\s+)?([\w.\"]+)\s*\(", sql, re.I):
        name = m.group(1).replace('"', "").lower()
        start = m.end()
        depth, i = 1, start
        while i < len(sql) and depth:
            depth += {"(": 1, ")": -1}.get(sql[i], 0)
            i += 1
        body = sql[start : i - 1]
        columns, table_pk = [], []
        for item in split_top_level(body):
            low = item.lower()
            if low.startswith(CONSTRAINT_PREFIXES):
                pk = re.search(r"primary\s+key\s*\(([^)]*)\)", item, re.I)
                if pk:
                    table_pk += [c.strip().strip('"').lower() for c in pk.group(1).split(",")]
                continue
            col = re.match(r'"?(\w+)"?\s+(.*)', item, re.S)
            if not col:
                continue
            rest = " ".join(col.group(2).split())
            stop = TYPE_STOP.search(" " + rest)
            col_type = (rest[: stop.start() - 1] if stop else rest).strip()
            default = re.search(r"\bdefault\s+(.+?)(?=\s+(?:not\s+null|null|primary|references|constraint|check|unique)\b|$)", rest, re.I)
            columns.append({
                "name": col.group(1).lower(),
                "type": col_type,
                "not_null": bool(re.search(r"\bnot\s+null\b|\bprimary\s+key\b", rest, re.I)),
                "default": default.group(1).strip() if default else "",
                "pk": bool(re.search(r"\bprimary\s+key\b", rest, re.I)),
                "fk": bool(re.search(r"\breferences\b", rest, re.I)),
            })
        for c in columns:
            if c["name"] in table_pk:
                c["pk"] = c["not_null"] = True
        tables[name] = columns

    literal = r"('(?:[^']|'')*')"
    table_comments = {
        m.group(1).replace('"', "").lower(): unquote(m.group(2))
        for m in re.finditer(r"comment\s+on\s+table\s+([\w.\"]+)\s+is\s+" + literal, sql, re.I)
    }
    column_comments = {}
    for m in re.finditer(r"comment\s+on\s+column\s+([\w.\"]+)\s+is\s+" + literal, sql, re.I):
        table, _, column = m.group(1).replace('"', "").lower().rpartition(".")
        column_comments[(table, column)] = unquote(m.group(2))
    return tables, table_comments, column_comments


def cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def render() -> str:
    files = sorted(ROOT.glob("*/docs/database/**/*.sql"))
    by_group: dict[str, dict] = {}
    for f in files:
        group = f.relative_to(ROOT).parts[0]
        tables, tcom, ccom = parse_sql(f.read_text(encoding="utf-8"))
        g = by_group.setdefault(group, {"tables": {}, "tcom": {}, "ccom": {}, "src": {}})
        g["tables"].update(tables)
        g["tcom"].update(tcom)
        g["ccom"].update(ccom)
        for t in tables:
            g["src"][t] = f.relative_to(ROOT).as_posix()

    lines = [
        "# 테이블 정의서",
        "",
        "> 자동 생성 문서. 손으로 고치지 않는다. 원본은 `<그룹>/docs/database/` 의 DDL 과 `comment on` 이다.",
        "> 재생성: `python3 tools/deliverables/gen_table_spec.py`",
        "",
    ]
    if not by_group:
        lines.append("DDL 파일이 없다 (`*/docs/database/**/*.sql`).")
        return "\n".join(lines) + "\n"

    missing = []
    for group, g in by_group.items():
        for t, cols in g["tables"].items():
            if t not in g["tcom"]:
                missing.append(f"{group}: `{t}` (테이블)")
            missing += [f"{group}: `{t}.{c['name']}`" for c in cols if (t, c["name"]) not in g["ccom"]]
    lines.append(f"테이블 {sum(len(g['tables']) for g in by_group.values())}개, 주석 누락 {len(missing)}건.")
    if missing:
        lines += ["", "<details><summary>주석 누락 목록</summary>", ""] + [f"- {m}" for m in missing] + ["", "</details>"]

    for group in sorted(by_group):
        g = by_group[group]
        lines += ["", f"## {group} DB", ""]
        for t in sorted(g["tables"]):
            lines += [
                f"### {t}",
                "",
                f"{cell(g['tcom'].get(t, '(주석 없음)'))} — 원본 `{g['src'][t]}`",
                "",
                "| No | 컬럼 | 타입 | NULL | 기본값 | 키 | 설명 |",
                "|---:|---|---|:---:|---|:---:|---|",
            ]
            for i, c in enumerate(g["tables"][t], 1):
                key = "/".join(k for k, on in (("PK", c["pk"]), ("FK", c["fk"])) if on)
                lines.append(
                    f"| {i} | `{c['name']}` | {cell(c['type'])} | {'N' if c['not_null'] else 'Y'} "
                    f"| {cell(c['default'])} | {key} | {cell(g['ccom'].get((t, c['name']), ''))} |"
                )
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="생성 결과가 기존 파일과 다르면 exit 1")
    args = parser.parse_args()
    content = render()
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != content:
            print(f"{OUT.relative_to(ROOT)} 가 DDL 과 다릅니다. 재생성하세요.", file=sys.stderr)
            return 1
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(content, encoding="utf-8")
    print(f"생성: {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
