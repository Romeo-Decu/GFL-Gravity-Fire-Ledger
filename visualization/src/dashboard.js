import { verifyLedger, verifyFile } from "./ledger-verify.js";

const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const clean = (t) => String(t).replace(/\*\*/g, "").replace(/`/g, "");
const NEG_STATES = new Set(["withdrawn", "rejected", "superseded"]);
const C = { blue: "#6cb4ff", ember: "#e8833a", soot: "#5b6675", fog: "#d8e1ea", muted: "#8a9bb0", rule: "#26364a", panel: "#16212f" };

const [memory, series, ledgerText, pubPipeline, pubOwner, caps, transfer, vault, families, aiF, comp, preds, an, relevance, emap, indus] = await Promise.all([
  fetch("./data/experiment_memory.json").then((r) => r.json()),
  fetch("./data/b6_series.json").then((r) => r.json()),
  fetch("./data/ledger.jsonl").then((r) => r.text()),
  fetch("./data/release-a.pub.json").then((r) => r.json()),
  fetch("./data/owner.pub.json").then((r) => r.json()),
  fetch("./data/capabilities.json").then((r) => r.json()),
  fetch("./data/transfer_pmma100.json").then((r) => r.json()),
  fetch("./data/vault.json").then((r) => r.json()),
  fetch("./data/families.json").then((r) => r.json()),
  fetch("./data/ai_findings.json").then((r) => r.json()),
  fetch("./data/comparable_runs.json").then((r) => r.json()),
  fetch("./data/predictions.json").then((r) => r.json()),
  fetch("./data/analysis.json").then((r) => r.json()),
  fetch("./data/relevance.json").then((r) => (r.ok ? r.json() : null)).catch(() => null),
  fetch("./data/evidence_map.json").then((r) => (r.ok ? r.json() : null)).catch(() => null),
  fetch("./data/indus_relevance.json").then((r) => (r.ok ? r.json() : null)).catch(() => null),
]);
const records = new Map(memory.records.map((r) => [r.id, r]));
const entries = ledgerText.split("\n").filter((l) => l.trim()).map((l) => JSON.parse(l));
const verified = new Map(); // seq -> result

// ---------------------------------------------------------------- hero budget
const h = series.headline;
const b6 = an.runs.B6, b6u = b6.uq;
$("#h-rate").textContent = b6.record.rate_mm_s.toFixed(2);
const segDefs = Object.values(series.segment.definitions).map((d) => d.ols_mm_s);
const ref01 = series.segment.definitions["rel_peak_0.1"];
const hac = [ref01.ols_mm_s - 2.306 * ref01.se_hac_mm_s, ref01.ols_mm_s + 2.306 * ref01.se_hac_mm_s];
const distinct = new Set(series.robustness.grid.filter((g) => g.fitted).map((g) => g["rate_rel_0.1_mm_s"])).size;
$("#h-budget").innerHTML = [
  ["Reported interval, 95 %", `${b6.record.interval_mm_s[0].toFixed(2)}–${b6.record.interval_mm_s[1].toFixed(2)} mm/s: scatter of the frames and choice of front definition together`],
  ["Statistical only", `${b6u.layer1_statistical_95_mm_s[0].toFixed(2)}–${b6u.layer1_statistical_95_mm_s[1].toFixed(2)} mm/s, block bootstrap on 10 frames`],
  ["Across front definitions", `nine definitions give ${b6u.layer2_analyst_choice.definition_range_mm_s[0].toFixed(2)}–${b6u.layer2_analyst_choice.definition_range_mm_s[1].toFixed(2)} mm/s; their spread enters the interval as a ±${b6u.layer2_analyst_choice.systematic_mm_s.toFixed(2)} mm/s term, not as a hard bound`],
  ["Spatial scale", "±3 % allowance; the ruler lies behind the sample (ISS-020)"],
  ["Not in NASA's archive", '<span class="unknown">the pyrolysis front (only the luminous edge is imaged); the flow speed at the sample surface; a repeat of this run</span>'],
  ["Source", "NASA PSI-25, the public archive named by the challenge; files re-downloaded with identical fingerprints"],
].map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join("");

// ---------------------------------------------------------------- ledger chain
const chain = $("#chain");
chain.innerHTML = entries.map((e) => `<button class="block${e.type === "approval" ? " approval" : ""}" role="listitem" data-seq="${e.seq}" title="seq ${e.seq} · ${esc(e.type)}" aria-label="Ledger entry ${e.seq}, ${esc(e.type)}"></button>`).join("");
chain.addEventListener("click", (ev) => {
  const b = ev.target.closest(".block");
  if (!b) return;
  location.hash = "ledger";
  const row = document.querySelector(`#ledger-body tr[data-seq="${b.dataset.seq}"]`);
  document.querySelectorAll("#ledger-body tr.sel").forEach((r) => r.classList.remove("sel"));
  if (row) { row.classList.add("sel"); row.scrollIntoView({ block: "center" }); }
});

renderLedgerTable();
const t0 = performance.now();
verifyLedger(ledgerText, [pubPipeline, pubOwner], (n, total) => {
  $("#chain-status").textContent = `Checking ${n} of ${total}…`;
}).then((res) => {
  let ok = 0;
  for (const r of res) {
    verified.set(r.seq, r);
    if (r.ok) ok++;
    const b = chain.querySelector(`[data-seq="${r.seq}"]`);
    b.classList.add(r.ok ? "ok" : "bad");
    b.title = `seq ${r.seq} · ${r.type} · ${r.ok ? "valid" : r.errors.join(", ")}`;
  }
  const ms = Math.round(performance.now() - t0);
  const engine = res[0]?.engine ?? "";
  $("#chain-status").innerHTML = `${ok} of ${res.length} entries valid (${engine}, ${ms} ms). Head <span class="hash">${esc(res.at(-1).entry_hash.slice(0, 16))}…</span>`;
  renderLedgerTable();
  verifyPageData(res);
});

function renderLedgerTable() {
  $("#ledger-body").innerHTML = entries.map((e) => {
    const r = verified.get(e.seq);
    const loc = e.object?.location ?? (e.qualifies ? `qualifies ${e.qualifies.slice(0, 10)}… (${(e.qualifiers || []).join(", ")})` : e.anchor ? "anchor" : "");
    const check = !r ? "…" : r.ok ? '<span class="res-ok">valid</span>' : `<span class="res-bad">${esc(r.errors.join(", "))}</span>`;
    return `<tr data-seq="${e.seq}"><td>${e.seq}</td><td>${esc(e.type)}${e.supersedes ? " (supersedes)" : ""}</td><td>${esc(loc)}</td><td class="hash">${esc(e.entry_hash.slice(0, 20))}…</td><td>${check}</td></tr>`;
  }).join("");
}

// ---------------------------------------------------------------- case file
const steps = memory.storyline.steps;
const PHASE_ICON = { measure: "flame_front", extend: "comparison", attack: "red_team", reproduce: "reproducible", explain: "exposure",
  blind: "blind", audit: "auditor", settle: "validator", rule: "decision", correct: "supersession" };
const NEG_OUT = new Set(["rejected", "withdrawn", "superseded"]);
$("#timeline").innerHTML = steps.map((s, i) => {
  const cls = s.outcome === "superseded" ? "sup" : NEG_OUT.has(s.outcome) ? "neg" : "";
  return `<li class="${cls}"><button type="button" data-i="${i}" aria-current="${i === 0}">
    <span class="t-date"><img class="t-icon" src="./assets/brand/icons/${PHASE_ICON[s.phase] || "info"}.svg" alt="">${esc(s.date)} · ${esc(s.phase)}</span>
    <span class="t-cap">${esc(s.caption)}</span>
    <span class="t-out ${NEG_OUT.has(s.outcome) ? "neg" : ""}">${esc(s.outcome)} · ${s.records.join(", ")}</span></button></li>`;
}).join("");
$("#timeline").addEventListener("click", (ev) => {
  const b = ev.target.closest("button[data-i]");
  if (!b) return;
  document.querySelectorAll("#timeline button").forEach((x) => x.setAttribute("aria-current", "false"));
  b.setAttribute("aria-current", "true");
  showStep(Number(b.dataset.i));
});

function recordHtml(r, full) {
  const last = r.history.at(-1);
  const files = [...new Map(r.history.flatMap((x) => x.files).map((f) => [f.path, f])).values()];
  const fileItems = files.map((f) => {
    const seal = f.ledger.at(-1);
    if (!seal) return `<li><code>${esc(f.path)}</code><span class="qual">not sealed in the ledger</span></li>`;
    const quals = [...new Set(f.ledger.flatMap((s) => s.qualifications.flatMap((q) => q.qualifiers)))];
    const sup = f.ledger.some((s) => s.superseded_by) ? '<span class="qual">superseded</span>' : "";
    return `<li><span><code>${esc(f.path)}</code><br><span class="hash">ledger seq ${seal.seq} · sha256 ${esc((seal.sha256 || "").slice(0, 16))}…</span>
      ${quals.length ? `<br><span class="qual">qualifiers: ${esc(quals.join(", "))}</span>` : ""} ${sup}</span>
      <button class="btn" data-verify="${esc(f.path)}" data-sha="${esc(seal.sha256)}">Re-hash file</button><span class="vres"></span></li>`;
  }).join("");
  const hist = r.history.length > 1 ? `<p class="meta">${r.history.length} entries in the register: ${r.history.map((x) => esc(x.status.slice(0, 40))).join(" → ")}</p>` : "";
  return `<div class="rec"><div class="rec-head"><span class="rec-id">${r.id}</span><span class="state ${esc(r.current_state)}">${esc(r.current_state)}</span>
    ${r.ledger_qualifiers?.length ? `<span class="qual">${esc(r.ledger_qualifiers.join(", "))}</span>` : ""}</div>
    ${hist}<div class="rec-text">${esc(clean(full ? last.text : last.text.slice(0, 900) + (last.text.length > 900 ? "…" : "")))}</div>
    ${files.length ? `<ul class="files">${fileItems}</ul>` : ""}
    ${r.cited_by.length ? `<p class="meta">Cited later by ${r.cited_by.join(", ")}</p>` : ""}</div>`;
}

function showStep(i) {
  const s = steps[i];
  $("#inspector").innerHTML = `<h3>${esc(s.caption)}</h3><p class="insp-cap">${esc(s.date)} · ${esc(s.phase)} · outcome: ${esc(s.outcome)}. Caption is an editorial summary; the register rows below are the record.</p>
    ${s.records.map((id) => recordHtml(records.get(id), true)).join("")}`;
}
showStep(0);

document.addEventListener("click", async (ev) => {
  const b = ev.target.closest("button[data-verify]");
  if (!b) return;
  b.disabled = true;
  const out = b.nextElementSibling;
  const r = await verifyFile(`./data/files/${b.dataset.verify}`, b.dataset.sha);
  out.innerHTML = r.state === "ok" ? ' <span class="res-ok">matches the ledger</span>'
    : r.state === "missing" ? ' <span class="res-bad">not published with this page</span>'
    : ` <span class="res-bad">altered: ${esc(r.sha256.slice(0, 16))}…</span>`;
  b.disabled = false;
});

