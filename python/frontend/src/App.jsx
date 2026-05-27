import { useState } from 'react';
import { runScript, getConfig, saveConfig, getMysqlData, getMongoData, getViewData } from './api.js';
import Terminal from './Terminal';
import DataTable from './DataTable';

const TABLES     = ['period', 'education_indicator', 'economy_indicator', 'employment_indicator'];
const MYSQL_KEYS = ['host', 'user', 'password', 'database', 'mysql_path'];
const MONGO_KEYS = ['mongo_host', 'mongo_port', 'mongo_user', 'mongo_password', 'mongo_database'];

const VIEWS = [
  { key: 'v_full_indicators',           label: 'Full Indicators',          icon: '📋' },
  { key: 'v_education_vs_unemployment', label: 'Education vs Unemployment', icon: '🎓' },
  { key: 'v_unemployment_vs_economy',   label: 'Unemployment vs Economy',   icon: '💹' },
  { key: 'v_poverty_trend',             label: 'Poverty Trend',             icon: '📉' },
  { key: 'v_audit_activity',            label: 'Audit Activity',            icon: '🔍' },
  { key: 'v_indicator_averages',        label: 'Indicator Averages',        icon: '📊' },
  { key: 'v_year_over_year',            label: 'Year Over Year',            icon: '📅' },
  { key: 'v_spending_vs_outcomes',      label: 'Spending vs Outcomes',      icon: '💰' },
  { key: 'v_population_distribution',   label: 'Population Distribution',   icon: '👥' },
];

/* ── Shared styles ─────────────────────────────────────────────────── */
const inputStyle = {
  width: '100%',
  background: '#0d0d0d',
  border: '1px solid #333',
  borderRadius: '3px',
  padding: '8px 12px',
  color: '#eee',
  fontFamily: "'Barlow Condensed', sans-serif",
  fontSize: '1rem',
  fontWeight: 600,
  outline: 'none',
};

const fieldLabel = {
  display: 'block',
  fontSize: '0.6rem',
  color: '#666',
  marginBottom: '3px',
  fontFamily: "'Russo One', sans-serif",
  textTransform: 'uppercase',
  letterSpacing: '0.15em',
};

const actionBtn = (color = '#cc1a1a', disabled = false) => ({
  background: disabled ? '#222' : color,
  border: 'none',
  borderRadius: '3px',
  color: disabled ? '#555' : '#fff',
  padding: '10px 24px',
  cursor: disabled ? 'not-allowed' : 'pointer',
  fontFamily: "'Russo One', sans-serif",
  fontSize: '0.78rem',
  letterSpacing: '0.1em',
  textTransform: 'uppercase',
  transition: 'filter 0.1s',
});

/* ── SmashPanel — the big diagonal menu tile ────────────────────────── */
function SmashPanel({ label, icon, color, sublabel, active, onClick, running }) {
  const isActive = active;
  return (
    <div
      onClick={onClick}
      style={{
        background: color,
        cursor: 'pointer',
        padding: '0',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
        justifyContent: 'flex-end',
        position: 'relative',
        overflow: 'hidden',
        transition: 'filter 0.15s, transform 0.1s',
        filter: isActive ? 'brightness(1.15)' : 'brightness(0.85)',
        transform: isActive ? 'scale(1.02)' : 'scale(1)',
        outline: isActive ? '3px solid #fff' : 'none',
        outlineOffset: '-3px',
        minHeight: '120px',
        userSelect: 'none',
      }}
    >
      {/* diagonal shine overlay */}
      <div style={{
        position: 'absolute', inset: 0,
        background: 'linear-gradient(135deg, rgba(255,255,255,0.12) 0%, transparent 50%)',
        pointerEvents: 'none',
      }} />

      {/* icon */}
      <div style={{
        position: 'absolute', top: '14px', left: '50%', transform: 'translateX(-50%)',
        fontSize: '2rem', lineHeight: 1,
        filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.5))',
      }}>{icon}</div>

      {/* label */}
      <div style={{ padding: '12px 14px', width: '100%', background: 'rgba(0,0,0,0.25)' }}>
        <div style={{ fontFamily: "'Russo One', sans-serif", fontSize: '1rem', color: '#fff', letterSpacing: '0.05em', textShadow: '1px 1px 3px rgba(0,0,0,0.8)' }}>
          {label}
        </div>
        {sublabel && (
          <div style={{ fontFamily: "'Barlow Condensed'", fontSize: '0.72rem', color: 'rgba(255,255,255,0.7)', fontWeight: 600, marginTop: '2px' }}>
            {sublabel}
          </div>
        )}
      </div>

      {/* running indicator */}
      {running && (
        <div style={{
          position: 'absolute', top: 8, right: 8,
          width: 10, height: 10, borderRadius: '50%',
          background: '#ffd700',
          animation: 'pulse-dot 0.6s ease-in-out infinite',
        }} />
      )}
    </div>
  );
}

