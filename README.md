# lab-report

用于中文课程实验报告的 Codex 技能。

- 严格遵守实验要求和指定顺序；有报告模板时沿用模板。
- 先检查 Markdown 内部草稿，再生成 Word；使用真实实验数据。
- 默认使用简短清楚的中文、黑色文字和微软雅黑常规体，避免大面积留白。课程模板规定优先。
- 完成后渲染实际 Word，由具备视觉能力的模型逐页检查。
- 默认只交付 Word 和实验要求的代码、图片；不自动交付 PDF 或制作压缩包。

## 安装与使用

将本仓库克隆到 Codex 的技能目录，目录名保持为 `lab-report`。默认位置为 `~/.codex/skills/lab-report`；设置了 `CODEX_HOME` 时使用该目录下的 `skills/lab-report`。

```bash
git clone https://github.com/ysqd1/lab-report.git ~/.codex/skills/lab-report
```

如果目标目录已存在，应先核对内容，避免覆盖本地修改。让 Codex 重新加载技能后，可输入：

```text
使用 $lab-report，按实验指导书和模板完成实验报告。
```

技能说明见 [SKILL.md](SKILL.md)。`scripts/normalize_docx.py` 可统一现有 Word 的字体与文字颜色，仅依赖 Python 标准库。报告生成与视觉检查需使用当前环境可用的文档工具。
