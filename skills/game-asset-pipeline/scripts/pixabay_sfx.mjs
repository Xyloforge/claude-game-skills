#!/usr/bin/env node
/*
 * Search and download Pixabay sound effects through a real headless Chrome (curl, wget, fetch and Python requests get
 * a 403 from Pixabay's bot protection; so does Playwright's bundled Chromium with its "HeadlessChrome" user-agent).
 *
 *   node pixabay_sfx.mjs search <outDir> "sword clash" "metal impact" ...
 *       Saves <outDir>/_results/<query>.json and prints the top results: id, length, title, author, AI flag.
 *   node pixabay_sfx.mjs get <outDir> clang1=241729 clang2=393837 ...
 *       Downloads each id (it must appear in a saved search) to <outDir>/<name>.mp3 plus <name>-source.json
 *       (title, author, id, page URL, SHA-256) for AUDIO.md.
 *
 * Needs Google Chrome installed and Playwright (`npm i -g playwright` or any cached playwright-core; set
 * PLAYWRIGHT_PATH to its folder if it is not found). Runs headless. It pauses between requests, solves no
 * CAPTCHA and guesses no CDN URLs. If a search returns a verification page, stop and pick sounds by hand on
 * pixabay.com into a folder; the processing step needs no network.
 */
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { homedir } from "node:os";
import { join } from "node:path";

const PAUSE_SEARCH = 2200, PAUSE_DOWNLOAD = 1800;

function loadPlaywright() {
  const require = createRequire(import.meta.url);
  const tries = [process.env.PLAYWRIGHT_PATH, "playwright", "playwright-core"].filter(Boolean);
  const npx = join(homedir(), ".npm/_npx");
  if (existsSync(npx)) {
    for (const d of readdirSync(npx)) {
      for (const name of ["playwright", "playwright-core"]) tries.push(join(npx, d, "node_modules", name));
    }
  }
  for (const t of tries) {
    try { return require(t); } catch { /* try the next location */ }
  }
  throw new Error("Playwright not found: npm i -g playwright, or set PLAYWRIGHT_PATH to a playwright(-core) folder.");
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const slug = (q) => q.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

async function openBrowser() {
  const { chromium } = loadPlaywright();
  const browser = await chromium.launch({ channel: "chrome", headless: true });
  const version = browser.version();
  const context = await browser.newContext({
    userAgent: `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${version} Safari/537.36`,
    locale: "en-US",
    viewport: { width: 1440, height: 900 },
  });
  return { browser, page: await context.newPage() };
}

async function searchPage(page, query) {
  const url = `https://pixabay.com/sound-effects/search/${encodeURIComponent(query)}/`;
  const res = await page.goto(url, { waitUntil: "domcontentloaded" });
  try {
    await page.waitForFunction(() => window.__BOOTSTRAP__?.page?.results, null, { timeout: 30000 });
  } catch {
    throw new Error(`"${query}": no results data (HTTP ${res?.status()}, title "${await page.title()}"). Likely a bot check; pick by hand.`);
  }
  return page.evaluate(() => window.__BOOTSTRAP__.page.results);
}

async function search(outDir, queries) {
  const dir = join(outDir, "_results");
  mkdirSync(dir, { recursive: true });
  const { browser, page } = await openBrowser();
  try {
    for (const q of queries) {
      const results = await searchPage(page, q);
      writeFileSync(join(dir, `${slug(q)}.json`), JSON.stringify({ query: q, results }, null, 2));
      console.log(`\n# ${q} (${results.length} results)`);
      for (const r of results.slice(0, 15)) {
        const ai = r.isAiGenerated ? "  [AI - avoid]" : "";
        const len = r.duration != null ? `${Number(r.duration).toFixed(1)}s` : "?";
        console.log(`${String(r.id).padEnd(8)} ${len.padStart(6)}  ${r.name || r.title || ""}  - ${r.user?.username || r.username || "?"}${ai}`);
      }
      await sleep(PAUSE_SEARCH);
    }
  } finally {
    await browser.close();
  }
}

function savedResults(outDir) {
  const dir = join(outDir, "_results");
  const byId = new Map();
  if (!existsSync(dir)) return byId;
  for (const f of readdirSync(dir)) {
    if (!f.endsWith(".json")) continue;
    for (const r of JSON.parse(readFileSync(join(dir, f), "utf8")).results) byId.set(String(r.id), r);
  }
  return byId;
}

async function get(outDir, pairs) {
  const byId = savedResults(outDir);
  const wanted = pairs.map((p) => {
    const [name, id] = p.split("=");
    const item = byId.get(id);
    if (!name || !item) throw new Error(`${p}: use name=id with an id from a saved search (run search first).`);
    return { name, id, item };
  });
  const { browser, page } = await openBrowser();
  try {
    await page.goto("https://pixabay.com/sound-effects/", { waitUntil: "domcontentloaded" });
    for (const { name, id, item } of wanted) {
      const path = join(outDir, `${name}.mp3`);
      if (existsSync(path)) { console.log(`skip ${name}: exists`); continue; }
      const src = item.sources?.src;
      if (!src) { console.log(`skip ${name}: result ${id} has no sources.src`); continue; }
      // Fetch inside the page so the request carries the browser's session, as a click would.
      const r = await page.evaluate(async (url) => {
        const res = await fetch(url);
        if (!res.ok) return { status: res.status };
        const buf = new Uint8Array(await res.arrayBuffer());
        let bin = "";
        for (let i = 0; i < buf.length; i += 0x8000) bin += String.fromCharCode(...buf.subarray(i, i + 0x8000));
        return { status: res.status, type: res.headers.get("content-type") || "", data: btoa(bin) };
      }, src);
      if (r.status !== 200 || !r.type.startsWith("audio/")) { console.log(`fail ${name}: HTTP ${r.status} ${r.type || ""}`); continue; }
      const bytes = Buffer.from(r.data, "base64");
      writeFileSync(path, bytes);
      writeFileSync(join(outDir, `${name}-source.json`), JSON.stringify({
        name, id: item.id, title: item.name || item.title, author: item.user?.username || item.username,
        page: `https://pixabay.com/sound-effects/${item.id}/`, isAiGenerated: !!item.isAiGenerated,
        bytes: bytes.length, sha256: createHash("sha256").update(bytes).digest("hex"),
      }, null, 2));
      console.log(`ok ${name}: ${bytes.length} bytes from ${id}`);
      await sleep(PAUSE_DOWNLOAD);
    }
  } finally {
    await browser.close();
  }
}

const [cmd, outDir, ...rest] = process.argv.slice(2);
if (!["search", "get"].includes(cmd) || !outDir || !rest.length) {
  console.log('Usage:\n  node pixabay_sfx.mjs search <outDir> "query" ...\n  node pixabay_sfx.mjs get <outDir> name=id ...');
  process.exit(1);
}
(cmd === "search" ? search(outDir, rest) : get(outDir, rest)).catch((e) => { console.error(e.message); process.exit(1); });
