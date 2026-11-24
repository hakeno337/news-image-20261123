// The World Today, 23 November 2026 — second version.
// This entry's whole job is delivery: entry.png sits beside this file in
// the repository, and the program copies it, byte for byte, to the output
// as entry.png, so the judge sees exactly the image the repository holds.
// Before copying, it checks the file against the gate's own limits: a
// whole PNG or JPEG, at most 1 MiB, at most 1024 by 1024 pixels.
//
// In the grader the output is /output; outside it, MAKEFUN_OUTPUT_DIR
// stands in:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(source);

if (bytes.length > 1024 * 1024) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB gate limit`);
}

const isPng = bytes.length > 24 && bytes.toString('latin1', 1, 4) === 'PNG';
const isJpeg = bytes.length > 2 && bytes[0] === 0xff && bytes[1] === 0xd8;
if (!isPng && !isJpeg) {
  throw new Error('entry.png is neither a PNG nor a JPEG');
}

if (isPng) {
  const w = bytes.readUInt32BE(16);
  const h = bytes.readUInt32BE(20);
  if (w > 1024 || h > 1024) {
    throw new Error(`entry.png is ${w}x${h}, over the 1024x1024 gate limit`);
  }
}

if (isJpeg) {
  // Walk the segments to the start-of-frame marker holding the dimensions.
  let off = 2;
  let dims = null;
  while (off + 9 < bytes.length && bytes[off] === 0xff) {
    const marker = bytes[off + 1];
    if (marker >= 0xc0 && marker <= 0xcf && marker !== 0xc4 && marker !== 0xc8 && marker !== 0xcc) {
      dims = { h: bytes.readUInt16BE(off + 5), w: bytes.readUInt16BE(off + 7) };
      break;
    }
    off += 2 + bytes.readUInt16BE(off + 2);
  }
  if (dims && (dims.w > 1024 || dims.h > 1024)) {
    throw new Error(`entry image is ${dims.w}x${dims.h}, over the 1024x1024 gate limit`);
  }
}

copyFileSync(source, join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
