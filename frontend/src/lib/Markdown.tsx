import React from 'react';

// Minimal, dependency-free Markdown renderer — enough for the governance
// docs (headings, paragraphs, lists, tables, rules, inline bold/code/links).

function inline(text: string): React.ReactNode[] {
  const nodes: React.ReactNode[] = [];
  const re = /(\*\*([^*]+)\*\*|`([^`]+)`|\[([^\]]+)\]\(([^)]+)\))/g;
  let last = 0;
  let m: RegExpExecArray | null;
  let k = 0;
  while ((m = re.exec(text))) {
    if (m.index > last) nodes.push(text.slice(last, m.index));
    if (m[2] !== undefined) nodes.push(<strong key={k++}>{m[2]}</strong>);
    else if (m[3] !== undefined) nodes.push(<code key={k++} style={{ background: 'var(--bg)', padding: '1px 5px', borderRadius: 3, fontFamily: 'var(--font-mono)', fontSize: '0.85em' }}>{m[3]}</code>);
    else if (m[4] !== undefined) nodes.push(<a key={k++} href={m[5]} style={{ color: 'var(--accent)' }}>{m[4]}</a>);
    last = m.index + m[0].length;
  }
  if (last < text.length) nodes.push(text.slice(last));
  return nodes;
}

function splitRow(line: string): string[] {
  return line.replace(/^\||\|$/g, '').split('|').map(c => c.trim());
}

export default function Markdown({ text }: { text: string }) {
  const lines = text.replace(/\r\n/g, '\n').split('\n');
  const out: React.ReactNode[] = [];
  let i = 0;
  let key = 0;
  let list: string[] = [];

  const flushList = () => {
    if (list.length) {
      out.push(
        <ul key={key++} style={{ margin: '10px 0 16px', paddingLeft: 22, lineHeight: 1.6 }}>
          {list.map((li, idx) => <li key={idx}>{inline(li)}</li>)}
        </ul>
      );
      list = [];
    }
  };

  while (i < lines.length) {
    const line = lines[i];

    if (/^\s*[-*]\s+/.test(line)) { list.push(line.replace(/^\s*[-*]\s+/, '')); i++; continue; }
    flushList();

    if (line.trim() === '') { i++; continue; }

    if (/^#{1,6}\s/.test(line)) {
      const level = line.match(/^#+/)![0].length;
      const content = line.replace(/^#+\s/, '');
      const sizes = ['1.6rem', '1.3rem', '1.12rem', '1rem', '0.95rem', '0.9rem'];
      out.push(
        <div key={key++} style={{ fontSize: sizes[level - 1], fontWeight: 600, margin: level <= 2 ? '26px 0 12px' : '18px 0 8px', color: level <= 2 ? 'var(--accent)' : 'var(--accent2)' }}>
          {inline(content)}
        </div>
      );
      i++; continue;
    }

    if (/^---+$/.test(line.trim())) {
      out.push(<hr key={key++} style={{ border: 0, borderTop: '1px solid var(--border)', margin: '20px 0' }} />);
      i++; continue;
    }

    // table: header row followed by a separator row of dashes
    if (line.includes('|') && i + 1 < lines.length && /^\s*\|?[\s:|-]+\|[\s:|-]+$/.test(lines[i + 1])) {
      const header = splitRow(line);
      i += 2;
      const rows: string[][] = [];
      while (i < lines.length && lines[i].includes('|')) { rows.push(splitRow(lines[i])); i++; }
      out.push(
        <div key={key++} style={{ overflowX: 'auto', margin: '12px 0 20px' }}>
          <table style={{ borderCollapse: 'collapse', width: '100%', fontSize: '0.88rem' }}>
            <thead>
              <tr>{header.map((h, x) => <th key={x} style={{ textAlign: 'left', padding: '8px 10px', borderBottom: '1px solid var(--accent2)', color: 'var(--accent2)' }}>{inline(h)}</th>)}</tr>
            </thead>
            <tbody>
              {rows.map((r, y) => (
                <tr key={y}>{r.map((c, x) => <td key={x} style={{ padding: '8px 10px', borderBottom: '1px solid var(--border)', verticalAlign: 'top' }}>{inline(c)}</td>)}</tr>
              ))}
            </tbody>
          </table>
        </div>
      );
      continue;
    }

    out.push(<p key={key++} style={{ margin: '0 0 14px', lineHeight: 1.65 }}>{inline(line)}</p>);
    i++;
  }
  flushList();

  return <div style={{ color: 'var(--text)' }}>{out}</div>;
}
