# 示例

本目录提供虚构材料，用于在不暴露真实项目代码的情况下试用 `cn-patent`。

## 快速开始

建议先跑小案例：

```text
Use $cn-patent to scan examples/quickstart-case/knowledge and draft a Chinese technical disclosure.
Keep company/product names generic, run prior-art search if available, and export both Markdown and Word.
```

文件：

- `quickstart-case/knowledge/architecture.md`
- `quickstart-case/knowledge/meeting-notes.md`
- `quickstart-case/expected/minimal-disclosure.md`

## 较完整示例

`example_batch_job_scheduler/` 是更完整的虚构案件，包含架构说明、示例代码、示例 Word 和示例 PPT。适合测试 Office 转换、项目扫描和更完整的专利点挖掘流程。

建议提示词：

```text
Use $cn-patent to scan examples/example_batch_job_scheduler/knowledge.
Mine candidate patent points, run prior-art search if available, and generate a timestamped Markdown and Word disclosure.
```

## 输出位置

生成的交付物建议写入：

```text
outputs/<case-name>/
```

每次交付的交底书使用：

```text
案件名_YYYYMMDDHHmmss.md
案件名_YYYYMMDDHHmmss.docx
```