// ---------------------------------------------------------------- plots
const layoutBase = {
  paper_bgcolor: C.panel, plot_bgcolor: C.panel, font: { family: "IBM Plex Sans", color: C.fog, size: 12 },
  margin: { l: 56, r: 16, t: 12, b: 44 }, xaxis: { gridcolor: C.rule, zeroline: false }, yaxis: { gridcolor: C.rule, zeroline: false },
  showlegend: false, hoverlabel: { bgcolor: "#0f1722", font: { family: "IBM Plex Sans" } },
};
const cfg = { displayModeBar: false, responsive: true };
const fr = series.frames.filter((f) => f.t_s < 100 && f.lead_mm["0.1"] !== null);
const why = (f) => {
  const g = f.gates, reasons = [];
  if (!g.G1) reasons.push("no flame"); if (!g.G2) reasons.push("edge at border"); if (!g.G3) reasons.push("flame clipped");
  if (!g.G4) reasons.push("after gap"); if (!g.G5) reasons.push("near flow change"); if (f.air == null) reasons.push("no overlay");
  return reasons.length ? reasons.join(", ") : "usable";
};
const seg = series.segment, def01 = seg.definitions["rel_peak_0.1"];
const segFr = fr.filter((f) => f.usable && f.t_s >= seg.t_start_s && f.t_s <= seg.t_end_s);
const tm = segFr.reduce((a, f) => a + f.t_s, 0) / segFr.length, xm = segFr.reduce((a, f) => a + f.lead_mm["0.1"], 0) / segFr.length;
const fitX = [seg.t_start_s - 1, seg.t_end_s + 1];
const bands = [];
const ch = series.air_changes;
const edges = [0, ...ch.map((c) => c.t_s), 75];
for (let k = 0; k < edges.length - 1; k++) {
  const air = k === 0 ? ch[0].from : ch[k - 1].to;
  bands.push({ type: "rect", xref: "x", yref: "paper", x0: edges[k], x1: edges[k + 1], y0: 0, y1: 1, fillcolor: k % 2 ? "rgba(108,180,255,0.05)" : "rgba(108,180,255,0.0)", line: { width: 0 } });
  bands.push({ type: "line", xref: "x", yref: "paper", x0: edges[k + 1], x1: edges[k + 1], y0: 0, y1: 1, line: { color: C.rule, width: 1, dash: "dot" } });
  bands.push({ xref: "x", yref: "paper", x: (edges[k] + edges[k + 1]) / 2, y: 1.0, text: `air ${air}`, showarrow: false, font: { color: C.muted, size: 11 }, yanchor: "top", _ann: true });
}
Plotly.newPlot("plot-xt", [
  { x: fr.map((f) => f.t_s), y: fr.map((f) => f.lead_mm["0.1"]), mode: "markers", type: "scatter",
    marker: { size: 8, color: fr.map((f) => (f.usable ? C.blue : "rgba(0,0,0,0)")), line: { color: fr.map((f) => (f.usable ? C.blue : C.soot)), width: 1.5 } },
    text: fr.map((f) => `${f.image}<br>t = ${f.t_s} s, exposure ${f.exposure_s.toFixed(4)} s<br>${why(f)}`), hovertemplate: "%{text}<br>edge %{y:.1f} mm<extra></extra>" },
  { x: fitX, y: fitX.map((t) => xm + def01.ols_mm_s * (t - tm)), mode: "lines", line: { color: "#fff", width: 2 },
    hovertemplate: `fit, air 3: ${def01.ols_mm_s.toFixed(2)} mm/s<extra></extra>` },
], { ...layoutBase, shapes: bands.filter((b) => !b._ann), annotations: bands.filter((b) => b._ann).map(({ _ann, ...a }) => a),
  xaxis: { ...layoutBase.xaxis, title: "time from first frame (s)", range: [0, 75] }, yaxis: { ...layoutBase.yaxis, title: "leading edge (mm)" } }, cfg);

const defNames = { "rel_peak_0.05": "0.05 of peak", "rel_peak_0.1": "0.1 of peak (reference)", "rel_peak_0.2": "0.2 of peak", "rel_peak_0.5": "0.5 of peak",
  "abs_2e+05": "absolute 2e5", "abs_5e+05": "absolute 5e5", "abs_1e+06": "absolute 1e6", peak_position: "peak position" };
const dk = Object.keys(defNames).filter((k) => seg.definitions[k]);
Plotly.newPlot("plot-def", [{
  y: dk.map((k) => defNames[k]), x: dk.map((k) => seg.definitions[k].ols_mm_s), type: "scatter", mode: "markers", orientation: "h",
  marker: { size: 10, color: dk.map((k) => (k === "rel_peak_0.1" ? "#fff" : C.blue)) },
  error_x: { type: "data", symmetric: false, color: C.muted, thickness: 1.5,
    array: dk.map((k) => seg.definitions[k].boot95_mm_s[1] - seg.definitions[k].ols_mm_s),
    arrayminus: dk.map((k) => seg.definitions[k].ols_mm_s - seg.definitions[k].boot95_mm_s[0]) },
  hovertemplate: "%{y}: %{x:.3f} mm/s<extra></extra>",
}], { ...layoutBase, margin: { ...layoutBase.margin, l: 150 },
  xaxis: { ...layoutBase.xaxis, title: "spread rate (mm/s)", range: [1.6, 3.1] }, yaxis: { ...layoutBase.yaxis, autorange: "reversed" },
  shapes: [{ type: "line", x0: 2.274, x1: 2.274, yref: "paper", y0: 0, y1: 1, line: { color: C.soot, dash: "dash", width: 1 } }],
  annotations: [{ x: 2.274, yref: "paper", y: 1.02, text: "superseded 2.274", showarrow: false, font: { color: C.muted, size: 11 } }] }, cfg);

const grid = series.robustness.grid.filter((g) => g.fitted);
Plotly.newPlot("plot-rob", [{
  x: grid.map((g) => g.rate_rel_0_1_mm_s ?? g["rate_rel_0.1_mm_s"]), y: grid.map((g) => (g.g3_factor == null ? "clipping gate off" : `clipping ≤ ${g.g3_factor}× median`)),
  type: "scatter", mode: "markers", marker: { size: 9, color: grid.map((g) => g.clock_shift_s), colorscale: [[0, C.ember], [0.5, "#fff"], [1, C.blue]], opacity: 0.85 },
  text: grid.map((g) => `guard ${g.guard_s} s, clock shift ${g.clock_shift_s} s, ${g.frames} frames`), hovertemplate: "%{x:.3f} mm/s<br>%{text}<extra></extra>",
}], { ...layoutBase, margin: { ...layoutBase.margin, l: 150 }, xaxis: { ...layoutBase.xaxis, title: "spread rate, 0.1 of peak (mm/s)", range: [1.6, 2.4] } }, cfg);

const xv = series.cross_validation, label = { ALL: "All 77 frames", PRE_GAP: "Before the 106 s gap", ACTIVE: "13–53 s (old window)", NOCLIP: "17–52.5 s, no clipping" };
$("#xval-body").innerHTML = Object.entries(xv).map(([k, v]) => `<tr><td>${label[k] ?? k}<br><span class="hash">${v.frames} frames</span></td><td>${(+v["gfl_rel_0.1"]).toFixed(2)}</td><td>${(+v.deepseek).toFixed(2)}</td><td>${(+v.kimi_primary).toFixed(2)}</td></tr>`).join("");

// ---------------------------------------------------------------- experiment memory
const allRecs = [...memory.records].sort((a, b) => b.history.at(-1).order - a.history.at(-1).order);
function renderMemory() {
  const q = $("#q").value.trim().toLowerCase(), kind = $("#kind").value, state = $("#state").value, neg = $("#neg").checked;
  const hits = allRecs.filter((r) => (!kind || r.kind === kind) && (!state || r.current_state === state) && (!neg || r.negative_record)
    && (!q || r.id.toLowerCase().includes(q) || r.history.some((x) => x.text.toLowerCase().includes(q))));
  $("#mem-count").textContent = `${hits.length} of ${allRecs.length} records${neg ? ", failures and corrections only" : ""}.`;
  $("#mem-list").innerHTML = hits.map((r) => {
    const last = r.history.at(-1);
    const cls = r.negative_record || NEG_STATES.has(r.current_state) ? "neg" : r.current_state;
    return `<details class="mem-item ${esc(cls)}"><summary><span class="rec-id">${r.id}</span><span class="state ${esc(r.current_state)}">${esc(r.current_state)}</span><span class="snip">${esc(clean(last.text).slice(0, 160))}…</span></summary>${recordHtml(r, true)}
      <p class="meta">Register line ${last.register_line}</p></details>`;
  }).join("");
}
["#q", "#kind", "#state", "#neg"].forEach((s) => $(s).addEventListener("input", renderMemory));
renderMemory();

// nav highlight
const navLinks = [...document.querySelectorAll(".masthead nav a[href^='#']")];
const obs = new IntersectionObserver((es) => es.forEach((e) => {
  if (e.isIntersecting) navLinks.forEach((a) => a.classList.toggle("active", a.getAttribute("href") === `#${e.target.id}`));
}), { rootMargin: "-40% 0px -55% 0px" });
["map", "capabilities", "architecture", "guide", "case", "rate", "predictions", "analysis", "ai", "transfer", "comparable", "relevance", "families", "memory", "vault", "files", "ledger"].forEach((id) => obs.observe(document.getElementById(id)));

// ---------------------------------------------------------------- function map
$("#cap-groups").innerHTML = caps.groups.map((g) => `<div class="cap-group"><h3>${esc(g.name)}</h3><div class="cap-tiles">${g.items.map((it) => {
  const link = it.open && it.status !== "designed"
    ? `<a class="btn" href="${esc(it.open)}">Open</a>${it.spec ? ` <a class="btn" href="./spec.html?doc=${encodeURIComponent(it.spec)}">Specification</a>` : ""}`
    : `<a class="btn" href="./spec.html?doc=${encodeURIComponent(it.spec)}">Read the specification</a>`;
  return `<article class="cap ${esc(it.status)}"><img src="./assets/brand/icons/${esc(it.icon)}.svg" alt="">
    <div class="cap-name">${esc(it.name)} <span class="pill ${esc(it.status)}">${esc(it.status)}</span></div>
    <p>${esc(it.summary)}</p><div>${link}</div></article>`;
}).join("")}</div></div>`).join("");

// ---------------------------------------------------------------- architecture map
const mods = new Map(caps.groups.flatMap((g) => g.items.map((it) => [it.id, it])));
const feeds = (id) => [...mods.values()].filter((m) => m.needs.includes(id)).map((m) => m.id);
const met = (m) => Object.values(m.maturity).filter(Boolean).length;
const meter = (m) => "●".repeat(met(m)) + "○".repeat(5 - met(m));
$("#arch-layers").innerHTML = caps.layers.map((L) => `<div class="arch-layer"><div class="arch-lname">${esc(L.name)}<span>${esc(L.hint)}</span></div>
  <div class="arch-nodes">${L.modules.map((id) => { const m = mods.get(id);
    return `<button type="button" class="arch-node ${esc(m.status)}" data-id="${id}" aria-pressed="false" title="${esc(m.status)}, ${met(m)} of 5 checks">
      <img src="./assets/brand/icons/${esc(m.icon)}.svg" alt=""><span class="an-name">${esc(m.name)}</span><span class="an-meter" aria-hidden="true">${meter(m)}</span></button>`; }).join("")}</div></div>`).join("");
const archChip = (id) => `<button type="button" class="arch-chip" data-id="${id}">${esc(mods.get(id).name)}</button>`;
const pathList = (a) => a.length ? `<ul class="arch-paths">${a.map((p) => `<li><code>${esc(p)}</code></li>`).join("")}</ul>` : '<p class="arch-none">none yet</p>';
const codeList = (a) => a.length ? a.map((p) => { const f = caps.files[p];
  return `<details class="code-file"><summary><code>${esc(p)}</code><span class="sub">${f.lines} lines${f.outline.length ? `, ${f.outline.length} functions` : ""}</span></summary>
    ${f.doc ? `<p class="cf-doc">${esc(f.doc)}</p>` : ""}<ul>${f.outline.map((o) => `<li><button type="button" class="cf-fn" data-code="${esc(p)}" data-line="${o.line}">${esc(o.name)}()</button>${o.doc ? `<span class="sub">${esc(o.doc)}</span>` : ""}</li>`).join("")}</ul>
    <button type="button" class="btn" data-code="${esc(p)}" data-line="1">Read the whole file</button></details>`; }).join("") : '<p class="arch-none">none yet</p>';
