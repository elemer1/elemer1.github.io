#!/usr/bin/env node
// Encrypts articles with `encrypted: true` in their front matter.
//
// Pipeline (runs in GitHub Actions):
//   1. `jekyll build`            First pass renders every article — including
//                                encrypted ones — to _site/ through the full
//                                Jekyll stack: kramdown, _layouts/post.html,
//                                _layouts/default.html, MathJax, TOC, etc.
//                                The plaintext we capture here is exactly
//                                what a non-encrypted post would look like.
//   2. `node scripts/encrypt.mjs` For each file with `encrypted: true`, read
//                                the rendered HTML from _site/, encrypt it
//                                with AES-GCM, and overwrite the source with
//                                a password-lock page containing the
//                                ciphertext. .md sources are converted to
//                                .html and the original .md is deleted so
//                                Jekyll doesn't re-render the plaintext.
//   3. `jekyll build`            Second pass rebuilds _site/ with the
//                                password-lock pages replacing the originals.
//
// After the visitor enters the correct password the decryptor calls
// `document.open(); document.write(plaintext); document.close();` so the
// decrypted document is byte-identical to what Jekyll produced in step 1.
// There is no client-side markdown rendering: .md and .html articles take
// the same code path after decryption.

import {
  readFileSync,
  writeFileSync,
  readdirSync,
  existsSync,
  statSync,
  unlinkSync,
} from "node:fs";
import { webcrypto as crypto } from "node:crypto";
import { join, dirname, extname, basename } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const HTML_DIR = join(ROOT, "_html");
const MD_DIR = join(ROOT, "_markdown");
const SITE_DIR = join(ROOT, "_site");
const PBKDF2_ITERATIONS = 200000;

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

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[c]);
}

function renderPage({ title, permalink, listed, payload }) {
  const fmLines = ["---"];
  fmLines.push(`title: ${JSON.stringify(title)}`);
  fmLines.push(`permalink: ${JSON.stringify(permalink)}`);
  if (listed) fmLines.push("listed: true");
  fmLines.push("---");
  const fm = fmLines.join("\n");

  const payloadJson = JSON.stringify(payload).replace(/</g, "\\u003c");

  return String.raw`${fm}
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${escapeHtml(title)} - Elemer</title>
<meta name="robots" content="noindex, nofollow">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
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
</style>
</head>
<body>
<div class="lock">
  <h1><a href="/">Elemer</a></h1>
  <form id="lock-form" autocomplete="off">
    <input id="pw" type="password" placeholder="Password" autofocus autocomplete="off" autocapitalize="none" autocorrect="off" spellcheck="false">
    <button id="submit" type="submit">Enter</button>
  </form>
  <div id="err" class="err" hidden>Wrong password.</div>
</div>
<script id="payload" type="application/json">${payloadJson}</script>
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

  form.addEventListener('submit', async function(e){
    e.preventDefault();
    err.hidden = true;
    btn.disabled = true;
    try {
      var plaintext = await decrypt(pw.value);
      document.open();
      document.write(plaintext);
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

function renderedPathForPermalink(permalink) {
  const clean = permalink.replace(/^\/+|\/+$/g, "");
  if (!clean) return join(SITE_DIR, "index.html");
  return join(SITE_DIR, clean, "index.html");
}

async function processFile(srcPath) {
  const filename = basename(srcPath);
  const raw = readFileSync(srcPath, "utf8");
  const parsed = parseFrontMatter(raw);
  if (!parsed) return false;
  const { fm } = parsed;
  if (fm.encrypted !== true) return false;
  if (!fm.password || typeof fm.password !== "string") {
    throw new Error(
      `${filename}: encrypted: true but no password in front matter`,
    );
  }
  if (!fm.title || !fm.permalink) {
    throw new Error(`${filename}: title and permalink are required`);
  }

  const renderedPath = renderedPathForPermalink(fm.permalink);
  if (!existsSync(renderedPath)) {
    throw new Error(
      `${filename}: rendered file not found at ${renderedPath}. ` +
        `Run \`bundle exec jekyll build\` before \`node scripts/encrypt.mjs\` ` +
        `so the encryptor can capture the fully rendered plaintext.`,
    );
  }
  const renderedHtml = readFileSync(renderedPath, "utf8");

  const ext = extname(filename).toLowerCase();
  const outName = basename(filename, ext) + ".html";
  const outPath = join(HTML_DIR, outName);

  const payload = await encryptBody(renderedHtml, fm.password);
  const page = renderPage({
    title: fm.title,
    permalink: fm.permalink,
    listed: !!fm.listed,
    payload,
  });
  writeFileSync(outPath, page);

  // Source was .md: remove the original so Jekyll doesn't also render it on
  // the second pass.
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
