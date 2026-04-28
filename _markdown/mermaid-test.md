---
title: Mermaid 流程图测试
permalink: /mermaid-test/
listed: false
math: false
mermaid: true
---

这个页面用于测试在 GitHub Pages 的 Markdown 页面里使用 Mermaid 流程图，并让图表在网页端直接渲染，而不是显示成普通代码块。

## Flowchart

下面使用的是标准 Markdown fenced code block：

````markdown
```mermaid
flowchart TD
  A[写 Markdown] --> B[Jekyll / kramdown 渲染]
  B --> C[default layout 加载 Mermaid]
  C --> D[网页显示流程图]
```
````

```mermaid
flowchart TD
  A[写 Markdown] --> B[Jekyll / kramdown 渲染]
  B --> C[default layout 加载 Mermaid]
  C --> D[网页显示流程图]
```

## Sequence diagram

```mermaid
sequenceDiagram
  participant Writer as Writer
  participant Jekyll as Jekyll
  participant Browser as Browser
  Writer->>Jekyll: 提交包含 ```mermaid 的 Markdown
  Jekyll->>Browser: 输出 code.language-mermaid
  Browser->>Browser: Mermaid 转换并渲染 SVG
```

## 说明

- Mermaid 只在 front matter 里设置 `mermaid: true` 的页面加载。
- 普通 Markdown 文章仍然不额外加载 Mermaid 脚本。
- 图表语法使用标准代码块：```` ```mermaid ````。
