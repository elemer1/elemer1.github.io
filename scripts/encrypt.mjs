#!/usr/bin/env node
// Encrypts articles with `encrypted: true` in their front matter, in place.
// Designed to run in GitHub Actions before `jekyll build`, so the deployed
// site serves a password prompt + ciphertext instead of the plaintext source.
//
// Source layout (plaintext + password live in the repo — keep the repo
// private):
//   _html/<name>.html      full standalone HTML doc after front matter
//   _markdown/<name>.md    markdown body after front matter
//
// Front matter:
//   ---
//   title: "..."
//   permalink: /slug/
//   listed: true
//   encrypted: true
//   password: "your-password"
//   ---
//
// Output: self-contained HTML at _html/<name>.html with a password prompt,
// the ciphertext, and a Web Crypto decryptor. The `encrypted` and `password`
// fields are stripped from the output front matter. When the source is .md,
// the original .md is removed and the output is written as .html.

import {
  readFileSync,
  writeFileSync,
  readdirSync,
  existsSync,
  statSync,
  unlinkSync,
} from "node:fs";
import { createHash, webcrypto as crypto } from "node:crypto";
import { join, dirname, extname, basename } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const HTML_DIR = join(ROOT, "_html");
const MD_DIR = join(ROOT, "_markdown");
const PBKDF2_ITERATIONS = 200000;
const HASH_MARKER = "<!-- elemer-encrypt source-hash:";

function parseFrontMatter(text) {
  if (!text.startsWith("---")) return null;
  const end = text.indexOf("\n---", 3);
  if (end === -1) return null;
  const fmText = text.slice(4, end);
  const body = text.slice(end + 4).replace(/^\r?\n/, "");
  const fm = {};
  for (const line of fmText.split(/\r?\n/)) {
    const m = line.match(/^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$/);
    if (!m) continue;
    let [, key, val] = m;
    val = val.trim();
    if (
      (val.startsWith('"') && val.endsWith('"')) ||
      (val.startsWith("'") && val.endsWith("'"))
    ) {
      val = val.slice(1, -1);
    } else if (val === "true") val = true;
    else if (val === "false") val = false;
    fm[key] = val;
  }
  return { fm, body };
}

function toBase64(u8) {
  return Buffer.from(u8).toString("base64");
}

async function encryptBody(plaintext, password) {
  const enc = new TextEncoder();
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const keyMaterial = await crypto.subtle.importKey(
    "raw",
    enc.encode(password),
    "PBKDF2",
    false,
    ["deriveKey"],
  );
  const key = await crypto.subtle.deriveKey(
    { name: "PBKDF2", salt, iterations: PBKDF2_ITERATIONS, hash: "SHA-256" },
    keyMaterial,
    { name: "AES-GCM", length: 256 },
    false,
    ["encrypt"],
  );
  const ct = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv },
    key,
    enc.encode(plaintext),
  );
  return {
    v: 1,
    iterations: PBKDF2_ITERATIONS,
    salt: toBase64(salt),
    iv: toBase64(iv),
    ciphertext: toBase64(new Uint8Array(ct)),
  };
}

function sourceHash({ fm, body, password, type }) {
  return createHash("sha256")
    .update(
      JSON.stringify({
        v: 1,
        type,
        password,
        title: fm.title ?? "",
        permalink: fm.permalink ?? "",
        listed: !!fm.listed,
        body,
      }),
    )
    .digest("hex");
}

function readExistingHash(path) {
  if (!existsSync(path)) return null;
  try {
    const head = readFileSync(path, "utf8").slice(0, 4096);
    const m = head.match(
      /<!-- elemer-encrypt source-hash: ([0-9a-f]{64}) -->/,
    );
    return m ? m[1] : null;
  } catch {
    return null;
  }
}