async function openCode(path, line) {
  const dlg = $("#code-view"), body = $("#cv-body");
  $("#cv-path").textContent = path;
  body.textContent = "Loading…";
  if (!dlg.open) dlg.showModal();
  try {
    const text = await fetch(`./data/code/${path}.txt`).then((r) => { if (!r.ok) throw new Error(r.status); return r.text(); });
    body.innerHTML = text.split("\n").map((l, i) => `<span class="ln${i + 1 === line ? " hit" : ""}" id="cv-l${i + 1}"><i>${i + 1}</i>${esc(l) || " "}</span>`).join("");
    if (line > 1) document.getElementById(`cv-l${line}`)?.scrollIntoView({ block: "center" });
  } catch { body.textContent = `The source could not be loaded here. It is in the repository at ${path}.`; }
}
$("#cv-close").addEventListener("click", () => $("#code-view").close());
// documents, reports and raw files open inside the page, so there is always a way back
async function openDoc(href, title) {
  const dlg = $("#doc-view"), body = $("#dv-body");
  $("#dv-title").textContent = title; $("#dv-open").href = href;
  body.replaceChildren(); body.textContent = "Loading…";
  if (!dlg.open) dlg.showModal();
  try {
    if (/(index|graph)\.html$/.test(href)) { body.className = "frame-host"; body.replaceChildren(Object.assign(document.createElement("iframe"), { src: href, title })); return; }
    const spec = href.match(/spec\.html\?doc=([\w.-]+\.md)$/);
    const text = await fetch(spec ? `./data/specs/${spec[1]}` : href).then((r) => { if (!r.ok) throw new Error(r.status); return r.text(); });
    body.replaceChildren();
    if (spec) { body.className = "spec"; body.innerHTML = (spec[1].startsWith("SPEC_") ? '<p class="banner">Specification of a function that is designed or partly built. It states what we want and how it will be done; it is not a claim that the function exists.</p>' : "") + marked.parse(text); }
    else if (href.endsWith(".html")) { body.className = "report-host"; const doc = new DOMParser().parseFromString(text, "text/html");
      const host = document.createElement("div"); body.append(host); const root = host.attachShadow({ mode: "open" });
      root.innerHTML = `<style>${[...doc.querySelectorAll("style")].map((s) => s.textContent).join("\n").replaceAll("body{", ":host{display:block;")}</style>${doc.body.innerHTML}`; }
    else { body.className = "raw"; const pre = document.createElement("pre"); pre.textContent = text; body.append(pre); }
    body.scrollTop = 0;
  } catch { body.textContent = "This document could not be loaded here. Use “Open in a new tab”."; }
}
$("#dv-close").addEventListener("click", () => $("#doc-view").close());
document.addEventListener("click", (ev) => {
  const a = ev.target.closest('a[href*="spec.html?doc="], a[href*="data/reports/"], a[href$="./index.html"], a[href$="./graph.html"]');
  if (!a || a.id === "dv-open") return;
  ev.preventDefault();
  if ($("#menu").open) $("#menu").open = false;
  openDoc(a.getAttribute("href"), a.dataset.title || (/(index|graph)\.html$/.test(a.getAttribute("href")) ? "Evidence graph (prototype)" : a.textContent.trim()));
});
document.querySelectorAll("code.cmd").forEach((c) => { const b = document.createElement("button"); b.type = "button"; b.className = "btn cmd-copy"; b.textContent = "Copy the command";
  b.addEventListener("click", () => navigator.clipboard.writeText(c.textContent).then(() => { b.textContent = "Copied"; }, () => { b.textContent = "Select the text above and copy it"; })); c.after(b); });
let archSel = null;
function drawArchLines() {
  const svg = $("#arch-lines"), map = $("#arch-map");
  const box = map.getBoundingClientRect();
  svg.setAttribute("viewBox", `0 0 ${box.width} ${box.height}`);
  const pos = (id) => { const r = map.querySelector(`.arch-node[data-id="${id}"]`).getBoundingClientRect(); return [r.left - box.left + r.width / 2, r.top - box.top, r.height]; };
  const link = (from, to, cls) => { const [x1, y1, h1] = pos(from), [x2, y2, h2] = pos(to);
    const a = y1 <= y2 ? [x1, y1 + h1, x2, y2] : [x1, y1, x2, y2 + h2]; const mid = (a[1] + a[3]) / 2;
    return `<path class="${cls}" d="M${a[0]},${a[1]} C${a[0]},${mid} ${a[2]},${mid} ${a[2]},${a[3]}"/>`; };
  const all = [...mods.values()].flatMap((x) => x.needs.map((n) => link(n, x.id, "all"))).join("");
  const m = archSel && mods.get(archSel);
  svg.innerHTML = all + (m ? m.needs.map((n) => link(n, archSel, "in")).join("") + feeds(archSel).map((f) => link(archSel, f, "out")).join("") : "");
}
function showArch(id, scroll) {
  archSel = id;
  const m = mods.get(id), out = feeds(id);
  document.querySelectorAll(".arch-node").forEach((b) => { const k = b.dataset.id;
    b.setAttribute("aria-pressed", String(k === id));
    b.classList.toggle("in", m.needs.includes(k)); b.classList.toggle("out", out.includes(k));
    b.classList.toggle("dim", k !== id && !m.needs.includes(k) && !out.includes(k)); });
  const specDocs = m.docs.filter((d) => d.startsWith("docs/specs/"));
  $("#arch-detail").innerHTML = `<div class="ad-head"><img src="./assets/brand/icons/${esc(m.icon)}.svg" alt=""><div><h3>${esc(m.name)}</h3>
      <span class="pill ${esc(m.status)}">${esc(m.status)}</span> <span class="ad-met">${met(m)} of 5 checks</span></div></div>
    <p class="ad-does">${esc(m.does)}</p>
    <ul class="ad-checks">${caps.criteria.map(([k, label]) => `<li class="${m.maturity[k] ? "yes" : "no"}"><span>${m.maturity[k] ? "●" : "○"}</span>${esc(label)}${k === "real_data" && m.real ? `<span class="sub">${esc(m.real[0])}: ${esc(m.real[1])}</span>` : ""}</li>`).join("")}</ul>
    <h4>Needs the output of</h4><div class="ad-chips in">${m.needs.map(archChip).join("") || '<p class="arch-none">nothing: it starts a chain</p>'}</div>
    <h4>Feeds</h4><div class="ad-chips out">${out.map(archChip).join("") || '<p class="arch-none">nothing yet</p>'}</div>
    <h4>Code: open a file to see what is inside</h4>${codeList(m.code)}<h4>Automated tests</h4>${codeList(m.tests)}<h4>Documents</h4>${pathList(m.docs)}
    <div class="ad-actions">${m.open && m.status !== "designed" ? `<a class="btn" href="${esc(m.open)}">Open the live section</a>` : ""}
      ${specDocs.map((d) => `<a class="btn" href="./spec.html?doc=${encodeURIComponent(d.split("/").pop())}">Read the specification</a>`).join("")}</div>`;
  drawArchLines();
  if (scroll && window.matchMedia("(max-width: 900px)").matches) $("#arch-detail").scrollIntoView({ block: "start" });
}
let tourAt = -1;
function showTour(i) {
  tourAt = i;
  const [id, text] = caps.tour[i];
  $("#arch-tour").innerHTML = `<div class="tour-card"><span class="tour-n">Step ${i + 1} of ${caps.tour.length}: ${esc(mods.get(id).name)}</span><p>${esc(text)}</p>
    <div><button type="button" class="btn" data-tour="${i - 1}"${i === 0 ? " disabled" : ""}>Back</button> <button type="button" class="btn" data-tour="${i + 1}"${i === caps.tour.length - 1 ? " disabled" : ""}>Next</button> <button type="button" class="btn" data-tour="-1">End the tour</button></div></div>`;
  showArch(id, false);
}
$("#architecture").addEventListener("click", (ev) => {
  const c = ev.target.closest("[data-code]"), t = ev.target.closest("[data-tour]"), b = ev.target.closest("[data-id]");
  if (c) openCode(c.dataset.code, Number(c.dataset.line));
  else if (ev.target.closest("#tour-start")) showTour(0);
  else if (t) { const i = Number(t.dataset.tour); if (i < 0) { tourAt = -1; $("#arch-tour").innerHTML = '<button type="button" class="btn" id="tour-start">New to GFL? Follow one measurement, step by step</button>'; } else showTour(i); }
  else if (b) showArch(b.dataset.id, true);
});
document.querySelectorAll("#menu a").forEach((a) => a.addEventListener("click", () => { $("#menu").open = false; }));
window.addEventListener("resize", drawArchLines);
showArch("front", false);

// ---------------------------------------------------------------- reports
$("#guide-reports").innerHTML = Object.keys(an.runs).map((r) => `<span class="rep"><strong>${esc(r)}</strong>
  <a class="btn" data-title="Report, run ${esc(r)}" href="./data/reports/${esc(r)}_report.html">Read the report</a> <a class="btn" data-title="Run ${esc(r)}: table of segments (CSV)" href="./data/reports/${esc(r)}_report.csv">CSV</a> <a class="btn" data-title="Run ${esc(r)}: full record (JSON)" href="./data/reports/${esc(r)}_report.json">JSON</a></span>`).join("");

// ---------------------------------------------------------------- files
const ROOT_LABEL = { repo: "Project files (in the repository)", fif_data: "NASA PSI-25 files (downloaded from NASA, not published here)", withheld: "Withheld test truth (published after scoring)" };
const TIER_LABEL = { 1: "primary evidence", 2: "source table", 3: "derived result", 4: "page data" };
const fmtBytes = (n) => n >= 1e9 ? `${(n / 1e9).toFixed(2)} GB` : n >= 1e6 ? `${(n / 1e6).toFixed(1)} MB` : n >= 1e3 ? `${(n / 1e3).toFixed(1)} kB` : `${n} B`;
const fileMap = new Map();
for (const e of entries) { const o = e.object; if (!o) continue; const k = `${o.root}:${o.location}`; const prev = fileMap.get(k);
  fileMap.set(k, { root: o.root, path: o.location, name: o.location.split("/").pop(), bytes: o.bytes, sha: o.sha256, seq: e.seq, utc: e.recorded_utc.slice(0, 10),
    what: TIER_LABEL[e.tier] || e.type, by: e.method?.tool || e.method?.script || (o.root === "fif_data" ? "NASA PSI download" : "sealed as written"), versions: (prev?.versions || 0) + 1 }); }
const allFiles = [...fileMap.values()];
const fileRow = (f, full) => `<li class="file"><span class="f-name">${esc(full ? f.path : f.name)}</span>
  <span class="f-meta">${esc(f.what)} · ${fmtBytes(f.bytes)} · ${esc(f.by)} · sealed ${esc(f.utc)}${f.versions > 1 ? ` · version ${f.versions}` : ""}</span>
  <span class="f-seal"><button type="button" class="btn f-seq" data-seq="${f.seq}">ledger entry ${f.seq}</button> <code title="${esc(f.sha)}">${esc(f.sha.slice(0, 16))}…</code> <button type="button" class="btn f-copy" data-sha="${esc(f.sha)}">copy fingerprint</button></span></li>`;
