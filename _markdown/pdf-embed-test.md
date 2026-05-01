---
title: PDF 嵌入预览测试
permalink: /pdf-embed-test/
listed: true
math: false
---

这个页面用于测试在 GitHub Pages 的 Markdown 页面里嵌入 PDF 文件，并让 PDF 直接在网页内预览、可以滚动阅读，而不是变成一个普通下载链接。

## 测试 PDF：清华自动化专业本科培养方案

下面使用的是可复用的 PDF include：

```liquid
{% raw %}{% include pdf.html src="/pdf/清华自动化专业本科培养方案.pdf" title="清华自动化专业本科培养方案" %}{% endraw %}
```

{% include pdf.html src="/pdf/清华自动化专业本科培养方案.pdf" title="清华自动化专业本科培养方案" %}

## 说明

- 把 PDF 文件放到仓库根目录的 `pdf/` 文件夹里，URL 即 `/pdf/<文件名>.pdf`。
- 使用 `{% raw %}{% include pdf.html src="..." title="..." height="..." %}{% endraw %}` 在文中内嵌 PDF。
  - `src`：PDF 路径，必填。中文文件名也可以。
  - `title`：可选，作为 iframe 的可访问标题。
  - `height`：可选，预览框的像素高度，默认 `780`；窄屏 (≤480px) 自动缩到 `540`。
- 阅读器是仓库自带的 PDF.js 官方 viewer (`/assets/pdfjs/web/viewer.html`)，提供经典的 PDF 工具栏：缩略图侧边栏、页码跳转、缩放、自适应宽度、全屏、搜索、打印、下载。
- 视图按需懒渲染，14 页或 100 页打开都很快，不会一次性把整份 PDF 拉到内存里。
