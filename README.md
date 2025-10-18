# Personal Website

极简个人网站，使用 Jekyll + GitHub Pages。

## 快速开始

### 1. 本地预览

```bash
# 安装依赖
bundle install

# 运行本地服务器
bundle exec jekyll serve

# 访问 http://localhost:4000
```

### 2. 部署到 GitHub Pages

1. 在 GitHub 创建新仓库，命名为 `username.github.io`（将 username 替换为你的 GitHub 用户名）
2. 修改 `_config.yml` 中的配置：
   - `title`: 你的名字
   - `email`: 你的邮箱
   - `url`: `https://username.github.io`
3. 将代码推送到 GitHub：

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/username.github.io.git
git push -u origin main
```

4. 在仓库设置中启用 GitHub Pages：
   - 进入 Settings > Pages
   - Source 选择 "GitHub Actions"
   - 等待几分钟，网站会自动部署

### 3. 配置自定义域名

1. 修改 `CNAME` 文件，将 `yourdomain.com` 替换为你的域名
2. 在你的域名服务商处添加 DNS 记录：
   - 对于根域名（example.com）：
     ```
     A    @    185.199.108.153
     A    @    185.199.109.153
     A    @    185.199.110.153
     A    @    185.199.111.153
     ```
   - 对于子域名（www.example.com）：
     ```
     CNAME    www    username.github.io
     ```
3. 提交 CNAME 文件到 GitHub
4. 在 GitHub Pages 设置中勾选 "Enforce HTTPS"

### 4. 添加文章

在 `_posts` 文件夹中创建新的 Markdown 文件：

- 文件名格式：`YYYY-MM-DD-title.md`
- 文件开头添加 front matter：

```yaml
---
layout: post
title: "文章标题"
date: YYYY-MM-DD
---
```

然后用 Markdown 格式写作。提交到 GitHub 后会自动发布。

## 目录结构

```
.
├── _config.yml          # Jekyll 配置
├── _layouts/            # 页面布局
│   ├── default.html     # 默认布局
│   └── post.html        # 文章布局
├── _posts/              # 博客文章（Markdown 文件）
├── assets/
│   └── css/
│       └── style.css    # 样式文件
├── index.html           # 首页
├── CNAME                # 自定义域名配置
└── .github/
    └── workflows/
        └── jekyll.yml   # 自动部署配置
```

## 自定义

- 修改 [_config.yml](_config.yml) 更新网站信息
- 修改 [index.html](index.html) 更新首页内容
- 修改 [assets/css/style.css](assets/css/style.css) 调整样式
