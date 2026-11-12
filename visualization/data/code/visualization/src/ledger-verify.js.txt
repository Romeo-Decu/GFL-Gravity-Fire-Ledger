// GFL ledger verification in the browser (and in Node for tests).
// Reproduces src/gfl_ledger/core.py exactly:
//   canonical(body) = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
//   entry_hash      = sha256(canonical(entry without entry_hash, sig))
//   sig             = Ed25519 over bytes.fromhex(entry_hash)
// Numbers are kept as their original lexemes (never re-formatted by JavaScript), so a value such as
// 1.0 or 1e-05 hashes exactly as Python wrote it.

const NUM = Symbol("num");

// Minimal JSON parser that keeps number tokens as strings.
export function parseRaw(text) {
  let i = 0;
  const ws = () => { while (i < text.length && " \t\n\r".includes(text[i])) i++; };
  function value() {
    ws();
    const c = text[i];
    if (c === "{") {
      i++; const obj = {}; ws();
      if (text[i] === "}") { i++; return obj; }
      for (;;) {
        ws(); const k = str(); ws(); i++; // ':'
        obj[k] = value(); ws();
        if (text[i] === ",") { i++; continue; }
        i++; return obj; // '}'
      }
    }
    if (c === "[") {
      i++; const arr = []; ws();
      if (text[i] === "]") { i++; return arr; }
      for (;;) {
        arr.push(value()); ws();
        if (text[i] === ",") { i++; continue; }
        i++; return arr;
      }
    }
    if (c === '"') return str();
    if (text.startsWith("true", i)) { i += 4; return true; }
    if (text.startsWith("false", i)) { i += 5; return false; }
    if (text.startsWith("null", i)) { i += 4; return null; }
    const m = /^-?\d+(\.\d+)?([eE][+-]?\d+)?/.exec(text.slice(i));
    if (!m) throw new Error(`JSON parse error at ${i}`);
    i += m[0].length;
    return { [NUM]: m[0] };
  }
  function str() {
    const start = i; i++;
    while (text[i] !== '"') { if (text[i] === "\\") i++; i++; }
    i++;
    return JSON.parse(text.slice(start, i));
  }
  const v = value();
  return v;
}

// Python json.dumps string escaping with ensure_ascii=False.
function pyString(s) {
  let out = '"';
  for (const ch of s) {
    const code = ch.codePointAt(0);
    if (ch === '"') out += '\\"';
    else if (ch === "\\") out += "\\\\";
    else if (ch === "\n") out += "\\n";
    else if (ch === "\r") out += "\\r";
    else if (ch === "\t") out += "\\t";
    else if (ch === "\b") out += "\\b";
    else if (ch === "\f") out += "\\f";
    else if (code < 0x20) out += "\\u" + code.toString(16).padStart(4, "0");
    else out += ch;
  }
  return out + '"';
}

// Python sorts keys by code point; JS default sort compares UTF-16 units. Compare code points.
function cpCompare(a, b) {
  const A = Array.from(a, (c) => c.codePointAt(0)), B = Array.from(b, (c) => c.codePointAt(0));
  for (let k = 0; k < Math.min(A.length, B.length); k++) if (A[k] !== B[k]) return A[k] - B[k];
  return A.length - B.length;
}

export function canonical(v) {
  if (v === null) return "null";
  if (v === true) return "true";
  if (v === false) return "false";
  if (typeof v === "string") return pyString(v);
  if (Array.isArray(v)) return "[" + v.map(canonical).join(",") + "]";
  if (v && v[NUM] !== undefined) return v[NUM];
  const keys = Object.keys(v).sort(cpCompare);
  return "{" + keys.map((k) => pyString(k) + ":" + canonical(v[k])).join(",") + "}";
}

export function plain(v) {
  if (v === null || typeof v !== "object") return v;
  if (v[NUM] !== undefined) return Number(v[NUM]);
  if (Array.isArray(v)) return v.map(plain);
  return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, plain(x)]));
}

const enc = new TextEncoder();
const hex = (buf) => Array.from(new Uint8Array(buf), (b) => b.toString(16).padStart(2, "0")).join("");
const unhex = (h) => new Uint8Array(h.match(/../g).map((x) => parseInt(x, 16)));
const unb64 = (s) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));

export async function sha256Hex(bytes) {
  return hex(await crypto.subtle.digest("SHA-256", bytes));
}

async function makeVerifier(pubB64) {
  const raw = unb64(pubB64);
  try {
    const key = await crypto.subtle.importKey("raw", raw, { name: "Ed25519" }, false, ["verify"]);
    return { engine: "WebCrypto Ed25519", verify: (sig, msg) => crypto.subtle.verify({ name: "Ed25519" }, key, sig, msg) };
  } catch {
    // Fallback for browsers without Ed25519 in WebCrypto (approved dependency, DEC on ADR-001 stack).
    const ed = await import("https://cdn.jsdelivr.net/npm/@noble/ed25519@2.1.0/+esm");
    ed.etc.sha512Async = async (...m) => new Uint8Array(await crypto.subtle.digest("SHA-512", ed.etc.concatBytes(...m)));
    return { engine: "noble-ed25519 2.1.0", verify: (sig, msg) => ed.verifyAsync(sig, msg, raw) };
  }
}

// Verify every entry: content hash, sequence, prev link, signature. Returns per-entry results.
export async function verifyLedger(ledgerText, publicKeys, onProgress) {
  const lines = ledgerText.split("\n").filter((l) => l.trim());
  const verifiers = {};
  for (const k of publicKeys) verifiers[k.key_id] = await makeVerifier(k.public_key_b64);
  const results = [];
  let prev = "0".repeat(64);
  for (let i = 0; i < lines.length; i++) {
    const raw = parseRaw(lines[i]);
    const e = plain(raw);
    const body = Object.fromEntries(Object.entries(raw).filter(([k]) => k !== "entry_hash" && k !== "sig"));
    const h = await sha256Hex(enc.encode(canonical(body)));
    const errors = [];
    if (h !== e.entry_hash) errors.push("content does not match entry_hash");
    if (e.seq !== i) errors.push("sequence number out of order");
    if (e.prev !== prev) errors.push("prev link broken");
    const v = verifiers[e.key_id];
    let sigOk = false;
    if (!v) errors.push(`unknown key ${e.key_id}`);
    else {
      sigOk = await v.verify(unb64(e.sig), unhex(e.entry_hash));
      if (!sigOk) errors.push("signature invalid");
    }
    results.push({ seq: i, type: e.type, entry_hash: e.entry_hash, computed: h, ok: errors.length === 0, errors,
                   engine: v ? v.engine : null, entry: e });
    prev = e.entry_hash;
    if (onProgress) onProgress(i + 1, lines.length);
  }
  return results;
}

// Verify a fetched file against the sha256 sealed in the ledger.
export async function verifyFile(url, expectedSha256) {
  const res = await fetch(url);
  if (!res.ok) return { state: "missing", status: res.status };
  const got = await sha256Hex(await res.arrayBuffer());
  return { state: got === expectedSha256 ? "ok" : "altered", sha256: got };
}
