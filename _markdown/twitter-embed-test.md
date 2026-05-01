---
title: Twitter / X Cards 嵌入测试
permalink: /twitter-embed-test/
listed: true
twitter: true
---

这个页面用于测试在 GitHub Pages 的 Markdown 页面里嵌入 Twitter / X 推文卡片，让推文以官方原生卡片形式渲染（含头像、正文、附件、时间戳），而不是只显示一个超链接。

## 测试推文

下面使用的是可复用的 Twitter include：

```liquid
{% raw %}{% include twitter.html url="https://twitter.com/jack/status/20" %}{% endraw %}
```

{% include twitter.html url="https://twitter.com/jack/status/20" %}

## 暗色主题

```liquid
{% raw %}{% include twitter.html url="https://twitter.com/Twitter/status/1445078208190291973" theme="dark" %}{% endraw %}
```

{% include twitter.html url="https://twitter.com/Twitter/status/1445078208190291973" theme="dark" %}

## 隐藏会话上下文

`conversation="none"` 会隐藏被回复的上文，只显示当前推文：

```liquid
{% raw %}{% include twitter.html url="https://twitter.com/elonmusk/status/1507041396242407424" conversation="none" %}{% endraw %}
```

{% include twitter.html url="https://twitter.com/elonmusk/status/1507041396242407424" conversation="none" %}

## 原始推文链接

如果上面的卡片没有渲染，可以点击下面的原始链接确认推文是否可访问：

[https://twitter.com/jack/status/20](https://twitter.com/jack/status/20)

## 说明

- 在 front matter 中加上 `twitter: true`，页面才会加载 Twitter `widgets.js` 渲染脚本。普通文章不会额外加载这个脚本。
- 使用 `{% raw %}{% include twitter.html url="..." %}{% endraw %}` 在文中内嵌推文卡片。
  - `url`：推文链接，必填。`twitter.com` 或 `x.com` 都可以。
  - `theme`：可选，`light`（默认）或 `dark`。
  - `conversation`：可选，`all`（默认）显示完整上下文，`none` 只显示这一条。
  - `align`：可选，`center`（默认）/`left`/`right`，控制卡片在容器中的对齐方式。
  - `cards`：可选，`visible`（默认）显示链接预览卡片，`hidden` 不显示。
  - `lang`：可选，卡片内界面语言，默认 `en`。
- 卡片自动设置 `data-dnt="true"`，告诉 Twitter 不要为本次嵌入个性化追踪用户。
- Twitter / X 推文删除后，卡片会自动 fallback 成普通 blockquote + 链接，不会留下空白。
- 普通 Markdown 链接只能跳转，不能在页面中渲染推文卡片。
