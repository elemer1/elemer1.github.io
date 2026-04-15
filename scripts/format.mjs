#!/usr/bin/env node
// Format markdown / html prose with @huacnlee/autocorrect.
// Applies the chinese-copywriting-guidelines spacing & punctuation rules.
// Front matter and YAML headers are preserved.

import { readFileSync, writeFileSync } from 'fs';
import { extname, basename } from 'path';
import * as autocorrect from '@huacnlee/autocorrect';

const files = process.argv.slice(2);
if (files.length === 0) {
  console.error('Usage: node scripts/format.mjs <file> [<file> ...]');
  process.exit(1);
}

let changed = 0;
let errors = 0;

for (const file of files) {
  try {
    const original = readFileSync(file, 'utf8');
    const ext = extname(file).slice(1).toLowerCase();
    const filetype = ext === 'md' ? 'markdown' : ext || 'text';
    const result = autocorrect.formatFor(original, filetype);

    if (result.error) {
      console.error(`  error: ${file}: ${result.error}`);
      errors++;
      continue;
    }

    if (original !== result.out) {
      writeFileSync(file, result.out);
      console.log(`  formatted: ${basename(file)}`);
      changed++;
    }
  } catch (e) {
    console.error(`  error: ${file}: ${e.message}`);
    errors++;
  }
}

console.log(`\n${changed} file(s) formatted, ${errors} error(s)`);
process.exit(errors > 0 ? 1 : 0);