function treeHtml(node, depth) {
  const dirs = Object.keys(node.dirs).sort(), n = (x) => x.files.length + Object.values(x.dirs).reduce((s, d) => s + n(d), 0);
  return dirs.map((d) => `<details${depth === 0 ? " open" : ""}><summary><span class="d-name">${esc(depth === 0 ? ROOT_LABEL[d] || d : d)}</span><span class="d-count">${n(node.dirs[d])} files</span></summary>${treeHtml(node.dirs[d], depth + 1)}</details>`).join("")
    + (node.files.length ? `<ul class="file-list">${node.files.sort((a, b) => a.name.localeCompare(b.name)).map((f) => fileRow(f, false)).join("")}</ul>` : "");
}
function renderFiles() {
  const q = $("#files-q").value.trim().toLowerCase();
  if (q) { const hit = allFiles.filter((f) => f.path.toLowerCase().includes(q) || f.sha.startsWith(q));
    $("#files-count").textContent = `${hit.length} of ${allFiles.length} files`;
    $("#files-tree").innerHTML = hit.length ? `<ul class="file-list flat">${hit.slice(0, 200).map((f) => fileRow(f, true)).join("")}</ul>` : '<p class="arch-none">No sealed file matches. Try part of a run name or a file type.</p>';
    return; }
  const root = { dirs: {}, files: [] };
  for (const f of allFiles) { let node = (root.dirs[f.root] ||= { dirs: {}, files: [] });
    for (const part of f.path.split("/").slice(0, -1)) node = (node.dirs[part] ||= { dirs: {}, files: [] });
    node.files.push(f); }
  $("#files-count").textContent = `${allFiles.length} files, ${fmtBytes(allFiles.reduce((s, f) => s + f.bytes, 0))} sealed in total`;
  $("#files-tree").innerHTML = treeHtml(root, 0);
}
$("#files-q").addEventListener("input", renderFiles);
$("#files-tree").addEventListener("click", (ev) => {
  const s = ev.target.closest(".f-seq"), c = ev.target.closest(".f-copy");
  if (s) { location.hash = "ledger"; const row = document.querySelector(`#ledger-body tr[data-seq="${s.dataset.seq}"]`);
    document.querySelectorAll("#ledger-body tr.sel").forEach((r) => r.classList.remove("sel")); if (row) { row.classList.add("sel"); row.scrollIntoView({ block: "center" }); } }
  if (c) navigator.clipboard.writeText(c.dataset.sha).then(() => { c.textContent = "copied"; }, () => { c.previousElementSibling.textContent = c.dataset.sha; c.remove(); });
});
renderFiles();

// ---------------------------------------------------------------- transferability
const PROFILE_LABEL = { documentary_summary: "Compare published summaries", qualitative_mechanism: "Same mechanism, qualitatively",
  quantitative_transfer: "Transfer the number", model_calibration: "Calibrate a model", model_validation: "Validate a model" };
const CONCL_LABEL = { directly_supported: "Directly supported", conditionally_informative: "Conditionally informative",
  qualitatively_informative: "Qualitatively informative", not_transferable_on_current_evidence: "Not transferable on current evidence", undetermined: "Undetermined" };
const profKeys = Object.keys(transfer.profiles);
$("#tr-tabs").innerHTML = profKeys.map((k, i) => `<button role="tab" data-p="${k}" aria-selected="${k === "quantitative_transfer"}">${PROFILE_LABEL[k] || k}</button>`).join("");
function showProfile(k) {
  const r = transfer.profiles[k];
  document.querySelectorAll("#tr-tabs button").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.p === k)));
  const blocking = r.gate_assessments.filter((g) => g.status === "fail" || g.status === "unknown").map((g) => g.gate_id.replaceAll("_", " "));
  $("#tr-verdict").className = `tr-verdict ${r.conclusion}`;
  $("#tr-verdict").innerHTML = `<p class="tr-concl">${CONCL_LABEL[r.conclusion] || r.conclusion}</p><p>${esc(r.primary_reason)}</p>
    ${blocking.length ? `<p>Blocking gates:</p><ul>${blocking.map((b) => `<li>${esc(b)}</li>`).join("")}</ul>` : ""}
    ${r.unresolved_conflicts?.length ? `<p>Unresolved source conflict: ${esc(r.unresolved_conflicts.map((c) => c.description || c.id).join("; "))}</p>` : ""}
    <p>Not allowed to conclude: ${esc(r.prohibited_extrapolations.join(", "))}.</p>`;
  $("#tr-gates").innerHTML = r.gate_assessments.map((g) => `<tr><td>${esc(g.gate_id.replaceAll("_", " "))}</td><td><span class="gs ${esc(g.status)}">${esc(g.status)}</span></td>
    <td>${esc(transfer.gates[g.gate_id]?.pass_when || "")}</td></tr>`).join("");
}
$("#tr-tabs").addEventListener("click", (ev) => { const b = ev.target.closest("button[data-p]"); if (b) showProfile(b.dataset.p); });
showProfile("quantitative_transfer");
$("#tr-note").textContent = `Engine ${transfer.profiles.quantitative_transfer.engine} ${transfer.profiles.quantitative_transfer.engine_version}, ruleset ${transfer.ruleset}. Gate states are ${transfer.gate_state_origin}. Computing them from measured data is the designed next step (function map: physics regime gates).`;

// ---------------------------------------------------------------- vault
const T = vault.entries_by_tier;
const K = vault.tier1_by_kind || {};
$("#v-tiers").innerHTML = [["Tier 1, recorded as received", T["1"] || 0], ...Object.entries(K).map(([k, v]) => [`<span class="sub">of which ${esc(k)}</span>`, v]), ["Tier 2, source tables as published", T["2"] || 0],
  ["Tier 3, derivations (outside the vault)", T["3"] || 0], ["Tier 4, supersessions", T["4"] || 0],
  ["Qualifications, anchors, approvals", T["None"] || 0]].map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join("");
$("#v-keys").innerHTML = vault.keys.map((k) => `<li><strong>${esc(k.role)}</strong> key <span class="hash">${esc(k.key_id)}</span>
  <span class="sub">${esc(k.holder || "")}. ${k.role === "owner" ? "Signs approvals only; held offline by the owner." : "Signs processing entries; cannot sign approvals."}</span></li>`).join("")
  + `<li>${vault.owner_approvals.length} owner-signed approval(s): ${vault.owner_approvals.map((a) => esc(a.decision)).join(", ")}</li>`;
const lastAnchors = vault.anchors.slice(-4).reverse();
$("#v-anchors").innerHTML = `<li>${vault.anchors.length} anchors of the chain head: Git commits and RFC 3161 timestamps (FreeTSA); ${vault.tsa_tokens.length} timestamp tokens published with the repository.</li>`
  + lastAnchors.map((a) => `<li>${esc(a.kind)} <span class="sub">${esc(a.recorded_utc)} ${a.anchor?.commit ? "commit " + esc(a.anchor.commit.slice(0, 10)) : ""}</span></li>`).join("");
$("#v-sealed").innerHTML = vault.sealed_objects.map((o) => `<tr><td>${o.seq}</td><td>${o.tier}</td><td>${esc(o.location)}</td><td class="hash">${esc((o.sha256 || "").slice(0, 20))}…</td>
  <td>${o.root === "repo" ? "repository" : "NASA raw data, outside Git: hash only, reported missing if absent"}</td></tr>`).join("");

// ---------------------------------------------------------------- NASA families
$("#fam-head").innerHTML = `<tr><th scope="col">Family</th><th scope="col">What it studies</th>${families.stages.map((st, i) => `<th scope="col" class="stage-h" title="${esc(st)}">${i + 1}. ${esc(st)}</th>`).join("")}</tr>`;
$("#fam-body").innerHTML = families.families.map((f) => `<tr><th scope="row">${esc(f.name)}<span class="sub">${esc(f.phase)}</span></th>
  <td>${esc(f.phenomenon)}<span class="sub">${esc(f.treatment)}. Collection: ${esc(f.collection)}.</span>
  ${f.depth.length ? `<ul class="depth">${f.depth.map((d) => `<li>${esc(d)}</li>`).join("")}</ul>` : ""}</td>
  ${families.stages.map((st, i) => `<td class="stage ${i < f.stage ? "done" : ""}" aria-label="${esc(st)}: ${i < f.stage ? "done" : "not yet"}"><span></span></td>`).join("")}</tr>`).join("");

// ---------------------------------------------------------------- AI findings, ranked by GFL's check
function secondCheck(f) {
  const c = f.second_check; if (!c) return "";
  const notOk = c.labels.filter((l) => l.label !== "SUPPORTED");
  const head = notOk.length ? `${notOk.length} of ${c.labels.length} sentences read as partly supported` : `all ${c.labels.length} sentences read as supported`;
  return `<details class="sc"><summary>Second model: ${esc(head)}${c.state !== "current wording" ? "; wording corrected after this check" : ""}</summary>
    <ul>${c.labels.map((l) => `<li><span class="sc-l ${esc(l.label)}">${esc(l.label.toLowerCase().replace("_", " "))}</span> ${esc(c.checked_sentences[l.n - 1] || "")}${l.label !== "SUPPORTED" ? `<span class="sub">${esc(l.reason)}</span>` : ""}</li>`).join("")}</ul></details>`;
}
const VERDICT = { upheld: "upheld", partly_upheld: "partly upheld", not_upheld: "not upheld", fabricated: "fabricated" };
const citeLinks = (t) => esc(t).replace(/\[([A-Z]+-\d+[A-Z]?(?:,\s*[A-Z]+-\d+[A-Z]?)*)\]/g, (_, ids) =>
  `[${ids.split(/,\s*/).map((id) => `<a href="#memory" class="cite" data-id="${id}">${id}</a>`).join(", ")}]`);
$("#ai-n").textContent = String(aiF.models.length);
$("#ai-summary").innerHTML = Object.entries(aiF.counts).map(([v, n]) => `<span class="vchip ${v}"><strong>${n}</strong> ${VERDICT[v]}</span>`).join("")
  + `<span class="ai-label">${aiF.all_passed ? "Every summary passed the citation check" : "Citation check failed"}</span>`;
$("#ai-list").innerHTML = aiF.findings.map((f) => `<li class="aif ${f.verdict}">
  <div class="aif-head"><span class="vchip ${f.verdict}">${VERDICT[f.verdict]}</span><span class="aif-who">${esc(f.model)}, ${esc(f.role)}</span><span class="sub">${esc(f.workflow)} · ${esc(f.date)}</span></div>
  <p class="aif-claim">${esc(f.claim)}</p><p class="aif-sum">${citeLinks(f.summary)}</p>${secondCheck(f)}</li>`).join("");