/* ── Central circle button (like the character art) ─────────────────── */
function CenterOrb({ tab }) {
  const icons = { Pipeline: '⚔️', Data: '📊', Config: '⚙️' };
  return (
    <div style={{
      width: '100px', height: '100px', borderRadius: '50%',
      background: 'radial-gradient(circle at 35% 35%, #555, #111)',
      border: '4px solid #888',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontSize: '2.4rem',
      boxShadow: '0 0 0 6px #222, 0 0 0 8px #444',
      flexShrink: 0,
    }}>
      {icons[tab]}
    </div>
  );
}

/* ── Pipeline tab ───────────────────────────────────────────────────── */
function PipelineTab() {
  const [lines, setLines]       = useState([]);
  const [running, setRunning]   = useState(null);
  const [exitCode, setExitCode] = useState(null);

  const run = async (script) => {
    setLines([]);
    setExitCode(null);
    setRunning(script);
    try {
      await runScript(script,
        line => setLines(prev => [...prev, line]),
        code => { setExitCode(code); setRunning(null); }
      );
    } catch {
      setLines(prev => [...prev, '[ERROR] Could not reach the backend.']);
      setRunning(null);
    }
  };

  const scripts = [
    { key: 'extraction', label: 'Extraction', icon: '🌐', color: '#2a9a2a', sublabel: 'INEGI & World Bank → CSV' },
    { key: 'mysql',      label: 'MySQL',      icon: '🗄️', color: '#1a7acc', sublabel: 'CSV → MySQL database'    },
    { key: 'mongodb',    label: 'MongoDB',    icon: '🍃', color: '#d4820a', sublabel: 'MySQL → MongoDB export'  },
  ];

  return (
    <div style={{ animation: 'slide-in 0.2s ease-out' }}>
      {/* 3-panel grid like Smash menu */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: '4px', marginBottom: '16px' }}>
        {scripts.map(s => (
          <SmashPanel
            key={s.key}
            label={s.label}
            icon={s.icon}
            color={s.color}
            sublabel={s.sublabel}
            active={running === null ? false : running === s.key}
            onClick={() => !running && run(s.key)}
            running={running === s.key}
          />
        ))}
      </div>

      {exitCode !== null && (
        <div style={{
          display: 'flex', alignItems: 'center', gap: '10px',
          marginBottom: '12px', padding: '10px 16px',
          background: exitCode === 0 ? 'rgba(68,221,102,0.1)' : 'rgba(255,68,68,0.1)',
          border: `2px solid ${exitCode === 0 ? 'var(--ok)' : 'var(--err)'}`,
          borderRadius: '4px',
          fontFamily: "'Russo One', sans-serif",
          fontSize: '0.88rem',
          color: exitCode === 0 ? 'var(--ok)' : 'var(--err)',
          letterSpacing: '0.1em',
        }}>
          {exitCode === 0 ? '🏆 GAME CLEAR!' : `💀 KO — EXIT CODE ${exitCode}`}
        </div>
      )}
      <Terminal lines={lines} running={!!running} />
    </div>
  );
}

