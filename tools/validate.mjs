#!/usr/bin/env node
/*
 * Repository checks, run in CI and before every release:
 *   - plugin.json and marketplace.json parse and carry their required fields;
 *   - every skill folder listed in plugin.json has a SKILL.md whose front matter has a `name` matching the folder
 *     and a non-empty `description`;
 *   - every relative Markdown link inside a skill points at a file that exists;
 *   - no skill file carries private links or machine paths (wiki links like [[note]], ~/.claude/skills paths, home
 *     folders): skills are general and must work on any machine;
 *   - every .mjs script passes `node --check` and every .py script compiles.
 * Exits 1 on the first group of failures, printing all of them.
 */
import { execFileSync } from "node:child_process";
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
// Things that only make sense on one person's machine or notes.
const PRIVATE = [
  [/\[\[[^\]]+\]\]/, "private wiki link ([[...]])"],
  [/~\/\.claude\/skills/, "hard-coded ~/.claude/skills path (use ${CLAUDE_SKILL_DIR})"],
  [/\/(Users|home)\/[a-z0-9_.-]+\//i, "absolute home-folder path"],
];
const problems = [];
const fail = (msg) => problems.push(msg);

function readJson(rel) {
  try { return JSON.parse(readFileSync(join(root, rel), "utf8")); } catch (e) { fail(`${rel}: ${e.message}`); return null; }
}
function walk(dir) {
  return readdirSync(dir).flatMap((n) => { const p = join(dir, n); return statSync(p).isDirectory() ? walk(p) : [p]; });
}
function frontMatter(text) {
  const m = /^---\n([\s\S]*?)\n---/.exec(text);
  if (!m) return null;
  const out = {};
  for (const line of m[1].split("\n")) { const kv = /^([a-z-]+):\s*(.*)$/.exec(line); if (kv) out[kv[1]] = kv[2].trim(); }
  return out;
}

const plugin = readJson(".claude-plugin/plugin.json");
const market = readJson(".claude-plugin/marketplace.json");
if (plugin && !/^[a-z0-9]+(-[a-z0-9]+)*$/.test(plugin.name || "")) fail("plugin.json: name must be kebab-case");
if (market) {
  if (!market.name || !market.owner || !market.owner.name) fail("marketplace.json: name and owner.name are required");
  if (!Array.isArray(market.plugins) || !market.plugins.length) fail("marketplace.json: plugins must list at least one plugin");
  (market.plugins || []).forEach((p, i) => { if (!p.name || !p.source) fail(`marketplace.json: plugins[${i}] needs name and source`); });
  if (plugin && !(market.plugins || []).some((p) => p.name === plugin.name)) fail("marketplace.json does not list plugin.json's plugin");
}

for (const rel of (plugin && plugin.skills) || []) {
  const dir = join(root, rel), md = join(dir, "SKILL.md");
  if (!existsSync(md)) { fail(`${rel}: SKILL.md missing`); continue; }
  const fm = frontMatter(readFileSync(md, "utf8"));
  const folder = rel.split("/").filter(Boolean).pop();
  if (!fm) fail(`${rel}/SKILL.md: no front matter`);
  else {
    if (fm.name !== folder) fail(`${rel}/SKILL.md: name "${fm.name}" should be "${folder}"`);
    if (!fm.description) fail(`${rel}/SKILL.md: description is empty`);
  }
  for (const file of walk(dir)) {
    if (file.endsWith(".md")) {
      const text = readFileSync(file, "utf8");
      for (const [, target] of text.matchAll(/\]\(([^)#\s]+)(?:#[^)]*)?\)/g)) {
        if (/^[a-z]+:/i.test(target)) continue; // URLs
        if (!existsSync(resolve(dirname(file), target))) fail(`${relative(root, file)}: broken link ${target}`);
      }
      for (const [re, what] of PRIVATE) if (re.test(text)) fail(`${relative(root, file)}: ${what}`);
    }
    try {
      if (file.endsWith(".mjs") || file.endsWith(".js")) execFileSync(process.execPath, ["--check", file], { stdio: "pipe" });
      if (file.endsWith(".py")) execFileSync("python3", ["-c", "import ast,sys; ast.parse(open(sys.argv[1]).read())", file], { stdio: "pipe" });
    } catch (e) { fail(`${relative(root, file)}: ${String(e.stderr || e.message).trim().split("\n")[0]}`); }
  }
}

if (problems.length) { console.error(problems.map((p) => `✗ ${p}`).join("\n")); process.exit(1); }
console.log(`✓ ${((plugin && plugin.skills) || []).length} skills, manifests, links and scripts OK`);
