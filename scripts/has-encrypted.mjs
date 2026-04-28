#!/usr/bin/env node
// Detect whether any source article asks for password encryption.
// Prints a GitHub Actions output line: encrypted=true|false.

import { appendFileSync, existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join, extname } from 'node:path';

const ROOT = process.cwd();
const SOURCE_DIRS = ['_markdown', '_html'];

function listFiles(dir, exts) {
  if (!existsSync(dir) || !statSync(dir).isDirectory()) return [];
  return readdirSync(dir)
    .filter((name) => exts.has(extname(name).toLowerCase()))
    .map((name) => join(dir, name));
}

function parseFrontMatter(text) {
  if (!text.startsWith('---')) return null;
  const end = text.indexOf('\n---', 3);
  if (end === -1) return null;
  const fmText = text.slice(4, end);
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
    } else if (val === 'true') val = true;
    else if (val === 'false') val = false;
    fm[key] = val;
  }
  return fm;
}

let encrypted = false;
for (const dirName of SOURCE_DIRS) {
  const dir = join(ROOT, dirName);
  for (const file of listFiles(dir, new Set(['.md', '.html']))) {
    const fm = parseFrontMatter(readFileSync(file, 'utf8'));
    if (fm && (fm.encrypted === true || fm.encrypted === 'true')) {
      encrypted = true;
      break;
    }
  }
  if (encrypted) break;
}

const value = encrypted ? 'true' : 'false';
console.log(`encrypted=${value}`);
if (process.env.GITHUB_OUTPUT) {
  appendFileSync(process.env.GITHUB_OUTPUT, `encrypted=${value}\n`);
}
