import React, { useState } from 'react';
import {
  Database,
  Cpu,
  Route,
  ShieldCheck,
  CheckCircle2,
  Clock,
  AlertCircle,
  FileText,
  Search,
  ExternalLink,
  ChevronDown,
  ChevronRight,
  Code2,
  GitBranch,
} from 'lucide-react';

export default function PpiDocs() {
  const [expandedReq, setExpandedReq] = useState('R1');
  const [filterCategory, setFilterCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  const ppiGroups = [
    {
      categoryId: 'data',
      categoryName: '1. Ingesta y Limpieza de Datos Geoespaciales',
      icon: Database,
      items: [
        {
          id: 'R1',
          name: 'Gestión Documental y Versionamiento',
          status: 'Aprobado',
          summary: 'Informe técnico bajo norma APA 7ma ed. con trazabilidad git, bitácoras y ADRs.',
          acceptanceCriteria:
            'Repositorio con control de versiones Git, registro de arquitectura documental y estructura técnica reproducible.',
          technicalEvidence:
            'Carpeta vault/ con notas Obsidian, diagramas Mermaid y especificaciones de diseño algorítmico.',
          files: ['vault/MOC.md', 'diagramas/arquitectura.mmd'],
        },
        {
          id: 'R2',
          name: 'Pipeline de Datos MEData y Bounding Box',
          status: 'Aprobado',
          summary: 'Extracción de 251.150 siniestros reales con filtrado en Bounding Box metropolitano de Medellín.',
          acceptanceCriteria:
            'Limpieza geoespacial estricta: latitud [6.15, 6.38], longitud [-75.68, -75.48], eliminación de nulos e imputación de severidades.',
          technicalEvidence:
            'Base de datos SQLite optimizada en data/sqlite/incidents.db y consultas de agregación en app/services/data_service.py.',
          files: ['app/services/data_service.py', 'data/sqlite/incidents.db'],
        },
      ],
    },
    {
      categoryId: 'algorithms',
      categoryName: '2. Algoritmos Clásicos y Estructuras de Datos Avanzadas',
      icon: Cpu,
      items: [
        {
          id: 'R3',
          name: 'Ordenamiento Masivo (Divide & Conquer)',
          status: 'Aprobado',
          summary: 'Implementación desde cero de Merge Sort, Quick Sort, Heap Sort y Counting Sort probados de 1K a 1M.',
          acceptanceCriteria:
            'Algoritmos implementados sin librerías externas de ordenamiento. Telemetría empírica O(n log n) verificable.',
          technicalEvidence:
            'Módulo app/algorithms/sorting.py con suite de pruebas automáticas en tests/test_sorting.py.',
          files: ['app/algorithms/sorting.py', 'tests/test_sorting.py'],
        },
        {
          id: 'R4',
          name: 'Indexación Espacial 2D con KD-Tree',
          status: 'Aprobado',
          summary: 'Búsqueda de vecinos próximos k-NN geodésica logrando speedups de más de 3.000x sobre escaneo lineal.',
          acceptanceCriteria:
            'Construcción en O(n log n) y consulta en O(log n) euclidiana/haversine sobre los vértices viales.',
          technicalEvidence:
            'Módulo app/algorithms/spatial_kdtree.py con pruebas de exactitud k-NN en tests/test_spatial_kdtree.py.',
          files: ['app/algorithms/spatial_kdtree.py', 'tests/test_spatial_kdtree.py'],
        },
      ],
    },
    {
      categoryId: 'routing',
      categoryName: '3. Inteligencia Espacial y Teoría de Grafos',
      icon: Route,
      items: [
        {
          id: 'R5',
          name: 'Clustering Geodésico con DBSCAN',
          status: 'Aprobado',
          summary: 'Identificación de puntos críticos (hotspots) de siniestralidad con ε=150m y densidad mínima.',
          acceptanceCriteria:
            'Agrupamiento geodésico no supervisado que identifique clústeres densos de accidentalidad y filtre ruido.',
          technicalEvidence:
            'Módulo app/algorithms/clustering_dbscan.py y endpoint REST /api/v1/clusters/dbscan.',
          files: ['app/algorithms/clustering_dbscan.py', 'app/api/v1/clusters.py'],
        },
        {
          id: 'R6',
          name: 'Enrutamiento Multiobjetivo en Grafos',
          status: 'Aprobado',
          summary: 'Dijkstra y A* balanceando distancia euclidiana y riesgo vial acumulado (-80% a -90% exposición).',
          acceptanceCriteria:
            'Cálculo simultáneo de ruta más corta vs ruta más segura mediante combinación lineal de pesos (alpha distancia, beta riesgo).',
          technicalEvidence:
            'Módulo app/algorithms/graph_routing.py, endpoint /api/v1/routing/calculate y test tests/test_routing.py.',
          files: ['app/algorithms/graph_routing.py', 'app/api/v1/routing.py'],
        },
      ],
    },
    {
      categoryId: 'platform',
      categoryName: '4. Plataforma, Calidad y Memoria del Proyecto',
      icon: ShieldCheck,
      items: [
        {
          id: 'R7',
          name: 'Backend Modular FastAPI REST',
          status: 'Aprobado',
          summary: 'API REST asíncrona con contratos OpenAPI 3.0 y endpoints de telemetría de CPU en nanosegundos.',
          acceptanceCriteria:
            'Esquemas Pydantic v2 estrictos, documentación Swagger interactiva en /docs y soporte CORS total.',
          technicalEvidence:
            'Estructura modular en app/api/v1/* con validaciones de tipos en app/models/schemas.py.',
          files: ['app/main.py', 'app/models/schemas.py'],
        },
        {
          id: 'R8',
          name: 'Frontend React & Leaflet Inmersivo',
          status: 'Aprobado',
          summary: 'Visualizador cartográfico con mapa neutro de alto contraste, capas de densidad e inspector contextual.',
          acceptanceCriteria:
            'SPA interactiva con Leaflet, identidad AburráSegura Urban Safety Intelligence, diseño responsivo y sin elementos superpuestos.',
          files: ['frontend/src/components/MapView.jsx', 'frontend/src/components/AlgorithmLab.jsx'],
        },
        {
          id: 'R9',
          name: 'Aseguramiento de Calidad con Pytest',
          status: 'Aprobado',
          summary: '15+ pruebas automatizadas de regresión algorítmica, validación de cotas y tolerancia cero a errores.',
          acceptanceCriteria:
            '100% de tests unitarios pasando en suite de pytest, probando casos normales y extremos de grafos y árboles.',
          technicalEvidence:
            'Suite en carpeta tests/ ejecutada con éxito mediante pytest.',
          files: ['tests/test_routing.py', 'tests/test_sorting.py', 'tests/test_clustering_dbscan.py'],
        },
        {
          id: 'R10',
          name: 'Bóveda de Conocimiento Obsidian',
          status: 'Aprobado',
          summary: 'Memoria técnica interconectada con mapas de contenido (MOCs), demostraciones matemáticas y código.',
          acceptanceCriteria:
            'Red hipertextual de conocimiento con demostraciones formales de cotas asintóticas e inventario técnico.',
          technicalEvidence:
            'Carpeta vault/ con enlaces bidireccionales y fórmulas LaTeX renderizables.',
          files: ['vault/'],
        },
      ],
    },
  ];

  // Filtro de requerimientos
  const filteredGroups = ppiGroups
    .filter((g) => filterCategory === 'all' || g.categoryId === filterCategory)
    .map((g) => ({
      ...g,
      items: g.items.filter((item) => {
        if (!searchQuery.trim()) return true;
        const q = searchQuery.toLowerCase();
        return (
          item.id.toLowerCase().includes(q) ||
          item.name.toLowerCase().includes(q) ||
          item.summary.toLowerCase().includes(q)
        );
      }),
    }))
    .filter((g) => g.items.length > 0);

  return (
    <div
      style={{
        maxWidth: '1280px',
        margin: '0 auto',
        padding: '24px 20px',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
      }}
      className="animate-fade-in"
    >
      {/* Cabecera Técnica */}
      <div
        className="card-surface"
        style={{
          padding: '22px 26px',
          borderLeft: '4px solid var(--c-petrol)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '16px',
        }}
      >
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
            <span
              style={{
                fontSize: '11px',
                fontWeight: 700,
                color: 'var(--c-teal-700)',
                backgroundColor: 'var(--c-teal-soft)',
                padding: '3px 9px',
                borderRadius: '6px',
                letterSpacing: '0.04em',
                textTransform: 'uppercase',
              }}
            >
              Documentación Oficial del Proyecto
            </span>
            <span style={{ fontSize: '12px', color: 'var(--c-text-2)' }}>
              8vo Semestre &bull; Tecnológico de Antioquia 2026
            </span>
          </div>

          <h1 style={{ margin: 0, fontSize: '22px', fontWeight: 800, color: 'var(--c-text)', letterSpacing: '-0.02em' }}>
            Ficha Técnica PPI &bull; Matriz de Requerimientos R1 a R10
          </h1>
          <p style={{ margin: '4px 0 0 0', fontSize: '13px', color: 'var(--c-text-2)', maxWidth: '820px', lineHeight: 1.45 }}>
            Trazabilidad de criterios de aceptación y evidencia técnica demostrable para la evaluación del Proyecto Pedagógico Integrador.
          </p>
        </div>

        {/* Resumen Compacto de Cumplimiento */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            backgroundColor: 'var(--c-route-safe-soft)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            padding: '10px 16px',
            borderRadius: '10px',
          }}
        >
          <CheckCircle2 size={24} color="var(--c-route-safe)" />
          <div>
            <div style={{ fontSize: '11px', color: 'var(--c-text-2)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Estado General
            </div>
            <div style={{ fontSize: '15px', fontWeight: 800, color: '#047857', fontFamily: 'var(--font-mono)' }}>
              10 / 10 Aprobados (100%)
            </div>
          </div>
        </div>
      </div>

      {/* Controles de Filtrado Rápido */}
      <div
        className="card-surface"
        style={{
          padding: '14px 20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '14px',
        }}
      >
        {/* Filtros por Categoría */}
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {[
            { id: 'all', label: 'Todos (R1–R10)' },
            { id: 'data', label: 'Ingesta de Datos' },
            { id: 'algorithms', label: 'Algoritmos & KD-Tree' },
            { id: 'routing', label: 'DBSCAN & Grafos' },
            { id: 'platform', label: 'Plataforma & QA' },
          ].map((cat) => {
            const active = filterCategory === cat.id;
            return (
              <button
                key={cat.id}
                onClick={() => setFilterCategory(cat.id)}
                style={{
                  padding: '6px 13px',
                  borderRadius: '7px',
                  fontSize: '12px',
                  fontWeight: active ? 700 : 500,
                  backgroundColor: active ? 'var(--c-petrol)' : 'var(--c-surface-2)',
                  color: active ? '#ffffff' : 'var(--c-text)',
                  border: `1px solid ${active ? 'var(--c-petrol)' : 'var(--c-border)'}`,
                  boxShadow: active ? 'var(--sh-1)' : 'none',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                }}
              >
                {cat.label}
              </button>
            );
          })}
        </div>

        {/* Buscador de requerimientos */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            backgroundColor: 'var(--c-surface-2)',
            padding: '6px 12px',
            borderRadius: '8px',
            border: '1px solid var(--c-border)',
          }}
        >
          <Search size={14} color="var(--c-text-2)" />
          <input
            type="text"
            placeholder="Buscar por ID o palabra clave..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{
              backgroundColor: 'transparent',
              border: 'none',
              color: 'var(--c-text)',
              fontSize: '12px',
              outline: 'none',
              width: '200px',
            }}
          />
        </div>
      </div>

      {/* Lista de Requerimientos en Acordeón Técnico */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {filteredGroups.map((group, gIdx) => {
          const GroupIcon = group.icon;
          return (
            <div key={gIdx} className="card-surface" style={{ padding: '20px 22px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
                <div
                  style={{
                    width: '32px',
                    height: '32px',
                    borderRadius: '8px',
                    backgroundColor: 'rgba(16, 42, 67, 0.08)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'var(--c-petrol)',
                  }}
                >
                  <GroupIcon size={16} />
                </div>
                <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 700, color: 'var(--c-text)' }}>
                  {group.categoryName}
                </h3>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {group.items.map((item) => {
                  const isExpanded = expandedReq === item.id;
                  return (
                    <div
                      key={item.id}
                      style={{
                        borderRadius: '9px',
                        backgroundColor: isExpanded ? 'var(--c-surface-3)' : 'var(--c-surface)',
                        border: `1px solid ${isExpanded ? 'var(--c-teal)' : 'var(--c-border)'}`,
                        overflow: 'hidden',
                        transition: 'all 0.18s ease',
                      }}
                    >
                      {/* Cabecera del ítem */}
                      <div
                        onClick={() => setExpandedReq(isExpanded ? null : item.id)}
                        style={{
                          padding: '13px 16px',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between',
                          cursor: 'pointer',
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                          <span
                            style={{
                              fontSize: '11.5px',
                              fontWeight: 800,
                              fontFamily: 'var(--font-mono)',
                              color: 'var(--c-route-short-ink)',
                              backgroundColor: 'var(--c-route-short-soft)',
                              padding: '2px 8px',
                              borderRadius: '5px',
                            }}
                          >
                            {item.id}
                          </span>
                          <strong style={{ fontSize: '13.5px', color: 'var(--c-text)' }}>{item.name}</strong>
                        </div>

                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                          <span
                            style={{
                              fontSize: '11px',
                              fontWeight: 700,
                              color: '#047857',
                              backgroundColor: 'var(--c-route-safe-soft)',
                              padding: '3px 9px',
                              borderRadius: '999px',
                              display: 'flex',
                              alignItems: 'center',
                              gap: '5px',
                            }}
                          >
                            <CheckCircle2 size={12} /> {item.status}
                          </span>
                          <ChevronDown
                            size={15}
                            color="var(--c-text-2)"
                            style={{
                              transform: isExpanded ? 'rotate(180deg)' : 'none',
                              transition: 'transform 0.2s ease',
                            }}
                          />
                        </div>
                      </div>

                      {/* Contenido expandido con evidencia y criterios */}
                      {isExpanded && (
                        <div
                          className="animate-fade-in"
                          style={{
                            padding: '0 16px 16px 16px',
                            borderTop: '1px solid var(--c-border)',
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '12px',
                            paddingTop: '12px',
                          }}
                        >
                          <p style={{ margin: 0, fontSize: '12.5px', color: 'var(--c-text)', lineHeight: 1.55 }}>
                            {item.summary}
                          </p>

                          <div
                            style={{
                              backgroundColor: 'var(--c-surface)',
                              padding: '12px 14px',
                              borderRadius: '8px',
                              border: '1px solid var(--c-border)',
                              display: 'flex',
                              flexDirection: 'column',
                              gap: '8px',
                            }}
                          >
                            <div style={{ fontSize: '11.5px', color: 'var(--c-text-2)', lineHeight: 1.45 }}>
                              <strong style={{ color: 'var(--c-text)' }}>Criterio de Aceptación:</strong>{' '}
                              {item.acceptanceCriteria}
                            </div>

                            {item.technicalEvidence && (
                              <div style={{ fontSize: '11.5px', color: 'var(--c-text-2)', lineHeight: 1.45 }}>
                                <strong style={{ color: 'var(--c-route-short-ink)' }}>Evidencia Técnica:</strong>{' '}
                                {item.technicalEvidence}
                              </div>
                            )}

                            {item.files && (
                              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap', marginTop: '4px' }}>
                                <span style={{ fontSize: '11px', color: 'var(--c-text-2)', fontWeight: 600 }}>Archivos asociados:</span>
                                {item.files.map((f, fIdx) => (
                                  <span
                                    key={fIdx}
                                    style={{
                                      fontSize: '11px',
                                      fontFamily: 'var(--font-mono)',
                                      color: 'var(--c-petrol)',
                                      backgroundColor: 'var(--c-surface-2)',
                                      padding: '2px 8px',
                                      borderRadius: '5px',
                                      border: '1px solid var(--c-border)',
                                    }}
                                  >
                                    {f}
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
