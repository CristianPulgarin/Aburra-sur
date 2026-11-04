import { apiUrl } from '../api.js';
import React, { useEffect, useMemo, useState } from 'react';
import {
  Activity,
  AlertTriangle,
  Calendar,
  Car,
  Clock,
  Download,
  HeartCrack,
  Layers,
  MapPin,
  RefreshCw,
  Sparkles,
  WifiOff,
  X,
} from 'lucide-react';

const SEVERITIES = [
  { id: 'ALL', label: 'Todas' },
  { id: 'SOLO DAÑOS', label: 'Solo daños', color: 'var(--c-route-safe)' },
  { id: 'CON HERIDOS', label: 'Con heridos', color: 'var(--risk-2)' },
  { id: 'CON MUERTOS', label: 'Con muertos', color: 'var(--risk-4)' },
];
const WEEKDAYS = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];
const WEEKDAYS_LONG = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'];
const MONTHS = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
const CLASS_LABELS = {
  CHOQUE: 'Choque',
  OTRO: 'Otro',
  ATROPELLO: 'Atropello',
  'CAIDA OCUPANTE': 'Caída de ocupante',
  VOLCAMIENTO: 'Volcamiento',
  INCENDIO: 'Incendio',
};

const fmt = (n) => (n ?? 0).toLocaleString('es-CO');
const pct = (part, total) => (total ? ((part / total) * 100).toFixed(1) : '0.0');

function useAnalytics(filters, reloadKey) {
  const [state, setState] = useState({ data: null, loading: true, error: null });

  useEffect(() => {
    const controller = new AbortController();
    const params = new URLSearchParams();
    if (filters.anio) params.set('anio', filters.anio);
    if (filters.gravedad) params.set('gravedad', filters.gravedad);
    if (filters.comuna) params.set('comuna', filters.comuna);

    setState((s) => ({ ...s, loading: true, error: null }));
    fetch(apiUrl(`/api/v1/incidents/analytics?${params}`), { signal: controller.signal })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => setState({ data, loading: false, error: null }))
      .catch((err) => {
        if (err.name !== 'AbortError') setState((s) => ({ ...s, loading: false, error: err.message }));
      });
    return () => controller.abort();
  }, [filters.anio, filters.gravedad, filters.comuna, reloadKey]);

  return state;
}

function Card({ title, subtitle, icon: Icon, iconColor = 'var(--c-petrol)', action, children, style }) {
  return (
    <section className="card-surface" style={{ padding: '20px 22px', minWidth: 0, ...style }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12, marginBottom: 16 }}>
        <div>
          <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700, color: 'var(--c-text)' }}>{title}</h3>
          {subtitle && <p style={{ margin: '3px 0 0', fontSize: 12, color: 'var(--c-text-2)' }}>{subtitle}</p>}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          {action}
          {Icon && (
            <div style={{ width: 30, height: 30, borderRadius: 8, background: 'var(--c-surface-2)', display: 'grid', placeItems: 'center', flexShrink: 0 }}>
              <Icon size={15} color={iconColor} />
            </div>
          )}
        </div>
      </header>
      {children}
    </section>
  );
}

