#!/usr/bin/env node
/*
 * Measure a web game on a simulated phone: frame times and 2D-canvas calls per frame.
 *
 *   node phone_perf.mjs <url> [--setup "<js>"] [--wait 3] [--frames 180] [--throttle 4] [--dpr 3]
 *                             [--size 844x390] [--off "<js>"]...
 *
 *   --setup  JavaScript run in the page once it has loaded, to reach the scene worth measuring (start a run, spawn
 *            the biggest swarm, open a menu). It may return a promise.
 *   --wait   seconds to let the scene settle after setup before measuring.
 *   --off    JavaScript that switches one draw layer off (for example "game.drawGround = () => {}"); each --off is
 *            measured on its own after the baseline, so the layer whose removal saves the most stands out.
 *
 * Runs headless Chromium at a phone landscape size with a 3x screen, touch and CPU throttling (DevTools
 * Emulation.setCPUThrottlingRate). Prints median, p95 and worst frame time, frames over 50 ms, and the canvas calls
 * per frame (save, restore, fill, stroke, drawImage, fillText, strokeText, ...). Targets: median near 16.7 ms on
 * the worst-case scene, nothing over 50 ms while scrolling, fewer than about 500 save/restore pairs a frame.
 *
 * Needs Playwright (`npm i -g playwright`, or any cached playwright-core; set PLAYWRIGHT_PATH to its folder).
 */
import { existsSync, readdirSync } from "node:fs";
import { createRequire } from "node:module";
import { homedir } from "node:os";
import { join } from "node:path";

function loadPlaywright() {
  const require = createRequire(import.meta.url);
  const tries = [process.env.PLAYWRIGHT_PATH, "playwright", "playwright-core"].filter(Boolean);
  const npx = join(homedir(), ".npm/_npx");
  if (existsSync(npx)) for (const d of readdirSync(npx)) for (const n of ["playwright", "playwright-core"]) tries.push(join(npx, d, "node_modules", n));
  for (const t of tries) { try { return require(t); } catch { /* try the next location */ } }
  throw new Error("Playwright not found: npm i -g playwright, or set PLAYWRIGHT_PATH to a playwright(-core) folder.");
}

function parseArgs(argv) {
  const o = { url: null, setup: "", wait: 3, frames: 180, throttle: 4, dpr: 3, size: "844x390", off: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i], v = () => { if (i + 1 >= argv.length) throw new Error(`${a} needs a value`); return argv[++i]; };
    if (a === "--setup") o.setup = v();
    else if (a === "--wait") o.wait = Number(v());
    else if (a === "--frames") o.frames = Number(v());
    else if (a === "--throttle") o.throttle = Number(v());
    else if (a === "--dpr") o.dpr = Number(v());
    else if (a === "--size") o.size = v();
    else if (a === "--off") o.off.push(v());
    else if (!o.url) o.url = a;
    else throw new Error(`unknown argument ${a}`);
  }
  if (!o.url) throw new Error("usage: node phone_perf.mjs <url> [--setup js] [--off js]...");
  if (!/^\d+x\d+$/.test(o.size)) throw new Error("--size must look like 844x390");
  return o;
}

// Counts calls on every 2D context in the page; installed before any page script runs.
function counter() {
  window.__calls = {};
  const P = CanvasRenderingContext2D.prototype;
  ["save", "restore", "fill", "stroke", "fillRect", "drawImage", "fillText", "strokeText", "measureText", "beginPath", "ellipse", "arc",
    "createLinearGradient", "createRadialGradient", "createPattern", "getImageData", "putImageData"].forEach((m) => {
    const orig = P[m];
    P[m] = function () { window.__calls[m] = (window.__calls[m] || 0) + 1; return orig.apply(this, arguments); };
  });
}

async function sample(page, frames) {
  return page.evaluate(async (n) => {
    window.__calls = {};
    const t = []; let last = performance.now();
    await new Promise((res) => { let k = 0; function f(now) { t.push(now - last); last = now; if (++k < n) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
    const s = t.slice(1).sort((a, b) => a - b), at = (q) => +s[Math.min(s.length - 1, Math.floor(s.length * q))].toFixed(1);
    const per = {}; for (const k in window.__calls) per[k] = Math.round(window.__calls[k] / n);
    return { median: at(0.5), p95: at(0.95), worst: at(1), over50: s.filter((x) => x > 50).length, calls: per };
  }, frames);
}

function report(label, r) {
  const calls = Object.entries(r.calls).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k} ${v}`).join(", ");
  console.log(`${label.padEnd(14)} median ${r.median} ms  p95 ${r.p95}  worst ${r.worst}  >50ms ${r.over50}`);
  console.log(`${"".padEnd(14)} per frame: ${calls || "(no 2D canvas calls)"}`);
}

const o = parseArgs(process.argv.slice(2));
const [w, h] = o.size.split("x").map(Number);
const { chromium } = loadPlaywright();
const browser = await chromium.launch({ headless: true });
try {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: o.dpr, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.addInitScript(counter);
  await page.goto(o.url, { waitUntil: "load" });
  if (o.setup) await page.evaluate(`(async () => { ${o.setup} })()`);
  await page.waitForTimeout(o.wait * 1000);
  const cdp = await ctx.newCDPSession(page);
  if (o.throttle > 1) await cdp.send("Emulation.setCPUThrottlingRate", { rate: o.throttle });
  console.log(`${o.url}  ${o.size} at ${o.dpr}x, CPU ${o.throttle}x slower, ${o.frames} frames`);
  report("baseline", await sample(page, o.frames));
  for (const js of o.off) {
    await page.reload({ waitUntil: "load" });
    if (o.setup) await page.evaluate(`(async () => { ${o.setup} })()`);
    await page.evaluate(js);
    await page.waitForTimeout(o.wait * 1000);
    report(`off: ${js.slice(0, 40)}`, await sample(page, o.frames));
  }
  if (errors.length) console.log(`page errors: ${errors.slice(0, 3).join(" | ")}`);
} finally {
  await browser.close();
}