function renderPage({ title, permalink, listed, type, payload, hash }) {
  const fmLines = ["---"];
  fmLines.push(`title: ${JSON.stringify(title)}`);
  fmLines.push(`permalink: ${JSON.stringify(permalink)}`);
  if (listed) fmLines.push("listed: true");
  fmLines.push("---");
  const fm = fmLines.join("\n");

  const payloadJson = JSON.stringify({ type, ...payload });

  return String.raw`${fm}
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${escapeHtml(title)} - Elemer</title>
<meta name="robots" content="noindex, nofollow">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
${HASH_MARKER} ${hash} -->
<style>
*{margin:0;padding:0;box-sizing:border-box;color:#000}
html,body{height:100%;background:#fff}
body{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",微软雅黑,Arial,sans-serif;font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
.lock{max-width:320px;margin:0 auto;padding:120px 20px;text-align:left}
.lock h1{font-size:20px;font-weight:600;margin-bottom:24px}
.lock h1 a{color:#000;text-decoration:none}
.lock h1 a:hover{text-decoration:underline}
.lock form{display:flex;gap:8px}
.lock input{flex:1;min-width:0;padding:8px 10px;font:inherit;color:#000;background:#fff;border:1px solid #000;border-radius:0;outline:none}
.lock input:focus{border-color:#0000ee}
.lock button{padding:8px 14px;font:inherit;color:#fff;background:#000;border:1px solid #000;cursor:pointer}
.lock button:hover{background:#0000ee;border-color:#0000ee}
.lock button:disabled{opacity:.5;cursor:wait}
.lock .err{margin-top:12px;font-size:14px;color:#b00020}
.md-post{max-width:650px;margin:0 auto;padding:60px 20px}
.md-post header{margin-bottom:60px}
.md-post header h1{font-size:20px;font-weight:600}
.md-post header h1 a{color:#000;text-decoration:none}
.md-post .post-title{font-size:32px;font-weight:700;margin:0 0 30px 0;line-height:1.25}
.md-post main h1{font-size:28px;font-weight:700;margin:50px 0 25px 0;line-height:1.25}
.md-post main h2{font-size:22px;font-weight:700;margin:40px 0 20px 0;line-height:1.3}
.md-post main h3{font-size:19px;font-weight:600;margin:30px 0 15px 0;line-height:1.35}
.md-post main h4{font-size:17px;font-weight:600;margin:25px 0 12px 0;line-height:1.4}
.md-post main p{margin:15px 0}
.md-post main ul,.md-post main ol{margin:15px 0;padding-left:30px}
.md-post main li{margin:5px 0}
.md-post main a{color:#0000ee;text-decoration:none}
.md-post main a:hover{text-decoration:underline}
.md-post main blockquote{margin:20px 0;padding:10px 16px;border-left:4px solid #d0d7de;background:#f6f8fa;color:#57606a}
.md-post main img{max-width:100%;height:auto;display:block}
.md-post main hr{border:0;border-top:1px solid #000;margin:40px 0}
.md-post main pre{overflow-x:auto;max-width:100%;background:#f6f8fa;padding:14px 16px;border-radius:6px;font-size:14px;line-height:1.5;margin:20px 0}
.md-post main code{font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;font-size:.9em;padding:2px 5px;background:#f6f8fa;border-radius:4px}
.md-post main pre code{padding:0;background:transparent;font-size:inherit;border-radius:0}
.md-post main table{display:block;max-width:100%;overflow-x:auto;border-collapse:collapse;margin:20px 0;font-size:15px}
.md-post main th,.md-post main td{padding:8px 12px;border:1px solid #e5e5e5;vertical-align:top;text-align:left;line-height:1.5}
.md-post main th{background:#f6f8fa;font-weight:600}
</style>
</head>
<body>
<div class="lock" id="lock">
  <h1><a href="/">Elemer</a></h1>
  <form id="lock-form" autocomplete="off">
    <input id="pw" type="password" placeholder="Password" autofocus autocomplete="off" autocapitalize="none" autocorrect="off" spellcheck="false">
    <button id="submit" type="submit">Enter</button>
  </form>
  <div id="err" class="err" hidden>Wrong password.</div>
</div>
<script id="payload" type="application/json">${payloadJson.replace(/</g, "\\u003c")}</script>
<script>
(function(){
  var PAYLOAD = JSON.parse(document.getElementById('payload').textContent);
  var form = document.getElementById('lock-form');
  var pw = document.getElementById('pw');
  var btn = document.getElementById('submit');
  var err = document.getElementById('err');

  function b64ToBytes(s){
    var bin = atob(s);
    var out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }

  async function decrypt(password){
    var enc = new TextEncoder();
    var km = await crypto.subtle.importKey(
      'raw', enc.encode(password), 'PBKDF2', false, ['deriveKey']
    );
    var key = await crypto.subtle.deriveKey(
      { name: 'PBKDF2', salt: b64ToBytes(PAYLOAD.salt), iterations: PAYLOAD.iterations, hash: 'SHA-256' },
      km,
      { name: 'AES-GCM', length: 256 },
      false,
      ['decrypt']
    );
    var pt = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv: b64ToBytes(PAYLOAD.iv) },
      key,
      b64ToBytes(PAYLOAD.ciphertext)
    );
    return new TextDecoder().decode(pt);
  }

  function renderMarkdown(md, title){
    var body = '<main>' + mdToHtml(md) + '</main>';
    return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
      + '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
      + '<title>' + escapeHtml(title) + ' - Elemer</title>'
      + '<meta name="robots" content="noindex, nofollow">'
      + '<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">'
      + document.querySelector('style').outerHTML
      + '</head><body><article class="md-post">'
      + '<header><h1><a href="/">Elemer</a></h1></header>'
      + '<h1 class="post-title">' + escapeHtml(title) + '</h1>'
      + body
      + '</article></body></html>';
  }

  function escapeHtml(s){
    return s.replace(/[&<>"']/g, function(c){
      return { '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c];
    });
  }

  // Minimal markdown → HTML (headings, paragraphs, lists, code, bold/italic, links, hr, blockquote).
  function mdToHtml(src){
    var lines = src.replace(/\r\n?/g, '\n').split('\n');
    var html = '', i = 0;
    function inline(t){
      t = t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      t = t.replace(/\`([^\`]+)\`/g, '<code>$1</code>');
      t = t.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
      t = t.replace(/\*([^*]+)\*/g, '<em>$1</em>');
      t = t.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
      return t;
    }
    while (i < lines.length){
      var line = lines[i];
      if (/^\s*$/.test(line)) { i++; continue; }
      var h = line.match(/^(#{1,6})\s+(.*)$/);
      if (h) { html += '<h' + h[1].length + '>' + inline(h[2]) + '</h' + h[1].length + '>'; i++; continue; }
      if (/^\s*---\s*$/.test(line)) { html += '<hr>'; i++; continue; }
      if (/^\`\`\`/.test(line)) {
        i++;
        var code = '';
        while (i < lines.length && !/^\`\`\`/.test(lines[i])) { code += lines[i] + '\n'; i++; }
        i++;
        html += '<pre><code>' + code.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') + '</code></pre>';
        continue;
      }
      if (/^\s*>\s?/.test(line)) {
        var bq = '';
        while (i < lines.length && /^\s*>\s?/.test(lines[i])) { bq += lines[i].replace(/^\s*>\s?/, '') + '\n'; i++; }
        html += '<blockquote>' + mdToHtml(bq) + '</blockquote>';
        continue;
      }
      if (/^\s*[-*]\s+/.test(line)) {
        var items = [];
        while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) {
          items.push(lines[i].replace(/^\s*[-*]\s+/, ''));
          i++;
        }
        html += '<ul>' + items.map(function(x){ return '<li>' + inline(x) + '</li>'; }).join('') + '</ul>';
        continue;
      }
      if (/^\s*\d+\.\s+/.test(line)) {
        var oitems = [];
        while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) {
          oitems.push(lines[i].replace(/^\s*\d+\.\s+/, ''));
          i++;
        }
        html += '<ol>' + oitems.map(function(x){ return '<li>' + inline(x) + '</li>'; }).join('') + '</ol>';
        continue;
      }
      var para = line;
      i++;
      while (i < lines.length && !/^\s*$/.test(lines[i]) && !/^(#{1,6}\s|>\s|[-*]\s|\d+\.\s|\`\`\`|---\s*$)/.test(lines[i])) {
        para += ' ' + lines[i];
        i++;
      }
      html += '<p>' + inline(para) + '</p>';
    }
    return html;
  }

  form.addEventListener('submit', async function(e){
    e.preventDefault();
    err.hidden = true;
    btn.disabled = true;
    try {
      var plaintext = await decrypt(pw.value);
      var doc = PAYLOAD.type === 'markdown'
        ? renderMarkdown(plaintext, ${JSON.stringify(title)})
        : plaintext;
      document.open();
      document.write(doc);
      document.close();
    } catch (e2) {
      err.hidden = false;
      btn.disabled = false;
      pw.select();
    }
  });
})();
</script>
</body>
</html>
`;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[c]);
}

