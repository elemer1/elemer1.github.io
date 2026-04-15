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

## Custom domain

The `CNAME` file contains `elemer.net`. To use a different domain:

1. Replace the contents of `CNAME` with your domain.
2. At your DNS provider, point the domain at GitHub Pages:
   - **Apex domain:** four `A` records to `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - **Subdomain:** a single `CNAME` to `<username>.github.io`
3. In **Settings → Pages**, enable **Enforce HTTPS**.
