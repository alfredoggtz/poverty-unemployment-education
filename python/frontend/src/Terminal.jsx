import { useEffect, useRef } from 'react';

export default function Terminal({ lines, running }) {
  const bottomRef = useRef(null);
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [lines]);

  return (
    <div style={{
      background: '#0a0a0a',
      border: '2px solid #333',
      borderTop: '3px solid var(--gold)',
      padding: '14px 16px',
      height: '240px',
      overflowY: 'auto',
      fontFamily: "'Share Tech Mono', monospace",
      fontSize: '0.78rem',
      borderRadius: '4px',
    }}>
      <div style={{ color: 'var(--gold)', marginBottom: '8px', fontSize: '0.65rem', letterSpacing: '0.15em', fontFamily: "'Russo One'" }}>
        ▶ BATTLE LOG — PIPELINE ONLINE
      </div>
      {lines.length === 0 && <span style={{ color: '#555' }}>3... 2... 1... GO!</span>}
      {lines.map((line, i) => (
        <div key={i} style={{
          color: line.includes('[ERROR]') ? 'var(--err)' : line.includes('[OK]') ? 'var(--ok)' : '#ccc',
          lineHeight: '1.7',
        }}>
          <span style={{ color: 'var(--red)', userSelect: 'none' }}>▶ </span>{line}
        </div>
      ))}
      {running && <div style={{ color: 'var(--gold)', fontWeight: 700, animation: 'pulse-dot 0.8s infinite' }}>▶ EXECUTING...</div>}
      <div ref={bottomRef} />
    </div>
  );
}