async function processFile(srcPath) {
  const filename = basename(srcPath);
  const raw = readFileSync(srcPath, "utf8");
  const parsed = parseFrontMatter(raw);
  if (!parsed) return false;
  const { fm, body } = parsed;
  if (fm.encrypted !== true) return false;
  if (!fm.password || typeof fm.password !== "string") {
    throw new Error(`${filename}: encrypted: true but no password in front matter`);
  }
  if (!fm.title || !fm.permalink) {
    throw new Error(`${filename}: title and permalink are required`);
  }

  const ext = extname(filename).toLowerCase();
  const type = ext === ".md" ? "markdown" : "html";
  const outName = basename(filename, ext) + ".html";
  const outPath = join(HTML_DIR, outName);

  const hash = sourceHash({ fm, body, password: fm.password, type });
  const existingHash = readExistingHash(outPath);
  if (existingHash === hash && outPath === srcPath) {
    console.log(`  unchanged: ${outName}`);
    return true;
  }

  const payload = await encryptBody(body, fm.password);
  const page = renderPage({
    title: fm.title,
    permalink: fm.permalink,
    listed: !!fm.listed,
    type,
    payload,
    hash,
  });
  writeFileSync(outPath, page);

  // Source was .md: remove the original so Jekyll doesn't also render it.
  if (srcPath !== outPath && existsSync(srcPath)) {
    unlinkSync(srcPath);
  }
  console.log(`  encrypted: ${outName}`);
  return true;
}

async function main() {
  const sources = [];
  for (const dir of [HTML_DIR, MD_DIR]) {
    if (!existsSync(dir) || !statSync(dir).isDirectory()) continue;
    for (const f of readdirSync(dir)) {
      if (/\.(html|md)$/i.test(f)) sources.push(join(dir, f));
    }
  }
  let processed = 0;
  for (const src of sources) {
    if (await processFile(src)) processed++;
  }
  if (processed === 0) {
    console.log("No files with `encrypted: true`; nothing to do.");
  } else {
    console.log(`Done. ${processed} file(s) encrypted.`);
  }
}

main().catch((e) => {
  console.error("Encryption failed:", e.message);
  process.exit(1);
});
