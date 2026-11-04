import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar.jsx';
import MapView from './components/MapView.jsx';
import AlgorithmLab from './components/AlgorithmLab.jsx';
import Dashboard from './components/Dashboard.jsx';
import PpiDocs from './components/PpiDocs.jsx';

export default function App() {
  const [activeTab, setActiveTab] = useState(() => {
    if (typeof window !== 'undefined') {
      const hash = window.location.hash.replace('#', '');
      if (['map', 'lab', 'dashboard', 'docs'].includes(hash)) {
        return hash;
      }
    }
    return 'map';
  });

  useEffect(() => {
    const onHashChange = () => {
      const hash = window.location.hash.replace('#', '');
      if (['map', 'lab', 'dashboard', 'docs'].includes(hash)) {
        setActiveTab(hash);
      }
    };
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    window.location.hash = tab;
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: 'var(--c-bg)',
        color: 'var(--c-text)',
        fontFamily: "'Inter', sans-serif",
      }}
    >
      {/* Barra de Navegación AburráSegura — Urban Safety Intelligence */}
      <Navbar activeTab={activeTab} setActiveTab={handleTabChange} />

      {/* Vista Activa */}
      <main style={{ flex: 1, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
        {activeTab === 'map' && <MapView />}
        {activeTab === 'lab' && <AlgorithmLab />}
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'docs' && <PpiDocs />}
      </main>

      {/* Footer solo visible en módulos de contenido analítico (no en el mapa a pantalla completa) */}
      {activeTab !== 'map' && (
        <footer className="app-footer">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <strong>AburráSegura — Urban Safety Intelligence</strong>
            <span>&bull;</span>
            <span>Tecnológico de Antioquia &mdash; Facultad de Ingeniería (2026)</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <span>Proyecto Pedagógico Integrador (PPI)</span>
            <span>&bull;</span>
            <span>Análisis y Complejidad de Algoritmos</span>
          </div>
        </footer>
      )}
    </div>
  );
}
