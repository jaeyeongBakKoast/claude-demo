#!/usr/bin/env python3
"""JUnit XML 결과에서 단위 시험 결과서(docs/quality/generated/unit-test-report.md)를 생성한다.

입력: <그룹>/<모듈>/build/test-results/**/*.xml
  - Gradle: 테스트를 돌리면 build/test-results/test/TEST-*.xml 이 생긴다
  - pytest: uv run pytest --junitxml=build/test-results/pytest/junit.xml
사용:
    python3 tools/deliverables/gen_test_report.py
"""
from __future__ import annotations

import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/quality/generated/unit-test-report.md"


def commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def cases_of(xml_file: Path) -> list[dict]:
    root = ET.parse(xml_file).getroot()
    suites = [root] if root.tag == "testsuite" else root.iter("testsuite")
    cases = []
    for suite in suites:
        for tc in suite.iter("testcase"):
            if tc.find("failure") is not None or tc.find("error") is not None:
                result = "실패"
            elif tc.find("skipped") is not None:
                result = "건너뜀"
            else:
                result = "통과"
            cases.append({
                "class": tc.get("classname", suite.get("name", "")),
                "name": tc.get("name", ""),
                "time": float(tc.get("time") or 0),
                "result": result,
            })
    return cases


def render() -> str:
    by_module: dict[str, list[dict]] = {}
    for f in sorted(ROOT.glob("*/*/build/test-results/**/*.xml")):
        module = "/".join(f.relative_to(ROOT).parts[:2])
        try:
            by_module.setdefault(module, []).extend(cases_of(f))
        except ET.ParseError:
            print(f"건너뜀 (XML 오류): {f.relative_to(ROOT)}", file=sys.stderr)

    lines = [
        "# 단위 시험 결과서",
        "",
        "> 자동 생성 문서. 손으로 고치지 않는다. 원본은 각 모듈의 `build/test-results/` JUnit XML 이다.",
        f"> 생성 일시 {datetime.now().strftime('%Y-%m-%d %H:%M')}, 커밋 `{commit()}`.",
        "> 재생성: 모듈 테스트 실행 후 `python3 tools/deliverables/gen_test_report.py`",
        "",
    ]
    if not by_module:
        lines.append("시험 결과 파일이 없다. 모듈 테스트를 먼저 실행한다.")
        return "\n".join(lines) + "\n"

    def count(cases: list[dict], result: str) -> int:
        return sum(c["result"] == result for c in cases)

    lines += ["## 요약", "", "| 모듈 | 전체 | 통과 | 실패 | 건너뜀 | 통과율 |", "|---|---:|---:|---:|---:|---:|"]
    total: list[dict] = []
    for module, cases in by_module.items():
        total += cases
        ran = len(cases) - count(cases, "건너뜀")
        rate = f"{count(cases, '통과') / ran * 100:.1f}%" if ran else "-"
        lines.append(f"| {module} | {len(cases)} | {count(cases, '통과')} | {count(cases, '실패')} | {count(cases, '건너뜀')} | {rate} |")
    ran = len(total) - count(total, "건너뜀")
    rate = f"{count(total, '통과') / ran * 100:.1f}%" if ran else "-"
    lines.append(f"| **합계** | {len(total)} | {count(total, '통과')} | {count(total, '실패')} | {count(total, '건너뜀')} | {rate} |")

    for module, cases in by_module.items():
        lines += ["", f"## {module}", "", "| No | 클래스 | 케이스 | 결과 | 시간(s) |", "|---:|---|---|:---:|---:|"]
        for i, c in enumerate(cases, 1):
            lines.append(f"| {i} | `{c['class']}` | {c['name']} | {c['result']} | {c['time']:.3f} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    content = render()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(content, encoding="utf-8")
    print(f"생성: {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
