---
title: PDF 嵌入预览测试
permalink: /pdf-embed-test/
listed: true
math: false
---

这个页面用于测试在 GitHub Pages 的 Markdown 页面里嵌入 PDF 文件，并让 PDF 直接在网页内预览、可滚动阅读，而不是变成一个普通下载链接。

## 测试 PDF：清华自动化专业本科培养方案

下面使用的是可复用的 PDF include：

```liquid
{% raw %}{% include pdf.html src="/pdf/清华自动化专业本科培养方案.pdf" title="清华自动化专业本科培养方案" height="900" %}{% endraw %}
```

{% include pdf.html src="/pdf/清华自动化专业本科培养方案.pdf" title="清华自动化专业本科培养方案" height="900" %}

## 原始 PDF 链接

如果上面的预览框没有显示，可以点击下面的原始链接直接打开 PDF：

[/pdf/清华自动化专业本科培养方案.pdf](/pdf/清华自动化专业本科培养方案.pdf)

## 说明

- 把 PDF 文件放到仓库根目录的 `pdf/` 文件夹里，URL 即 `/pdf/<文件名>.pdf`。
- 使用 `{% raw %}{% include pdf.html src="..." title="..." height="..." %}{% endraw %}` 在文章中内嵌 PDF。
  - `src`：PDF 路径，必填。中文文件名也可以，include 会自动做 URL 编码。
  - `title`：可选，作为 iframe 的可访问标题。
  - `height`：可选，预览框的高度（像素），默认 `800`。在窄屏（≤480px）下会自动缩小到 `480px`。
- 预览框内部由浏览器原生 PDF Viewer 渲染，支持滚动阅读、翻页、缩放和搜索。
- URL 末尾的 `#view=FitH` 参数让 PDF 默认按宽度适配，避免一开页就要横向滚动。
- 如果浏览器不支持原生 PDF 预览（极少数情况），下方会显示一个"在新标签页打开 PDF"的回退链接。
