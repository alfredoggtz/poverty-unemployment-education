/**
 * api.js
 * Centralized API client for communicating with the FastAPI backend.
 */

const BASE = 'http://127.0.0.1:8000';

// ── Script execution ─────────────────────────────────────────────────────────

/**
 * Runs a pipeline script and streams its output line by line.
 * @param {'extraction'|'mysql'|'mongodb'} script
 * @param {(line: string) => void} onLine  - called for each output line
 * @param {(code: number) => void} onDone  - called when process exits
 */
export async function runScript(script, onLine, onDone) {
  const res = await fetch(`${BASE}/run/${script}`, { method: 'POST' });
  const reader = res.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    for (const line of chunk.split('\n')) {
      const data = line.replace(/^data: /, '').trim();
      if (!data) continue;

      const exit = data.match(/^\[EXIT:(-?\d+)\]$/);
      if (exit) {
        onDone(parseInt(exit[1]));
      } else {
        onLine(data);
      }
    }
  }
}

// ── Config ───────────────────────────────────────────────────────────────────

export async function getConfig() {
  const res = await fetch(`${BASE}/config`);
  return res.json();
}

export async function saveConfig(data) {
  const res = await fetch(`${BASE}/config`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ data }),
  });
  return res.json();
}

// ── Data ─────────────────────────────────────────────────────────────────────

export async function getMysqlData(table) {
  const res = await fetch(`${BASE}/data/mysql/${table}`);
  return res.json();
}

export async function getMongoData(collection) {
  const res = await fetch(`${BASE}/data/mongodb/${collection}`);
  return res.json();
}

// ── Views ─────────────────────────────────────────────────────────────────────

export async function getViewData(viewName) {
  const res = await fetch(`${BASE}/views/${viewName}`);
  return res.json();
}
