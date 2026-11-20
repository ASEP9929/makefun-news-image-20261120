// news-image-20261120 entry: "The World in One Day" for Friday
// 20 November 2026. The image is entry.png beside this file: a front
// page drawn for 20 November 2026 (Trump-Xi-Putin trilateral summit in
// Shenzhen, ICJ Myanmar genocide ruling, Cyclone Akvan landfall,
// Voyager 1 one light-day, GTA VI passing $1.8bn, Kyiv embassy strikes).
// This program only copies it to the output directory, so every run
// writes the exact same bytes. Node standard library only, no network.
// Deterministic by construction: the program reads one fixed file and
// copies it byte for byte, so a second run can only write the same PNG.
//
// Run outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, 'entry.png'), target);

// Sanity check: the output must be the whole image we ship, nothing else.
const bytes = statSync(target).size;
if (bytes === 0 || bytes > 1048576) {
  throw new Error(`entry.png is ${bytes} bytes, expected 1..1048576`);
}
const check = readFileSync(target);
const source = readFileSync(join(here, 'entry.png'));
if (check.length !== source.length || !check.equals(source)) {
  throw new Error('output mismatch: copied bytes differ from entry.png');
}
// The file must be a whole PNG: the judge tells PNG from JPEG by the
// first bytes, so refuse anything that is not a PNG signature.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!check.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error('output is not a PNG file');
}
console.log(`wrote ${target} (${bytes} bytes, verified)`);
