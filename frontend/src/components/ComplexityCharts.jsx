import { apiUrl } from '../api.js';
import React, { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { Activity, GitBranch, Layers, Network, Play, RotateCcw, Search, Table2, WifiOff } from 'lucide-react';

// Paleta categórica validada (orden fijo, nunca cíclico). Ver --series-* en index.css.
const S = ['var(--series-1)', 'var(--series-2)', 'var(--series-3)', 'var(--series-4)', 'var(--series-5)'];

const CLASSES = [
  { id: 'O(1)', label: 'O(1)', f: () => 1, color: S[0] },
  { id: 'O(log n)', label: 'O(log n)', f: (n) => Math.log2(n), color: S[1] },
  { id: 'O(n)', label: 'O(n)', f: (n) => n, color: S[2] },
  { id: 'O(n log n)', label: 'O(n log n)', f: (n) => n * Math.log2(n), color: S[3] },
  { id: 'O(n^2)', label: 'O(n²)', f: (n) => n * n, color: S[4] },
];
const SWEEP_SIZES = [1000, 2500, 5000, 10000, 25000, 50000, 100000, 251150];

const SORT_ALGOS = [
  { id: 'merge_sort', label: 'Merge Sort', color: S[0], f: (n) => n * Math.log2(n), fLabel: 'n·log₂n' },
  { id: 'quick_sort', label: 'Quick Sort', color: S[1], f: (n) => n * Math.log2(n), fLabel: 'n·log₂n' },
  { id: 'heap_sort', label: 'Heap Sort', color: S[2], f: (n) => n * Math.log2(n), fLabel: 'n·log₂n' },
  { id: 'counting_sort', label: 'Counting Sort', color: S[3], f: (n) => n, fLabel: 'n' },
  { id: 'timsort', label: 'Timsort', color: S[4], f: (n) => n * Math.log2(n), fLabel: 'n·log₂n' },
];
const DISTRIBUTIONS = [
  { id: 'random', label: 'Aleatorio' },
  { id: 'sorted', label: 'Casi ordenado' },
  { id: 'reversed', label: 'Invertido' },
  { id: 'duplicates', label: 'Duplicados' },
];

// ---------------------------------------------------------------------------
// Formato
// ---------------------------------------------------------------------------
const fmtInt = (n) => Math.round(n ?? 0).toLocaleString('es-CO');
const fmtN = (n) => (n >= 1e6 ? `${n / 1e6}M` : n >= 1000 ? `${+(n / 1000).toFixed(1)}k` : String(n));

function fmtTime(ms) {
  if (ms == null || Number.isNaN(ms)) return '—';
  if (ms < 0.001) return `${+(ms * 1e6).toPrecision(3)} ns`;
  if (ms < 1) return `${+(ms * 1e3).toPrecision(3)} µs`;
  if (ms < 1000) return `${+ms.toPrecision(3)} ms`;
  return `${+(ms / 1000).toPrecision(3)} s`;
}

// ---------------------------------------------------------------------------
// Escalas y ticks
// ---------------------------------------------------------------------------
function makeScale(min, max, r0, r1, log) {
  if (log) {
    const a = Math.log10(min);
    const b = Math.log10(max);
    return (v) => r0 + ((Math.log10(Math.max(v, min)) - a) / (b - a || 1)) * (r1 - r0);
  }
  return (v) => r0 + ((v - min) / (max - min || 1)) * (r1 - r0);
}

function logTicks(min, max) {
  const lo = Math.floor(Math.log10(min));
  const hi = Math.ceil(Math.log10(max));
  const decades = [];
  for (let e = lo; e <= hi; e++) decades.push(10 ** e);
  if (hi - lo >= 3) return decades.filter((v) => v >= min / 1.001 && v <= max * 1.001);
  const out = [];
  decades.forEach((d) => [1, 2, 5].forEach((m) => out.push(d * m)));
  return out.filter((v) => v >= min / 1.001 && v <= max * 1.001);
}

function linTicks(min, max, count = 5) {
  const raw = (max - min) / count;
  const mag = 10 ** Math.floor(Math.log10(raw || 1));
  const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => s >= raw) || raw;
  const out = [];
  for (let v = Math.ceil(min / step) * step; v <= max + step * 1e-6; v += step) out.push(+v.toFixed(10));
  return out;
}

function useWidth() {
  const ref = useRef(null);
  const [w, setW] = useState(720);
  useLayoutEffect(() => {
    if (!ref.current) return;
    const ro = new ResizeObserver(([e]) => setW(Math.max(280, e.contentRect.width)));
    ro.observe(ref.current);
    return () => ro.disconnect();
  }, []);
  return [ref, w];
}

