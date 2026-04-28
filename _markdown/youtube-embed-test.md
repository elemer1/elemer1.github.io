---
title: YouTube 视频嵌入测试
permalink: /youtube-embed-test/
listed: true
---

这个页面用于测试在 GitHub Pages 的 Markdown 页面里嵌入 YouTube 视频，并让视频可以直接在网页中播放，而不是显示成普通链接。

## 测试视频

下面使用的是 YouTube 的 `embed` 地址：

```text
https://www.youtube.com/embed/EN7frwQIbKc
```

<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin: 20px 0;">
  <iframe
    src="https://www.youtube.com/embed/EN7frwQIbKc"
    title="YouTube video player"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
  </iframe>
</div>

## 原始视频链接

如果上面的播放器没有显示，可以点击下面的原始链接检查视频是否可访问：

[https://youtu.be/EN7frwQIbKc?si=D_1rJ6gba2Wj9Z8M](https://youtu.be/EN7frwQIbKc?si=D_1rJ6gba2Wj9Z8M)

## 说明

- 所有正式文章都放在 `_markdown/` 文件夹里。
- `_markdown/` 里的 Markdown 文件会自动套用网站文章模板。
- Markdown 普通链接只能跳转，不能直接播放。
- 要在网页中直接播放 YouTube 视频，需要使用 `<iframe>`。
- `youtu.be/...` 链接需要转换成 `youtube.com/embed/...` 格式。
