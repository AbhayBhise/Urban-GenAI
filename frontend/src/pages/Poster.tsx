import { useState } from 'react';
import { Printer, ExternalLink, Code, Eye, Copy, Check, Sparkles, Download, Layers } from 'lucide-react';

const LATEX_POSTER_CODE = `\\documentclass[final]{beamer}
\\usepackage[orientation=portrait,size=a1,scale=1.2]{beamerposter}
\\usepackage[utf8]{inputenc}
\\usepackage{amsmath,amssymb}
\\usepackage{booktabs}
\\usepackage{tabularx}
\\usepackage{graphicx}
\\usepackage{xcolor}

\\definecolor{NavyBlue}{RGB}{2, 132, 199}
\\definecolor{DarkNavy}{RGB}{11, 25, 44}
\\definecolor{CyanAccent}{RGB}{0, 212, 255}

\\title{\\textbf{UrbanGen AI: Multi-Model Generative Framework for Satellite Imagery Processing}}
\\author{Abhay Bhise, Disha Satpute, Vaishnavi Phad, Vedant Ingle}
\\institute{Guides: Prof. Savita Mane \\& Prof. Pramod Ganjewar \\\\ Department of Computer Engineering, MIT AOE, Pune}

\\begin{document}
% Refer to docs/poster/poster.tex for full compilation code
\\end{document}`;

