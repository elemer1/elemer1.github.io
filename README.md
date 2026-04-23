# elemer.net

A minimal personal website built with Jekyll and hosted on GitHub Pages.

Live at **[elemer.net](https://elemer.net)**.

## Design principles

1. **Speed.** Static HTML, served from GitHub Pages' global CDN. CSS is inlined; no web fonts; no JavaScript framework.
2. **Minimal.** A 650px column, system fonts, pure black on white. The content is the design.
3. **Two file types only.** Markdown for prose, raw HTML for interactive pieces. Nothing else.
4. **LaTeX support.** MathJax loads by default on every page so any post can use `$...$` and `$$...$$`.
5. **Drop-in publishing.** Drop a file into the right folder, add three lines of front matter, run `./publish.sh`. That's it.
6. **Mobile and desktop friendly.** Responsive by default; nothing breaks at small widths.
7. **Private by default.** No analytics, no RSS feed, no search-engine indexing, no opt-in for AI training crawlers. Sharing is for humans you send the link to.

## Folder layout

```
.
├── _config.yml          # Jekyll config
├── _layouts/
│   ├── default.html     # Site shell (inlined CSS, MathJax, fonts)
│   └── post.html        # Wrapper for markdown posts
├── _markdown/           # Markdown posts
├── _html/               # Standalone HTML pages
├── assets/
│   └── favicon.svg
├── index.html           # Homepage (lists everything with `listed: true`)
├── 404.html             # Custom not-found page
├── robots.txt           # Crawler / AI-bot deny list
├── CNAME                # Custom domain (elemer.net)
├── publish.sh           # One-command publish script
├── package.json         # Node deps (autocorrect formatter)
├── scripts/
│   └── format.mjs       # Chinese typography formatter
└── .github/workflows/
    └── jekyll.yml       # GitHub Pages build action
```

## Writing a new post

### Markdown post

1. Create a file in `_markdown/`, e.g. `_markdown/my-essay.md`
2. Add this front matter at the top:

   ```yaml
   ---
   title: My Essay
   permalink: /my-essay/
   listed: true
   ---
   ```

3. Write the body in Markdown. LaTeX works out of the box:

   ```markdown
   Inline math: $E = mc^2$

   Display math:
   $$\int_0^\infty e^{-x^2}\,dx = \frac{\sqrt{\pi}}{2}$$
   ```

4. Run `./publish.sh`.

### Standalone HTML page

1. Create a file in `_html/`, e.g. `_html/compound.html`
2. Add this front matter at the very top of the file (above `<!DOCTYPE html>`):

   ```yaml
   ---
   title: "Compound · A Memo to CEO"
   permalink: /compound/
   listed: true
   ---
   <!DOCTYPE html>
   <html>
     ...
   </html>
   ```

3. Run `./publish.sh`.

The HTML file is served as-is, with no layout wrapping. It can include its own CSS, JS, fonts, animations — anything.

## Front matter reference

Every published file uses the same three-field schema:

| Field       | Required | Purpose                                                                |
| ----------- | -------- | ---------------------------------------------------------------------- |
| `title`     | yes      | Shown on the homepage list and in the browser tab                      |
| `permalink` | yes      | The URL the file is served at, e.g. `/compound/`                       |
| `listed`    | yes      | `true` to appear on the homepage; omit or set `false` to hide          |

Optional:

| Field   | Purpose                                                                            |
| ------- | ---------------------------------------------------------------------------------- |
| `math`  | Set `false` to skip MathJax on a page (useful if `$...$` is used for prices, etc.) |

There are deliberately no `date` fields. This site only publishes long-half-life writing.

## Bibliography format

Posts that cite sources use a single unified format. The section always appears
at the end of the article, preceded by a `---` divider.

### Rules

1. **Header.** `## 参考文献` (H2). Do not use `# 参考文献` (H1) or bold text
   (`**参考文献**`).
2. **Grouping.** For long bibliographies, group entries under `### subsection`
   headers (e.g. `### 哲学与认知科学`, `### 评测基准`). Short ones can skip
   subsections.
3. **Entries.** APA-style on a single bullet line starting with `- `:
   - `Author, A. B., & Author, C. D. (Year). Article title. *Journal*, Volume(Issue), pages.`
   - Italicize book / journal titles with `*...*`.
   - Do **not** bold author names.
4. **Links.** Use Markdown syntax `[label](url)`. Preferred labels:
   - `[DOI](https://doi.org/...)` for journal articles
   - `[arXiv:2005.14165](https://arxiv.org/abs/2005.14165)` for arXiv preprints
   - `[JSTOR]`, `[PDF]`, `[IEEE]`, `[OUP]`, etc. for known platforms
   - `[原文](...)` for primary-source URLs without a better label
   - a domain label (e.g. `[swebench.com](...)`) for sites / leaderboards
   - Join multiple links with ` ｜ ` (full-width pipe with spaces).
5. **No footnote-style references.** Do not use `[^N]: ...`; use the bulleted
   list instead.

### Template

```markdown
---

## 参考文献

### 语言模型

- Brown, T. B., Mann, B., Ryder, N., et al. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems*, 33. [arXiv:2005.14165](https://arxiv.org/abs/2005.14165)
- Clark, A., & Chalmers, D. (1998). The extended mind. *Analysis*, 58(1), 7–19. [DOI](https://doi.org/10.1093/analys/58.1.7) ｜ [JSTOR](http://www.jstor.org/stable/3328150)

### 官方文档

- Anthropic. (2024, November 25). Introducing the Model Context Protocol. [原文](https://www.anthropic.com/news/model-context-protocol)
```

## Publishing

```bash
./publish.sh
```

The script stages all changes, commits with a timestamped message, and pushes to GitHub. GitHub Pages rebuilds and the site is live in 1–2 minutes.

To preview locally before publishing:

```bash
bundle install            # first time only
bundle exec jekyll serve  # then open http://localhost:4000
```

## Chinese typography auto-formatting

Every time you run `./publish.sh`, Markdown files in `_markdown/` and
`index.html` are automatically rewritten to follow the
[Chinese Copywriting Guidelines](https://github.com/sparanoid/chinese-copywriting-guidelines):

- A space is inserted between Chinese and Latin / digits
  (`100USD` → `100 USD`, `Hello世界` → `Hello 世界`)
- Half-width punctuation next to Chinese is converted to full-width
  (`你好,世界` → `你好，世界`)

What is **not** automated (still up to you):

- Proper-noun capitalization (`iPhone`, `GitHub`, `JavaScript`, `macOS`)
- Choosing between `「」` and `""` for quotation marks
- Avoiding repeated punctuation like `！！！`

This runs through [`@huacnlee/autocorrect`](https://github.com/huacnlee/autocorrect),
which is markdown-aware: front matter keys, code blocks' fences, and URLs are
left alone. Files in `_html/` are **never** touched.

To format manually without publishing:

```bash
npm run format
```

The first run installs the formatter (one-time `npm install`); subsequent runs
are instant. If Node.js is not installed, `publish.sh` warns and skips this
step instead of failing.

> **Note:** Front matter `title` values are formatted (so `酒精的安全剂量为0`
> becomes `酒精的安全剂量为 0` on the homepage), but `permalink` values are
> not modified — keep permalinks ASCII-safe to be safe.

## Typography

The font stack is bilingual and uses Apple's system fonts where available:

```css
font-family:
  -apple-system, BlinkMacSystemFont, "SF Pro Text",  /* Latin: SF Pro on Apple */
  "Helvetica Neue", Helvetica,                        /* Latin fallback */
  "PingFang SC",                                      /* Chinese: PingFang on Apple */
  "Hiragino Sans GB",                                 /* Chinese fallback */
  "Microsoft YaHei", 微软雅黑,                         /* Chinese on Windows */
  Arial, sans-serif;
```

Browsers fall back per glyph, so Latin and Chinese characters in the same paragraph each render in their best available font. Zero web fonts are downloaded.

## Privacy

This site is built to be **shared by hand**, not crawled or indexed. The
philosophy is: if you want someone to read a piece, you send them the link.

### No RSS / no newsletter

The `jekyll-feed` plugin has been removed from the `Gemfile`. There is no
`feed.xml`, no Atom feed, and no newsletter signup. There is intentionally no
way to subscribe — readers come back when they choose to.

### No search-engine indexing

Two layers of protection, so compliant crawlers stay out:

1. **`robots.txt`** disallows `/` for `User-agent: *` (every crawler that
   honors the standard, including Googlebot, Bingbot, Baiduspider, etc.).
2. **`<meta name="robots" content="noindex, nofollow">`** is injected into
   every page that uses the default layout (homepage, 404, all markdown
   posts), as a second layer in case `robots.txt` is missed.

> Already-indexed pages take 1–2 weeks to drop from Google after this lands.
> If you need them gone faster, submit a removal request in Google Search
> Console.

### No AI training crawlers

`robots.txt` also lists every known AI training / scraping bot by name, so
that bots which only honor a record matching their own `User-agent` (instead
of the wildcard) are also blocked. The list is sourced from the
community-maintained [ai.robots.txt](https://github.com/ai-robots-txt/ai.robots.txt)
project and currently covers, among others:

- **OpenAI** — `GPTBot`, `ChatGPT-User`, `OAI-SearchBot`
- **Anthropic** — `ClaudeBot`, `Claude-Web`, `anthropic-ai`
- **Google** — `Google-Extended`
- **Perplexity** — `PerplexityBot`, `Perplexity-User`
- **Common Crawl** — `CCBot`
- **ByteDance** — `Bytespider`
- **Meta** — `FacebookBot`, `Meta-ExternalAgent`, `Meta-ExternalFetcher`
- **Amazon** — `Amazonbot`
- **Apple** — `Applebot-Extended`
- **Cohere** — `cohere-ai`
- Other research / scraping bots: `Diffbot`, `AI2Bot`, `DuckAssistBot`,
  `ImagesiftBot`, `YouBot`, `Timpibot`, `omgili`, `omgilibot`

When new bots show up, copy them from
[ai.robots.txt](https://github.com/ai-robots-txt/ai.robots.txt) into
`robots.txt` and re-publish.

### Limits

`robots.txt` only blocks bots that **respect** it. Bad-faith scrapers ignore
it. Real protection from those would need server-side rate limiting or
authentication, which GitHub Pages does not offer. The trade-off is accepted:
this site lives at the edge with zero infrastructure.

## Custom domain

The `CNAME` file contains `elemer.net`. To use a different domain:

1. Replace the contents of `CNAME` with your domain.
2. At your DNS provider, point the domain at GitHub Pages:
   - **Apex domain:** four `A` records to `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - **Subdomain:** a single `CNAME` to `<username>.github.io`
3. In **Settings → Pages**, enable **Enforce HTTPS**.