function Kpi({ label, value, hint, icon: Icon, color, active, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={!onClick}
      className="card-surface"
      style={{
        padding: '16px 20px',
        textAlign: 'left',
        cursor: onClick ? 'pointer' : 'default',
        border: active ? `2px solid ${color}` : '1px solid var(--c-border)',
        font: 'inherit',
        color: 'inherit',
        transition: 'border-color 0.16s ease',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: 11.5, color: 'var(--c-text-2)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
          {label}
        </span>
        <Icon size={16} color={color} />
      </div>
      <div style={{ fontSize: 26, fontWeight: 800, marginTop: 8, fontFamily: 'var(--font-mono)', lineHeight: 1.1 }}>{value}</div>
      <div style={{ fontSize: 11.5, color: 'var(--c-text-2)', marginTop: 4 }}>{hint}</div>
    </button>
  );
}

// Gráfico de columnas en SVG. `highlight` marca la columna activa; `onSelect` la vuelve clicable.
function ColumnChart({ values, labels, color = 'var(--c-petrol-500)', highlight, onSelect, height = 150, labelEvery = 1 }) {
  const [hover, setHover] = useState(null);
  const max = Math.max(1, ...values);
  const n = values.length;
  const w = 100 / n;
  const shown = hover ?? highlight;

  return (
    <div>
      <div style={{ height: 18, fontSize: 12, fontFamily: 'var(--font-mono)', color: 'var(--c-text-2)' }}>
        {shown != null && (
          <>
            <strong style={{ color: 'var(--c-text)' }}>{labels[shown]}</strong> · {fmt(values[shown])} siniestros
          </>
        )}
      </div>
      <svg viewBox={`0 0 100 ${height}`} preserveAspectRatio="none" style={{ width: '100%', height, display: 'block' }} role="img">
        {values.map((v, i) => {
          const h = (v / max) * (height - 4);
          const active = i === highlight || i === hover;
          return (
            <rect
              key={i}
              x={i * w + w * 0.12}
              y={height - h}
              width={w * 0.76}
              height={Math.max(h, 0.5)}
              rx={0.6}
              fill={active ? 'var(--c-teal)' : color}
              opacity={highlight != null && !active ? 0.45 : 1}
              style={{ cursor: onSelect ? 'pointer' : 'default', transition: 'opacity 0.15s' }}
              onMouseEnter={() => setHover(i)}
              onMouseLeave={() => setHover(null)}
              onClick={onSelect ? () => onSelect(i) : undefined}
            >
              <title>{`${labels[i]}: ${fmt(v)}`}</title>
            </rect>
          );
        })}
      </svg>
      <div style={{ display: 'flex', marginTop: 6 }}>
        {labels.map((l, i) => (
          <span
            key={i}
            style={{ width: `${w}%`, textAlign: 'center', fontSize: 10.5, color: 'var(--c-text-2)', fontFamily: 'var(--font-mono)', overflow: 'hidden' }}
          >
            {i % labelEvery === 0 ? l : ''}
          </span>
        ))}
      </div>
    </div>
  );
}

function BarList({ items, selected, onSelect, color = 'var(--c-petrol-600)', maxHeight }) {
  const max = Math.max(1, ...items.map((i) => i.value));
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 6, maxHeight, overflowY: maxHeight ? 'auto' : 'visible', paddingRight: maxHeight ? 4 : 0 }}>
      {items.map((it, idx) => {
        const active = selected === it.key;
        return (
          <div
            key={it.key}
            onClick={onSelect ? () => onSelect(active ? null : it.key) : undefined}
            style={{
              padding: '5px 8px',
              borderRadius: 7,
              cursor: onSelect ? 'pointer' : 'default',
              background: active ? 'var(--c-teal-soft)' : 'transparent',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8, fontSize: 12, marginBottom: 4 }}>
              <span style={{ fontWeight: active ? 700 : 600, color: active ? 'var(--c-teal-700)' : 'var(--c-text)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                <span style={{ color: 'var(--c-text-2)', marginRight: 6, fontWeight: 500 }}>{idx + 1}.</span>
                {it.label}
              </span>
              <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, whiteSpace: 'nowrap' }}>
                {fmt(it.value)}
                {it.extra && <span style={{ fontSize: 10.5, color: 'var(--c-text-2)', fontWeight: 500, marginLeft: 6 }}>{it.extra}</span>}
              </span>
            </div>
            <div style={{ height: 7, background: 'var(--c-surface-2)', borderRadius: 4, overflow: 'hidden' }}>
              <div style={{ width: `${(it.value / max) * 100}%`, height: '100%', background: active ? 'var(--c-teal)' : color, borderRadius: 4, transition: 'width 0.3s ease' }} />
            </div>
          </div>
        );
      })}
    </div>
  );
}

