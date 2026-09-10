import { useState, useEffect } from 'react';
import { Database, AlertCircle, CheckCircle2 } from 'lucide-react';

const API_URL = 'http://localhost:8000';

export default function DatasetExplorer() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_URL}/datasets`)
      .then(res => res.json())
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div style={{ color: 'var(--muted)', textAlign: 'center', padding: '40px' }}>Loading dataset info...</div>;

  return (
    <>
      <div className="panel-header">
        <h1 className="panel-title">Dataset Explorer</h1>
        <div className="panel-desc">Explore the datasets used for training models in UrbanGen AI.</div>
      </div>

      <div className="grid-2">
        {/* Pune Datasets */}
        <div className="card">
          <div className="card-title">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Database size={18} /> Pune Urban Datasets
            </div>
            {data?.pune_datasets?.exists ? 
              <span style={{ color: 'var(--success)', display: 'flex', alignItems: 'center', gap: '4px' }}><CheckCircle2 size={16} /> Available</span> :
              <span style={{ color: '#FF5252', display: 'flex', alignItems: 'center', gap: '4px' }}><AlertCircle size={16} /> Missing</span>
            }
          </div>
          <div style={{ margin: '15px 0' }}>
            <div style={{ color: 'var(--muted)', fontSize: '0.9rem', marginBottom: '10px' }}>
              Curated Sentinel-2 and WorldCover data for Pune City.
            </div>
            <div className="metric" style={{ marginBottom: '10px' }}>
              <span className="metric-label">Location</span>
              <span className="metric-value" style={{ fontSize: '1rem' }}>{data?.pune_datasets?.path}</span>
            </div>
            <div className="metric">
              <span className="metric-label">Files Count</span>
              <span className="metric-value" style={{ fontSize: '1.2rem' }}>{data?.pune_datasets?.files} files</span>
            </div>
          </div>
        </div>

        {/* UCMerced Datasets */}
        <div className="card">
          <div className="card-title">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Database size={18} /> UCMerced LandUse
            </div>
            {data?.ucmerced?.exists ? 
              <span style={{ color: 'var(--success)', display: 'flex', alignItems: 'center', gap: '4px' }}><CheckCircle2 size={16} /> Available</span> :
              <span style={{ color: '#FF5252', display: 'flex', alignItems: 'center', gap: '4px' }}><AlertCircle size={16} /> Missing</span>
            }
          </div>
          <div style={{ margin: '15px 0' }}>
            <div style={{ color: 'var(--muted)', fontSize: '0.9rem', marginBottom: '10px' }}>
              Standard land use classification dataset (21 classes).
            </div>
            <div className="metric" style={{ marginBottom: '10px' }}>
              <span className="metric-label">Location</span>
              <span className="metric-value" style={{ fontSize: '1rem' }}>{data?.ucmerced?.path}</span>
            </div>
            <div className="metric">
              <span className="metric-label">Classes</span>
              <span className="metric-value" style={{ fontSize: '1.2rem' }}>{data?.ucmerced?.classes} classes</span>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