// ---------------------------------------------------------------------------
// Gráfico de líneas con escala log/lineal, crosshair, tooltip y etiquetas directas
// series: [{ id, label, color, points: [{ x, y, est }], reference?: bool }]
// ---------------------------------------------------------------------------
function LineChart({ series, xLog = true, yLog = true, yFormat = fmtTime, xLabel = 'Tamaño de entrada n', yLabel, height = 300, refLine }) {
  const [wrapRef, width] = useWidth();
  const [hoverX, setHoverX] = useState(null);
  const m = { l: 62, r: width < 520 ? 16 : 104, t: 12, b: 42 };
  const iw = width - m.l - m.r;
  const ih = height - m.t - m.b;

  const all = series.flatMap((s) => s.points).filter((p) => p.y != null && (!yLog || p.y > 0));
  if (!all.length) return <div ref={wrapRef} style={{ height, display: 'grid', placeItems: 'center', color: 'var(--c-text-2)', fontSize: 13 }}>Sin datos todavía</div>;

  const xs = [...new Set(series.filter((s) => !s.reference).flatMap((s) => s.points.map((p) => p.x)))].sort((a, b) => a - b);
  let [x0, x1] = [Math.min(...xs), Math.max(...xs)];
  let y0 = Math.min(...all.map((p) => p.y));
  let y1 = Math.max(...all.map((p) => p.y));
  if (refLine != null) {
    y0 = Math.min(y0, refLine);
    y1 = Math.max(y1, refLine);
  }
  if (yLog) {
    y0 = 10 ** Math.floor(Math.log10(y0));
    y1 = 10 ** Math.ceil(Math.log10(y1));
  } else {
    const pad = (y1 - y0) * 0.08 || 1;
    y0 = Math.max(0, y0 - pad);
    y1 += pad;
  }
  if (x0 === x1) x1 = x0 * 10;

  const sx = makeScale(x0, x1, m.l, m.l + iw, xLog);
  const sy = makeScale(y0, y1, m.t + ih, m.t, yLog);
  const yt = yLog ? logTicks(y0, y1) : linTicks(y0, y1);
  const xt = xLog ? xs : linTicks(x0, x1);

  // Etiquetas al final de cada serie, separadas para que no se encimen
  const ends = series
    .filter((s) => !s.reference && s.points.length)
    .map((s) => {
      const last = [...s.points].sort((a, b) => a.x - b.x).at(-1);
      return { s, y: sy(last.y), x: sx(last.x) };
    })
    .sort((a, b) => a.y - b.y);
  for (let i = 1; i < ends.length; i++) if (ends[i].y - ends[i - 1].y < 14) ends[i].y = ends[i - 1].y + 14;

  const onMove = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const px = ((e.clientX - rect.left) / rect.width) * width;
    let best = null;
    xs.forEach((x) => {
      if (best == null || Math.abs(sx(x) - px) < Math.abs(sx(best) - px)) best = x;
    });
    setHoverX(best);
  };

  const hoverRows =
    hoverX == null
      ? []
      : series
          .map((s) => ({ s, p: s.points.find((p) => p.x === hoverX) }))
          .filter((r) => r.p)
          .sort((a, b) => b.p.y - a.p.y);
  const tipLeft = hoverX != null && sx(hoverX) > width * 0.6;

  return (
    <div ref={wrapRef} style={{ position: 'relative', width: '100%' }}>
      <svg width={width} height={height} style={{ display: 'block', overflow: 'visible' }} onMouseMove={onMove} onMouseLeave={() => setHoverX(null)} role="img" aria-label={yLabel}>
        {yt.map((v) => (
          <g key={`y${v}`}>
            <line x1={m.l} x2={m.l + iw} y1={sy(v)} y2={sy(v)} stroke="var(--c-border)" strokeWidth={1} opacity={0.7} />
            <text x={m.l - 8} y={sy(v)} dy="0.32em" textAnchor="end" fontSize={10.5} fill="var(--c-text-2)" fontFamily="var(--font-mono)">
              {yFormat(v)}
            </text>
          </g>
        ))}
        {xt.map((v) => (
          <text key={`x${v}`} x={sx(v)} y={m.t + ih + 16} textAnchor="middle" fontSize={10.5} fill="var(--c-text-2)" fontFamily="var(--font-mono)">
            {fmtN(v)}
          </text>
        ))}
        <line x1={m.l} x2={m.l + iw} y1={m.t + ih} y2={m.t + ih} stroke="var(--c-border-strong)" />
        <text x={m.l + iw / 2} y={height - 4} textAnchor="middle" fontSize={11} fill="var(--c-text-2)">
          {xLabel}
          {xLog ? ' (escala log)' : ''}
        </text>
        {yLabel && (
          <text transform={`translate(12 ${m.t + ih / 2}) rotate(-90)`} textAnchor="middle" fontSize={11} fill="var(--c-text-2)">
            {yLabel}
            {yLog ? ' (log)' : ''}
          </text>
        )}
        {refLine != null && <line x1={m.l} x2={m.l + iw} y1={sy(refLine)} y2={sy(refLine)} stroke="var(--c-text-2)" strokeWidth={1} />}

        {hoverX != null && <line x1={sx(hoverX)} x2={sx(hoverX)} y1={m.t} y2={m.t + ih} stroke="var(--c-text-2)" strokeWidth={1} opacity={0.5} />}

        {series.map((s) => {
          const pts = [...s.points].filter((p) => p.y != null && (!yLog || p.y > 0)).sort((a, b) => a.x - b.x);
          const d = pts.map((p, i) => `${i ? 'L' : 'M'}${sx(p.x)},${sy(p.y)}`).join('');
          return (
            <g key={s.id}>
              <path d={d} fill="none" stroke={s.color} strokeWidth={s.reference ? 1.5 : 2} strokeDasharray={s.reference ? '5 4' : undefined} strokeLinejoin="round" opacity={s.reference ? 0.75 : 1} />
              {!s.reference &&
                pts.map((p) => (
                  <circle
                    key={p.x}
                    cx={sx(p.x)}
                    cy={sy(p.y)}
                    r={p.x === hoverX ? 5.5 : 4}
                    fill={p.est ? 'var(--c-surface)' : s.color}
                    stroke={p.est ? s.color : 'var(--c-surface)'}
                    strokeWidth={2}
                  />
                ))}
            </g>
          );
        })}

        {width >= 520 &&
          ends.map(({ s, y, x }) => (
            <g key={`lab-${s.id}`}>
              <line x1={x + 6} x2={x + 16} y1={y} y2={y} stroke={s.color} strokeWidth={2} />
              <text x={x + 20} y={y} dy="0.32em" fontSize={11} fontWeight={600} fill="var(--c-text)">
                {s.label}
              </text>
            </g>
          ))}
      </svg>

      {hoverX != null && hoverRows.length > 0 && (
        <div
          style={{
            position: 'absolute',
            top: m.t,
            left: tipLeft ? undefined : sx(hoverX) + 12,
            right: tipLeft ? width - sx(hoverX) + 12 : undefined,
            background: 'var(--c-surface)',
            border: '1px solid var(--c-border-strong)',
            borderRadius: 8,
            boxShadow: 'var(--sh-2)',
            padding: '8px 10px',
            fontSize: 12,
            pointerEvents: 'none',
            minWidth: 170,
            zIndex: 2,
          }}
        >
          <div style={{ fontWeight: 700, marginBottom: 4 }}>n = {fmtInt(hoverX)}</div>
          {hoverRows.map(({ s, p }) => (
            <div key={s.id} style={{ display: 'flex', alignItems: 'center', gap: 6, lineHeight: 1.6 }}>
              <span style={{ width: 10, height: 3, borderRadius: 2, background: s.color, flexShrink: 0 }} />
              <span style={{ flex: 1, color: 'var(--c-text-2)' }}>{s.label}</span>
              <strong style={{ fontFamily: 'var(--font-mono)' }}>{yFormat(p.y)}</strong>
              {p.est && <span style={{ fontSize: 10, color: 'var(--c-text-2)' }}>extrap.</span>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function Legend({ series, showMarkers = true }) {
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px 16px', fontSize: 12, marginBottom: 8, alignItems: 'center' }}>
      {series.map((s) => (
        <span key={s.id} style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
          <svg width={18} height={8}>
            <line x1={0} x2={18} y1={4} y2={4} stroke={s.color} strokeWidth={s.reference ? 1.5 : 2} strokeDasharray={s.reference ? '4 3' : undefined} />
          </svg>
          {s.label}
        </span>
      ))}
      {showMarkers && (
        <span style={{ display: 'inline-flex', alignItems: 'center', gap: 10, color: 'var(--c-text-2)', marginLeft: 'auto' }}>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
            <svg width={10} height={10}><circle cx={5} cy={5} r={4} fill="var(--c-text-2)" /></svg> medido
          </span>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
            <svg width={10} height={10}><circle cx={5} cy={5} r={3.5} fill="var(--c-surface)" stroke="var(--c-text-2)" strokeWidth={1.5} /></svg> extrapolado
          </span>
        </span>
      )}
    </div>
  );
}

function DataTable({ series, yFormat = fmtTime }) {
  const xs = [...new Set(series.filter((s) => !s.reference).flatMap((s) => s.points.map((p) => p.x)))].sort((a, b) => a - b);
  const rows = series.filter((s) => !s.reference);
  return (
    <div style={{ overflowX: 'auto', marginTop: 10 }}>
      <table style={tableStyle}>
        <thead>
          <tr>
            <th style={th}>n</th>
            {rows.map((s) => (
              <th key={s.id} style={{ ...th, textAlign: 'right' }}>
                {s.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {xs.map((x) => (
            <tr key={x} style={{ borderTop: '1px solid var(--c-border)' }}>
              <td style={{ ...td, fontFamily: 'var(--font-mono)' }}>{fmtInt(x)}</td>
              {rows.map((s) => {
                const p = s.points.find((q) => q.x === x);
                return (
                  <td key={s.id} style={{ ...td, textAlign: 'right', fontFamily: 'var(--font-mono)' }}>
                    {p ? yFormat(p.y) : '—'}
                    {p?.est ? '*' : ''}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{ fontSize: 11, color: 'var(--c-text-2)', marginTop: 4 }}>* valor extrapolado</div>
    </div>
  );
}

const tableStyle = { width: '100%', borderCollapse: 'collapse', fontSize: 12.5 };
const th = { padding: '6px 8px', textAlign: 'left', fontSize: 11, color: 'var(--c-text-2)', textTransform: 'uppercase', letterSpacing: '0.04em', whiteSpace: 'nowrap' };
const td = { padding: '7px 8px', verticalAlign: 'top' };

function ChartCard({ title, subtitle, series, yFormat, yLabel, yLog = true, xLog = true, refLine, note, showMarkers, controls }) {
  const [showTable, setShowTable] = useState(false);
  const [log, setLog] = useState(yLog);
  return (
    <section className="card-surface" style={{ padding: '18px 20px', minWidth: 0 }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap', marginBottom: 10 }}>
        <div style={{ minWidth: 0 }}>
          <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700 }}>{title}</h3>
          {subtitle && <p style={{ margin: '3px 0 0', fontSize: 12, color: 'var(--c-text-2)', maxWidth: 720, lineHeight: 1.45 }}>{subtitle}</p>}
        </div>
        <div style={{ display: 'flex', gap: 6, alignItems: 'flex-start' }}>
          {controls}
          <button type="button" onClick={() => setLog(!log)} style={chip(false)} title="Cambiar escala del eje Y">
            Eje Y: {log ? 'log' : 'lineal'}
          </button>
          <button type="button" onClick={() => setShowTable(!showTable)} style={{ ...chip(showTable), display: 'inline-flex', alignItems: 'center', gap: 5 }}>
            <Table2 size={13} /> Tabla
          </button>
        </div>
      </header>
      <Legend series={series} showMarkers={showMarkers} />
      <LineChart series={series} yFormat={yFormat} yLabel={yLabel} yLog={log} xLog={xLog} refLine={refLine} />
      {note && <p style={{ margin: '8px 0 0', fontSize: 12, color: 'var(--c-text-2)', lineHeight: 1.5 }}>{note}</p>}
      {showTable && <DataTable series={series} yFormat={yFormat} />}
    </section>
  );
}

const chip = (active) => ({
  padding: '5px 10px',
  borderRadius: 7,
  fontSize: 12,
  fontWeight: active ? 700 : 500,
  background: active ? 'var(--c-petrol)' : 'var(--c-surface)',
  color: active ? '#fff' : 'var(--c-text)',
  border: `1px solid ${active ? 'var(--c-petrol)' : 'var(--c-border)'}`,
  cursor: 'pointer',
  whiteSpace: 'nowrap',
});

// Curva teórica c·f(n) anclada al primer punto medido
function fitted(points, f, id, label) {
  const first = points.find((p) => !p.est) || points[0];
  if (!first) return null;
  const c = first.y / f(first.x);
  return { id, label, color: 'var(--c-text-2)', reference: true, points: points.map((p) => ({ x: p.x, y: c * f(p.x) })) };
}

// ---------------------------------------------------------------------------
// 1. Barrido en vivo de la jerarquía asintótica
// ---------------------------------------------------------------------------
function describeAnswer(r) {
  switch (r.complexity_class) {
    case 'O(1)':
      return r.found ? `Radicado ${r.sample_result} encontrado con un solo acceso` : 'Radicado no encontrado';
    case 'O(log n)':
      return r.found ? `Fecha localizada en la posición ${fmtInt(r.match_index)} del arreglo ordenado` : 'Fecha no encontrada';
    case 'O(n)':
      return `${fmtInt(r.matches_count)} siniestros en La Candelaria · ${fmtInt(r.fatal_count)} con muertos · riesgo ${fmtInt(r.total_risk_score)}`;
    case 'O(n log n)':
      return `${fmtInt(r.is_extrapolated ? 30000 : r.size_n)} registros ordenados por fecha`;
    case 'O(n^2)':
      return r.is_extrapolated
        ? `≈ ${fmtInt(r.pairs_at_proximity)} pares a menos de 50 m (estimado a partir de la muestra de ${fmtInt(r.sample_measured_n)})`
        : `${fmtInt(r.pairs_at_proximity)} pares de siniestros a menos de 50 m`;
    default:
      return r.description;
  }
}

function HierarchySweep() {
  const [runs, setRuns] = useState({}); // n -> respuesta del endpoint
  const [running, setRunning] = useState(false);
  const [error, setError] = useState(null);
  const [selectedN, setSelectedN] = useState(null);
  const cancelRef = useRef(false);

  const run = async () => {
    cancelRef.current = false;
    setRunning(true);
    setError(null);
    setRuns({});
    for (const n of SWEEP_SIZES) {
      if (cancelRef.current) break;
      try {
        const resp = await fetch(apiUrl('/api/v1/benchmarks/complexity'), {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ complexity_class: 'all', size: n }),
        });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data = await resp.json();
        setRuns((r) => ({ ...r, [n]: data }));
        setSelectedN(n);
      } catch (e) {
        setError(e.message);
        break;
      }
    }
    setRunning(false);
  };

  useEffect(() => {
    run();
    return () => {
      cancelRef.current = true;
    };
  }, []);

  const sizes = Object.keys(runs).map(Number).sort((a, b) => a - b);
  const byClass = (cls) => sizes.map((n) => ({ n, r: runs[n].results.find((x) => x.complexity_class === cls.id) })).filter((x) => x.r);

  const timeSeries = CLASSES.map((c) => ({
    id: c.id,
    label: c.label,
    color: c.color,
    points: byClass(c).map(({ n, r }) => ({ x: n, y: r.time_ms, est: r.is_extrapolated })),
  }));

  // t(n)/f(n) normalizado al primer n: si la clase es correcta la línea se mantiene cerca de 1
  const ratioSeries = CLASSES.map((c) => {
    const pts = byClass(c);
    const base = pts[0] ? pts[0].r.time_ms / c.f(pts[0].n) : 1;
    return {
      id: c.id,
      label: c.label,
      color: c.color,
      points: pts.map(({ n, r }) => ({ x: n, y: r.time_ms / c.f(n) / base, est: r.is_extrapolated })),
    };
  });

  const current = selectedN && runs[selectedN];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div className="card-surface" style={{ padding: '14px 20px', display: 'flex', alignItems: 'center', gap: 14, flexWrap: 'wrap' }}>
        <div style={{ flex: 1, minWidth: 240, fontSize: 13, lineHeight: 1.5 }}>
          Se ejecutan los 5 algoritmos sobre los siniestros reales para{' '}
          <strong>n = {SWEEP_SIZES.map(fmtN).join(', ')}</strong>. Cada punto es una medición con <code>time.perf_counter_ns</code> en el backend.
        </div>
        <div style={{ fontSize: 12, fontFamily: 'var(--font-mono)', color: 'var(--c-text-2)' }}>
          {sizes.length}/{SWEEP_SIZES.length} tamaños
        </div>
        <button
          type="button"
          onClick={running ? () => (cancelRef.current = true) : run}
          style={{ ...chip(true), display: 'inline-flex', alignItems: 'center', gap: 6, padding: '8px 14px' }}
        >
          {running ? <RotateCcw size={14} style={{ animation: 'spin 1s linear infinite' }} /> : <Play size={14} fill="currentColor" />}
          {running ? 'Detener' : 'Volver a medir'}
        </button>
      </div>

      {error && sizes.length === 0 ? (
        <Offline message={error} />
      ) : (
        <>
          <ChartCard
            title="Tiempo de ejecución vs. tamaño de entrada"
            subtitle="En escala log-log cada clase es una recta cuya pendiente es el exponente: O(n) sube 1 década por década de n y O(n²) sube 2. O(1) y O(log n) quedan casi planas."
            series={timeSeries}
            yLabel="Tiempo"
            note="O(n²) se mide sobre m = 2.500 y se extrapola con (n/m)²; O(n log n) se mide hasta 30.000 y se extrapola con n·log n. Esos puntos aparecen huecos."
          />
          <ChartCard
            title="Constante oculta normalizada: t(n) / f(n)"
            subtitle="Divide el tiempo medido entre la función teórica de su clase y normaliza al primer tamaño. Si la complejidad teórica es correcta, la línea se mantiene cerca de 1 (línea de referencia)."
            series={ratioSeries}
            yFormat={(v) => `${+v.toPrecision(2)}×`}
            yLabel="t(n)/f(n) relativo"
            refLine={1}
            note="Solo los puntos medidos validan la clase: los extrapolados repiten la constante de la última medición real (n = 2.500 para O(n²), 30.000 para O(n log n)). O(1) y O(log n) oscilan más porque tardan nanosegundos y el ruido del sistema pesa más."
          />

          {current && (
            <section className="card-surface" style={{ padding: '18px 20px' }}>
              <header style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap', marginBottom: 12 }}>
                <div>
                  <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700 }}>Respuestas de cada algoritmo</h3>
                  <p style={{ margin: '3px 0 0', fontSize: 12, color: 'var(--c-text-2)' }}>Lo que devolvió cada algoritmo y cuántas operaciones hizo frente a la cota teórica.</p>
                </div>
                <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                  {sizes.map((n) => (
                    <button key={n} type="button" onClick={() => setSelectedN(n)} style={chip(n === selectedN)}>
                      n = {fmtN(n)}
                    </button>
                  ))}
                </div>
              </header>
              <div style={{ overflowX: 'auto' }}>
                <table style={tableStyle}>
                  <thead>
                    <tr>
                      <th style={th}>Clase</th>
                      <th style={th}>Algoritmo</th>
                      <th style={th}>Respuesta</th>
                      <th style={{ ...th, textAlign: 'right' }}>Operaciones</th>
                      <th style={{ ...th, textAlign: 'right' }}>Cota teórica</th>
                      <th style={{ ...th, textAlign: 'right' }}>Tiempo</th>
                      <th style={th}>Estado</th>
                    </tr>
                  </thead>
                  <tbody>
                    {current.results.map((r) => {
                      const cls = CLASSES.find((c) => c.id === r.complexity_class);
                      return (
                        <tr key={r.complexity_class} style={{ borderTop: '1px solid var(--c-border)' }}>
                          <td style={{ ...td, whiteSpace: 'nowrap', fontWeight: 700 }}>
                            <span style={{ display: 'inline-block', width: 10, height: 3, borderRadius: 2, background: cls?.color, marginRight: 6, verticalAlign: 'middle' }} />
                            {cls?.label || r.complexity_class}
                          </td>
                          <td style={td}>{r.name}</td>
                          <td style={{ ...td, minWidth: 220 }}>{describeAnswer(r)}</td>
                          <td style={{ ...td, textAlign: 'right', fontFamily: 'var(--font-mono)' }}>{fmtInt(r.operations_count)}</td>
                          <td style={{ ...td, textAlign: 'right', fontFamily: 'var(--font-mono)', color: 'var(--c-text-2)' }}>{r.theoretical_formula}</td>
                          <td style={{ ...td, textAlign: 'right', fontFamily: 'var(--font-mono)', fontWeight: 700, whiteSpace: 'nowrap' }}>{fmtTime(r.time_ms)}</td>
                          <td style={{ ...td, whiteSpace: 'nowrap', color: r.is_extrapolated ? 'var(--c-warn-ink)' : 'var(--c-route-safe-ink)', fontSize: 12, fontWeight: 600 }}>
                            {r.is_extrapolated ? 'Extrapolado' : 'Medido'}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
              {current.results.find((r) => r.extrapolation_note) && (
                <p style={{ margin: '10px 0 0', fontSize: 12, color: 'var(--c-text-2)' }}>{current.results.find((r) => r.extrapolation_note).extrapolation_note}</p>
              )}
            </section>
          )}
        </>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// 2. Resultados consolidados de la Fase 4
// ---------------------------------------------------------------------------
function useFase4() {
  const [state, setState] = useState({ data: null, error: null });
  useEffect(() => {
    fetch(apiUrl('/api/v1/benchmarks/fase4-results'))
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((data) => setState({ data, error: null }))
      .catch((e) => setState({ data: null, error: e.message }));
  }, []);
  return state;
}

function SortingCharts({ data }) {
  const [dist, setDist] = useState('random');
  const rows = (algo) => (data.sorting[algo.id] || []).filter((r) => r.distribution === dist);
  const time = SORT_ALGOS.map((a) => ({
    id: a.id,
    label: a.label,
    color: a.color,
    points: rows(a).map((r) => ({ x: r.size, y: r.time_ms_mean, est: r.estimated })),
  }));
  const constant = SORT_ALGOS.map((a) => ({
    id: a.id,
    label: `${a.label} / ${a.fLabel}`,
    color: a.color,
    points: rows(a).map((r) => ({ x: r.size, y: (r.time_ms_mean * 1e6) / a.f(r.size), est: r.estimated })),
  }));
  const distControls = (
    <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
      {DISTRIBUTIONS.map((d) => (
        <button key={d.id} type="button" onClick={() => setDist(d.id)} style={chip(dist === d.id)}>
          {d.label}
        </button>
      ))}
    </div>
  );
  return (
    <>
      <ChartCard
        title="Ordenamiento: tiempo vs. n (1.000 a 1.000.000)"
        subtitle="Media de varias repeticiones por tamaño. Counting Sort (O(n + k)) crece más lento que los O(n log n); Timsort es nativo en C y por eso queda muy por debajo."
        series={time}
        yLabel="Tiempo medio"
        controls={distControls}
      />
      <ChartCard
        title="Constante oculta por algoritmo: t(n) / f(n)"
        subtitle="Nanosegundos por unidad de trabajo teórico. Una línea plana confirma la complejidad; su altura es la constante c que la notación O esconde."
        series={constant}
        yFormat={(v) => `${+v.toPrecision(3)} ns`}
        yLabel="c (ns)"
        note="Timsort es el sort nativo de Python, escrito en C: su constante es unas 100 veces menor que la de los algoritmos implementados en Python puro. Con datos casi ordenados o invertidos detecta corridas y se acerca a O(n)."
      />
    </>
  );
}

function SpatialCharts({ data }) {
  const rows = data.spatial.kdtree_vs_linear;
  const times = [
    { id: 'kd', label: 'KD-Tree O(log n)', color: S[0], points: rows.map((r) => ({ x: r.size, y: r.kdtree_query_time_ms })) },
    { id: 'lin', label: 'Lineal O(n)', color: S[1], points: rows.map((r) => ({ x: r.size, y: r.linear_query_time_ms })) },
  ];
  const speed = [
    { id: 'real', label: 'Aceleración medida', color: S[0], points: rows.map((r) => ({ x: r.size, y: r.speedup_factor })) },
    { id: 'teo', label: 'Teórica n / log₂n', color: S[1], points: rows.map((r) => ({ x: r.size, y: r.theoretical_speedup })) },
  ];
  const fx = (v) => `${fmtInt(v)}×`;
  return (
    <>
      <ChartCard
        title="Vecinos más cercanos: KD-Tree vs. búsqueda lineal"
        subtitle={`Tiempo total de ${rows[0]?.queries ?? ''} consultas k-NN (k = ${rows[0]?.k ?? ''}). La búsqueda lineal crece con n; el KD-Tree se mantiene casi constante.`}
        series={times}
        yLabel="Tiempo de consulta"
        showMarkers={false}
      />
      <ChartCard
        title="Factor de aceleración del KD-Tree"
        subtitle="Cuántas veces más rápido es el KD-Tree que el barrido lineal, comparado con la ganancia teórica n / log₂n."
        series={speed}
        yFormat={fx}
        yLabel="Aceleración"
        showMarkers={false}
        note="La aceleración medida queda por debajo de la teórica por el costo de recorrer el árbol y por la poda que exige k = 5 vecinos, pero crece al mismo ritmo."
      />
    </>
  );
}

function ClusteringCharts({ data }) {
  const rows = data.clustering.dbscan_scaling;
  const measured = { id: 'dbscan', label: 'DBSCAN medido', color: S[0], points: rows.map((r) => ({ x: r.size, y: r.time_ms })) };
  const series = [measured, fitted(measured.points, (n) => n * Math.log2(n), 'nlogn', 'Teórica n log n'), fitted(measured.points, (n) => n * n, 'n2', 'Teórica n²')].filter(Boolean);
  return (
    <>
      <ChartCard
        title="DBSCAN con KD-Tree: tiempo vs. n"
        subtitle="Las curvas punteadas son c·f(n) ancladas al primer punto. La curva medida cae entre n log n y n²: al crecer la densidad cada consulta por radio devuelve más vecinos."
        series={series}
        yLabel="Tiempo"
        showMarkers={false}
      />
      <section className="card-surface" style={{ padding: '18px 20px' }}>
        <h3 style={{ margin: '0 0 10px', fontSize: 15, fontWeight: 700 }}>Respuestas de DBSCAN por tamaño</h3>
        <div style={{ overflowX: 'auto' }}>
          <table style={tableStyle}>
            <thead>
              <tr>
                {['n', 'ε (m)', 'minPts', 'Clusters (puntos críticos)', 'Ruido', '% ruido', 'Tiempo'].map((h, i) => (
                  <th key={h} style={{ ...th, textAlign: i ? 'right' : 'left' }}>
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.size} style={{ borderTop: '1px solid var(--c-border)', fontFamily: 'var(--font-mono)' }}>
                  <td style={td}>{fmtInt(r.size)}</td>
                  <td style={{ ...td, textAlign: 'right' }}>{r.eps_meters}</td>
                  <td style={{ ...td, textAlign: 'right' }}>{r.min_samples}</td>
                  <td style={{ ...td, textAlign: 'right', fontWeight: 700 }}>{r.total_clusters}</td>
                  <td style={{ ...td, textAlign: 'right' }}>{fmtInt(r.noise_points)}</td>
                  <td style={{ ...td, textAlign: 'right' }}>{r.noise_percentage}%</td>
                  <td style={{ ...td, textAlign: 'right', fontWeight: 700 }}>{fmtTime(r.time_ms)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p style={{ margin: '8px 0 0', fontSize: 12, color: 'var(--c-text-2)' }}>
          Con pocos datos casi todo es ruido; con más siniestros emergen los puntos críticos y el ruido baja del 96% al {rows.at(-1)?.noise_percentage}%.
        </p>
      </section>
    </>
  );
}

function RoutingCharts({ data }) {
  const pairs = data.routing.routing_pairs;
  const algos = [
    { key: 'dijkstra', label: 'Dijkstra', color: S[0] },
    { key: 'astar_shortest', label: 'A* (ruta corta)', color: S[1] },
    { key: 'astar_safest', label: 'A* (ruta segura)', color: S[2] },
  ];
  const max = Math.max(...pairs.flatMap((p) => algos.map((a) => p[a.key].nodes_explored)));
  const avgPruning = pairs.reduce((s, p) => s + (p.astar_pruning_pct || 0), 0) / pairs.length;
  const [hover, setHover] = useState(null);

  return (
    <>
      <section className="card-surface" style={{ padding: '18px 20px' }}>
        <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700 }}>Nodos explorados: Dijkstra vs. A*</h3>
        <p style={{ margin: '3px 0 10px', fontSize: 12, color: 'var(--c-text-2)', lineHeight: 1.45 }}>
          Ambos son O((V + E) log V), pero la heurística Haversine de A* poda la búsqueda. Para la misma ruta corta, A* explora en promedio un{' '}
          <strong style={{ color: 'var(--c-text)' }}>{avgPruning.toFixed(1)}% menos</strong> de nodos que Dijkstra en los {pairs.length} pares. La ruta segura optimiza otro costo (distancia + riesgo), por eso a veces explora más.
        </p>
        <Legend series={algos.map((a) => ({ id: a.key, ...a }))} showMarkers={false} />
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {pairs.map((p, i) => (
            <div key={i} style={{ display: 'grid', gridTemplateColumns: 'minmax(140px, 260px) 1fr', gap: 12, alignItems: 'center' }}>
              <div style={{ fontSize: 12, lineHeight: 1.3 }}>{p.description}</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                {algos.map((a) => {
                  const v = p[a.key].nodes_explored;
                  const id = `${i}-${a.key}`;
                  return (
                    <div key={a.key} style={{ display: 'flex', alignItems: 'center', gap: 6, height: 10 }} onMouseEnter={() => setHover(id)} onMouseLeave={() => setHover(null)}>
                      <div style={{ width: `${(v / max) * 85}%`, minWidth: 2, height: 8, background: a.color, borderRadius: '0 4px 4px 0', opacity: hover && hover !== id ? 0.5 : 1 }} />
                      <span style={{ fontSize: 10.5, fontFamily: 'var(--font-mono)', color: 'var(--c-text-2)' }}>
                        {hover === id ? `${a.label}: ${v} nodos · ${fmtTime(p[a.key].time_ms)}` : v}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="card-surface" style={{ padding: '18px 20px' }}>
        <h3 style={{ margin: '0 0 10px', fontSize: 15, fontWeight: 700 }}>Respuestas del enrutamiento</h3>
        <div style={{ overflowX: 'auto' }}>
          <table style={tableStyle}>
            <thead>
              <tr>
                {['Trayecto', 'Distancia corta', 'Riesgo corta', 'Distancia segura', 'Riesgo segura', 'Reducción de riesgo', 'Poda A*'].map((h, i) => (
                  <th key={h} style={{ ...th, textAlign: i ? 'right' : 'left' }}>
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {pairs.map((p, i) => (
                <tr key={i} style={{ borderTop: '1px solid var(--c-border)' }}>
                  <td style={td}>{p.description}</td>
                  <td style={{ ...td, textAlign: 'right', fontFamily: 'var(--font-mono)' }}>{(p.dijkstra.distance_meters / 1000).toFixed(2)} km</td>
                  <td style={{ ...td, textAlign: 'right', fontFamily: 'var(--font-mono)' }}>{fmtInt(p.dijkstra.risk_score)}</td>
                  <td style={{ ...td, textAlign: 'right', fontFamily: 'var(--font-mono)' }}>{(p.astar_safest.distance_meters / 1000).toFixed(2)} km</td>
                  <td style={{ ...td, textAlign: 'right', fontFamily: 'var(--font-mono)' }}>{fmtInt(p.astar_safest.risk_score)}</td>
                  <td style={{ ...td, textAlign: 'right', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>{p.astar_safest.risk_reduction_pct}%</td>
                  <td style={{ ...td, textAlign: 'right', fontFamily: 'var(--font-mono)' }}>{p.astar_pruning_pct}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </>
  );
}

function Offline({ message }) {
  return (
    <div className="card-surface" style={{ padding: 28, textAlign: 'center' }}>
      <WifiOff size={28} color="var(--c-danger)" />
      <h3 style={{ margin: '10px 0 4px', fontSize: 16 }}>No se pudo conectar con el backend</h3>
      <p style={{ margin: 0, fontSize: 13, color: 'var(--c-text-2)' }}>
        Las gráficas solo muestran mediciones reales. Inicia FastAPI y recarga. <small>({message})</small>
      </p>
    </div>
  );
}

const SECTIONS = [
  { id: 'live', label: 'Jerarquía O(1) … O(n²) en vivo', icon: Layers },
  { id: 'sorting', label: 'Ordenamiento', icon: GitBranch },
  { id: 'spatial', label: 'KD-Tree vs. lineal', icon: Search },
  { id: 'clustering', label: 'DBSCAN', icon: Activity },
  { id: 'routing', label: 'Dijkstra vs. A*', icon: Network },
];

export default function ComplexityCharts() {
  // ?grafica=sorting|spatial|clustering|routing abre directamente una sección
  const [section, setSection] = useState(() => {
    const q = new URLSearchParams(window.location.search).get('grafica');
    return SECTIONS.some((s) => s.id === q) ? q : 'live';
  });
  const fase4 = useFase4();
  // El barrido en vivo se monta al visitarlo por primera vez y luego se conserva
  const [liveVisited, setLiveVisited] = useState(section === 'live');
  useEffect(() => {
    if (section === 'live') setLiveVisited(true);
  }, [section]);

  const body = useMemo(() => {
    if (section === 'live') return null;
    if (fase4.error) return <Offline message={fase4.error} />;
    if (!fase4.data) return <div style={{ padding: 40, textAlign: 'center', color: 'var(--c-text-2)' }}>Cargando resultados de la Fase 4…</div>;
    if (section === 'sorting') return <SortingCharts data={fase4.data} />;
    if (section === 'spatial') return <SpatialCharts data={fase4.data} />;
    if (section === 'clustering') return <ClusteringCharts data={fase4.data} />;
    return <RoutingCharts data={fase4.data} />;
  }, [section, fase4]);

  const hw = fase4.data?.metadata?.hardware;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', alignItems: 'center' }}>
        {SECTIONS.map((s) => {
          const Icon = s.icon;
          const active = section === s.id;
          return (
            <button key={s.id} type="button" onClick={() => setSection(s.id)} style={{ ...chip(active), display: 'inline-flex', alignItems: 'center', gap: 6, padding: '7px 13px' }}>
              <Icon size={14} />
              {s.label}
            </button>
          );
        })}
        {section !== 'live' && hw && (
          <span style={{ fontSize: 11.5, color: 'var(--c-text-2)', marginLeft: 'auto' }}>
            Fase 4 · {hw.cpu_count_logical} núcleos lógicos · Python {hw.python_version} · {hw.timestamp}
          </span>
        )}
      </div>
      {/* Las secciones montan aparte para que el barrido en vivo no se repita al cambiar de pestaña */}
      <div style={{ display: section === 'live' ? 'none' : 'contents' }}>{section !== 'live' && body}</div>
      <div style={{ display: section === 'live' ? 'contents' : 'none' }}>
        {liveVisited && <HierarchySweep />}
      </div>
    </div>
  );
}