export default function Poster() {
  const [activeTab, setActiveTab] = useState<'visual' | 'latex'>('visual');
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(LATEX_POSTER_CODE);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handlePrint = () => {
    const iframe = document.getElementById('poster-frame') as HTMLIFrameElement;
    if (iframe && iframe.contentWindow) {
      iframe.contentWindow.focus();
      iframe.contentWindow.print();
    } else {
      window.open('/poster/index.html', '_blank')?.print();
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      {/* Top Action Header */}
      <div style={{
        background: 'var(--surface)',
        border: '1px solid var(--border)',
        borderRadius: 12,
        padding: '20px 24px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: 16,
        boxShadow: 'var(--card-shadow)'
      }}>
        <div>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 6,
            fontSize: '0.74rem',
            fontFamily: 'var(--font-mono)',
            textTransform: 'uppercase',
            letterSpacing: '0.08em',
            color: 'var(--accent)',
            background: 'var(--active-tint)',
            padding: '3px 8px',
            borderRadius: 4,
            marginBottom: 8,
            border: '1px solid var(--border)'
          }}>
            <Sparkles size={12} />
            Academic Defense · 60 Marks Capstone Poster
          </div>
          <h1 style={{
            fontSize: '1.45rem',
            fontWeight: 800,
            color: 'var(--text)',
            fontFamily: 'var(--font-display)',
            marginBottom: 4
          }}>
            UrbanGen AI — Academic Research &amp; Defense Poster
          </h1>
          <p style={{ fontSize: '0.86rem', color: 'var(--muted)', margin: 0 }}>
            Official conference &amp; department defense poster for MIT Academy of Engineering, Pune.
          </p>
        </div>

        <div style={{ display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap' }}>
          <div style={{
            display: 'flex',
            background: 'var(--bg)',
            border: '1px solid var(--border)',
            borderRadius: 6,
            padding: 3
          }}>
            <button
              onClick={() => setActiveTab('visual')}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 6,
                padding: '6px 14px',
                borderRadius: 4,
                border: 'none',
                background: activeTab === 'visual' ? 'var(--surface)' : 'transparent',
                color: activeTab === 'visual' ? 'var(--accent)' : 'var(--muted)',
                fontWeight: 600,
                fontSize: '0.82rem',
                cursor: 'pointer'
              }}
            >
              <Eye size={14} /> Visual Poster
            </button>
            <button
              onClick={() => setActiveTab('latex')}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 6,
                padding: '6px 14px',
                borderRadius: 4,
                border: 'none',
                background: activeTab === 'latex' ? 'var(--surface)' : 'transparent',
                color: activeTab === 'latex' ? 'var(--accent)' : 'var(--muted)',
                fontWeight: 600,
                fontSize: '0.82rem',
                cursor: 'pointer'
              }}
            >
              <Code size={14} /> LaTeX Code
            </button>
          </div>

          <a
            href="/poster/UrbanGen_AI_Poster_AuthentiMark.pptx"
            download="UrbanGen_AI_Poster_AuthentiMark.pptx"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 8,
              padding: '8px 16px',
              borderRadius: 6,
              background: 'linear-gradient(135deg, #059669 0%, #047857 100%)',
              color: '#ffffff',
              fontWeight: 700,
              fontSize: '0.85rem',
              textDecoration: 'none',
              cursor: 'pointer',
              boxShadow: '0 2px 8px rgba(5, 150, 105, 0.3)'
            }}
          >
            <Download size={15} /> Download Canva PPTX
          </a>

          <a
            href="/poster/project_architecture.puml"
            download="project_architecture.puml"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 8,
              padding: '8px 16px',
              borderRadius: 6,
              background: 'linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%)',
              color: '#ffffff',
              fontWeight: 700,
              fontSize: '0.85rem',
              textDecoration: 'none',
              cursor: 'pointer',
              boxShadow: '0 2px 8px rgba(124, 58, 237, 0.3)'
            }}
          >
            <Code size={15} /> Download PlantUML (.puml)
          </a>

          <button
            onClick={handlePrint}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 8,
              padding: '8px 16px',
              borderRadius: 6,
              border: 'none',
              background: 'linear-gradient(135deg, var(--accent) 0%, #0369a1 100%)',
              color: '#ffffff',
              fontWeight: 700,
              fontSize: '0.85rem',
              cursor: 'pointer',
              boxShadow: '0 2px 8px rgba(2, 132, 199, 0.3)'
            }}
          >
            <Printer size={15} /> Print / Save Single-Page PDF
          </button>

          <a
            href="/poster/index.html"
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 6,
              padding: '8px 14px',
              borderRadius: 6,
              border: '1px solid var(--border)',
              background: 'var(--surface)',
              color: 'var(--text)',
              fontWeight: 600,
              fontSize: '0.85rem',
              textDecoration: 'none',
              cursor: 'pointer'
            }}
          >
            <ExternalLink size={14} /> Fullscreen
          </a>
        </div>
      </div>

      {/* Canva Editable Guide Notice */}
      <div style={{
        background: 'var(--surface)',
        border: '1px solid var(--border)',
        borderLeft: '4px solid var(--success)',
        borderRadius: 8,
        padding: '12px 18px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: 12,
        fontSize: '0.85rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <Layers size={18} style={{ color: 'var(--success)', flexShrink: 0 }} />
          <span style={{ color: 'var(--text)' }}>
            <strong>Canva Vector Editable (AuthentiMark Layout &amp; MIT AOE Branding):</strong> To edit in Canva, download <code>UrbanGen_AI_Poster_AuthentiMark.pptx</code>, open <a href="https://canva.com" target="_blank" rel="noreferrer" style={{ color: 'var(--accent)', fontWeight: 600 }}>canva.com</a>, click <strong>Upload / Import</strong>, and drag the file. All text boxes, shapes, equations, tables, and colors will be 100% vector-editable!
          </span>
        </div>
      </div>

      {/* Main Content Area */}
      {activeTab === 'visual' ? (
        <div style={{
          background: 'var(--surface)',
          border: '1px solid var(--border)',
          borderRadius: 12,
          overflow: 'hidden',
          boxShadow: 'var(--card-shadow)',
          display: 'flex',
          flexDirection: 'column',
          height: 'calc(100vh - 230px)',
          minHeight: 700
        }}>
          <iframe
            id="poster-frame"
            src="/poster/index.html"
            title="UrbanGen AI Poster"
            style={{
              width: '100%',
              height: '100%',
              border: 'none',
              display: 'block'
            }}
          />
        </div>
      ) : (
        <div style={{
          background: 'var(--surface)',
          border: '1px solid var(--border)',
          borderRadius: 12,
          padding: 24,
          boxShadow: 'var(--card-shadow)',
          display: 'flex',
          flexDirection: 'column',
          gap: 16
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text)', margin: '0 0 4px' }}>
                LaTeX Beamer Poster Source (<code style={{ color: 'var(--accent)' }}>docs/poster/poster.tex</code>)
              </h3>
              <p style={{ fontSize: '0.82rem', color: 'var(--muted)', margin: 0 }}>
                Compiles via <code>pdflatex poster.tex</code> to generate a vector PDF poster.
              </p>
            </div>
            <button
              onClick={handleCopy}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 6,
                padding: '7px 14px',
                borderRadius: 6,
                border: '1px solid var(--border)',
                background: 'var(--bg)',
                color: 'var(--text)',
                fontWeight: 600,
                fontSize: '0.82rem',
                cursor: 'pointer'
              }}
            >
              {copied ? <Check size={14} style={{ color: 'var(--success)' }} /> : <Copy size={14} />}
              {copied ? 'Copied!' : 'Copy Code'}
            </button>
          </div>

          <pre style={{
            background: 'var(--bg)',
            border: '1px solid var(--border)',
            borderRadius: 8,
            padding: 16,
            fontFamily: 'var(--font-mono)',
            fontSize: '0.82rem',
            lineHeight: 1.5,
            color: 'var(--text)',
            overflowX: 'auto',
            maxHeight: 520
          }}>
            {LATEX_POSTER_CODE}
          </pre>
        </div>
      )}
    </div>
  );
}