$("#ai-list").addEventListener("click", (ev) => {
  const a = ev.target.closest("a.cite"); if (!a) return;
  ev.preventDefault();
  $("#q").value = a.dataset.id; $("#kind").value = ""; $("#state").value = ""; $("#neg").checked = false; renderMemory();
  const d = [...document.querySelectorAll("#mem-list details")].find((x) => x.querySelector(".rec-id").textContent === a.dataset.id);
  if (d) { d.open = true; d.scrollIntoView({ block: "start" }); }
});
$("#ai-note").textContent = `${aiF.second_check ? `Second check: ${aiF.second_check.model} on the team's Azure Foundry read every sentence against its cited records (${Object.entries(aiF.second_check.tally).map(([k, v]) => `${v} ${k.toLowerCase().replace("_", " ")}`).join(", ")}); partly supported sentences were reworded. ` : ""}${aiF.ranking_rule} Summaries: ${aiF.label}. Checker: ${aiF.checker}. The same findings, the memory, the ledger check and the run ranking are served to any AI client by GFL's read-only MCP server (src/gfl_mcp).`;

// ---------------------------------------------------------------- pre-registered predictions and blind test
const VERDICT_CLASS = { supported: "pass", "not supported": "fail", "not testable": "unknown" };
const f3 = (x) => x.toFixed(3);
$("#pr-score").innerHTML = Object.entries(preds.scorecard).map(([k, n]) => `<span class="vchip"><strong>${n}</strong> ${esc(k)}</span>`).join("");
$("#pr-body").innerHTML = preds.predictions.map((p) => `<tr><td><strong>${esc(p.id)}</strong><span class="sub">${esc(p.claim)}</span></td>
  <td>${p.band_ratio ? `${p.band_ratio[0]}–${p.band_ratio[1]}` : "intervals must not overlap"}</td>
  <td>${p.measured ? `${f3(p.measured.rate_mm_s)} mm/s<span class="sub">${f3(p.measured.interval_mm_s[0])}–${f3(p.measured.interval_mm_s[1])}, air display ${p.measured.air_display}, ${p.measured.frames} frames</span>` : "—"}</td>
  <td>${p.ratio != null ? `${p.ratio}<span class="sub">${p.ratio_interval[0]}–${p.ratio_interval[1]}</span>` : "—"}</td>
  <td><span class="gs ${VERDICT_CLASS[p.verdict]}">${esc(p.verdict)}</span><span class="sub">${esc(p.why || "")}</span></td></tr>`).join("");
const bt = preds.blind_test, cases = Object.keys(bt.truth_mm_s);
{ const cs = Object.keys(bt.truth_mm_s), AC = [C.blue, C.ember, "#e6c36a", "#9ad18b", "#c99bff", C.fog], pct = (v, c) => 100 * (v / bt.truth_mm_s[c] - 1);
  Plotly.newPlot("plot-blind", bt.rows.map((r, i) => ({ name: r.analyst, x: cs, y: cs.map((c) => (r.cases[c] ? pct(r.cases[c].speed, c) : null)), mode: "markers", offsetgroup: String(i),
      marker: { size: 9, color: AC[i % AC.length], symbol: r.analyst.startsWith("GFL") ? "diamond" : "circle" },
      error_y: { type: "data", symmetric: false, color: AC[i % AC.length], thickness: 1.5, width: 3,
        array: cs.map((c) => r.cases[c] ? pct(r.cases[c].ci95[1], c) - pct(r.cases[c].speed, c) : 0), arrayminus: cs.map((c) => r.cases[c] ? pct(r.cases[c].speed, c) - pct(r.cases[c].ci95[0], c) : 0) },
      hovertemplate: `${r.analyst} %{x}: %{y:+.1f} % from the truth<extra></extra>` })),
    { ...layoutBase, scattermode: "group", showlegend: true, legend: { orientation: "h", y: -0.25, font: { color: C.muted } },
      shapes: [{ type: "line", xref: "paper", x0: 0, x1: 1, y0: 0, y1: 0, line: { color: C.fog, width: 2 } }],
      annotations: [{ xref: "paper", x: 0.995, y: 0, xanchor: "right", yanchor: "bottom", text: "true speed", showarrow: false, font: { color: C.fog } }],
      xaxis: { ...layoutBase.xaxis, type: "category", title: "synthetic case (in T4 the luminous edge drifts from the true front)" },
      yaxis: { ...layoutBase.yaxis, type: "linear", title: "error against the known truth (%)", ticksuffix: " %" } }, cfg); }
$("#pr-blind-lede").textContent = `Four synthetic burns with a known true speed, generated after the methods were frozen; the truth stayed sealed (SHA-256 ${bt.truth_sha256.slice(0, 12)}…) until every analyst had delivered. Each case hides one difficulty: ${cases.map((c) => `${c} ${bt.stress[c]}`).join("; ")}. Every external script was re-run by GFL. The test scores whether the stated 95 % interval contains the truth.`;
$("#pr-blind-head").innerHTML = `<tr><th scope="col">Analyst</th>${cases.map((c) => `<th scope="col">${c}<span class="sub">truth ${bt.truth_mm_s[c]}</span></th>`).join("")}<th scope="col">Covered</th></tr>`;
$("#pr-blind-body").innerHTML = bt.rows.map((r) => `<tr${r.analyst.startsWith("GFL") ? ' class="own"' : ""}><td><strong>${esc(r.analyst)}</strong><span class="sub">mean error ${(100 * r.mean_rel_error).toFixed(1)} %</span></td>
  ${cases.map((c) => { const x = r.cases[c]; return x ? `<td><span class="gs ${x.covers ? "pass" : "fail"}">${f3(x.speed)}</span><span class="sub">${f3(x.ci95[0])}–${f3(x.ci95[1])}</span></td>` : "<td>—</td>"; }).join("")}
  <td>${esc(r.coverage)}</td></tr>`).join("");
const pp = preds.post_protocol[0];
$("#pr-post").textContent = `R-W3 could not read B11 because a bright pre-burn frame opened the burn record (ISS-049). R-W4 changes only that gate, and was sealed before it ran. B11 then gives ${f3(pp.display_2.rate_mm_s)} mm/s at air display 2 (${f3(pp.display_2.interval_mm_s[0])}–${f3(pp.display_2.interval_mm_s[1])}), ratio ${pp.ratio_display_2} to B6, just under the P-B11a band, and ${f3(pp.display_0.rate_mm_s)} mm/s at display 0, slower with ${pp.display_0_slower_non_overlapping ? "non-overlapping" : "overlapping"} intervals. ${pp.note}`;
const tp = preds.thickness_series.points, runColor = { B6: "#fff", B9: C.blue, B11: "#e6c36a", B13: C.ember };
const jit = (p) => p.thickness_um * (1 + 0.04 * ((p.air_display % 5) - 2));
Plotly.newPlot("plot-thick", [
  ...Object.keys(runColor).map((run) => { const q = tp.filter((p) => p.run === run); return {
    name: run, x: q.map(jit), y: q.map((p) => p.rate_mm_s), type: "scatter", mode: "markers", marker: { size: 9, color: runColor[run] },
    error_y: { type: "data", symmetric: false, color: C.muted, thickness: 1.2, array: q.map((p) => p.interval_mm_s[1] - p.rate_mm_s), arrayminus: q.map((p) => p.rate_mm_s - p.interval_mm_s[0]) },
    text: q.map((p) => `${run}, ${p.thickness_um} µm, air display ${p.air_display}, ${p.frames} frames`), hovertemplate: "%{text}<br>%{y:.3f} mm/s<extra></extra>" }; }),
  { name: "∝ 1/thickness (through B6)", x: [80, 500], y: [80, 500].map((t) => preds.reference.rate_mm_s * 100 / t), mode: "lines", line: { color: C.soot, dash: "dash", width: 1 }, hoverinfo: "skip" },
], { ...layoutBase, showlegend: true, legend: { orientation: "h", y: -0.25, font: { color: C.muted } },
  xaxis: { ...layoutBase.xaxis, type: "log", title: "PMMA film thickness (µm)", tickvals: [100, 200, 400] },
  yaxis: { ...layoutBase.yaxis, type: "log", title: "spread rate (mm/s)" } }, cfg);
const ex = preds.thickness_series.exponent;
$("#pr-thick-note").textContent = `${preds.thickness_series.note} Weighted fit of rate ∝ thickness^n: n = ${ex.B13_display_3.n_weighted} (95 % ${ex.B13_display_3.ci95[0]} to ${ex.B13_display_3.ci95[1]}) with B13's registered segment, ${ex.B13_display_4.n_weighted} (${ex.B13_display_4.ci95[0]} to ${ex.B13_display_4.ci95[1]}) with its display-4 segment; the inverse-thickness law n = −1 lies inside both, and the data cannot tell it from a steeper law. B13's material is inferred, not named in NASA's table; without B13 the three remaining points give n = ${ex.without_B13.n_weighted} (95 % ${ex.without_B13.ci95[0]} to ${ex.without_B13.ci95[1]}, one degree of freedom), which constrains nothing. Points at one thickness are spread slightly sideways by air display so they do not overlap.`;
$("#pr-note").textContent = `${bt.lesson} Reference: B6 under ${preds.rule}, ${f3(preds.reference.rate_mm_s)} mm/s. Protocol: ${preds.protocol}, ${preds.registered}.`;

// ---------------------------------------------------------------- Ask GFL: analysis modules (A0–A7), by question
const GS = { pass: "pass", partial: "unknown", fail: "fail", unknown: "unknown" };
const RUNC = { B6: C.fog, B9: C.blue, B11: "#e6c36a", B13: C.ember };
const runs = Object.entries(an.runs);
fetch("./assets/derived/B6_frame_front.json").then((r) => r.json()).then((m) => { $("#an-frame-cap").textContent = `What GFL measures: B6 at t = ${m.t_s} s (${m.image}). Blue box: the rows averaged into a brightness profile. White line: leading edge at 50 % of peak brightness, the reference definition. Orange line: the same edge at 10 % of peak. The faint blue glow ahead of the bright flame is why the luminous edge is not the burning front, and why that offset stays an unknown with no bound (layer 3 below). ${m.source}.`; });
// 1. measured rate vs calibrated flow
Plotly.newPlot("plot-flow", runs.map(([run, r]) => { const s = r.regime_by_segment;
  return { name: `${run} (${r.cram1.prediction.thickness_um} µm)`, x: s.map((q) => Number(q.u_cm_s ?? 0)), y: s.map((q) => Number(q.rate_mm_s)), mode: "markers+lines",
    line: { color: RUNC[run], width: 1, dash: "dot" }, marker: { size: 9, color: RUNC[run] },
    error_y: { type: "data", symmetric: false, color: C.muted, thickness: 1, array: s.map((q) => q.interval_mm_s[1] - q.rate_mm_s), arrayminus: s.map((q) => q.rate_mm_s - Math.max(0, q.interval_mm_s[0])) },
    text: s.map((q) => `${run}, air display ${q.air_display}, ${q.frames} frames, ${q.label}`), hovertemplate: "%{text}<br>%{y:.3f} mm/s<extra></extra>" }; }),
  { ...layoutBase, showlegend: true, legend: { orientation: "h", y: -0.28, font: { color: C.muted } },
    xaxis: { ...layoutBase.xaxis, type: "linear", title: "opposing-flow speed, duct centreline (cm/s)" }, yaxis: { ...layoutBase.yaxis, type: "linear", title: "spread rate (mm/s)", rangemode: "tozero" } }, cfg);
$("#an-o2").innerHTML = (an.other_oxygen || []).map((r) => r.segments.length
  ? r.segments.map((s) => `<tr><td><strong>${esc(r.run)}</strong><span class="sub">${esc(r.material)}</span></td><td>${r.o2_pct} %</td><td>${s.air_display}<span class="sub">${s.flow_cm_s.toFixed(1)} cm/s</span></td><td>${s.frames}</td><td>${s.rate_mm_s.toFixed(2)}</td><td>${s.interval_mm_s[0].toFixed(2)}–${s.interval_mm_s[1].toFixed(2)}</td></tr>`).join("")
  : `<tr><td><strong>${esc(r.run)}</strong><span class="sub">${esc(r.material)}</span></td><td>${r.o2_pct} %</td><td colspan="4"><span class="gs unknown">not measurable</span> <span class="sub">${esc(r.not_measurable)}</span></td></tr>`).join("");
