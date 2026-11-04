import { apiUrl } from '../api.js';
import React, { useState, useEffect } from 'react';
import {
  Navigation,
  Cpu,
  BarChart3,
  FileCode2,
  ExternalLink,
  Menu,
  X,
  Shield,
  Layers,
} from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab }) {
  const [connectionStatus, setConnectionStatus] = useState('checking'); // 'connected' | 'disconnected' | 'checking' | 'waking'
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    let isMounted = true;
    // El hosting gratuito (Hugging Face Spaces) duerme el backend; mientras no responda por primera vez, se está despertando
    let everConnected = false;
    const startedAt = Date.now();
    const checkHealth = async () => {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 3500);
        const res = await fetch(apiUrl('/health'), {
          method: 'GET',
          signal: controller.signal,
        });
        clearTimeout(timeoutId);
        everConnected = everConnected || res.ok;
        if (isMounted) {
          setConnectionStatus(res.ok ? 'connected' : 'disconnected');
        }
      } catch {
        if (isMounted) {
          setConnectionStatus(!everConnected && Date.now() - startedAt < 90000 ? 'waking' : 'disconnected');
        }
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 12000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  const tabs = [
    {
      id: 'map',
      label: 'Rutas & Mapa Seguro',
      subtitle: 'Dijkstra / A* multiobjetivo',
      icon: Navigation,
    },
    {
      id: 'lab',
      label: 'Laboratorio Algorítmico',
      subtitle: 'Telemetría empírica vs teórica',
      icon: Cpu,
    },
    {
      id: 'dashboard',
      label: 'Analítica Urbana',
      subtitle: '251k siniestros históricos',
      icon: BarChart3,
    },
    {
      id: 'docs',
      label: 'Ficha Técnica PPI',
      subtitle: 'Requisitos R1 – R10',
      icon: FileCode2,
    },
  ];

  const currentTab = tabs.find((t) => t.id === activeTab) || tabs[0];

  return (
    <header className="topbar" role="banner">
      <div className="topbar-inner">
        {/* Identidad de Marca: AburráSegura — Urban Safety Intelligence */}
        <div className="brand">
          <div className="brand-mark" aria-hidden="true">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="#14b8a6" strokeWidth="2" />
              <circle cx="12" cy="8" r="1.5" fill="#38bdf8" />
              <circle cx="8" cy="13.5" r="1.5" fill="#10b981" />
              <circle cx="16" cy="13.5" r="1.5" fill="#f59e0b" />
              <path d="M12 8L8 13.5M12 8L16 13.5M8 13.5H16" stroke="rgba(255,255,255,0.4)" strokeWidth="1.2" strokeDasharray="1.5 1.5" />
            </svg>
          </div>

          <div>
            <div className="brand-name">
              Aburrá<span>Segura</span>
            </div>
            <div className="brand-tag">
              Urban Safety Intelligence
            </div>
          </div>
        </div>

        {/* Módulo activo en vista móvil */}
        <div className="topbar-current" aria-label={`Módulo actual: ${currentTab.label}`}>
          <span style={{ opacity: 0.5 }}>/</span>
          <span>{currentTab.label}</span>
        </div>

        {/* Navegación Desktop */}
        <nav className="topnav" aria-label="Navegación principal">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className="topnav-item"
                aria-current={isActive ? 'page' : undefined}
                type="button"
              >
                <Icon size={16} aria-hidden="true" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Extremo derecho: Estado de servicios, Documentación API y Botón Móvil */}
        <div className="topbar-end">
          {/* Indicador de estado real del backend FastAPI */}
          <div
            className={`status-pill ${connectionStatus === 'connected' ? 'is-ok' : connectionStatus === 'checking' ? '' : 'is-down'}`}
            title={
              connectionStatus === 'connected'
                ? 'Motor algorítmico FastAPI sincronizado en tiempo real'
                : connectionStatus === 'checking'
                ? 'Comprobando conexión con FastAPI...'
                : connectionStatus === 'waking'
                ? 'El servidor gratuito se estaba durmiendo; la primera respuesta puede tardar hasta un minuto'
                : 'No hay conexión con el backend FastAPI'
            }
            role="status"
            aria-live="polite"
          >
            <span className="status-dot" aria-hidden="true" />
            <span className="status-text">
              {connectionStatus === 'connected'
                ? 'FastAPI Online'
                : connectionStatus === 'checking'
                ? 'Conectando...'
                : connectionStatus === 'waking'
                ? 'Despertando servidor...'
                : 'Sin conexión'}
            </span>
          </div>

          {/* Enlace directo a Swagger OpenAPI */}
          <a
            href={apiUrl('/docs')}
            target="_blank"
            rel="noreferrer"
            className="topbar-link"
            title="Ver documentación técnica de endpoints OpenAPI (Swagger)"
          >
            <span>Swagger</span>
            <ExternalLink size={12} aria-hidden="true" />
          </a>

          {/* Botón de menú responsive */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="topbar-menu-btn"
            aria-label={mobileMenuOpen ? 'Cerrar menú' : 'Abrir menú de navegación'}
            aria-expanded={mobileMenuOpen}
            type="button"
          >
            {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {/* Menú deslizante para tabletas y teléfonos */}
      {mobileMenuOpen && (
        <div className="mobile-menu" role="dialog" aria-label="Menú móvil">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id);
                  setMobileMenuOpen(false);
                }}
                aria-current={isActive ? 'page' : undefined}
                type="button"
              >
                <Icon size={18} color={isActive ? '#14b8a6' : '#a9bccf'} aria-hidden="true" />
                <div>
                  <div>{tab.label}</div>
                  <small>{tab.subtitle}</small>
                </div>
              </button>
            );
          })}
        </div>
      )}
    </header>
  );
}
