import { verifyLedger, verifyFile } from "./ledger-verify.js";

const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const clean = (t) => String(t).replace(/\*\*/g, "").replace(/`/g, "");
const NEG_STATES = new Set(["withdrawn", "rejected", "superseded"]);
const C = { blue: "#6cb4ff", ember: "#e8833a", soot: "#5b6675", fog: "#d8e1ea", muted: "#8a9bb0", rule: "#26364a", panel: "#16212f" };

const [memory, series, ledgerText, pubPipeline, pubOwner] = await Promise.all([
  fetch("./data/experiment_memory.json").then((r) => r.json()),
  fetch("./data/b6_series.json").then((r) => r.json()),
  fetch("./data/ledger.jsonl").then((r) => r.text()),
  fetch("./data/release-a.pub.json").then((r) => r.json()),
  fetch("./data/owner.pub.json").then((r) => r.json()),
]);
const records = new Map(memory.records.map((r) => [r.id, r]));
const entries = ledgerText.split("\n").filter((l) => l.trim()).map((l) => JSON.parse(l));
const verified = new Map(); // seq -> result

// ---------------------------------------------------------------- hero budget
const h = series.headline;
$("#h-rate").textContent = h.rate_mm_s.toFixed(2);
$("#h-budget").innerHTML = [
  ["Statistical, 95 %", `${h.stat95[0].toFixed(2)}–${h.stat95[1].toFixed(2)} mm/s`],
  ["Front definition", `${h.definitions_rel[0].toFixed(2)}–${h.definitions_rel[1].toFixed(2)} mm/s`],
  ["Rule variants (60)", `${h.rule_variants[0].toFixed(2)}–${h.rule_variants[1].toFixed(2)} mm/s`],
  ["Spatial scale", "±3 %"],
  ["Ruler–sample parallax", '<span class="unknown">unknown</span>'],
  ["Flame edge vs pyrolysis front", '<span class="unknown">unknown</span>'],
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
const NEG_OUT = new Set(["rejected", "withdrawn", "superseded"]);
$("#timeline").innerHTML = steps.map((s, i) => {
  const cls = s.outcome === "superseded" ? "sup" : NEG_OUT.has(s.outcome) ? "neg" : "";
  return `<li class="${cls}"><button type="button" data-i="${i}" aria-current="${i === 0}">
    <span class="t-date">${esc(s.date)}</span>
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
["case", "rate", "memory", "ledger"].forEach((id) => obs.observe(document.getElementById(id)));
