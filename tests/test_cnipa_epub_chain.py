# -*- coding: utf-8 -*-
"""
串联验证：与同目录能力对齐——运行 `tools/cnipa_epub_search.py`（一步：爬取 + 解析，**不落盘 HTML**）。

需已安装：pip install -r tools/requirements-cnipa.txt && python -m playwright install chromium

在仓库根目录执行：

  python tests/test_cnipa_epub_chain.py

可选参数指定关键词：

  python tests/test_cnipa_epub_chain.py 批处理

无参数时本测试脚本仍传入「知识图谱」以便本地联调；**命令行直接运行** `cnipa_epub_search.py` **须自带关键词**（不设默认）。技能要求 Agent 在 Step 5 **每词一次 Bash、自行合并 JSON**（见 `prior_art_search.md`）；本测试单次传参仅为联调。默认验证 CLI 链路与 `EPUB_HITS_JSON` 输出契约；若想要求至少 1 条命中，可设置 `CNIPA_EXPECT_HITS=1`。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if argv:
        extra = argv
    else:
        extra = ["知识图谱"]
    os.environ.setdefault("EPUB_WAF_MAX_WAIT_SEC", "180")

    try:
        import playwright  # noqa: F401
    except ImportError:
        print("请先安装: pip install -r tools/requirements-cnipa.txt", file=sys.stderr)
        return 1

    cmd = [sys.executable, str(ROOT / "tools" / "cnipa_epub_search.py"), *extra]
    timeout = int(os.environ.get("CNIPA_CHAIN_TIMEOUT_SEC", "240"))
    result = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.stdout:
        print(result.stdout, end="")
    if result.returncode != 0:
        return result.returncode

    line = next(
        (ln for ln in result.stdout.splitlines() if ln.startswith("EPUB_HITS_JSON:")),
        "",
    )
    if not line:
        print("未找到 EPUB_HITS_JSON 输出行。", file=sys.stderr)
        return 3
    rows = json.loads(line.split(":", 1)[1].strip())
    if not rows and os.environ.get("CNIPA_EXPECT_HITS", "").lower() in {"1", "true", "yes"}:
        print("EPUB_HITS_JSON 为空；可能是检索词过窄或官方站点临时返回空结果。", file=sys.stderr)
        return 4
    if rows:
        first = rows[0]
        for key in ("title", "pub_number", "link"):
            if not first.get(key):
                print(f"第一条命中缺少字段: {key}", file=sys.stderr)
                return 5
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
