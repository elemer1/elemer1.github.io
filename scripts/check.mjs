#!/usr/bin/env node
// Repository safety checks for Elemer publishing.
// Keeps the site intentionally simple: prose Markdown belongs in _markdown/,
// every published item has stable front matter, and YouTube embeds use the
// reusable include instead of ad-hoc iframe markup.

import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join, extname, basename } from 'node:path';

const ROOT = process.cwd();
const MD_DIR = join(ROOT, '_markdown');
const HTML_DIR = join(ROOT, '_html');
const ALLOWED_ROOT_MD = new Set(['README.md']);
const repoVisibility = (
  process.env.ELEMER_REPO_VISIBILITY ||
  process.env.GITHUB_REPOSITORY_VISIBILITY ||
  ''
).toLowerCase();

let errors = 0;
let warnings = 0;
const permalinks = new Map();

function fail(message) {
  console.error(`error: ${message}`);
  errors++;
}

function warn(message) {
  console.warn(`warning: ${message}`);
  warnings++;
}

function listFiles(dir, exts) {
  if (!existsSync(dir) || !statSync(dir).isDirectory()) return [];
  return readdirSync(dir)
    .filter((name) => exts.has(extname(name).toLowerCase()))
    .map((name) => join(dir, name));
}

// Strict, line-based front matter parser. Catches the YAML pitfalls that
// have silently dropped pages from past Jekyll builds:
//   1. Unquoted values containing ": " (Ruby YAML reads them as a nested
//      mapping and then aborts), e.g. `title: Cat Wu: AI PM应该干什么`.
//   2. Tabs or indented lines (we expect a flat top-level map).
//   3. Lines that aren't a "key: value" pair at all.
function parseFrontMatter(text, file) {
  if (!text.startsWith('---')) return null;
  const end = text.indexOf('\n---', 3);
  if (end === -1) {
    fail(`${file}: front matter is not closed (missing trailing ---)`);
    return null;
  }
  const fmText = text.slice(4, end);
  const body = text.slice(end + 4).replace(/^\r?\n/, '');
  const fm = {};
  const lines = fmText.split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const lineNum = i + 2; // +1 for 0-index, +1 for the opening ---
    if (line.includes('\t')) {
      fail(`${file}: front matter line ${lineNum} contains a tab; YAML uses spaces`);
      continue;
    }
    if (/^\s/.test(line)) {
      fail(`${file}: front matter line ${lineNum} is indented; only flat top-level "key: value" pairs are allowed`);
      continue;
    }
    const m = line.match(/^([A-Za-z_][A-Za-z0-9_-]*):(?:\s+(.*))?$/);
    if (!m) {
      fail(`${file}: front matter line ${lineNum} is not a "key: value" pair: ${JSON.stringify(line)}`);
      continue;
    }
    let [, key, rawVal] = m;
    let val = (rawVal ?? '').trim();
    const quoted =
      val.length >= 2 &&
      ((val.startsWith('"') && val.endsWith('"')) ||
        (val.startsWith("'") && val.endsWith("'")));
    if (quoted) {
      val = val.slice(1, -1);
    } else {
      if (/:\s/.test(val)) {
        fail(
          `${file}: front matter "${key}" contains an unquoted ": " — Ruby YAML reads this as a nested mapping and Jekyll will silently drop the file. Wrap the value in quotes (e.g. ${key}: "${val}")`,
        );
        continue;
      }
      if (val === 'true') val = true;
      else if (val === 'false') val = false;
    }
    fm[key] = val;
  }
  return { fm, body };
}

function stripFencedCode(text) {
  return text.replace(/(^|\n)(```|~~~)[\s\S]*?\n\2/g, '\n');
}

function hasEncryptedTrue(fm) {
  return fm.encrypted === true || fm.encrypted === 'true';
}

function checkPermalink(file, fm) {
  if (!fm.permalink || typeof fm.permalink !== 'string') return;
  if (!fm.permalink.startsWith('/') || !fm.permalink.endsWith('/')) {
    fail(`${file}: permalink must start and end with / (${fm.permalink})`);
  }
  const owner = permalinks.get(fm.permalink);
  if (owner) {
    fail(`${file}: duplicate permalink ${fm.permalink}; already used by ${owner}`);
  } else {
    permalinks.set(fm.permalink, file);
  }
}

function checkMarkdownPost(file) {
  const raw = readFileSync(file, 'utf8');
  const parsed = parseFrontMatter(raw, file);
  if (!parsed) {
    fail(`${file}: missing YAML front matter`);
    return;
  }
  const { fm, body } = parsed;
  if (!fm.title) fail(`${file}: missing required front matter field: title`);
  if (!fm.permalink) fail(`${file}: missing required front matter field: permalink`);
  if (fm.listed !== true && fm.listed !== false) {
    fail(`${file}: listed must be explicitly true or false`);
  }
  checkPermalink(file, fm);

  const renderableBody = stripFencedCode(body);
  const iframeMatches = renderableBody.match(/<iframe[\s\S]*?>/gi) || [];
  for (const iframe of iframeMatches) {
    if (/src=["'][^"']*(youtu\.be|youtube\.com\/watch)/i.test(iframe)) {
      fail(`${file}: YouTube iframe must use youtube.com/embed/<VIDEO_ID>, not youtu.be or youtube.com/watch`);
    }
    if (/youtube\.com\/embed/i.test(iframe)) {
      warn(`${file}: prefer {% include youtube.html id="VIDEO_ID" %} over hand-written YouTube iframe markup`);
    }
  }

  if (/(```|~~~)[\s\S]*?<iframe[\s\S]*?\1/.test(body)) {
    warn(`${file}: iframe appears inside a fenced code block; it will display as code, not render`);
  }

  if (hasEncryptedTrue(fm) && repoVisibility === 'public') {
    warn(`${file}: encrypted: true in a public repository — plaintext and password are visible in git history; treat the lock as cosmetic`);
  }
}

function checkHtmlPage(file) {
  const raw = readFileSync(file, 'utf8');
  const parsed = parseFrontMatter(raw, file);
  if (!parsed) {
    fail(
      `${file}: missing YAML front matter — _html/ entries must declare title, permalink, and listed, otherwise Jekyll treats the file as a raw asset and the homepage skips it`,
    );
    return;
  }
  const { fm } = parsed;
  if (!fm.title) fail(`${file}: missing required front matter field: title`);
  if (!fm.permalink) fail(`${file}: missing required front matter field: permalink`);
  if (fm.listed !== true && fm.listed !== false) {
    fail(`${file}: listed must be explicitly true or false`);
  }
  checkPermalink(file, fm);
  if (hasEncryptedTrue(fm) && repoVisibility === 'public') {
    warn(`${file}: encrypted: true in a public repository — plaintext and password are visible in git history; treat the lock as cosmetic`);
  }
}

// Root-level Markdown should not become accidental articles.
for (const name of readdirSync(ROOT)) {
  const path = join(ROOT, name);
  if (!statSync(path).isFile()) continue;
  if (extname(name).toLowerCase() === '.md' && !ALLOWED_ROOT_MD.has(name)) {
    fail(`${name}: prose Markdown articles must live in _markdown/, not the repository root`);
  }
}

for (const file of listFiles(MD_DIR, new Set(['.md']))) checkMarkdownPost(file);
for (const file of listFiles(HTML_DIR, new Set(['.html']))) checkHtmlPage(file);

if (warnings > 0) console.warn(`\n${warnings} warning(s)`);
if (errors > 0) {
  console.error(`\nContent checks failed with ${errors} error(s).`);
  process.exit(1);
}
console.log('Content checks passed.');
