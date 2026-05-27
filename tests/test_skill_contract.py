#!/usr/bin/env python3
"""Offline contract checks for cn-patent."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


def _frontmatter_keys(skill_md: Path) -> set[str]:
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    assert lines and lines[0] == "---", "SKILL.md must start with YAML frontmatter"
    keys: set[str] = set()
    for line in lines[1:]:
        if line == "---":
            break
        if line and not line.startswith(" ") and ":" in line:
            keys.add(line.split(":", 1)[0].strip())
    return keys


def test_skill_frontmatter_contract() -> None:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    keys = _frontmatter_keys(ROOT / "SKILL.md")
    allowed = {"name", "description", "metadata", "allowed-tools"}
    unexpected = keys - allowed
    assert not unexpected, f"Unsupported SKILL.md frontmatter keys: {sorted(unexpected)}"
    assert {"name", "description"} <= keys
    assert "name: cn-patent" in skill_text


def test_codex_openai_yaml_exists() -> None:
    openai_yaml = ROOT / "agents" / "openai.yaml"
    text = openai_yaml.read_text(encoding="utf-8")
    assert "display_name:" in text
    assert "short_description:" in text
    assert "default_prompt:" in text
    assert "$cn-patent" in text


def test_china_patent_quality_reference_exists() -> None:
    ref = ROOT / "references" / "cn-patent-quality.md"
    text = ref.read_text(encoding="utf-8")
    assert "技术问题" in text
    assert "技术方案" in text
    assert "技术效果" in text
    assert "cnipa.gov.cn" in text
    assert "局令第84号" in text
    assert "2026-01-01" in text
    assert "整体分析" in text


def test_prompts_are_host_neutral() -> None:
    checked = [
        ROOT / "SKILL.md",
        *sorted((ROOT / "prompts").glob("*.md")),
        ROOT / "tools" / "README.md",
    ]
    legacy_var = "CLAUDE" + "_SKILL_DIR"
    offenders = [
        str(path.relative_to(ROOT))
        for path in checked
        if legacy_var in path.read_text(encoding="utf-8")
    ]
    assert not offenders, f"Host-specific path variable remains in: {offenders}"


def test_no_legacy_branding() -> None:
    forbidden = ["patent" + "-disclosure" + "-skill", "handsomest" + "Wei"]
    checked = [
        ROOT / "SKILL.md",
        ROOT / "README.md",
        ROOT / "INSTALL.md",
        ROOT / "agents" / "openai.yaml",
        *sorted((ROOT / "prompts").glob("*.md")),
        *sorted((ROOT / "references").glob("*.md")),
        *sorted((ROOT / "docs").rglob("*.md")),
        *sorted((ROOT / "examples").rglob("*.md")),
    ]
    offenders: list[str] = []
    for path in checked:
        text = path.read_text(encoding="utf-8")
        if any(term in text for term in forbidden):
            offenders.append(str(path.relative_to(ROOT)))
    assert not offenders, f"Legacy branding remains in: {offenders}"


def test_mermaid_render_strict_no_mermaid_smoke() -> None:
    with tempfile.TemporaryDirectory(prefix="cn-patent-test-") as tmp:
        tmp_path = Path(tmp)
        source = tmp_path / "draft.md"
        out = tmp_path / "out.md"
        source.write_text("# 技术交底书\n\n无 mermaid 图示。\n", encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "mermaid_render.py"),
                "-i",
                str(source),
                "-o",
                str(out),
                "--no-docx",
                "--strict",
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, result.stderr or result.stdout
        assert out.read_text(encoding="utf-8") == source.read_text(encoding="utf-8")


def test_cnipa_card_parser_extracts_abstract() -> None:
    from cnipa_epub_parse import hits_to_jsonable, parse_search_result_html

    html = """
    <html><body><div class="overview-default">
      <div class="item">
        <h1 class="title">一种识别船只数量的方法</h1>
        <div class="qrcode" title="http://epub.cnipa.gov.cn/patent/CN123456789A"></div>
        <dl>
          <dt>申请公布号：</dt><dd>CN123456789A</dd>
          <dt>摘要：</dt><dd>获取船只图片数据，训练检测模型，并根据测试结果确定船只数量。</dd>
        </dl>
      </div>
    </div></body></html>
    """
    rows = hits_to_jsonable(parse_search_result_html(html))
    assert rows == [
        {
            "title": "一种识别船只数量的方法",
            "pub_number": "CN123456789A",
            "link": "http://epub.cnipa.gov.cn/patent/CN123456789A",
            "abstract": "获取船只图片数据，训练检测模型，并根据测试结果确定船只数量。",
        }
    ]


def main() -> int:
    tests = [
        test_skill_frontmatter_contract,
        test_codex_openai_yaml_exists,
        test_china_patent_quality_reference_exists,
        test_prompts_are_host_neutral,
        test_no_legacy_branding,
        test_mermaid_render_strict_no_mermaid_smoke,
        test_cnipa_card_parser_extracts_abstract,
    ]
    for test in tests:
        test()
        print(f"ok - {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