$("#an-o2-note").textContent = "Measured with rule R-W4 unchanged, after the rule was frozen; no prediction was registered for these runs, because GFL has no sourced flame temperature at 17 % oxygen. They are not used by the theory, regime or transfer modules. One flight per condition; luminous-edge rates.";
if (an.oxygen_sensitivity) {
  const ox = an.oxygen_sensitivity, firm = ox.segments.filter((r) => r.excludes_no_change), sm = ox.summary;
  $("#an-oxy-concl").innerHTML = sm.ratio_range ? `From ${ox.reference.o2_pct} % to about ${firm[0].o2_pct} % oxygen the 100 µm film burns at <strong>${sm.ratio_range[0].toFixed(2)}–${sm.ratio_range[1].toFixed(2)} of the ${esc(ox.reference.run)} rate</strong> in ${firm.length} of ${sm.segments} measured segments, beyond the intervals of both runs. As a local power law that is rate ∝ X<sub>O₂</sub><sup>n</sup> with n ≈ ${sm.exponent_range[0].toFixed(1)} (${Math.min(...firm.map((r) => r.exponent_interval[0])).toFixed(1)} to ${Math.max(...firm.map((r) => r.exponent_interval[1])).toFixed(1)}): a drop of under four points of oxygen halves the rate.` : "No low-oxygen segment differs from the reference beyond both intervals.";
  const pts = [{ run: ox.reference.run, o2_pct: ox.reference.o2_pct, air_display: ox.reference.air_display, rate_mm_s: ox.reference.rate_mm_s, interval_mm_s: ox.reference.interval_mm_s }, ...ox.segments];
  Plotly.newPlot("plot-oxy", [{ type: "scatter", mode: "markers+text", x: pts.map((p) => p.o2_pct), y: pts.map((p) => p.rate_mm_s), text: pts.map((p) => `${p.run}, display ${p.air_display}`), textposition: "middle right", textfont: { color: C.muted, size: 11 },
    error_y: { type: "data", symmetric: false, array: pts.map((p) => p.interval_mm_s[1] - p.rate_mm_s), arrayminus: pts.map((p) => p.rate_mm_s - p.interval_mm_s[0]), color: C.blue, thickness: 1.5 },
    marker: { color: C.blue, size: 9 }, hovertemplate: "%{text}<br>%{x} % O₂<br>%{y:.2f} mm/s<extra></extra>" }],
    { ...layoutBase, xaxis: { ...layoutBase.xaxis, title: "initial oxygen (%, NASA table)", range: [16, 23] }, yaxis: { ...layoutBase.yaxis, title: "spread rate (mm/s)", rangemode: "tozero" } }, cfg);
  $("#an-oxy-note").textContent = `Exploratory, not pre-registered: the runs were measured before this comparison was written. ${ox.constraint_on_theory} Limits: ${ox.limits.join("; ")}. The third segment (${ox.segments.filter((r) => !r.excludes_no_change).map((r) => `${r.run} at display ${r.air_display}, ratio ${r.ratio_interval[0].toFixed(2)}–${r.ratio_interval[1].toFixed(2)}`).join(", ") || "none"}) is too uncertain to count either way. Run B16, at the same oxygen level, was too dim to measure at all. Module: src/gfl_analysis/oxygen.py.`;
}
$("#an-flow-note").textContent = `Flow speed from NASA's fan calibration: U = 1.0066 × air display, measured on the duct centreline; the speed at the sample surface is not known. In the thermal regime the rate should not depend on flow. B13's thermal segments differ by ${Math.round(100 * an.runs.B13.flow_independence.relative_spread)} %, so flow independence is not shown there; B11 at zero forced flow is slower.`;
Plotly.newPlot("plot-uq", ["layer1_statistical_95_mm_s", "reported_interval_mm_s", "interval_with_bounded_unknowns_mm_s"].map((k, i) => ({
  name: ["statistical only", "with analyst choice (reported)", "with bounded physical unknowns"][i], type: "scatter", mode: "markers",
  y: runs.map(([run]) => run), x: runs.map(([, r]) => r.uq.rate_mm_s), marker: { size: 8, color: [C.blue, C.fog, C.ember][i] },
  error_x: { type: "data", symmetric: false, thickness: [6, 3, 1.5][i], width: 0, color: [C.blue, C.fog, C.ember][i],
    array: runs.map(([, r]) => r.uq[k][1] - r.uq.rate_mm_s), arrayminus: runs.map(([, r]) => r.uq.rate_mm_s - r.uq[k][0]) },
  offset: i, hovertemplate: "%{y}: %{x:.3f} mm/s<extra></extra>" })),
  { ...layoutBase, height: 280, showlegend: true, legend: { orientation: "h", y: -0.35, font: { color: C.muted } },
    xaxis: { ...layoutBase.xaxis, title: "spread rate (mm/s)" }, yaxis: { ...layoutBase.yaxis, autorange: "reversed" } }, cfg);
const u = an.runs.B6.uq;
$("#an-uq").innerHTML = [["Statistical", `${f3(u.layer1_statistical_95_mm_s[0])}–${f3(u.layer1_statistical_95_mm_s[1])} mm/s for B6: scatter of the frames about the fitted line (bootstrap 95 %).`],
  ["Analyst choice", `± ${f3(u.layer2_analyst_choice.systematic_mm_s)} mm/s: what changes if another reasonable front definition is chosen.`],
  ...u.layer3_physical_unknowns.map((e) => [`Not knowable from these images: ${e.what}`, `${e.bound_rel ? `bounded ±${100 * e.bound_rel} %` : "no bound, kept outside the interval"}. ${e.evidence}. Reduced by ${e.reduced_by}.`])
].map(([a, b]) => `<tr><td><strong>${esc(a)}</strong></td><td>${esc(b)}</td></tr>`).join("");
// 2. theory vs measurement
const th = [80, 100, 150, 200, 300, 400, 500], tb = (t) => an.runs.B6.cram1.prediction.band_mm_s.map((v) => v * 100 / t);
Plotly.newPlot("plot-theory", [
  { x: th, y: th.map((t) => tb(t)[1]), mode: "lines", line: { width: 0 }, hoverinfo: "skip", showlegend: false },
  { name: "thin-fuel theory band", x: th, y: th.map((t) => tb(t)[0]), mode: "lines", fill: "tonexty", fillcolor: "rgba(108,180,255,0.15)", line: { width: 0 }, hoverinfo: "skip" },
  ...runs.map(([run, r]) => ({ name: run, x: [r.cram1.prediction.thickness_um * (run === "B9" ? 1.04 : 1)], y: [r.record.rate_mm_s], mode: "markers", marker: { size: 10, color: RUNC[run] },
    error_y: { type: "data", symmetric: false, color: C.muted, array: [r.record.interval_mm_s[1] - r.record.rate_mm_s], arrayminus: [r.record.rate_mm_s - r.record.interval_mm_s[0]] },
    hovertemplate: `${run}: %{y:.3f} mm/s<extra></extra>` }))],
  { ...layoutBase, showlegend: true, legend: { orientation: "h", y: -0.28, font: { color: C.muted } },
    xaxis: { ...layoutBase.xaxis, type: "log", title: "PMMA film thickness (µm)", tickvals: [100, 200, 400] }, yaxis: { ...layoutBase.yaxis, type: "log", title: "spread rate (mm/s)", tickvals: [0.3, 0.5, 1, 2, 3, 5] } }, cfg);
$("#an-runs").innerHTML = runs.map(([run, r]) => { const c = r.cram1, p = c.prediction;
  return `<tr><td><strong>${esc(run)}</strong><span class="sub">${p.thickness_um} µm, ${r.flow.value_cm_s} cm/s</span></td>
  <td>${f3(r.record.rate_mm_s)} mm/s<span class="sub">${f3(r.record.interval_mm_s[0])}–${f3(r.record.interval_mm_s[1])}</span></td>
  <td>${f3(p.band_mm_s[0])}–${f3(p.band_mm_s[1])} mm/s<span class="sub">Delichatsios ${f3(p.rate_mm_s_by_constant.Delichatsios_pi_over_4)}, EST ${f3(p.rate_mm_s_by_constant.EST_1)}, de Ris ${f3(p.rate_mm_s_by_constant.de_Ris_sqrt2)}</span></td>
  <td>${an.cram1_measured_over_lowest_theory[run]}</td></tr>`; }).join("");
$("#an-runs-note").textContent = "The lowest theory value is the Delichatsios constant with the flame-temperature ratio F at the low end of its published range (4.4); the band's upper end is the de Ris constant with F = 5.5. That is why the ratio is not the measured rate divided by one of the three constants shown. PMMA properties from Rojas-Alva 2022; the flame-temperature ratio F = 4.76, fitted to data in the literature, is never used, so the comparison is not circular. The theory over-predicts more as the fuel thickens (1.04, 0.95, 0.86, 0.79), which agrees with the measured thickness exponent of −1.19 and points to a heat loss the thin theory leaves out. A thin-to-thick check finds no sign that the 400 µm run alone became thermally thick.";
// 3. regime map
const rc = an.regime_curve, segs = runs.flatMap(([run, r]) => r.regime_by_segment.filter((q) => q.u_cm_s).map((q) => ({ run, ...q })));
Plotly.newPlot("plot-regime", [
  { name: "closeness to the radiative limit", x: rc.u_cm_s, y: rc.radiative_closeness, mode: "lines", line: { color: C.ember, width: 2 } },
  { name: "closeness to the kinetic limit", x: rc.u_cm_s, y: rc.kinetic_closeness, mode: "lines", line: { color: C.blue, width: 2 } },
  { name: "limit", x: [rc.u_cm_s[0], rc.u_cm_s.at(-1)], y: [1, 1], mode: "lines", line: { color: C.muted, dash: "dash", width: 1 }, hoverinfo: "skip" },
  { name: "measured flow levels", x: segs.map((q) => q.u_cm_s), y: segs.map((q) => q.radiation_number), mode: "markers", marker: { size: 9, color: segs.map((q) => RUNC[q.run]), symbol: "diamond" },
    text: segs.map((q) => `${q.run}, ${q.u_cm_s} cm/s: ${q.label}`), hovertemplate: "%{text}<extra></extra>" }],
  { ...layoutBase, showlegend: true, legend: { orientation: "h", y: -0.28, font: { color: C.muted } },
    xaxis: { ...layoutBase.xaxis, type: "log", title: "opposing-flow speed (cm/s)" }, yaxis: { ...layoutBase.yaxis, type: "log", title: "closeness to limit (1 = limit)", range: [Math.log10(0.003), Math.log10(30)], tickvals: [0.01, 0.1, 1, 10] },
    shapes: [{ type: "rect", xref: "x", yref: "paper", x0: rc.u_cm_s[0], x1: 1, y0: 0, y1: 1, fillcolor: "rgba(232,131,58,0.08)", line: { width: 0 } },
             { type: "rect", xref: "x", yref: "paper", x0: 60, x1: rc.u_cm_s.at(-1), y0: 0, y1: 1, fillcolor: "rgba(108,180,255,0.08)", line: { width: 0 } }],
    annotations: [{ x: Math.log10(0.5), y: 1.04, xref: "x", yref: "paper", text: "radiative", showarrow: false, font: { color: C.ember } },
                  { x: Math.log10(85), y: 1.04, xref: "x", yref: "paper", text: "kinetic", showarrow: false, font: { color: C.blue } },
                  { x: Math.log10(8), y: 1.04, xref: "x", yref: "paper", text: "thermal: heat transfer sets the rate", showarrow: false, font: { color: C.fog } }] }, cfg);
$("#an-regime-note").textContent = "Radiation number: surface re-radiation over the gas preheat length against conduction into the fuel. Damköhler number: gas residence time against chemical time, with PMMA gas kinetics from Rojas-Alva 2022; the kinetic limit is anchored where kinetics were seen for thin PMMA (about 60 cm/s). Both are order-of-magnitude groups with some approximate properties: they say where a run sits, not a measured boundary. GFL does not model kinetics; it says when kinetics would matter.";
// 4. transfer
const gids = Object.keys(an.transfer[0].gates);
$("#an-tr-head").innerHTML = `<tr><th scope="col">From → to</th>${gids.map((g) => `<th scope="col">${esc(g.replaceAll("_", " "))}</th>`).join("")}<th scope="col">Conclusion</th></tr>`;
$("#an-tr-body").innerHTML = an.transfer.map((t) => `<tr><td><strong>${esc(t.source)} → ${esc(t.target)}</strong></td>${gids.map((g) => `<td><span class="gs ${GS[t.gates[g].status]}" title="${esc(t.gates[g].reasons.join(" "))}">${esc(t.gates[g].status)}</span></td>`).join("")}<td>${esc(t.conclusion.replaceAll("_", " "))}</td></tr>`).join("");
$("#an-tr-note").textContent = "No pair reaches \"directly supported\": the offset between the luminous edge and the burning front has no bound, so the uncertainty condition stays partial. GFL prefers saying \"informative under stated conditions\" to a confidence the data do not carry.";
const GCOL = { pass: C.blue, partial: "#e6c36a", fail: C.ember, unknown: C.muted };
Plotly.newPlot("plot-gates", ["pass", "partial", "fail", "unknown"].map((st) => { const pts = an.transfer.flatMap((t) => gids.filter((g) => t.gates[g].status === st).map((g) => [g, t]));
  return { name: st === "pass" ? "met" : st === "partial" ? "partly met" : st, x: pts.map(([g]) => g.replaceAll("_", " ")), y: pts.map(([, t]) => `${t.source} → ${t.target}`), mode: "markers",
    marker: { size: 20, symbol: "square", color: GCOL[st] }, text: pts.map(([g, t]) => t.gates[g].reasons.join(" ")), hovertemplate: "%{y}, %{x}<br>%{text}<extra></extra>" }; }).filter((tr) => tr.x.length),
  { ...layoutBase, showlegend: true, legend: { orientation: "h", y: -0.5, font: { color: C.muted } }, margin: { l: 80, r: 16, t: 12, b: 110 },
    xaxis: { ...layoutBase.xaxis, type: "category", categoryorder: "array", categoryarray: gids.map((g) => g.replaceAll("_", " ")), tickangle: -30 }, yaxis: { ...layoutBase.yaxis, type: "category", autorange: "reversed" } }, cfg);
