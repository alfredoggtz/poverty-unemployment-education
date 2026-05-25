import { useState } from 'react';
const PAGE_SIZE = 10;

export default function DataTable({ data }) {
  const [page, setPage] = useState(0);
  if (!data || data.length === 0)
    return <p style={{ color: '#555', fontSize: '0.9rem', marginTop: '12px', fontFamily: "'Russo One'", letterSpacing: '0.1em' }}>NO DATA FOUND</p>;

  const columns = Object.keys(data[0]);
  const totalPages = Math.ceil(data.length / PAGE_SIZE);
  const slice = data.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);

  const navBtn = (disabled, color = 'var(--red)') => ({
    background: disabled ? '#222' : color,
    border: 'none', borderRadius: '3px',
    padding: '6px 16px',
    color: disabled ? '#555' : '#fff',
    cursor: disabled ? 'not-allowed' : 'pointer',
    fontFamily: "'Russo One'", fontSize: '0.72rem', letterSpacing: '0.1em',
  });

  return (
    <div style={{ marginTop: '12px', animation: 'slide-in 0.2s ease-out' }}>
      <div style={{ overflowX: 'auto', border: '2px solid #333', borderRadius: '4px' }}>
        <table style={{ width: '100%', fontSize: '0.85rem', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: 'var(--red)' }}>
              {columns.map(col => (
                <th key={col} style={{ padding: '9px 14px', textAlign: 'left', color: '#fff', fontFamily: "'Russo One'", fontWeight: 400, letterSpacing: '0.08em', whiteSpace: 'nowrap', fontSize: '0.7rem', textTransform: 'uppercase' }}>
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {slice.map((row, i) => (
              <tr key={i} style={{ background: i % 2 === 0 ? '#1a1a1a' : '#141414', borderTop: '1px solid #2a2a2a' }}>
                {columns.map(col => (
                  <td key={col} style={{ padding: '8px 14px', whiteSpace: 'nowrap', color: '#ddd', fontFamily: "'Barlow Condensed'", fontSize: '0.95rem', fontWeight: 600 }}>
                    {row[col] != null
                      ? typeof row[col] === 'number'
                        ? Number.isInteger(row[col]) ? row[col] : row[col].toFixed(4)
                        : String(row[col])
                      : <span style={{ color: '#444' }}>—</span>}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {totalPages > 1 && (
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '10px', justifyContent: 'flex-end' }}>
          <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0} style={navBtn(page === 0)}>◀ PREV</button>
          <span style={{ color: '#666', fontSize: '0.75rem', fontFamily: "'Russo One'" }}>{page + 1} / {totalPages}</span>
          <button onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))} disabled={page === totalPages - 1} style={navBtn(page === totalPages - 1)}>NEXT ▶</button>
        </div>
      )}
    </div>
  );
}
