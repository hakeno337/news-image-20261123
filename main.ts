// The World Today, 23 November 2026: this program delivers the entry's image.
// It reads entry.png beside itself, checks it against the gate's own limits (a whole PNG or JPEG,
// at most 1 MiB and 1024 by 1024 pixels), and copies it byte for byte to the output as entry.png,
// so what the judge sees is exactly the file the repository holds.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(src);

if (bytes.length > 1024 * 1024) throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB gate limit`);

const isPng = bytes.length > 24 && bytes.toString('latin1', 1, 4) === 'PNG';
const isJpeg = bytes.length > 2 && bytes[0] === 0xff && bytes[1] === 0xd8;
if (!isPng && !isJpeg) throw new Error('entry.png is neither a PNG nor a JPEG');

if (isPng) {
  const w = bytes.readUInt32BE(16);
  const h = bytes.readUInt32BE(20);
  if (w > 1024 || h > 1024) throw new Error(`entry.png is ${w}x${h}, over the 1024x1024 gate limit`);
}

if (isJpeg) {
  // Walk the JPEG segments to the start-of-frame marker that carries the dimensions.
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

copyFileSync(src, join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