// 5. pre-registered tests
const pr = an.pre_registered;
$("#an-pre-lede").textContent = "A scientist can write down what a run should show before looking at it, and GFL holds them to it. This is how the four predictions above were made; the same function is open to any user, for any run.";
$("#an-pre-steps").innerHTML = ["Pick a run not analysed yet and a run already measured as reference.",
  "GFL proposes the expected rate from a stated law (thin-fuel 1/thickness, or the thickness exponent measured so far), or you enter your own value and band. Runs outside the law's domain get no proposal, with the reason.",
  "GFL seals the prediction: a SHA-256 fingerprint, a time, a ledger entry anchored in Git and by an independent timestamp authority, before the run is opened.",
  "When the run is measured with the frozen rule, GFL scores it: supported, not supported, or not testable. Not testable never counts as supported, and the score includes the reference run's own uncertainty."].map((x) => `<li>${esc(x)}</li>`).join("");
const LAW = { thin_fuel_inverse_thickness: "thin-fuel 1/thickness", empirical_exponent_rw4: "measured exponent −1.19" };
$("#an-pre").innerHTML = pr.registered.map((p) => `<tr><td><strong>${esc(p.target)}</strong><span class="sub">air display ${p.target_air_display}</span></td><td>${esc(LAW[p.law])}</td><td>${p.expected_ratio}</td><td>${p.band_ratio[0]}–${p.band_ratio[1]}</td><td>${f3(p.expected_rate_mm_s)} mm/s</td><td><span class="gs unknown">${esc(p.score.verdict)}</span><span class="sub">sealed ${esc(p.registered_utc.slice(0, 16).replace("T", " "))} UTC, ${esc(p.sha256.slice(0, 10))}…</span></td></tr>`).join("")
  + pr.not_predicted.filter((x, i, a) => a.findIndex((y) => y.target === x.target) === i).map((x) => `<tr><td><strong>${esc(x.target)}</strong></td><td colspan="4">no prediction: ${esc(x.out_of_domain.join("; "))}</td><td><span class="gs unknown">refused</span></td></tr>`).join("");
$("#an-pre-note").textContent = "Registered before these runs were measured, to be scored when they are measured with the frozen rule. B8's two bands overlap, so B8 alone cannot tell the two laws apart; a thicker run with PMMA named in the record at 21 % oxygen would. Earlier predictions rescored with the reference run's uncertainty: " + pr.earlier_scored_with_reference_uncertainty.map((x) => `${x.target} ratio ${x.score.ratio} (${x.score.ratio_interval_with_reference_uncertainty.join("–")}), ${x.score.verdict}`).join("; ") + " (B11 under the post-protocol rule R-W4).";
const ti = an.try_it, tiRuns = ti.runs.filter((r) => r.levels.length);
$("#ti-run").innerHTML = tiRuns.map((r) => `<option value="${esc(r.run)}">${esc(r.run)}: ${esc(r.material)}</option>`).join("");
$("#ti-law").innerHTML = Object.keys(ti.laws).map((k) => `<option value="${k}">${esc(LAW[k])}</option>`).join("");
function tiShow(resetAir) {
  const r = tiRuns.find((x) => x.run === $("#ti-run").value);
  if (resetAir) $("#ti-air").innerHTML = r.levels.map((l, i) => `<option value="${i}">${l.air_display} cm/s</option>`).join("");
  const lv = r.levels[Number($("#ti-air").value) || 0], law = $("#ti-law").value, p = lv.proposals[law];
  const ref = `${ti.reference.run} at air display ${ti.reference.air_display} (${ti.reference.rate_mm_s.toFixed(2)} mm/s)`;
  $("#ti-out").innerHTML = r.already_measured
    ? `<p class="ti-head refuse">Refused: ${esc(r.run)} is already measured.</p><p>A prediction written after the data were seen is not a prediction. GFL would have expected ${p ? `${p.expected_rate_mm_s.toFixed(2)} mm/s` : "nothing (outside the law's domain)"}; the scored result is in the Predictions section.</p>`
    : p ? `<p class="ti-head">Expected: ${p.expected_rate_mm_s.toFixed(2)} mm/s</p><p>That is ${p.expected_ratio} times the reference, ${esc(ref)}. The prediction counts as supported if the measured ratio falls between ${p.band_ratio[0]} and ${p.band_ratio[1]}. Basis: ${esc(ti.laws[law])}.</p>
       <p>To register it before the run is opened: <code>python -m gfl_analysis propose ${esc(r.run)} ${lv.air_display}</code>, then the pipeline seals and timestamps the file. This page cannot seal: the signing key never reaches a browser.</p>`
    : `<p class="ti-head refuse">No prediction for ${esc(r.run)}.</p><p>GFL declines instead of guessing:</p><ul>${lv.out_of_domain.map((w) => `<li>${esc(w)}</li>`).join("")}</ul>`;
}
$("#ti-run").addEventListener("change", () => tiShow(true)); $("#ti-air").addEventListener("change", () => tiShow(false)); $("#ti-law").addEventListener("change", () => tiShow(false));
$("#ti-run").value = "B8"; tiShow(true);
if (an.table_o2) { const o = an.table_o2, ok = o.filter((x) => !x.flagged), bad = o.filter((x) => x.flagged), lo = 0, hi = 26;
  Plotly.newPlot("plot-o2", [
    { name: "final = initial", x: [lo, hi], y: [lo, hi], mode: "lines", line: { color: C.muted, width: 1 }, hoverinfo: "skip" },
    { name: "drop of 3 points (threshold)", x: [lo, hi], y: [lo - 3, hi - 3], mode: "lines", line: { color: C.muted, width: 1, dash: "dash" }, hoverinfo: "skip" },
    { name: "floor, 10 %", x: [lo, hi], y: [10, 10], mode: "lines", line: { color: C.muted, width: 1, dash: "dot" }, hoverinfo: "skip" },
    { name: `not flagged (${ok.length} tests)`, x: ok.map((x) => x.o2_initial), y: ok.map((x) => x.o2_final), text: ok.map((x) => x.test), mode: "markers", marker: { size: 7, color: C.blue, opacity: 0.7 }, hovertemplate: "%{text}: %{x} % → %{y} %<extra></extra>" },
    { name: `flagged (${bad.length} tests)`, x: bad.map((x) => x.o2_initial), y: bad.map((x) => x.o2_final), text: bad.map((x) => x.test), mode: "markers+text", textposition: "middle right", textfont: { color: C.ember }, marker: { size: 10, color: C.ember, symbol: "diamond" }, hovertemplate: "%{text}: %{x} % → %{y} %<extra></extra>" }],
    { ...layoutBase, showlegend: true, legend: { orientation: "h", y: -0.28, font: { color: C.muted } }, margin: { ...layoutBase.margin, b: 90 },
      xaxis: { ...layoutBase.xaxis, type: "linear", title: "initial O₂, % by volume (as recorded by NASA)", range: [12, 25] }, yaxis: { ...layoutBase.yaxis, type: "linear", title: "final O₂, %", range: [0, 25] } }, cfg);
} else $("#plot-o2").hidden = true;
// 6–7. clean data, provenance
$("#an-anom").innerHTML = (an.table_anomalies || []).map((f) => `<tr><td>${esc(f.test)}</td><td>${esc(f.check.replaceAll("_", " "))}</td><td>${esc(f.field ? `${f.field}: ` : "")}${esc(String(f.value ?? ""))}</td></tr>`).join("");
$("#an-note").textContent = "Flags say what a check saw, not what it means. On the synthetic test the detector found every anomaly that could be seen in the data (a saturated frame, brightness flicker, a pre-burn gap) and nothing else; the luminous-edge offset cannot be seen in images at all.";
$("#an-prov").textContent = `Every file behind every number on this page is in the signed ledger, and the ledger is also exported in the W3C PROV-O standard (${vault.prov_summary.entities} entities, readable by any provenance tool): data/derived/analysis/GFL_LEDGER_PROV_O.jsonld. Status of all results: ${an.status}.`;

// ---------------------------------------------------------------- comparable runs
const DIM_LABEL = { material: "Material", geometry: "Geometry", thickness_um: "Thickness", width_cm: "Width", flow_restrictor: "Flow restrictor", air_setting: "Air setting 3", initial_o2_pct: "Initial O₂" };
const LEVEL_LABEL = { same_conditions: "same recorded conditions", close: "close: one condition differs", distant: "distant", not_comparable: "not comparable" };
$("#comp-counts").innerHTML = Object.entries(comp.counts).map(([k, n]) => `<span class="vchip lv-${k}"><strong>${n}</strong> ${LEVEL_LABEL[k]}</span>`).join("");
$("#comp-head").innerHTML = `<tr><th scope="col">#</th><th scope="col">Run</th><th scope="col">As recorded by NASA</th>${comp.dimensions.map((d) => `<th scope="col">${DIM_LABEL[d]}</th>`).join("")}<th scope="col">Level</th></tr>`;
const shown = comp.runs.filter((r) => r.level !== "not_comparable");
$("#comp-body").innerHTML = shown.map((r) => `<tr><td>${r.rank}</td><td><strong>${esc(r.test)}</strong><span class="sub">${esc(r.pi)}, table row ${r.table_row}</span></td>
  <td>${esc(r.material_as_recorded)}<span class="sub">air display: ${esc(r.air_display_as_recorded || "empty")}</span></td>
  ${comp.dimensions.map((d) => `<td><span class="gs ${r.states[d] === "match" ? "pass" : r.states[d] === "differs" ? "fail" : "unknown"}">${esc(r.states[d])}</span></td>`).join("")}
  <td>${esc(LEVEL_LABEL[r.level])}</td></tr>`).join("");
$("#comp-note").textContent = `Reference: ${comp.reference.test} (${comp.reference.material_as_recorded}), air setting ${comp.reference.air_setting}. ${comp.counts.not_comparable} runs with another material or geometry are not listed. Not recorded in the table, so outside the comparison: ${comp.not_recorded_in_table.join("; ")}. Table verified against its ledger seal (SHA-256 ${comp.table.sha256.slice(0, 12)}…) before ranking. Tool: ${comp.tool}.`;