/* ── Data tab ───────────────────────────────────────────────────────── */
function DataTab() {
  const [source, setSource]   = useState('mysql');
  const [selected, setSelected] = useState('period');
  const [data, setData]       = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState(null);

  const query = async () => {
    setLoading(true); setError(null);
    try {
      setData(source === 'mysql' ? await getMysqlData(selected) : await getMongoData(selected));
    } catch { setError('STAGE UNAVAILABLE — is the backend running?'); }
    finally { setLoading(false); }
  };

  return (
    <div style={{ animation: 'slide-in 0.2s ease-out' }}>
      {/* Source panels */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px', marginBottom: '14px' }}>
        {['mysql', 'mongodb'].map((s, i) => (
          <SmashPanel
            key={s}
            label={s.toUpperCase()}
            icon={s === 'mysql' ? '🗄️' : '🍃'}
            color={s === 'mysql' ? '#1a7acc' : '#d4820a'}
            sublabel={s === 'mysql' ? 'Relational database' : 'Document store'}
            active={source === s}
            onClick={() => setSource(s)}
          />
        ))}
      </div>

      <div style={{ display: 'flex', gap: '10px', alignItems: 'flex-end', marginBottom: '14px', background: '#141414', border: '1px solid #2a2a2a', padding: '14px', borderRadius: '4px' }}>
        <div style={{ flex: 1 }}>
          <label style={fieldLabel}>Table / Collection</label>
          <select value={selected} onChange={e => setSelected(e.target.value)} style={{ ...inputStyle, cursor: 'pointer' }}>
            {TABLES.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
        </div>
        <button onClick={query} disabled={loading} style={actionBtn('#cc1a1a', loading)}>
          {loading ? '▶ LOADING...' : '▶ SELECT'}
        </button>
      </div>

      {error && <p style={{ color: 'var(--err)', fontSize: '0.82rem', fontFamily: "'Russo One'", letterSpacing: '0.08em', marginBottom: '10px' }}>{error}</p>}
      {data && <DataTable data={data} />}
    </div>
  );
}

/* ── Config tab ─────────────────────────────────────────────────────── */
function ConfigSection({ title, color, icon, keys, cfg, setCfg }) {
  return (
    <div style={{ flex: 1, background: '#141414', border: `2px solid ${color}`, borderTop: `4px solid ${color}`, borderRadius: '4px', padding: '16px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
        <span style={{ fontSize: '1.2rem' }}>{icon}</span>
        <span style={{ fontFamily: "'Russo One', sans-serif", fontSize: '0.78rem', color, letterSpacing: '0.1em', textTransform: 'uppercase' }}>{title}</span>
      </div>
      <div style={{ display: 'grid', gap: '10px' }}>
        {keys.filter(k => k in cfg).map(key => (
          <div key={key}>
            <label style={fieldLabel}>{key}</label>
            <input
              type={key.toLowerCase().includes('password') ? 'password' : 'text'}
              value={cfg[key]}
              onChange={e => setCfg(prev => ({ ...prev, [key]: e.target.value }))}
              style={inputStyle}
            />
          </div>
        ))}
      </div>
    </div>
  );
}

function ConfigTab() {
  const [cfg, setCfg]         = useState(null);
  const [saved, setSaved]     = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState(null);

  const load = async () => {
    setLoading(true);
    try { setCfg(await getConfig()); }
    catch { setError('Could not load config.txt'); }
    finally { setLoading(false); }
  };

  const save = async () => {
    setLoading(true); setSaved(false);
    try { await saveConfig(cfg); setSaved(true); setTimeout(() => setSaved(false), 3000); }
    catch { setError('Could not save config.txt'); }
    finally { setLoading(false); }
  };

  return (
    <div style={{ animation: 'slide-in 0.2s ease-out' }}>
      {!cfg ? (
        <div style={{ background: '#141414', border: '1px solid #2a2a2a', borderRadius: '4px', padding: '24px', textAlign: 'center' }}>
          <div style={{ fontSize: '2.5rem', marginBottom: '12px' }}>⚙️</div>
          <p style={{ color: '#666', fontSize: '0.9rem', marginBottom: '18px', fontFamily: "'Barlow Condensed'", fontWeight: 600, letterSpacing: '0.05em' }}>
            Press START to load configuration
          </p>
          <button onClick={load} disabled={loading} style={actionBtn('#cc1a1a', loading)}>
            {loading ? '▶ LOADING...' : '▶ LOAD CONFIG'}
          </button>
          {error && <p style={{ color: 'var(--err)', marginTop: '10px', fontSize: '0.82rem', fontFamily: "'Russo One'" }}>{error}</p>}
        </div>
      ) : (
        <div>
          <div style={{ display: 'flex', gap: '10px', marginBottom: '14px', flexWrap: 'wrap' }}>
            <ConfigSection title="MySQL — P1" color="#1a7acc" icon="🗄️" keys={MYSQL_KEYS} cfg={cfg} setCfg={setCfg} />
            <ConfigSection title="MongoDB — P2" color="#d4820a" icon="🍃" keys={MONGO_KEYS} cfg={cfg} setCfg={setCfg} />
          </div>
          <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
            <button onClick={save} disabled={loading} style={actionBtn('#cc1a1a', loading)}>
              {loading ? '▶ SAVING...' : '▶ SAVE'}
            </button>
            {saved && (
              <span style={{ color: 'var(--ok)', fontSize: '0.82rem', fontFamily: "'Russo One'", letterSpacing: '0.1em' }}>
                ✔ SETTINGS SAVED!
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}


/* ── Views tab ──────────────────────────────────────────────────────── */
function ViewsTab() {
  const [selected, setSelected] = useState(VIEWS[0].key);
  const [data, setData]         = useState(null);
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState(null);

  const query = async () => {
    setLoading(true);
    setError(null);
    try { setData(await getViewData(selected)); }
    catch { setError('VIEW UNAVAILABLE — is the backend running?'); }
    finally { setLoading(false); }
  };

  const current = VIEWS.find(v => v.key === selected);

  return (
    <div style={{ animation: 'slide-in 0.2s ease-out' }}>
      {/* View tiles grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: '4px', marginBottom: '14px' }}>
        {VIEWS.map(v => (
          <SmashPanel
            key={v.key}
            label={v.label}
            icon={v.icon}
            color={selected === v.key ? '#8a2be2' : '#3a1a6a'}
            sublabel={v.key}
            active={selected === v.key}
            onClick={() => setSelected(v.key)}
          />
        ))}
      </div>

      {/* Query bar */}
      <div style={{ display: 'flex', gap: '10px', alignItems: 'center', marginBottom: '14px', background: '#141414', border: '1px solid #2a2a2a', padding: '14px', borderRadius: '4px' }}>
        <span style={{ fontSize: '1.4rem' }}>{current?.icon}</span>
        <span style={{ fontFamily: "'Russo One', sans-serif", fontSize: '0.82rem', color: '#8a2be2', letterSpacing: '0.08em', flex: 1, textTransform: 'uppercase' }}>
          {current?.label}
        </span>
        <span style={{ fontFamily: "'Share Tech Mono', monospace", fontSize: '0.72rem', color: '#555', flex: 2 }}>
          {selected}
        </span>
        <button onClick={query} disabled={loading} style={actionBtn(loading ? '#222' : '#8a2be2', loading)}>
          {loading ? '▶ LOADING...' : '▶ QUERY VIEW'}
        </button>
      </div>

      {error && <p style={{ color: 'var(--err)', fontSize: '0.82rem', fontFamily: "'Russo One'", letterSpacing: '0.08em', marginBottom: '10px' }}>{error}</p>}
      {data && <DataTable data={data} />}
    </div>
  );
}

/* ── Main App ────────────────────────────────────────────────────────── */
const TABS = [
  { key: 'Pipeline', label: 'Smash',         icon: '⚔️', color: '#cc1a1a',  sublabel: 'Run pipeline scripts' },
  { key: 'Data',     label: 'Games & More',  icon: '📊', color: '#1a7acc',  sublabel: 'Query data' },
  { key: 'Config',   label: 'Settings',      icon: '⚙️', color: '#2a9a2a',  sublabel: 'Configure connections' },
  { key: '_vault',   label: 'Vault',         icon: '🏆', color: '#cc2a6a',  sublabel: 'v1.0.0 — Ultimate' },
];

export default function App() {
  const [tab, setTab] = useState('Pipeline');

  return (
    <div style={{ minHeight: '100vh', background: '#111', display: 'flex', flexDirection: 'column' }}>

      {/* ── Main menu grid — like the Smash home screen ── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 220px', gridTemplateRows: 'auto', background: '#0a0a0a' }}>

        {/* Left big panel + right grid */}
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 3fr', gap: '3px', padding: '3px', minHeight: '220px' }}>

          {/* LEFT — active tab big tile, spans all rows */}
          <div style={{
            background: tab === 'Pipeline' ? '#cc1a1a'
                      : tab === 'Data'     ? '#1a7acc'
                      : tab === 'Config'   ? '#2a9a2a'
                      : tab === 'Views'    ? '#8a2be2'
                      :                     '#d4820a',
            display: 'flex', flexDirection: 'column', justifyContent: 'flex-end',
            padding: '20px',
            position: 'relative',
            overflow: 'hidden',
            cursor: 'default',
          }}>
            <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, transparent 60%)', pointerEvents: 'none' }} />
            <div style={{ fontSize: '3.5rem', marginBottom: '8px', filter: 'drop-shadow(0 3px 6px rgba(0,0,0,0.6))' }}>
              {tab === 'Pipeline' ? '⚔️' : tab === 'Data' ? '📊' : tab === 'Config' ? '⚙️' : tab === 'Views' ? '👁️' : '🌐'}
            </div>
            <div style={{ fontFamily: "'Russo One', sans-serif", fontSize: '2rem', color: '#fff', textShadow: '2px 2px 6px rgba(0,0,0,0.8)', letterSpacing: '0.03em' }}>
              {tab === 'Pipeline' ? 'Smash' : tab === 'Data' ? 'Data' : tab === 'Config' ? 'Config' : tab === 'Views' ? 'Vault' : 'Online'}
            </div>
            <div style={{ fontFamily: "'Barlow Condensed'", fontSize: '0.8rem', color: 'rgba(255,255,255,0.7)', fontWeight: 600, marginTop: '4px' }}>
              {tab === 'Pipeline' ? 'Run pipeline scripts' : tab === 'Data' ? 'Query the database' : tab === 'Config' ? 'Configure connections' : tab === 'Views' ? 'MySQL Views' : 'Pipeline'}
            </div>
          </div>

          {/* RIGHT — 3 rows: Games & More, Spirits, then bottom split */}
          <div style={{ display: 'grid', gridTemplateRows: '1fr 1fr 1fr', gap: '3px' }}>

            {/* TOP — Games & More / Data */}
            <SmashPanel label="Games & More" icon="📊" color="#1a7acc" sublabel="Query data"
              active={tab === 'Data'} onClick={() => setTab('Data')} />

            {/* MIDDLE — Spirits / Config */}
            <SmashPanel label="Spirits" icon="⚙️" color="#2a9a2a" sublabel="Configure"
              active={tab === 'Config'} onClick={() => setTab('Config')} />

            {/* BOTTOM — split into Online + Vault */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '3px' }}>
              <SmashPanel label="Online" icon="🌐" color="#d4820a" sublabel="Pipeline"
                active={tab === 'Pipeline'} onClick={() => setTab('Pipeline')} />
              <SmashPanel label="Vault" icon="👁️" color="#8a2be2" sublabel="MySQL Views"
                active={tab === 'Views'} onClick={() => setTab('Views')} />
            </div>
          </div>
        </div>

        {/* Right sidebar — like Smash's right nav icons */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '3px', padding: '3px', background: '#0a0a0a' }}>
          {[
            { key: 'Pipeline', icon: '⚔️', label: 'SMASH',    color: '#cc1a1a' },
            { key: 'Data',     icon: '📊', label: 'DATA',     color: '#1a7acc' },
            { key: 'Config',   icon: '⚙️', label: 'CONFIG',   color: '#2a9a2a' },
            { key: 'Views',    icon: '👁️', label: 'VIEWS',    color: '#8a2be2' },
          ].map(t => (
            <div key={t.key} onClick={() => setTab(t.key)} style={{
              background: tab === t.key ? t.color : '#1a1a1a',
              border: tab === t.key ? `2px solid #fff` : '2px solid #2a2a2a',
              padding: '12px 10px',
              cursor: 'pointer',
              display: 'flex', alignItems: 'center', gap: '10px',
              transition: 'all 0.1s',
              flex: 1,
            }}>
              <span style={{ fontSize: '1.4rem' }}>{t.icon}</span>
              <span style={{ fontFamily: "'Russo One'", fontSize: '0.7rem', color: tab === t.key ? '#fff' : '#888', letterSpacing: '0.1em' }}>{t.label}</span>
            </div>
          ))}

          {/* Clock / version */}
          <div style={{ background: '#111', border: '1px solid #222', padding: '10px', textAlign: 'center', marginTop: 'auto' }}>
            <div style={{ fontFamily: "'Russo One'", fontSize: '0.65rem', color: '#555', letterSpacing: '0.1em' }}>v1.0 ULTIMATE</div>
          </div>
        </div>
      </div>

      {/* ── Hint bar ── */}
      <div style={{ background: '#0d0d0d', borderTop: '2px solid #222', borderBottom: '2px solid #222', padding: '7px 20px', textAlign: 'center' }}>
        <span style={{ fontFamily: "'Barlow Condensed'", fontSize: '0.85rem', color: '#666', fontWeight: 600, letterSpacing: '0.05em', fontStyle: 'italic' }}>
          A great place to get started!
        </span>
      </div>

      {/* ── Content area ── */}
      <div style={{ flex: 1, padding: '24px 28px', maxWidth: '1100px', width: '100%' }}>
        {tab === 'Pipeline' && <PipelineTab />}
        {tab === 'Data'     && <DataTab />}
        {tab === 'Config'   && <ConfigTab />}
        {tab === 'Views'    && <ViewsTab />}
      </div>
    </div>
  );
}
