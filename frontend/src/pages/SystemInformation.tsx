import React, { useState, useEffect } from 'react';
import { Cpu, HardDrive, Terminal } from 'lucide-react';

const API_URL = 'http://localhost:8000';

export default function SystemInformation() {
  const [sysInfo, setSysInfo] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_URL}/system`)
      .then(res => res.json())
      .then(d => {
        setSysInfo(d);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div style={{ color: 'var(--muted)', textAlign: 'center', padding: '40px' }}>Loading system info...</div>;

  return (
    <>
      <div className="panel-header">
        <h1 className="panel-title">System Information</h1>
        <div className="panel-desc">Hardware and environment details running UrbanGen AI.</div>
      </div>

      <div className="grid-2">
        {/* CPU & Memory */}
        <div className="card">
          <div className="card-title">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Cpu size={18} /> CPU & Memory
            </div>
          </div>
          <div style={{ margin: '15px 0' }}>
            <div className="metric" style={{ marginBottom: '10px' }}>
              <span className="metric-label">Processor</span>
              <span className="metric-value" style={{ fontSize: '1rem' }}>{sysInfo?.cpu}</span>
            </div>
            <div className="metric">
              <span className="metric-label">System RAM</span>
              <span className="metric-value" style={{ fontSize: '1.2rem' }}>{sysInfo?.ram}</span>
            </div>
          </div>
        </div>

        {/* GPU & CUDA */}
        <div className="card">
          <div className="card-title">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <HardDrive size={18} /> GPU Compute
            </div>
          </div>
          <div style={{ margin: '15px 0' }}>
            <div className="metric" style={{ marginBottom: '10px' }}>
              <span className="metric-label">Graphics Card</span>
              <span className="metric-value" style={{ fontSize: '1rem' }}>{sysInfo?.gpu}</span>
            </div>
            <div className="metric">
              <span className="metric-label">CUDA Version</span>
              <span className="metric-value" style={{ fontSize: '1.2rem' }}>{sysInfo?.cuda}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div className="card" style={{ marginTop: '30px' }}>
        <div className="card-title">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Terminal size={18} /> Software Environment
          </div>
        </div>
        <div style={{ margin: '15px 0', display: 'flex', gap: '40px' }}>
          <div className="metric">
            <span className="metric-label">OS</span>
            <span className="metric-value" style={{ fontSize: '1rem' }}>{sysInfo?.os}</span>
          </div>
          <div className="metric">
            <span className="metric-label">PyTorch Version</span>
            <span className="metric-value" style={{ fontSize: '1rem' }}>{sysInfo?.pytorch}</span>
          </div>
        </div>
      </div>
    </>
  );
}
