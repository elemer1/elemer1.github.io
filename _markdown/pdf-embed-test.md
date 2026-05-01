---
title: PDF 嵌入预览测试
permalink: /pdf-embed-test/
listed: true
math: false
pdf: true
---

这个页面用于测试在 GitHub Pages 的 Markdown 页面里嵌入 PDF 文件，并让 PDF 直接在网页内预览、可以跟随主页面整体滚动阅读，而不是变成一个普通下载链接，也不是塞在 iframe 里独立滚动。

## 测试 PDF：清华自动化专业本科培养方案

下面使用的是可复用的 PDF include：

```liquid
{% raw %}{% include pdf.html src="/pdf/清华自动化专业本科培养方案.pdf" title="清华自动化专业本科培养方案" %}{% endraw %}
```

{% include pdf.html src="/pdf/清华自动化专业本科培养方案.pdf" title="清华自动化专业本科培养方案" %}

## 说明

- 把 PDF 文件放到仓库根目录的 `pdf/` 文件夹里，URL 即 `/pdf/<文件名>.pdf`。
- 在文章 front matter 里加一行 `pdf: true`，让页面加载 PDF.js。
- 使用 `{% raw %}{% include pdf.html src="..." title="..." %}{% endraw %}` 在文中内嵌 PDF。
  - `src`：PDF 路径，必填。中文文件名也可以，浏览器加载时会自动处理 URL 编码。
  - `title`：可选，作为容器的可访问标题。
- PDF.js 把每一页渲染成独立的 canvas，按页顺序铺在文章里，所以可以像普通图片一样跟着页面滚动。视口外的页面采用 IntersectionObserver 懒渲染，节省性能。
- 外框使用经典 PDF 阅读器风格：深灰底 + 白色页面 + 投影。