// ---------------------------------------------------------------- fire-safety evidence map (PSI records)
if (emap) {
  const inv = emap.investigations, ids = Object.keys(inv), fns = emap.vocabulary.functions.filter((f) => f !== "combustion fundamentals");
  const models = Object.keys(Object.values(inv)[0].dropped);
  const slotCell = (s) => s.status === "agreed" ? `${esc(s.value)}<span class="sub">“${esc(Object.values(s.quotes).find(Boolean) || "")}”</span>`
    : s.status === "disputed" ? `<span class="unknown">disputed</span><span class="sub">${Object.entries(s.given).map(([m, v]) => `${esc(m)}: ${esc(v)}`).join("; ")}</span>`
    : `<span class="unknown">${s.status === "single extractor" ? "one extractor only" : "not stated"}</span>`;
  const name = (i) => `${i}${inv[i].acronym ? " " + inv[i].acronym : ""}`;
  $("#map-tabs").innerHTML = fns.map((f, k) => `<button role="tab" data-f="${esc(f)}" aria-selected="${k === 0}">${esc(f)}</button>`).join("");
  const showFn = (f) => {
    document.querySelectorAll("#map-tabs button").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.f === f)));
    const rows = emap.by_function[f], agreed = rows.filter((r) => r.status === "agreed").map((r) => r.study);
    const full = agreed.filter((i) => Object.values(inv[i].slots).every((s) => s.status === "agreed"));
    const prs = emap.pairs.filter((p) => p.shared_functions.includes(f) && agreed.includes(p.from) && agreed.includes(p.to));
    const n = (v) => prs.filter((p) => p.verdict === v).length;
    const rank = indus ? Object.fromEntries(indus.ranking[f].map((x, k) => [x.study, { k: k + 1, ...x }])) : null;
    const top = rank ? indus.ranking[f].slice(0, agreed.length).filter((x) => agreed.includes(x.study)).length : null;
    $("#map-concl").innerHTML = `<strong>${agreed.length} of 24 investigations</strong> give evidence for ${esc(f)} by both extractors${rows.length > agreed.length ? ` (${rows.length - agreed.length} more by one only)` : ""}. `
      + `All four conditions are stated in the record for ${full.length} of them. Among their ${prs.length} pairs: ${n("conditionally informative")} conditionally informative, ${n("not directly transferable")} not directly transferable (a recorded condition differs), ${n("not established")} not established (a condition is not stated; unknown is not compatible).`
      + (rank ? ` INDUS, asked “${esc(indus.questions[f])}”, puts ${top} of these ${agreed.length} in its top ${agreed.length}.` : "");
    $("#map-indus-h").hidden = !rank;
    $("#map-rows").innerHTML = rows.map((r) => {
      const v = inv[r.study], g = v.functions.find((x) => x.function === f), first = Object.values(g.by)[0];
      return `<tr><td><a href="https://psi.nasa.gov/" title="NASA PSI record ${esc(r.study)}">${esc(r.study)}</a><span class="sub">${esc(v.title)}</span></td>
        <td>${esc(first.statement || "")}<span class="sub">“${esc(first.quote)}”${r.status === "agreed" ? "" : ` · named by ${esc(Object.keys(g.by)[0])} only`}</span></td>
        ${Object.keys(emap.vocabulary.slots).map((s) => `<td>${slotCell(v.slots[s])}</td>`).join("")}
        ${rank ? `<td>${rank[r.study] ? `rank ${rank[r.study].k} of 24<span class="sub">${rank[r.study].score.toFixed(3)}</span>` : "—"}</td>` : ""}</tr>`;
    }).join("");
  };
  $("#map-tabs").addEventListener("click", (e) => { const b = e.target.closest("button"); if (b) showFn(b.dataset.f); });
  showFn(fns.includes("flame spread") ? "flame spread" : fns[0]);
  const c = emap.pair_verdicts, tot = emap.pairs.length;
  $("#map-pairs").textContent = `All ${tot} pairs of investigations, on the conditions both extractors agreed on: ${c["conditionally informative"] || 0} conditionally informative, ${c["not directly transferable"] || 0} not directly transferable, ${c["not established"] || 0} not established, ${c["no shared fire-safety function"] || 0} with no fire-safety function in common. Record text carries no quantitative conditions, so no pair is ever marked transferable outright.`;
  const opts = ids.map((i) => `<option value="${i}">${esc(name(i))}</option>`).join("");
  $("#map-a").innerHTML = opts; $("#map-b").innerHTML = opts;
  const ci = emap.pairs.find((p) => p.verdict === "conditionally informative") || emap.pairs[0];
  $("#map-a").value = ci.from; $("#map-b").value = ci.to;
  const showPair = () => {
    const a = $("#map-a").value, b = $("#map-b").value;
    const p = emap.pairs.find((x) => (x.from === a && x.to === b) || (x.from === b && x.to === a));
    if (!p) { $("#map-verdict").innerHTML = `<p class="tr-concl">Same investigation</p>`; $("#map-gates").innerHTML = ""; return; }
    $("#map-verdict").className = `tr-verdict ${p.verdict === "conditionally informative" ? "" : "undetermined"}`;
    const why = Object.entries(p.gates).filter(([, s]) => s !== "pass").map(([g, s]) => `${g.replace("_", " ")}: ${s === "fail" ? "differs" : "not stated or disputed"}`);
    $("#map-verdict").innerHTML = `<p class="tr-concl">${esc(p.verdict[0].toUpperCase() + p.verdict.slice(1))}</p>
      <p>${p.shared_functions.length ? `Shared functions: ${esc(p.shared_functions.join(", "))}.` : "The two records name no fire-safety function in common."}</p>
      ${why.length && p.shared_functions.length ? `<ul>${why.map((w) => `<li>${esc(w)}</li>`).join("")}</ul>` : ""}`;
    $("#map-gates").innerHTML = Object.entries(p.gates).map(([g, s]) => `<tr><td>${esc(g.replace("_", " "))}</td><td><span class="gs ${s}">${s}</span></td><td>${slotCell(inv[a].slots[g])}</td><td>${slotCell(inv[b].slots[g])}</td></tr>`).join("");
  };
  $("#map-a").addEventListener("change", showPair); $("#map-b").addEventListener("change", showPair); showPair();
  // every pair at once: a matrix coloured by verdict, filtered by verdict
  const VERD = ["no shared fire-safety function", "not established", "not directly transferable", "conditionally informative"];
  const VCOL = ["#243042", "#e6c36a", C.ember, C.blue];
  const pairOf = (a, b) => emap.pairs.find((x) => (x.from === a && x.to === b) || (x.from === b && x.to === a));
  const short = ids.map((i) => inv[i].acronym || i);
  let cat = null;
  const pick = (a, b) => { $("#map-a").value = a; $("#map-b").value = b; showPair(); $("#map-verdict").scrollIntoView({ block: "nearest", behavior: "smooth" }); };
  const drawMatrix = () => {
    const wide = $("#plot-map").clientWidth, ml = wide < 520 ? 70 : 140, size = Math.max(4, Math.floor((Math.min(wide, 760) - ml - 10) / ids.length) - 2);
    const traces = VERD.map((v, k) => {
      const pts = [];
      ids.forEach((a, ia) => ids.forEach((b, ib) => { if (a !== b && pairOf(a, b).verdict === v) pts.push([ib, ia, a, b]); }));
      return { type: "scatter", mode: "markers", x: pts.map((q) => q[0]), y: pts.map((q) => q[1]), customdata: pts.map((q) => [q[2], q[3]]),
        text: pts.map((q) => { const p = pairOf(q[2], q[3]); return `${name(q[2])} and ${name(q[3])}<br>${v}${p.shared_functions.length ? "<br>shared: " + p.shared_functions.join(", ") : ""}`; }),
        hoverinfo: "text", marker: { symbol: "square", size, color: VCOL[k], opacity: cat === null || cat === k ? 1 : 0.12 } };
    });
    const ax = { tickmode: "array", tickvals: ids.map((_, k) => k), ticktext: wide < 520 ? ids.map((i) => i.replace("PSI-", "")) : short, range: [-0.7, ids.length - 0.3], fixedrange: true, showgrid: false, zeroline: false };
    Plotly.react("plot-map", traces, { ...layoutBase, height: Math.min(wide, 760) - ml + 130, margin: { l: ml, r: 10, t: 10, b: wide < 520 ? 40 : 120 }, xaxis: { ...ax, tickangle: -60 }, yaxis: { ...ax, range: [ids.length - 0.3, -0.7] }, hovermode: "closest" }, cfg);
    $("#map-cats").innerHTML = `<button data-c="" aria-pressed="${cat === null}">all ${emap.pairs.length} pairs</button>` + VERD.map((v, k) => `<button data-c="${k}" aria-pressed="${cat === k}"><span class="sw" style="background:${VCOL[k]}"></span>${c[v] || 0} ${esc(v)}</button>`).slice().reverse().join("");
    const sel = cat === null ? [] : emap.pairs.filter((p) => p.verdict === VERD[cat]);
    $("#map-list").innerHTML = sel.map((p) => `<button class="btn" data-a="${p.from}" data-b="${p.to}">${esc(name(p.from))} ↔ ${esc(name(p.to))}</button>`).join("");
  };
  drawMatrix();
  $("#plot-map").on("plotly_click", (e) => { const [a, b] = e.points[0].customdata; pick(a, b); });
  $("#map-cats").addEventListener("click", (e) => { const b = e.target.closest("button"); if (b) { cat = b.dataset.c === "" ? null : Number(b.dataset.c); drawMatrix(); } });
  $("#map-list").addEventListener("click", (e) => { const b = e.target.closest("button"); if (b) pick(b.dataset.a, b.dataset.b); });
  const dropped = Object.values(inv).reduce((t, v) => t + Object.values(v.dropped).reduce((x, y) => x + y, 0), 0);
  $("#map-note").textContent = `${emap.label} Extractors: ${models.join(" and ")}, one call per record, no history. A value stands only when both gave it, each with a passage found word for word in the record; ${dropped} items failed that check and were dropped. The check proves the passage exists, not that it was read correctly, so the passage is shown. `
    + (indus ? `Relevance: ${indus.model} (${indus.label}) ` : "") + "Protocol, fixed and anchored before the run: docs/GFL_EVIDENCE_MAP_PROTOCOL_v1.md.";
} else { $("#map").hidden = true; }

// ---------------------------------------------------------------- literature relevance (INDUS)
if (relevance) {
  $("#relevance").hidden = false;
  $("#rel-tabs").innerHTML = relevance.results.map((q, i) => `<button role="tab" data-q="${i}" aria-selected="${i === 0}">${esc(q.id)}</button>`).join("");
  const showQ = (i) => {
    const q = relevance.results[i];
    document.querySelectorAll("#rel-tabs button").forEach((b) => b.setAttribute("aria-selected", String(Number(b.dataset.q) === i)));
    $("#rel-why").innerHTML = `<strong>${esc(q.question)}</strong><br>Why we ask: ${esc(q.why)}`;
    $("#rel-list").innerHTML = q.hits.map((h) => `<li><span class="rel-score">${h.score.toFixed(3)}</span><span class="rel-src">${esc(h.file.replace(/\.pdf$/i, ""))}, page ${h.page}</span><span class="sub">“${esc(h.snippet)}…”</span></li>`).join("");
  };
  $("#rel-tabs").addEventListener("click", (ev) => { const b = ev.target.closest("button[data-q]"); if (b) showQ(Number(b.dataset.q)); });
  showQ(0);
  $("#rel-note").textContent = `Model ${relevance.model} (sentence-transformers ${relevance.sentence_transformers}), run ${relevance.run_utc} on the owner's machine; ${relevance.corpus.length} files, ${relevance.passages} passages of about ${relevance.chunk_chars} characters. Scores are cosine similarities for ordering what to read, not probabilities. Snippets are short pointers; read the source.`;
}

// ---------------------------------------------------------------- page data against the ledger
async function verifyPageData(res) {
  const files = ["experiment_memory.json", "b6_series.json", "capabilities.json", "transfer_pmma100.json", "vault.json", "families.json",
    "ai_findings.json", "comparable_runs.json", "predictions.json", "analysis.json", ...(relevance ? ["relevance.json"] : [])];
  const latest = {};
  for (const r of res) { const loc = r.entry.object?.location; if (loc) latest[loc] = r.entry.object.sha256; }
  const out = [];
  for (const f of files) {
    const exp = latest[`visualization/data/${f}`];
    if (!exp) { out.push([f, "not sealed"]); continue; }
    const r = await verifyFile(`./data/${f}`, exp);
    out.push([f, r.state]);
  }
  const good = out.filter((x) => x[1] === "ok").length;
  const bad = out.filter((x) => x[1] !== "ok");
  $("#data-status").innerHTML = `Data shown on this page: ${good} of ${out.length} files match their ledger seals${bad.length ? ` <span class="res-bad">(${bad.map((b) => esc(b.join(": "))).join(", ")})</span>` : ""}.`;
}