function downloadCsv(filename, header, rows) {
  const esc = (v) => `"${String(v ?? '').replace(/"/g, '""')}"`;
  const csv = [header, ...rows].map((r) => r.map(esc).join(',')).join('\n');
  const blob = new Blob(['﻿' + csv], { type: 'text/csv;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

const chipStyle = (active) => ({
  padding: '6px 12px',
  borderRadius: 7,
  fontSize: 12,
  fontWeight: active ? 700 : 500,
  background: active ? 'var(--c-petrol)' : 'var(--c-surface)',
  color: active ? '#fff' : 'var(--c-text)',
  border: `1px solid ${active ? 'var(--c-petrol)' : 'var(--c-border)'}`,
  cursor: 'pointer',
});

const selectStyle = {
  background: 'var(--c-surface)',
  color: 'var(--c-text)',
  border: '1px solid var(--c-border-strong)',
  borderRadius: 7,
  padding: '6px 10px',
  fontSize: 12,
  fontWeight: 600,
  maxWidth: 260,
};

const labelStyle = { fontSize: 11.5, color: 'var(--c-text-2)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em' };

export default function Dashboard() {
  const [gravedad, setGravedad] = useState(null);
  const [anio, setAnio] = useState(null);
  const [comuna, setComuna] = useState(null);
  const [reloadKey, setReloadKey] = useState(0);

  const { data, loading, error } = useAnalytics({ anio, gravedad, comuna }, reloadKey);
  // Catálogo de años y comunas sin filtros para poblar los selectores
  const { data: base } = useAnalytics({}, reloadKey);

  const hasFilters = gravedad || anio || comuna;
  const reset = () => {
    setGravedad(null);
    setAnio(null);
    setComuna(null);
  };

  const insights = useMemo(() => {
    if (!data || !data.total_incidents) return [];
    const out = [];
    const peakHour = data.by_hour.indexOf(Math.max(...data.by_hour));
    const peakDay = data.by_weekday.indexOf(Math.max(...data.by_weekday));
    const night = [22, 23, 0, 1, 2, 3, 4, 5].reduce((s, h) => s + data.by_hour[h], 0);
    out.push(`La hora pico es ${String(peakHour).padStart(2, '0')}:00–${String(peakHour).padStart(2, '0')}:59 con ${fmt(data.by_hour[peakHour])} siniestros.`);
    out.push(`El ${WEEKDAYS_LONG[peakDay]} concentra la mayor siniestralidad (${pct(data.by_weekday[peakDay], data.total_incidents)}% del total).`);
    out.push(`El ${pct(night, data.total_incidents)}% ocurre en horario nocturno (22:00–05:59).`);
    if (!comuna && data.communes[0]) {
      out.push(`${data.communes[0].comuna} lidera con el ${pct(data.communes[0].count, data.total_incidents)}% de los casos.`);
    }
    const fatalTop = [...data.communes].filter((c) => c.count >= 300).sort((a, b) => b.fatal / b.count - a.fatal / a.count)[0];
    if (fatalTop && fatalTop.fatal > 0 && gravedad !== 'CON MUERTOS') {
      out.push(`Mayor letalidad relativa: ${fatalTop.comuna} (${((fatalTop.fatal / fatalTop.count) * 1000).toFixed(1)} muertes por cada 1.000 siniestros).`);
    }
    return out;
  }, [data, comuna, gravedad]);

  if (error && !data) {
    return (
      <div style={{ maxWidth: 640, margin: '60px auto', padding: '0 20px' }}>
        <div className="card-surface" style={{ padding: 28, textAlign: 'center' }}>
          <WifiOff size={32} color="var(--c-danger)" />
          <h2 style={{ margin: '12px 0 6px', fontSize: 18 }}>No se pudo conectar con el backend</h2>
          <p style={{ fontSize: 13, color: 'var(--c-text-2)', lineHeight: 1.5 }}>
            Inicia FastAPI con <code>start.ps1</code> o la tarea de VS Code <strong>“AburráSegura: iniciar todo”</strong> y vuelve a intentarlo.
            <br />
            <small>Detalle: {error}</small>
          </p>
          <button type="button" onClick={() => setReloadKey((k) => k + 1)} style={{ ...chipStyle(true), marginTop: 10, display: 'inline-flex', gap: 6, alignItems: 'center' }}>
            <RefreshCw size={13} /> Reintentar
          </button>
        </div>
      </div>
    );
  }

  if (!data) {
    return <div style={{ padding: 60, textAlign: 'center', color: 'var(--c-text-2)' }}>Cargando analítica…</div>;
  }

  const sev = data.by_severity || {};
  const total = data.total_incidents;
  const years = Object.keys(base?.by_year || data.by_year);
  const yearValues = years.map((y) => data.by_year[y] || 0);
  const communeOptions = (base?.communes || data.communes).map((c) => c.comuna).filter((c) => c !== 'Sin información');

  const filterLabel = [
    gravedad && SEVERITIES.find((s) => s.id === gravedad)?.label,
    anio && `Año ${anio}`,
    comuna,
  ]
    .filter(Boolean)
    .join(' · ');

  return (
    <div style={{ maxWidth: 1440, width: '100%', margin: '0 auto', padding: '24px 20px', display: 'flex', flexDirection: 'column', gap: 18, boxSizing: 'border-box' }} className="animate-fade-in">
      {/* Cabecera */}
      <div className="card-surface" style={{ padding: '20px 24px', borderLeft: '4px solid var(--c-petrol)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6, flexWrap: 'wrap' }}>
          <span style={{ fontSize: 11, fontWeight: 700, color: 'var(--c-teal-700)', background: 'var(--c-teal-soft)', padding: '3px 9px', borderRadius: 6, letterSpacing: '0.04em', textTransform: 'uppercase' }}>
            Inteligencia territorial
          </span>
          <span style={{ fontSize: 12, color: 'var(--c-text-2)' }}>MEData Medellín · datos reales consultados en SQLite</span>
          {loading && <RefreshCw size={13} color="var(--c-text-2)" style={{ animation: 'spin 1s linear infinite' }} />}
        </div>
        <h1 style={{ margin: 0, fontSize: 22, fontWeight: 800, letterSpacing: '-0.02em' }}>Analítica de accidentalidad vial en Medellín</h1>
        <p style={{ margin: '4px 0 0', fontSize: 13, color: 'var(--c-text-2)' }}>
          {fmt(base?.total_incidents ?? total)} incidentes georreferenciados (2014–2020). Combina filtros o haz clic en las gráficas para profundizar.
        </p>
      </div>

      {/* Filtros siempre visibles */}
      <div className="card-surface" style={{ padding: '14px 20px', display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: '12px 22px', background: 'var(--c-surface-2)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
          <span style={labelStyle}>Gravedad</span>
          {SEVERITIES.map((s) => {
            const id = s.id === 'ALL' ? null : s.id;
            return (
              <button key={s.id} type="button" onClick={() => setGravedad(id)} style={chipStyle(gravedad === id)}>
                {s.label}
              </button>
            );
          })}
        </div>
        <label style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={labelStyle}>Año</span>
          <select value={anio ?? ''} onChange={(e) => setAnio(e.target.value || null)} style={selectStyle}>
            <option value="">2014–2020</option>
            {years.map((y) => (
              <option key={y} value={y}>
                {y}
              </option>
            ))}
          </select>
        </label>
        <label style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={labelStyle}>Comuna</span>
          <select value={comuna ?? ''} onChange={(e) => setComuna(e.target.value || null)} style={selectStyle}>
            <option value="">Todas</option>
            {communeOptions.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </label>
        {hasFilters && (
          <button
            type="button"
            onClick={reset}
            style={{ display: 'flex', alignItems: 'center', gap: 5, padding: '6px 11px', borderRadius: 7, fontSize: 12, fontWeight: 600, color: 'var(--c-danger)', background: 'var(--c-danger-soft)', border: '1px solid #fecaca', cursor: 'pointer', marginLeft: 'auto' }}
          >
            <X size={13} /> Limpiar filtros
          </button>
        )}
      </div>

      {/* KPIs */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 14 }}>
        <Kpi label="Siniestros" value={fmt(total)} hint={filterLabel || 'Histórico completo'} icon={Activity} color="var(--c-petrol)" />
        <Kpi
          label="Solo daños"
          value={fmt(sev['SOLO DAÑOS'])}
          hint={`${pct(sev['SOLO DAÑOS'], total)}% · peso de riesgo 1`}
          icon={Car}
          color="var(--c-route-safe)"
          active={gravedad === 'SOLO DAÑOS'}
          onClick={() => setGravedad(gravedad === 'SOLO DAÑOS' ? null : 'SOLO DAÑOS')}
        />
        <Kpi
          label="Con heridos"
          value={fmt(sev['CON HERIDOS'])}
          hint={`${pct(sev['CON HERIDOS'], total)}% · peso de riesgo 3`}
          icon={AlertTriangle}
          color="var(--risk-2)"
          active={gravedad === 'CON HERIDOS'}
          onClick={() => setGravedad(gravedad === 'CON HERIDOS' ? null : 'CON HERIDOS')}
        />
        <Kpi
          label="Con muertos"
          value={fmt(sev['CON MUERTOS'])}
          hint={`${total ? (((sev['CON MUERTOS'] || 0) / total) * 1000).toFixed(1) : 0} por cada 1.000 siniestros`}
          icon={HeartCrack}
          color="var(--risk-4)"
          active={gravedad === 'CON MUERTOS'}
          onClick={() => setGravedad(gravedad === 'CON MUERTOS' ? null : 'CON MUERTOS')}
        />
        <Kpi label="Índice de riesgo" value={total ? (data.total_risk_score / total).toFixed(2) : '0'} hint="Peso medio por siniestro (1 a 10)" icon={Layers} color="var(--risk-3)" />
      </div>

      {/* Hallazgos automáticos */}
      {insights.length > 0 && (
        <Card title="Hallazgos clave" subtitle="Generados automáticamente a partir de los filtros activos" icon={Sparkles} iconColor="var(--c-teal)">
          <ul style={{ margin: 0, paddingLeft: 18, display: 'grid', gap: 6, fontSize: 13, lineHeight: 1.45 }}>
            {insights.map((t) => (
              <li key={t}>{t}</li>
            ))}
          </ul>
        </Card>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 440px), 1fr))', gap: 18 }}>
        <Card title="Serie anual" subtitle="Clic en un año para filtrar. 2020 refleja el confinamiento por pandemia." icon={Calendar} iconColor="var(--c-route-short)">
          <ColumnChart
            values={yearValues}
            labels={years}
            highlight={anio ? years.indexOf(String(anio)) : null}
            onSelect={(i) => setAnio(String(anio) === years[i] ? null : years[i])}
          />
        </Card>

        <Card title="Distribución por hora del día" subtitle="Horas con mayor exposición al riesgo" icon={Clock} iconColor="var(--risk-3)">
          <ColumnChart values={data.by_hour} labels={data.by_hour.map((_, h) => String(h).padStart(2, '0'))} color="var(--c-route-short)" labelEvery={3} />
        </Card>

        <Card title="Día de la semana" subtitle="Promedio semanal acumulado" icon={Calendar} iconColor="var(--c-petrol)">
          <ColumnChart values={data.by_weekday} labels={WEEKDAYS} color="var(--c-petrol-600)" height={120} />
        </Card>

        <Card title="Estacionalidad mensual" subtitle="Siniestros por mes del año" icon={Calendar} iconColor="var(--c-teal)">
          <ColumnChart values={data.by_month} labels={MONTHS} color="var(--c-teal-600)" height={120} />
        </Card>

        <Card title="Clase de accidente" subtitle="Tipología del siniestro" icon={Car} iconColor="var(--c-route-short)">
          <BarList
            items={data.by_class.map((c) => ({
              key: c.clase,
              label: CLASS_LABELS[c.clase] || c.clase,
              value: c.count,
              extra: `${pct(c.count, total)}%`,
            }))}
            color="var(--c-route-short)"
          />
        </Card>

        <Card
          title="Ranking de comunas"
          subtitle="Clic para filtrar todo el tablero por comuna"
          icon={MapPin}
          iconColor="var(--c-route-safe)"
          action={
            <button
              type="button"
              title="Descargar CSV"
              onClick={() =>
                downloadCsv(
                  'comunas_siniestralidad.csv',
                  ['comuna', 'siniestros', 'con_heridos', 'con_muertos'],
                  data.communes.map((c) => [c.comuna, c.count, c.injured, c.fatal])
                )
              }
              style={{ background: 'none', border: '1px solid var(--c-border)', borderRadius: 7, padding: '5px 7px', cursor: 'pointer', display: 'grid', placeItems: 'center' }}
            >
              <Download size={14} color="var(--c-text-2)" />
            </button>
          }
        >
          <BarList
            items={data.communes.map((c) => ({ key: c.comuna, label: c.comuna, value: c.count, extra: c.fatal ? `${c.fatal} †` : null }))}
            selected={comuna}
            onSelect={setComuna}
            maxHeight={330}
          />
        </Card>
      </div>

      <Card
        title={`Barrios con más siniestros${comuna ? ` en ${comuna}` : ''}`}
        subtitle="Top 12 según los filtros activos"
        icon={AlertTriangle}
        iconColor="var(--risk-4)"
        action={
          <button
            type="button"
            title="Descargar CSV"
            onClick={() =>
              downloadCsv('barrios_siniestralidad.csv', ['barrio', 'comuna', 'siniestros', 'con_muertos'], data.top_barrios.map((b) => [b.barrio, b.comuna, b.count, b.fatal]))
            }
            style={{ background: 'none', border: '1px solid var(--c-border)', borderRadius: 7, padding: '5px 7px', cursor: 'pointer', display: 'grid', placeItems: 'center' }}
          >
            <Download size={14} color="var(--c-text-2)" />
          </button>
        }
      >
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12.5 }}>
            <thead>
              <tr style={{ textAlign: 'left', color: 'var(--c-text-2)', fontSize: 11, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                <th style={{ padding: '6px 8px' }}>#</th>
                <th style={{ padding: '6px 8px' }}>Barrio</th>
                <th style={{ padding: '6px 8px' }}>Comuna</th>
                <th style={{ padding: '6px 8px', textAlign: 'right' }}>Siniestros</th>
                <th style={{ padding: '6px 8px', textAlign: 'right' }}>% del filtro</th>
                <th style={{ padding: '6px 8px', textAlign: 'right' }}>Con muertos</th>
              </tr>
            </thead>
            <tbody>
              {data.top_barrios.map((b, i) => (
                <tr key={`${b.barrio}-${b.comuna}`} style={{ borderTop: '1px solid var(--c-border)' }}>
                  <td style={{ padding: '7px 8px', color: 'var(--c-text-2)' }}>{i + 1}</td>
                  <td style={{ padding: '7px 8px', fontWeight: 600 }}>{b.barrio}</td>
                  <td style={{ padding: '7px 8px', color: 'var(--c-text-2)' }}>{b.comuna}</td>
                  <td style={{ padding: '7px 8px', textAlign: 'right', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>{fmt(b.count)}</td>
                  <td style={{ padding: '7px 8px', textAlign: 'right', fontFamily: 'var(--font-mono)' }}>{pct(b.count, total)}%</td>
                  <td style={{ padding: '7px 8px', textAlign: 'right', fontFamily: 'var(--font-mono)', color: b.fatal ? 'var(--c-danger)' : 'var(--c-text-2)' }}>{fmt(b.fatal)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
