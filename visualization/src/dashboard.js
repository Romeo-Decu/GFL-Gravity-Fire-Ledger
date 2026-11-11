import { verifyLedger, verifyFile } from "./ledger-verify.js";

const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const clean = (t) => String(t).replace(/\*\*/g, "").replace(/`/g, "");
const NEG_STATES = new Set(["withdrawn", "rejected", "superseded"]);
const C = { blue: "#6cb4ff", ember: "#e8833a", soot: "#5b6675", fog: "#d8e1ea", muted: "#8a9bb0", rule: "#26364a", panel: "#16212f" };

const [memory, series, ledgerText, pubPipeline, pubOwner, caps, transfer, vault, families, aiF, comp, preds, an, relevance] = await Promise.all([
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
]);
const records = new Map(memory.records.map((r) => [r.id, r]));
const entries = ledgerText.split("\n").filter((l) => l.trim()).map((l) => JSON.parse(l));
const verified = new Map(); // seq -> result

// ---------------------------------------------------------------- hero budget
const h = series.headline;
$("#h-rate").textContent = h.rate_mm_s.toFixed(2);
const segDefs = Object.values(series.segment.definitions).map((d) => d.ols_mm_s);
const ref01 = series.segment.definitions["rel_peak_0.1"];
const hac = [ref01.ols_mm_s - 2.306 * ref01.se_hac_mm_s, ref01.ols_mm_s + 2.306 * ref01.se_hac_mm_s];
const distinct = new Set(series.robustness.grid.filter((g) => g.fitted).map((g) => g["rate_rel_0.1_mm_s"])).size;
$("#h-budget").innerHTML = [
  ["Reference definition", "leading edge at 0.1 of each frame's peak; the lowest of the eight definitions"],
  ["Statistical, 95 % (approximate)", `${h.stat95[0].toFixed(2)}–${h.stat95[1].toFixed(2)} mm/s, block bootstrap on 10 frames; HAC t-interval ${hac[0].toFixed(2)}–${hac[1].toFixed(2)}`],
  ["Front definition", `${Math.min(...segDefs).toFixed(2)}–${Math.max(...segDefs).toFixed(2)} mm/s (relative ${h.definitions_rel[0].toFixed(2)}–${h.definitions_rel[1].toFixed(2)}; absolute thresholds and peak higher)`],
  ["Window-rule variants", `${h.rule_variants[0].toFixed(2)}–${h.rule_variants[1].toFixed(2)} mm/s (60 variants, ${distinct} distinct rates; segment minimums not varied)`],
  ["Spatial scale", "±3 % allowance; ruler lies behind the sample (ISS-020 open)"],
  ["Flow speed at the sample", '<span class="unknown">not established: the display reads 3 cm/s (NASA Table A.1); transducer position and response time not reconciled (ISS-013)</span>'],
  ["Ruler–sample parallax", '<span class="unknown">unknown</span>'],
  ["Flame edge vs pyrolysis front", '<span class="unknown">unknown</span>'],
  ["Status", '<span class="unknown">provisional</span>'],
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
["capabilities", "case", "rate", "predictions", "analysis", "ai", "transfer", "comparable", "relevance", "families", "memory", "vault", "ledger"].forEach((id) => obs.observe(document.getElementById(id)));

// ---------------------------------------------------------------- function map
$("#cap-groups").innerHTML = caps.groups.map((g) => `<div class="cap-group"><h3>${esc(g.name)}</h3><div class="cap-tiles">${g.items.map((it) => {
  const link = it.open && it.status !== "designed"
    ? `<a class="btn" href="${esc(it.open)}">Open</a>${it.spec ? ` <a class="btn" href="./spec.html?doc=${encodeURIComponent(it.spec)}">Specification</a>` : ""}`
    : `<a class="btn" href="./spec.html?doc=${encodeURIComponent(it.spec)}">Read the specification</a>`;
  return `<article class="cap ${esc(it.status)}"><img src="./assets/brand/icons/${esc(it.icon)}.svg" alt="">
    <div class="cap-name">${esc(it.name)} <span class="pill ${esc(it.status)}">${esc(it.status)}</span></div>
    <p>${esc(it.summary)}</p><div>${link}</div></article>`;
}).join("")}</div></div>`).join("");

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
$("#pr-thick-note").textContent = `${preds.thickness_series.note} Weighted fit of rate ∝ thickness^n: n = ${ex.B13_display_3.n_weighted} (95 % ${ex.B13_display_3.ci95[0]} to ${ex.B13_display_3.ci95[1]}) with B13's registered segment, ${ex.B13_display_4.n_weighted} (${ex.B13_display_4.ci95[0]} to ${ex.B13_display_4.ci95[1]}) with its display-4 segment; the inverse-thickness law n = −1 lies inside both, and the data cannot tell it from a steeper law. Points at one thickness are spread slightly sideways by air display so they do not overlap.`;
$("#pr-note").textContent = `${bt.lesson} Reference: B6 under ${preds.rule}, ${f3(preds.reference.rate_mm_s)} mm/s. Protocol: ${preds.protocol}, ${preds.registered}.`;

// ---------------------------------------------------------------- analysis modules (A0–A7)
const GS = { pass: "pass", partial: "unknown", fail: "fail", unknown: "unknown" };
$("#an-runs").innerHTML = Object.entries(an.runs).map(([run, r]) => { const c = r.cram1, p = c.prediction;
  return `<tr><td><strong>${esc(run)}</strong><span class="sub">${p.thickness_um} µm, air display ${r.record.air_display} = ${r.flow.value_cm_s} cm/s</span></td>
  <td>${f3(r.record.rate_mm_s)} mm/s<span class="sub">${f3(r.record.interval_mm_s[0])}–${f3(r.record.interval_mm_s[1])}</span></td>
  <td>${f3(p.band_mm_s[0])}–${f3(p.band_mm_s[1])} mm/s<span class="sub">π/4 ${f3(p.rate_mm_s_by_constant.Delichatsios_pi_over_4)}, EST ${f3(p.rate_mm_s_by_constant.EST_1)}, √2 ${f3(p.rate_mm_s_by_constant.de_Ris_sqrt2)}</span></td>
  <td>${an.cram1_measured_over_lowest_theory[run]}<span class="sub">thin check τ/δ ${c.thin_check.ratio_tau_over_delta}</span></td>
  <td>${r.regime_by_segment.map((s) => `<span class="sub">display ${s.air_display}: ${esc(s.regime)}${s.radiation_number != null ? `, Da ${Math.round(s.damkohler)}, Rr ${s.radiation_number}` : ""}</span>`).join("")}</td></tr>`; }).join("");
$("#an-runs-note").textContent = "Thin-fuel theory (de Ris √2, Delichatsios π/4, EST 1) with PMMA properties from Rojas-Alva 2022, band over the published F range 4.4–5.5; the F = 4.76 fitted to data is never used. The theory over-predicts more as the fuel thickens (1.04, 0.95, 0.86, 0.79), consistent with the thickness exponent −1.19. Regime groups use NASA's fan calibration (U = 1.0066 × air display, duct centreline) and order-of-magnitude boundaries: they say when chemistry matters, they do not model it.";
const gids = Object.keys(an.transfer[0].gates);
$("#an-tr-head").innerHTML = `<tr><th scope="col">Source → target</th>${gids.map((g) => `<th scope="col">${esc(g.replaceAll("_", " "))}</th>`).join("")}<th scope="col">Conclusion</th></tr>`;
$("#an-tr-body").innerHTML = an.transfer.map((t) => `<tr><td><strong>${esc(t.source)} → ${esc(t.target)}</strong></td>${gids.map((g) => `<td><span class="gs ${GS[t.gates[g].status]}" title="${esc(t.gates[g].reasons.join(" "))}">${esc(t.gates[g].status)}</span></td>`).join("")}<td>${esc(t.conclusion.replaceAll("_", " "))}</td></tr>`).join("");
$("#an-tr-note").textContent = "Every gate state is computed from the run records (NASA table, proof sheets, frozen-rule rate files, CRAM-1, CRAM-2) and judged by the unchanged deterministic engine. No pair reaches \"directly supported\": the uncertainty gate stays partial while the luminous-edge offset has no bound.";
const u = an.runs.B6.uq;
$("#an-uq").innerHTML = [
  ["1. Statistical", `${f3(u.layer1_statistical_95_mm_s[0])}–${f3(u.layer1_statistical_95_mm_s[1])} mm/s (bootstrap 95 %)`],
  ["2. Analyst choice", `± ${f3(u.layer2_analyst_choice.systematic_mm_s)} mm/s across front definitions; reported interval ${f3(u.reported_interval_mm_s[0])}–${f3(u.reported_interval_mm_s[1])} mm/s`],
  ...u.layer3_physical_unknowns.map((e) => [`3. ${e.what}`, `${e.bound_rel ? `bounded ±${100 * e.bound_rel} %` : "no bound"}. ${e.evidence}`])].map(([a, b]) => `<tr><td><strong>${esc(a)}</strong></td><td>${esc(b)}</td></tr>`).join("");
$("#an-anom").innerHTML = (an.table_anomalies || []).map((f) => `<tr><td>${esc(f.test)}</td><td>${esc(f.check.replaceAll("_", " "))}</td><td>${esc(f.field ? `${f.field}: ` : "")}${esc(String(f.value ?? ""))}</td></tr>`).join("");
$("#an-note").textContent = `Flags are what the checks saw, not what they mean. On the synthetic test the detector found every anomaly that could be seen in the data (a saturated frame, flicker, a pre-burn gap) and nothing else; the luminous-edge offset cannot be seen in images. Provenance export: ${an.prov_summary.entities} entities in W3C PROV-O. Status: ${an.status}.`;

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
