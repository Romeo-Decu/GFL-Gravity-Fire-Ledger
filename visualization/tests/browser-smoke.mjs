import assert from "node:assert/strict";
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { dirname } from "node:path";
import { chromium, firefox } from "playwright";

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(here, "../..");
const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8"
};

const server = createServer(async (request, response) => {
  try {
    const pathname = decodeURIComponent(new URL(request.url, "http://127.0.0.1").pathname);
    const requestedPath = resolve(repoRoot, `.${pathname}`);
    const filePath = pathname.endsWith("/") ? resolve(requestedPath, "index.html") : requestedPath;
    if (filePath !== repoRoot && !filePath.startsWith(repoRoot + sep)) {
      response.writeHead(403).end("Forbidden");
      return;
    }
    const body = await readFile(filePath);
    response.writeHead(200, { "content-type": mimeTypes[extname(filePath)] ?? "application/octet-stream" });
    response.end(body);
  } catch {
    response.writeHead(404).end("Not found");
  }
});

await new Promise(resolveListen => server.listen(0, "127.0.0.1", resolveListen));
const address = server.address();
const appUrl = `http://127.0.0.1:${address.port}/visualization/`;

async function smoke(browserType, browserName) {
  const browser = await browserType.launch({ headless: true });
  try {
    const page = await browser.newPage({ acceptDownloads: true });
    await page.setViewportSize({ width: 1440, height: 1200 });
    const pageErrors = [];
    let stage = "navigation";
    page.on("pageerror", error => pageErrors.push({
      kind: "pageerror", stage, text: error.message, stack: error.stack
    }));
    page.on("console", message => {
      if (message.type() === "error") {
        pageErrors.push({ kind: "console", stage, text: message.text(), location: message.location() });
      }
    });
    page.on("requestfailed", request => {
      pageErrors.push({
        kind: "requestfailed", stage, url: request.url(), failure: request.failure()?.errorText
      });
    });

    await page.goto(appUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
    stage = "wait-for-graph-status";
    await page.waitForFunction(
      () => document.querySelector("#status")?.textContent.includes("nodes"),
      null,
      { timeout: 90000 }
    );
    stage = "wait-for-cytoscape";
    await page.locator("#graph canvas").first().waitFor({ state: "visible", timeout: 30000 });
    stage = "wait-for-plotly";
    await page.locator("#plot .main-svg").first().waitFor({ state: "visible", timeout: 30000 });

    stage = "inspect-graph";
    const nodeCount = await page.evaluate(() => window.fifCy?.nodes().length ?? 0);
    const edgeCount = await page.evaluate(() => window.fifCy?.edges().length ?? 0);
    assert.ok(nodeCount >= 10, `${browserName}: expected evidence nodes, got ${nodeCount}`);
    assert.ok(edgeCount >= 10, `${browserName}: expected evidence edges, got ${edgeCount}`);

    stage = "inspect-selection";
    const nodePosition = await page.evaluate(() => {
      const node = window.fifCy.$id("assert_b3_flow_2");
      return node.renderedPosition();
    });
    const graphBox = await page.locator("#graph").boundingBox();
    await page.mouse.click(graphBox.x + nodePosition.x, graphBox.y + nodePosition.y);
    await page.getByText("assert_b3_flow_2", { exact: true }).waitFor({ state: "visible" });
    const sourceLinkCount = await page.locator("#details a").count();
    assert.ok(sourceLinkCount >= 1, browserName + ": selected assertion should expose a source link");

    stage = "inspect-unknown-measurement";
    const measurementPosition = await page.evaluate(() => {
      const node = window.fifCy.$id("measurement_b3_spread_rate_unknown");
      return node.renderedPosition();
    });
    await page.mouse.click(graphBox.x + measurementPosition.x, graphBox.y + measurementPosition.y);
    await page.getByText("measurement_b3_spread_rate_unknown", { exact: true }).waitFor({ state: "visible" });
    const measurementDetails = await page.locator("#details").innerText();
    assert.match(measurementDetails, /evidence state\\s+unknown/i);
    assert.match(measurementDetails, /"value":\\s*null/);

    stage = "export-graph";
    const downloadPromise = page.waitForEvent("download");
    await page.getByRole("button", { name: "Export graph JSON" }).click();
    const download = await downloadPromise;
    assert.equal(download.suggestedFilename(), "fif-pmma100-bass-b3-record-reconciliation.json");

    stage = "completed-interactions";
    assert.deepEqual(pageErrors, [], `${browserName}: browser console/page errors: ${JSON.stringify(pageErrors)}`);
    process.stdout.write(`PASS ${browserName}: ${nodeCount} nodes, ${edgeCount} edges, Plotly chart and graph export\n`);
  } finally {
    await browser.close();
  }
}

try {
  await smoke(chromium, "Chromium");
  await smoke(firefox, "Firefox");
} finally {
  await new Promise(resolveClose => server.close(resolveClose));
}
