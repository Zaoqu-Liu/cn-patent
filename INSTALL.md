# 安装 cn-patent

`cn-patent` 的安装方式很简单：把整个仓库目录放进宿主应用的 `skills/` 目录，并确保 `SKILL.md` 保持在 `cn-patent/` 根部。

## Codex

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/Zaoqu-Liu/cn-patent ~/.codex/skills/cn-patent
```

安装后重启 Codex。

## Claude Code

项目内安装：

```bash
mkdir -p .claude/skills
git clone https://github.com/Zaoqu-Liu/cn-patent .claude/skills/cn-patent
```

全局安装：

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/Zaoqu-Liu/cn-patent ~/.claude/skills/cn-patent
```

## Cursor

全局安装：

```bash
mkdir -p ~/.cursor/skills
git clone https://github.com/Zaoqu-Liu/cn-patent ~/.cursor/skills/cn-patent
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.cursor\skills"
git clone https://github.com/Zaoqu-Liu/cn-patent "$env:USERPROFILE\.cursor\skills\cn-patent"
```

项目内安装路径：

```text
<project>/.cursor/skills/cn-patent/
```

安装后重启 Cursor；若应用提供技能发现或规则设置入口，可在那里确认 `cn-patent` 是否已被识别。

## 可选依赖

没有这些依赖时，skill 仍能指导撰写流程；安装后可以更稳定地处理 Office 材料、国知局查新和 Word 交付。

### Office 转换与 Word 导出

用于 `.docx` / `.pptx` 材料抽取，以及 Markdown 导出 Word：

```bash
pip install -r requirements.txt
```

### 国知局公布公告检索

用于优先查询国家知识产权局中国专利公布公告站：

```bash
pip install -r tools/requirements-cnipa.txt
python -m playwright install chromium
```

如果这一路径不可用，工作流会降级到公开网页检索，并在回复中说明降级原因。

### Mermaid 图示渲染

用于把 fenced mermaid 图渲染成 PNG，再嵌入 Word：

```bash
cd tools
npm install
```

如果 `mmdc` 提示找不到浏览器，可在 `tools/` 下执行：

```bash
npx puppeteer browsers install chrome-headless-shell
```

## 本地验证

在仓库根目录执行：

```bash
python tests/test_skill_contract.py
python -m py_compile tools/*.py tests/*.py
python tools/md_to_docx.py -i examples/quickstart-case/expected/minimal-disclosure.md -o /tmp/cn-patent-smoke.docx
```

Codex 结构校验：

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

安装 Playwright 后，可选跑一次国知局实时链路：

```bash
CNIPA_EXPECT_HITS=1 python tests/test_cnipa_epub_chain.py 知识图谱
```

这项依赖官方站点和本机浏览器环境，因此和离线验证命令分开。

## `${SKILL_DIR}` 是什么

本仓库的指令中用 `${SKILL_DIR}` 表示包含 `SKILL.md` 的目录。如果宿主没有自动设置该变量，执行工具命令前可手动设置：

```bash
export SKILL_DIR="/path/to/cn-patent"
```
