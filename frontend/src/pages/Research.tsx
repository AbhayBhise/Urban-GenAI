import { useState, useEffect } from 'react';
import type { LucideIcon } from 'lucide-react';
import {
  Compass,
  BookOpen,
  GitFork,
  Layers,
  CheckSquare,
  Activity,
  Bookmark,
  ChevronRight,
} from 'lucide-react';

import ResearchOverview from './research/ResearchOverview';
import LiteratureSurvey from './research/LiteratureSurvey';
import ResearchGap from './research/ResearchGap';
import SystemApproach from './research/SystemApproach';
import ComparisonMatrix from './research/ComparisonMatrix';
import ResearchProgress from './research/ResearchProgress';
import AcademicReferences from './research/AcademicReferences';

export type ResearchTabId = 'overview' | 'literature' | 'gap' | 'approach' | 'comparison' | 'progress' | 'references';

interface ResearchTab {
  id: ResearchTabId;
  label: string;
  subpath: string;
  icon: LucideIcon;
  badge?: string;
}

const RESEARCH_TABS: ResearchTab[] = [
  { id: 'overview', label: 'Overview & Planner Persona', subpath: '/research', icon: Compass },
  { id: 'literature', label: 'Literature Survey', subpath: '/research/literature', icon: BookOpen, badge: '7 Landmark Reviews' },
  { id: 'gap', label: 'Research Gap & Landscape', subpath: '/research/gap', icon: GitFork },
  { id: 'approach', label: 'System Approach & Models', subpath: '/research/approach', icon: Layers, badge: 'City Stack' },
  { id: 'comparison', label: 'Capability Matrix', subpath: '/research/comparison', icon: CheckSquare, badge: '16 Rows' },
  { id: 'progress', label: 'Progress & Live Metrics', subpath: '/research/progress', icon: Activity, badge: 'Verified' },
  { id: 'references', label: 'Academic References', subpath: '/research/references', icon: Bookmark, badge: 'DOIs' },
];

export default function Research() {
  // Parse initial tab from URL hash if present
  const getTabFromHash = (): ResearchTabId => {
    const hash = window.location.hash.toLowerCase();
    if (hash.includes('literature')) return 'literature';
    if (hash.includes('gap')) return 'gap';
    if (hash.includes('approach')) return 'approach';
    if (hash.includes('comparison')) return 'comparison';
    if (hash.includes('progress')) return 'progress';
    if (hash.includes('references')) return 'references';
    return 'overview';
  };

  const [activeTab, setActiveTab] = useState<ResearchTabId>(getTabFromHash());

  // Listen to hash changes for browser back/forward and deep-linking
  useEffect(() => {
    const handleHashChange = () => {
      setActiveTab(getTabFromHash());
    };
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  const handleTabChange = (tabId: ResearchTabId) => {
    setActiveTab(tabId);
    const tab = RESEARCH_TABS.find(t => t.id === tabId);
    if (tab) {
      window.location.hash = tab.subpath.replace('/', '');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '22px' }}>
      {/* Research Header Banner */}
      <div className="panel-header" style={{ marginBottom: 0 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent)', fontSize: '0.82rem', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 600, marginBottom: '6px' }}>
          <span>UrbanGen AI</span>
          <ChevronRight size={14} />
          <span>Research &amp; Innovation</span>
          <ChevronRight size={14} />
          <span style={{ color: 'var(--text)' }}>
            {RESEARCH_TABS.find(t => t.id === activeTab)?.label}
          </span>
        </div>
        <h1 className="panel-title" style={{ fontSize: '1.9rem', fontWeight: 700, letterSpacing: '-0.02em', color: '#FFF' }}>
          Research, Literature Survey &amp; Innovation
        </h1>
        <div className="panel-desc" style={{ maxWidth: '980px', fontSize: '0.94rem', lineHeight: 1.6 }}>
          Comprehensive scientific documentation, academic literature synthesis, and verified empirical metrics for the UrbanGen AI Multi-Model Generative Framework—designed as a decision-support and scenario-exploration environment for professional <strong>Urban Planners</strong>.
        </div>
      </div>

      {/* Sub-Navigation Tabs Bar */}
      <div
        style={{
          display: 'flex',
          gap: '6px',
          borderBottom: '1px solid var(--border)',
          paddingBottom: '10px',
          overflowX: 'auto',
          whiteSpace: 'nowrap',
          scrollbarWidth: 'thin',
        }}
      >
        {RESEARCH_TABS.map(tab => {
          const isActive = activeTab === tab.id;
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => handleTabChange(tab.id)}
              style={{
                background: isActive ? 'rgba(0, 212, 255, 0.12)' : 'rgba(15, 25, 35, 0.5)',
                color: isActive ? 'var(--accent)' : 'var(--text)',
                border: `1px solid ${isActive ? 'var(--accent)' : 'var(--border)'}`,
                borderRadius: '6px',
                padding: '10px 16px',
                fontSize: '0.84rem',
                fontWeight: isActive ? 600 : 500,
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                cursor: 'pointer',
                transition: 'all 0.15s ease',
                flexShrink: 0,
              }}
            >
              <Icon size={16} color={isActive ? 'var(--accent)' : 'var(--muted)'} />
              <span>{tab.label}</span>
              {tab.badge && (
                <span
                  style={{
                    background: isActive ? 'rgba(0, 212, 255, 0.25)' : 'rgba(30, 45, 64, 0.6)',
                    color: isActive ? '#FFF' : 'var(--muted)',
                    fontSize: '0.68rem',
                    padding: '2px 6px',
                    borderRadius: '4px',
                    marginLeft: '4px',
                  }}
                >
                  {tab.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Tab Body Render */}
      <div style={{ marginTop: '6px' }}>
        {activeTab === 'overview' && <ResearchOverview onNavigateTab={handleTabChange} />}
        {activeTab === 'literature' && <LiteratureSurvey />}
        {activeTab === 'gap' && <ResearchGap />}
        {activeTab === 'approach' && <SystemApproach />}
        {activeTab === 'comparison' && <ComparisonMatrix />}
        {activeTab === 'progress' && <ResearchProgress />}
        {activeTab === 'references' && <AcademicReferences />}
      </div>
    </div>
  );
}
