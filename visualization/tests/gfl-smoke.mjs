// Browser smoke test for the GFL dashboard (gfl.html) and the specification viewer.
// Checks what a judge would rely on: every ledger entry verifies in the browser, a sealed file
// re-hashes to its ledger value, the case file, plots, transfer engine, families, function map,
// memory search and spec pages render, and the page has no script errors or horizontal scroll on a phone.
import assert from "node:assert/strict";
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, resolve, sep, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium, firefox } from "playwright";

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, "..");
const types = { ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8", ".jsonl": "application/x-ndjson", ".md": "text/markdown; charset=utf-8",
  ".svg": "image/svg+xml", ".png": "image/png" };
const server = createServer(async (req, res) => {
  try {
    const path = decodeURIComponent(new URL(req.url, "http://127.0.0.1").pathname);
    const file = resolve(root, `.${path}`);
    if (!file.startsWith(root + sep)) return res.writeHead(403).end();
    const body = await readFile(file); // read first: a missing file must give 404, not a header written twice
    res.writeHead(200, { "content-type": types[extname(file)] ?? "application/octet-stream" }).end(body);
  } catch { res.writeHead(404).end(); }
});
await new Promise((r) => server.listen(0, "127.0.0.1", r));
const base = `http://127.0.0.1:${server.address().port}`;
const ledgerLines = (await readFile(resolve(root, "data/ledger.jsonl"), "utf8")).split("\n").filter(Boolean).length;

async function run(type, name) {
  const browser = await type.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
    const errors = [];
    page.on("pageerror", (e) => errors.push(e.message));
    await page.goto(`${base}/gfl.html`, { waitUntil: "load" });
    await page.waitForFunction(() => /entries valid/.test(document.querySelector("#chain-status").textContent), null, { timeout: 60000 });
    const status = await page.textContent("#chain-status");
    assert.match(status, new RegExp(`^${ledgerLines} of ${ledgerLines} entries valid`), `${name}: ${status}`);
    assert.equal(await page.locator(".block.bad").count(), 0, `${name}: invalid ledger blocks`);
    await page.waitForFunction(() => /files match/.test(document.querySelector("#data-status").textContent), null, { timeout: 30000 });
    assert.match(await page.textContent("#data-status"), /: 8 of 8 files match their ledger seals\.$/, `${name}: page data seals`);

    assert.equal(await page.locator("#timeline li").count(), 13);
    await page.locator("#timeline button").nth(11).click();
    assert.match(await page.textContent("#inspector"), /RES-021/);
    const rehash = page.locator("#inspector button[data-verify]").first();
    await rehash.click();
    await page.waitForFunction(() => document.querySelector("#inspector .vres")?.textContent.trim().length > 0);
    assert.match(await page.textContent("#inspector .vres"), /matches the ledger/, `${name}: file re-hash`);

    assert.ok(await page.locator("#ai-list li").count() >= 10, `${name}: AI findings`);
    assert.match(await page.textContent("#ai-summary"), /Every summary passed the citation check/);
    assert.ok(await page.locator("#comp-body tr").count() >= 5, `${name}: comparable runs`);
    const cited = await page.locator("#ai-list a.cite").first().getAttribute("data-id");
    await page.locator("#ai-list a.cite").first().click();
    assert.equal(await page.locator("#mem-list details[open] .rec-id").first().textContent(), cited, `${name}: citation opens its record`);
    for (const id of ["#plot-xt", "#plot-def", "#plot-rob"]) assert.ok(await page.locator(`${id} .main-svg`).count() > 0, `${name}: ${id}`);
    assert.equal(await page.locator("#xval-body tr").count(), 4);
    assert.match(await page.textContent("#tr-verdict"), /Undetermined/);
    await page.locator('#tr-tabs button[data-p="documentary_summary"]').click();
    assert.match(await page.textContent("#tr-verdict"), /Conditionally informative/);
    assert.ok(await page.locator("#fam-body tr").count() >= 8);
    assert.ok(await page.locator(".cap").count() >= 28);
    await page.fill("#q", "window");
    await page.check("#neg");
    assert.match(await page.textContent("#mem-count"), /failures and corrections only/);
    assert.ok(await page.locator(".mem-item").count() > 0);
    assert.deepEqual(errors, [], `${name}: page errors`);

    const spec = await browser.newPage();
    await spec.goto(`${base}/spec.html?doc=SPEC_portable_black_box.md`, { waitUntil: "load" });
    await spec.waitForFunction(() => document.querySelector("#spec h1"), null, { timeout: 20000 });
    assert.match(await spec.textContent("#spec h1"), /Portable black box/);
    await spec.goto(`${base}/spec.html?doc=../../etc/passwd`, { waitUntil: "load" });
    assert.match(await spec.textContent("#spec"), /No specification named/);

    const phone = await browser.newPage({ viewport: { width: 390, height: 844 } });
    await phone.goto(`${base}/gfl.html`, { waitUntil: "load" });
    await phone.waitForTimeout(1500);
    assert.ok(await phone.evaluate(() => document.documentElement.scrollWidth <= 392), `${name}: horizontal scroll on phone`);
    console.log(`${name}: ok (${status.split(" (")[0]})`);
  } finally {
    await browser.close();
  }
}

try {
  await run(chromium, "Chromium");
  await run(firefox, "Firefox");
} finally {
  await new Promise((r) => server.close(r));
}
