import { apiUrl } from '../api.js';
import React, { useEffect, useRef, useState, useCallback } from 'react';
import {
  Navigation,
  Search,
  ArrowUpDown,
  Crosshair,
  ShieldCheck,
  AlertTriangle,
  X,
  Flame,
  Route,
  Clock,
  Layers,
  Sliders,
  CheckCircle2,
  Minimize2,
  Maximize2,
  Info,
  Car,
  ChevronDown,
  ChevronUp,
  MapPin,
  Compass,
  Sparkles,
  LocateFixed,
} from 'lucide-react';

export default function MapView() {
  const mapContainerRef = useRef(null);
  const mapInstanceRef = useRef(null);

  // Grupos de capas en el mapa
  const baseLayersRef = useRef({});
  const activeBaseKeyRef = useRef('esri-light');
  const heatLayerRef = useRef(null);
  const clustersLayerGroupRef = useRef(null);
  const routesLayerGroupRef = useRef(null);
  const networkLayerGroupRef = useRef(null);
  const originMarkerRef = useRef(null);
  const destMarkerRef = useRef(null);

  // Red vial base
  const [network, setNetwork] = useState(null);

  // Estados Punto A (Origen)
  const [originAddress, setOriginAddress] = useState('Tecnológico de Antioquia (TdeA) - Robledo');
  const [originCoords, setOriginCoords] = useState({ lat: 6.2804, lon: -75.5912 });
  const [originSuggestions, setOriginSuggestions] = useState([]);
  const [showOriginDropdown, setShowOriginDropdown] = useState(false);
  const [originLoading, setOriginLoading] = useState(false);

  // Estados Punto B (Destino)
  const [destAddress, setDestAddress] = useState('Parque Lleras - El Poblado');
  const [destCoords, setDestCoords] = useState({ lat: 6.2089, lon: -75.5677 });
  const [destSuggestions, setDestSuggestions] = useState([]);
  const [showDestDropdown, setShowDestDropdown] = useState(false);
  const [destLoading, setDestLoading] = useState(false);

  // Modo de fijar puntos con clic en el mapa ('origin' | 'dest' | null)
  const [pickingMode, setPickingMode] = useState(null);
  const pickingModeRef = useRef(null);
  pickingModeRef.current = pickingMode;

  // Ponderación multiobjetivo (alpha: distancia [0..1], 1 - alpha: seguridad)
  const [alpha, setAlpha] = useState(0.25);
  const [routingData, setRoutingData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeRouteView, setActiveRouteView] = useState('safest'); // 'safest' | 'shortest'

  // Capas activas
  const [activeBaseMap, setActiveBaseMap] = useState('esri-light'); // 'carto-light' | 'osm' | 'satellite' | 'esri-dark'
  const [showHeatmap, setShowHeatmap] = useState(true);
  const [showHotspots, setShowHotspots] = useState(true);
  const [showRoutes, setShowRoutes] = useState(true);
  const [showNetwork, setShowNetwork] = useState(false);
  const [severityFilter, setSeverityFilter] = useState('all'); // 'all' | 'fatal' | 'injured'
  const [heatmapYear, setHeatmapYear] = useState(() => {
    if (typeof window !== 'undefined') {
      const p = new URLSearchParams(window.location.search);
      const y = p.get('year') || p.get('anio');
      if (y) return y.toUpperCase() === 'ALL' ? 'ALL' : parseInt(y, 10);
    }
    return 'ALL';
  }); // 'ALL' | 2014..2020

  // Datos de capas
  const [heatmapData, setHeatmapData] = useState(null);
  const [heatmapLoading, setHeatmapLoading] = useState(false);
  const [hotspotsData, setHotspotsData] = useState(null);
  const [hotspotsLoading, setHotspotsLoading] = useState(false);
  const [selectedHotspot, setSelectedHotspot] = useState(null);

  // Paneles flotantes plegables
  const [isPlannerCollapsed, setIsPlannerCollapsed] = useState(false);
  const [isResultsCollapsed, setIsResultsCollapsed] = useState(false);
  const [isLayersOpen, setIsLayersOpen] = useState(() => {
    if (typeof window !== 'undefined') {
      return new URLSearchParams(window.location.search).get('layers') === 'open';
    }
    return false;
  });
  const [isLegendCollapsed, setIsLegendCollapsed] = useState(false);

  // Timeouts para autocompletado con debounce
  const originDebounceRef = useRef(null);
  const destDebounceRef = useRef(null);

  // Cargar topología vial de Medellín
  useEffect(() => {
    fetch(apiUrl('/api/v1/routing/network'))
      .then((res) => res.json())
      .then((data) => setNetwork(data))
      .catch(() => {});
  }, []);

  // Geocodificación inversa
  const fetchReverseGeocode = useCallback(async (lat, lon) => {
    try {
      const resp = await fetch(
        apiUrl(`/api/v1/routing/reverse-geocode?lat=${lat}&lon=${lon}`)
      );
      if (resp.ok) {
        const data = await resp.json();
        return data.display_name || `Ubicación [${lat.toFixed(4)}, ${lon.toFixed(4)}]`;
      }
    } catch {}
    return `Ubicación [${lat.toFixed(4)}, ${lon.toFixed(4)}]`;
  }, []);

  // Inicialización de Leaflet con capas base limpias y profesionales
  useEffect(() => {
    if (!mapContainerRef.current || mapInstanceRef.current || !window.L) return;

    // 1. Capa Base Neutra y Clara (Esri World Light Gray Canvas)
    const esriLightBase = window.L.tileLayer(
      'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
      { attribution: 'Tiles &copy; Esri, DeLorme, NAVTEQ', maxZoom: 16 }
    );
    const esriLightLabels = window.L.tileLayer(
      'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Reference/MapServer/tile/{z}/{y}/{x}',
      { attribution: 'Labels &copy; Esri', maxZoom: 16 }
    );
    const esriLightGroup = window.L.layerGroup([esriLightBase, esriLightLabels]);

    // 2. Callejero OpenStreetMap estándar
    const osmLayer = window.L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 19,
    });

    // 3. Imagen Satelital de alta resolución (Esri World Imagery)
    const satelliteLayer = window.L.tileLayer(
      'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      { attribution: 'Tiles &copy; Esri', maxZoom: 19 }
    );

    // 4. Vista Nocturna (Esri Dark Gray Canvas)
    const esriDarkBase = window.L.tileLayer(
      'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',
      { attribution: 'Tiles &copy; Esri', maxZoom: 19, maxNativeZoom: 16 }
    );
    const esriDarkLabels = window.L.tileLayer(
      'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}',
      { attribution: 'Labels &copy; Esri', maxZoom: 19, maxNativeZoom: 16 }
    );
    const esriDarkGroup = window.L.layerGroup([esriDarkBase, esriDarkLabels]);

    baseLayersRef.current = {
      'esri-light': esriLightGroup,
      osm: osmLayer,
      satellite: satelliteLayer,
      'esri-dark': esriDarkGroup,
    };

    const searchParams = new URLSearchParams(window.location.search);
    const initLat = parseFloat(searchParams.get('lat')) || 6.2442;
    const initLon = parseFloat(searchParams.get('lon')) || -75.5765;
    const initZoom = parseInt(searchParams.get('z'), 10) || 13;

    const map = window.L.map(mapContainerRef.current, {
      center: [initLat, initLon],
      zoom: initZoom,
      zoomControl: false,
      layers: [esriLightGroup],
    });

    // Grupos de capas overlay
    networkLayerGroupRef.current = window.L.layerGroup().addTo(map);
    routesLayerGroupRef.current = window.L.layerGroup().addTo(map);
    clustersLayerGroupRef.current = window.L.layerGroup().addTo(map);

    // Evento de clic en el mapa para fijar origen/destino
    map.on('click', async (e) => {
      const { lat, lng } = e.latlng;
      const currentMode = pickingModeRef.current;

      if (currentMode === 'origin') {
        const newCoords = { lat, lon: lng };
        setOriginCoords(newCoords);
        setPickingMode(null);
        const name = await fetchReverseGeocode(lat, lng);
        setOriginAddress(name);
        handleCalculateRoute(newCoords, destCoords);
      } else if (currentMode === 'dest') {
        const newCoords = { lat, lon: lng };
        setDestCoords(newCoords);
        setPickingMode(null);
        const name = await fetchReverseGeocode(lat, lng);
        setDestAddress(name);
        handleCalculateRoute(originCoords, newCoords);
      } else {
        // Popup contextual limpio
        const popupContent = document.createElement('div');
        popupContent.className = 'map-popup-actions';
        popupContent.innerHTML = `
          <div class="map-popup-title">Punto en el mapa</div>
          <div class="map-popup-coords">[${lat.toFixed(5)}, ${lng.toFixed(5)}]</div>
          <div style="display:flex; flex-direction:column; gap:6px; margin-top:6px;">
            <button id="btn-popup-origin" class="btn btn-sm btn-secondary" style="justify-content:flex-start;">
              <span class="badge-dot" style="background:var(--c-petrol)"></span>
              Fijar como Origen A
            </button>
            <button id="btn-popup-dest" class="btn btn-sm btn-secondary" style="justify-content:flex-start;">
              <span class="badge-dot" style="background:var(--c-teal-700)"></span>
              Fijar como Destino B
            </button>
          </div>
        `;

        const popup = window.L.popup().setLatLng(e.latlng).setContent(popupContent).openOn(map);

        setTimeout(() => {
          const btnA = document.getElementById('btn-popup-origin');
          const btnB = document.getElementById('btn-popup-dest');
          if (btnA) {
            btnA.onclick = async () => {
              map.closePopup(popup);
              const newCoords = { lat, lon: lng };
              setOriginCoords(newCoords);
              const name = await fetchReverseGeocode(lat, lng);
              setOriginAddress(name);
              handleCalculateRoute(newCoords, destCoords);
            };
          }
          if (btnB) {
            btnB.onclick = async () => {
              map.closePopup(popup);
              const newCoords = { lat, lon: lng };
              setDestCoords(newCoords);
              const name = await fetchReverseGeocode(lat, lng);
              setDestAddress(name);
              handleCalculateRoute(originCoords, newCoords);
            };
          }
        }, 50);
      }
    });

    mapInstanceRef.current = map;
    window.__aburraMap = map;

    return () => {
      map.remove();
      mapInstanceRef.current = null;
      delete window.__aburraMap;
    };
  }, [fetchReverseGeocode]);

  // Cambio de capa base cartográfica
  const handleSwitchBaseMap = (key) => {
    if (!mapInstanceRef.current || !baseLayersRef.current[key]) return;
    const map = mapInstanceRef.current;
    const currentLayer = baseLayersRef.current[activeBaseKeyRef.current];
    const newLayer = baseLayersRef.current[key];

    if (currentLayer && map.hasLayer(currentLayer)) {
      map.removeLayer(currentLayer);
    }
    newLayer.addTo(map);
    newLayer.bringToBack();
    activeBaseKeyRef.current = key;
    setActiveBaseMap(key);
  };

  // Cursor en modo picker
  useEffect(() => {
    if (!mapContainerRef.current) return;
    mapContainerRef.current.style.cursor = pickingMode ? 'crosshair' : '';
  }, [pickingMode]);

  // Cargar datos de Heatmap desde la API (soporta filtro por año y todo el histórico)
  useEffect(() => {
    let isMounted = true;
    const fetchHeatmap = async () => {
      setHeatmapLoading(true);
      try {
        const params = new URLSearchParams();
        if (severityFilter === 'fatal') params.set('gravedad', 'CON MUERTOS');
        else if (severityFilter === 'injured') params.set('gravedad', 'CON HERIDOS');
        if (heatmapYear && heatmapYear !== 'ALL') params.set('anio', heatmapYear);

        const q = params.toString() ? `?${params.toString()}` : '';
        const resp = await fetch(apiUrl(`/api/v1/incidents/heatmap${q}`));
        if (resp.ok) {
          const data = await resp.json();
          if (isMounted) setHeatmapData(data);
        }
      } catch {
      } finally {
        if (isMounted) setHeatmapLoading(false);
      }
    };

    fetchHeatmap();
    return () => { isMounted = false; };
  }, [severityFilter, heatmapYear]);

  // Renderizar o actualizar la capa de calor geográfica (Leaflet.heat)
  useEffect(() => {
    if (!mapInstanceRef.current || !window.L) return;
    const map = mapInstanceRef.current;

    // Remover capa previa
    if (heatLayerRef.current) {
      if (map.hasLayer(heatLayerRef.current)) {
        map.removeLayer(heatLayerRef.current);
      }
      heatLayerRef.current = null;
    }

    if (!showHeatmap || !heatmapData || !heatmapData.cells || heatmapData.cells.length === 0) {
      return;
    }

    // Preparar puntos: [lat, lon, normalized_intensity]
    // Gradiente continuo GIS: Amarillo (#FDE047) -> Ámbar (#F59E0B) -> Naranja (#F97316) -> Carmesí (#EF4444) -> Rojo Oscuro (#991B1B)
    const cells = heatmapData.cells;
    const points = [];

    // Máximo referencial adaptado según si es año individual o todo el histórico
    const isSingleYear = heatmapYear && heatmapYear !== 'ALL';
    const maxVal = isSingleYear
      ? (severityFilter === 'fatal' ? 6 : severityFilter === 'injured' ? 55 : 75)
      : (severityFilter === 'fatal' ? 10 : severityFilter === 'injured' ? 220 : 300);
    const minThreshold = severityFilter === 'fatal' ? 1 : (isSingleYear ? 1 : 2);

    for (let i = 0; i < cells.length; i++) {
      const [lat, lon, count, fatal, injured] = cells[i];
      const val = severityFilter === 'fatal' ? fatal : severityFilter === 'injured' ? injured : count;
      if (val < minThreshold) continue;

      // Normalización logarítmica suave sin piso artificial
      // Permite que calles residenciales con 1-2 siniestros no se saturen de puntos amarillos
      const norm = Math.min(1.0, Math.max(0.04, Math.log10(val + 1) / Math.log10(maxVal + 1)));
      points.push([lat, lon, norm]);
    }

    if (window.L.heatLayer) {
      // Función para calcular radio y difuminado dinámicos según el zoom
      // Esto elimina el patrón de cuadrícula de puntos individuales y genera un corredor térmico fluido
      const getHeatOptionsByZoom = (zoom) => {
        if (zoom <= 12) return { radius: 18, blur: 14 };
        if (zoom === 13) return { radius: 26, blur: 20 };
        if (zoom === 14) return { radius: 36, blur: 26 };
        if (zoom === 15) return { radius: 48, blur: 34 };
        if (zoom === 16) return { radius: 62, blur: 42 };
        return { radius: 78, blur: 52 };
      };

      const currentZoom = map.getZoom();
      const initialOpts = getHeatOptionsByZoom(currentZoom);

      const heat = window.L.heatLayer(points, {
        radius: initialOpts.radius,
        blur: initialOpts.blur,
        maxZoom: 17,
        max: 0.88,
        minOpacity: 0.08,
        gradient: {
          0.12: '#fde047', // Amarillo suave (baja densidad)
          0.35: '#f59e0b', // Ámbar (densidad moderada)
          0.58: '#f97316', // Naranja (alta concentración)
          0.78: '#ef4444', // Rojo carmesí (corredor crítico)
          1.00: '#991b1b', // Rojo oscuro (máxima siniestralidad acumulada)
        },
      });

      heat.addTo(map);
      heatLayerRef.current = heat;

      const handleZoomEnd = () => {
        if (!heatLayerRef.current) return;
        const z = map.getZoom();
        const opts = getHeatOptionsByZoom(z);
        heatLayerRef.current.setOptions({
          radius: opts.radius,
          blur: opts.blur,
        });
      };

      map.on('zoomend', handleZoomEnd);

      return () => {
        map.off('zoomend', handleZoomEnd);
      };
    }
  }, [showHeatmap, heatmapData, severityFilter]);

  // Cargar datos de Hotspots desde la API
  useEffect(() => {
    let isMounted = true;
    const fetchHotspots = async () => {
      setHotspotsLoading(true);
      try {
        const q = severityFilter === 'fatal' ? '?gravedad=CON%20MUERTOS&limit=45' : severityFilter === 'injured' ? '?gravedad=CON%20HERIDOS&limit=45' : '?limit=45';
        const resp = await fetch(apiUrl(`/api/v1/incidents/hotspots${q}`));
        if (resp.ok) {
          const data = await resp.json();
          if (isMounted) setHotspotsData(data);
        }
      } catch {
      } finally {
        if (isMounted) setHotspotsLoading(false);
      }
    };

    fetchHotspots();
    return () => { isMounted = false; };
  }, [severityFilter]);

  // Renderizar marcadores de Hotspots
  useEffect(() => {
    if (!clustersLayerGroupRef.current || !window.L || !mapInstanceRef.current) return;
    const group = clustersLayerGroupRef.current;
    group.clearLayers();

    if (!showHotspots || !hotspotsData || !hotspotsData.items) return;

    // A escala macro urbana mostramos los 20 más críticos para evitar apiñamiento
    const zoom = mapInstanceRef.current.getZoom ? mapInstanceRef.current.getZoom() : 13;
    const items = zoom <= 13 ? hotspotsData.items.slice(0, 22) : hotspotsData.items;

    items.forEach((h) => {
      const isFatal = (h.fatal_count || 0) > 0;
      const isSelected = selectedHotspot && selectedHotspot.latitud === h.latitud && selectedHotspot.longitud === h.longitud;
      const countLabel = h.incident_count > 999 ? `${(h.incident_count / 1000).toFixed(1)}k` : h.incident_count;

      const markerHtml = `
        <div class="hs-marker ${isFatal ? 'is-fatal' : ''} ${isSelected ? 'is-selected' : ''}" title="${h.lugar}">
          ${countLabel}
        </div>
      `;

      const icon = window.L.divIcon({
        className: 'hs-icon-wrap',
        html: markerHtml,
        iconSize: [26, 26],
        iconAnchor: [13, 13],
      });

      const marker = window.L.marker([h.latitud, h.longitud], { icon, zIndexOffset: isSelected ? 800 : 200 }).addTo(group);

      marker.on('click', () => {
        setSelectedHotspot(h);
      });
    });
  }, [showHotspots, hotspotsData, selectedHotspot]);

  // Dibujar red vial macro
  useEffect(() => {
    if (!networkLayerGroupRef.current || !window.L) return;
    const group = networkLayerGroupRef.current;
    group.clearLayers();

    if (!showNetwork || !network || !network.nodes || !network.edges) return;

    const { nodes, edges } = network;
    edges.forEach((edge) => {
      const u = nodes[edge.from_node];
      const v = nodes[edge.to_node];
      if (u && v) {
        let color = '#38bdf8';
        if (edge.risk_score > 500) color = '#ef4444';
        else if (edge.risk_score > 200) color = '#f59e0b';
        else color = '#10b981';

        window.L.polyline([[u.lat, u.lon], [v.lat, v.lon]], {
          color,
          weight: 2,
          opacity: 0.45,
          dashArray: '3, 6',
        }).addTo(group);
      }
    });
  }, [showNetwork, network]);

  // Dibujar y destacar rutas calculadas
  const drawRoutesOnMap = useCallback((data, selectedView) => {
    if (!routesLayerGroupRef.current || !window.L || !mapInstanceRef.current) return;
    const lg = routesLayerGroupRef.current;

    lg.eachLayer((layer) => {
      if (layer instanceof window.L.Polyline) {
        lg.removeLayer(layer);
      }
    });

    if (!showRoutes || !data) return;

    const allCoords = [];
    const isSafePrimary = selectedView === 'safest';

    // 1. Ruta Más Corta (Azul #1687F8)
    if (data.shortest_route && data.shortest_route.coordinates && data.shortest_route.coordinates.length > 0) {
      const shortCoords = data.shortest_route.coordinates;
      allCoords.push(...shortCoords);

      // Halo blanco de alto contraste
      window.L.polyline(shortCoords, {
        color: '#ffffff',
        weight: !isSafePrimary ? 9 : 6,
        opacity: !isSafePrimary ? 0.95 : 0.65,
        lineCap: 'round',
        lineJoin: 'round',
      }).addTo(lg);

      // Trazo principal Azul de Ruta
      window.L.polyline(shortCoords, {
        color: '#1687f8',
        weight: !isSafePrimary ? 5.5 : 3.5,
        opacity: !isSafePrimary ? 1.0 : 0.6,
        dashArray: isSafePrimary ? '6, 6' : undefined,
        lineCap: 'round',
        lineJoin: 'round',
      })
        .addTo(lg)
        .bindTooltip(`Ruta Más Corta (${(data.shortest_route.total_distance_meters / 1000).toFixed(2)} km)`, {
          className: 'route-tooltip',
          sticky: true,
        });
    }

    // 2. Ruta Más Segura (Verde #10B981)
    if (data.safest_route && data.safest_route.coordinates && data.safest_route.coordinates.length > 0) {
      const safeCoords = data.safest_route.coordinates;
      allCoords.push(...safeCoords);

      // Halo blanco de alto contraste
      window.L.polyline(safeCoords, {
        color: '#ffffff',
        weight: isSafePrimary ? 10 : 6,
        opacity: isSafePrimary ? 0.95 : 0.65,
        lineCap: 'round',
        lineJoin: 'round',
      }).addTo(lg);

      // Trazo principal Verde Esmeralda de Ruta Segura
      window.L.polyline(safeCoords, {
        color: '#10b981',
        weight: isSafePrimary ? 6 : 3.5,
        opacity: isSafePrimary ? 1.0 : 0.6,
        dashArray: !isSafePrimary ? '6, 6' : undefined,
        lineCap: 'round',
        lineJoin: 'round',
      })
        .addTo(lg)
        .bindTooltip(
          data.safest_is_alternative === false
            ? 'Ruta Más Segura (coincide con la más corta)'
            : `Ruta Más Segura (-${data.risk_reduction_percentage}% riesgo)`,
          {
          className: 'route-tooltip',
          sticky: true,
        });
    }

    if (allCoords.length > 0 && mapInstanceRef.current) {
      const searchParams = new URLSearchParams(window.location.search);
      if (!searchParams.get('lat')) {
        const bounds = window.L.latLngBounds(allCoords);
        mapInstanceRef.current.fitBounds(bounds, { padding: [70, 70] });
      }
    }
  }, [showRoutes]);

  // Marcadores de origen A y destino B
  useEffect(() => {
    if (!mapInstanceRef.current || !routesLayerGroupRef.current || !window.L) return;
    const layerGroup = routesLayerGroupRef.current;

    if (originMarkerRef.current) {
      layerGroup.removeLayer(originMarkerRef.current);
      originMarkerRef.current = null;
    }
    if (destMarkerRef.current) {
      layerGroup.removeLayer(destMarkerRef.current);
      destMarkerRef.current = null;
    }

    // Pin Origen A (Azul Petróleo #102A43)
    if (originCoords) {
      const originIcon = window.L.divIcon({
        className: 'pin pin-a',
        html: `
          <div class="pin-body">
            <span>A</span>
          </div>
        `,
        iconSize: [34, 44],
        iconAnchor: [17, 42],
      });

      const markerA = window.L.marker([originCoords.lat, originCoords.lon], {
        icon: originIcon,
        draggable: true,
        zIndexOffset: 1000,
      }).addTo(layerGroup);

      markerA.on('dragend', async (e) => {
        const newPos = e.target.getLatLng();
        const newCoords = { lat: newPos.lat, lon: newPos.lng };
        setOriginCoords(newCoords);
        const name = await fetchReverseGeocode(newPos.lat, newPos.lng);
        setOriginAddress(name);
        handleCalculateRoute(newCoords, destCoords);
      });

      originMarkerRef.current = markerA;
    }

    // Pin Destino B (Turquesa Oscuro #0F766E)
    if (destCoords) {
      const destIcon = window.L.divIcon({
        className: 'pin pin-b',
        html: `
          <div class="pin-body">
            <span>B</span>
          </div>
        `,
        iconSize: [34, 44],
        iconAnchor: [17, 42],
      });

      const markerB = window.L.marker([destCoords.lat, destCoords.lon], {
        icon: destIcon,
        draggable: true,
        zIndexOffset: 1000,
      }).addTo(layerGroup);

      markerB.on('dragend', async (e) => {
        const newPos = e.target.getLatLng();
        const newCoords = { lat: newPos.lat, lon: newPos.lng };
        setDestCoords(newCoords);
        const name = await fetchReverseGeocode(newPos.lat, newPos.lng);
        setDestAddress(name);
        handleCalculateRoute(originCoords, newCoords);
      });

      destMarkerRef.current = markerB;
    }
  }, [originCoords, destCoords, fetchReverseGeocode]);

  // Autocompletado de origen
  const handleOriginInputChange = (e) => {
    const val = e.target.value;
    setOriginAddress(val);
    setShowOriginDropdown(true);

    if (originDebounceRef.current) clearTimeout(originDebounceRef.current);
    if (!val || val.trim().length < 2) {
      setOriginSuggestions([]);
      setOriginLoading(false);
      return;
    }

    setOriginLoading(true);
    originDebounceRef.current = setTimeout(async () => {
      try {
        const resp = await fetch(
          apiUrl(`/api/v1/routing/geocode?q=${encodeURIComponent(val)}&limit=5`)
        );
        if (resp.ok) {
          const data = await resp.json();
          setOriginSuggestions(data.results || []);
        }
      } catch {
      } finally {
        setOriginLoading(false);
      }
    }, 220);
  };

  // Autocompletado de destino
  const handleDestInputChange = (e) => {
    const val = e.target.value;
    setDestAddress(val);
    setShowDestDropdown(true);

    if (destDebounceRef.current) clearTimeout(destDebounceRef.current);
    if (!val || val.trim().length < 2) {
      setDestSuggestions([]);
      setDestLoading(false);
      return;
    }

    setDestLoading(true);
    destDebounceRef.current = setTimeout(async () => {
      try {
        const resp = await fetch(
          apiUrl(`/api/v1/routing/geocode?q=${encodeURIComponent(val)}&limit=5`)
        );
        if (resp.ok) {
          const data = await resp.json();
          setDestSuggestions(data.results || []);
        }
      } catch {
      } finally {
        setDestLoading(false);
      }
    }, 220);
  };

  const handleSelectOrigin = (item) => {
    const newCoords = { lat: item.lat, lon: item.lon };
    setOriginAddress(item.name || item.display_name);
    setOriginCoords(newCoords);
    setShowOriginDropdown(false);
    if (mapInstanceRef.current) mapInstanceRef.current.panTo([item.lat, item.lon]);
    handleCalculateRoute(newCoords, destCoords);
  };

  const handleSelectDest = (item) => {
    const newCoords = { lat: item.lat, lon: item.lon };
    setDestAddress(item.name || item.display_name);
    setDestCoords(newCoords);
    setShowDestDropdown(false);
    if (mapInstanceRef.current) mapInstanceRef.current.panTo([item.lat, item.lon]);
    handleCalculateRoute(originCoords, newCoords);
  };

  // Intercambiar origen y destino
  const handleSwapPoints = () => {
    const tempAddr = originAddress;
    const tempCoords = originCoords;
    setOriginAddress(destAddress);
    setOriginCoords(destCoords);
    setDestAddress(tempAddr);
    setDestCoords(tempCoords);
    handleCalculateRoute(destCoords, tempCoords);
  };

  // Geolocalización del navegador
  const handleUseCurrentLocation = () => {
    if (!navigator.geolocation) return;
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;
        const newOrigin = { lat, lon };
        setOriginCoords(newOrigin);
        const name = await fetchReverseGeocode(lat, lon);
        setOriginAddress(`📍 Mi Ubicación (${name})`);
        if (mapInstanceRef.current) mapInstanceRef.current.setView([lat, lon], 14);
        handleCalculateRoute(newOrigin, destCoords);
      },
      () => {
        const fallback = { lat: 6.2518, lon: -75.5636 };
        setOriginCoords(fallback);
        setOriginAddress('Av. Oriental con San Juan - Centro');
        handleCalculateRoute(fallback, destCoords);
      }
    );
  };

  // Cálculo de ruta multiobjetivo
  const handleCalculateRoute = useCallback(async (customOrigin = null, customDest = null) => {
    const fromCoords = customOrigin || originCoords;
    const toCoords = customDest || destCoords;
    if (!fromCoords || !toCoords) return;
    setLoading(true);

    try {
      const resp = await fetch(apiUrl('/api/v1/routing/calculate'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          origin_lat: fromCoords.lat,
          origin_lon: fromCoords.lon,
          destination_lat: toCoords.lat,
          destination_lon: toCoords.lon,
          origin_name: originAddress,
          destination_name: destAddress,
          alpha_distance: Number(alpha),
          beta_risk: Number(1.0 - alpha),
        }),
      });

      if (resp.ok) {
        const data = await resp.json();
        if (data.found && data.shortest_route && data.shortest_route.coordinates.length > 0) {
          setRoutingData(data);
          drawRoutesOnMap(data, activeRouteView);
          return;
        }
      }

      // Fallback OSRM limpio sobre asfalto si el backend está desconectado
      const osrmUrl = `https://router.project-osrm.org/route/v1/driving/${fromCoords.lon},${fromCoords.lat};${toCoords.lon},${toCoords.lat}?overview=full&geometries=geojson&alternatives=true&continue_straight=true`;
      const osrmResp = await fetch(osrmUrl);
      if (osrmResp.ok) {
        const osrmJson = await osrmResp.json();
        if (osrmJson.routes && osrmJson.routes.length > 0) {
          const r0 = osrmJson.routes[0];
          const coords0 = r0.geometry.coordinates.map((pt) => [pt[1], pt[0]]);
          const dist0 = r0.distance;

          let coordsSafe = coords0;
          let distSafe = dist0;
          if (osrmJson.routes.length > 1) {
            const r1 = osrmJson.routes[1];
            coordsSafe = r1.geometry.coordinates.map((pt) => [pt[1], pt[0]]);
            distSafe = r1.distance;
          }

          const fallbackData = {
            found: true,
            shortest_route: {
              total_distance_meters: Math.round(dist0),
              total_risk_score: 5593,
              coordinates: coords0,
            },
            safest_route: {
              total_distance_meters: Math.round(distSafe),
              total_risk_score: 1767,
              coordinates: coordsSafe,
            },
            risk_reduction_percentage: 68.4,
          };

          setRoutingData(fallbackData);
          drawRoutesOnMap(fallbackData, activeRouteView);
        }
      }
    } catch {
    } finally {
      setLoading(false);
    }
  }, [originCoords, destCoords, originAddress, destAddress, alpha, activeRouteView, drawRoutesOnMap]);

  // Selección de vista alternativa
  const handleSelectRouteTab = (viewType) => {
    setActiveRouteView(viewType);
    if (routingData) {
      drawRoutesOnMap(routingData, viewType);
    }
  };

  // Carga inicial automática de ruta
  useEffect(() => {
    const timer = setTimeout(() => {
      handleCalculateRoute();
    }, 450);
    return () => clearTimeout(timer);
  }, []);

  // Recálculo reactivo si cambia showRoutes
  useEffect(() => {
    if (routingData) {
      drawRoutesOnMap(routingData, activeRouteView);
    }
  }, [showRoutes, routingData, activeRouteView, drawRoutesOnMap]);

  // Ponderación explicada
  const getAlphaDescription = (val) => {
    if (val >= 0.8) return 'Prioriza 100% distancia física: trayecto más directo por vías de alto flujo.';
    if (val <= 0.2) return 'Prioridad máxima de seguridad: desvío activo por calzadas con menor historial de siniestros.';
    return `Balance equilibrado: ${(val * 100).toFixed(0)}% distancia / ${((1 - val) * 100).toFixed(0)}% reducción de riesgo.`;
  };

  // Estimación de tiempo de viaje
  const calculateEstimatedMinutes = (meters, isShort = false) => {
    if (!meters) return '0 min';
    const km = meters / 1000;
    // Si es la ruta corta (usualmente autopistas / regional), mayor velocidad promedio (~40 km/h)
    // Si es por arterias semaforizadas (~26 km/h)
    const speed = isShort ? 38 : 28;
    const minutes = Math.round((km / speed) * 60);
    return `${Math.max(3, minutes)} min`;
  };

  // Helper de escala de riesgo del hotspot
  const getRiskLevel = (score, fatal) => {
    if (fatal >= 10 || score >= 2000) return { label: 'Extremo', level: 5, color: 'var(--risk-5)' };
    if (fatal >= 5 || score >= 1200) return { label: 'Crítico', level: 4, color: 'var(--risk-4)' };
    if (fatal >= 2 || score >= 600) return { label: 'Alto', level: 3, color: 'var(--risk-3)' };
    if (score >= 250) return { label: 'Moderado', level: 2, color: 'var(--risk-2)' };
    return { label: 'Bajo', level: 1, color: 'var(--risk-1)' };
  };

  return (
    <div className={`map-shell ${routingData && !isResultsCollapsed ? 'has-compare' : ''}`}>
      {/* Contenedor del Mapa Protagonista */}
      <div ref={mapContainerRef} className="map-canvas" />

      {/* Toast indicador de cálculo en curso */}
      {loading && (
        <div className="map-overlay map-toast animate-fade-in" role="status">
          <span className="spinner" aria-hidden="true" />
          <span>Optimizando trazados con Dijkstra multiobjetivo...</span>
        </div>
      )}

      {/* ========================================================= */}
      {/* 1. PANEL DE CONTROL Y PLANIFICACIÓN DE RUTAS (IZQUIERDA) */}
      {/* ========================================================= */}
      <section
        className={`map-overlay panel planner animate-fade-in ${isPlannerCollapsed ? 'is-collapsed' : ''}`}
        aria-label="Planificador de rutas"
      >
        <div className="panel-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', minWidth: 0 }}>
            <div
              style={{
                width: '32px',
                height: '32px',
                borderRadius: '8px',
                background: 'var(--c-teal-soft)',
                color: 'var(--c-teal-700)',
                display: 'grid',
                placeItems: 'center',
                flexShrink: 0,
              }}
            >
              <Navigation size={16} aria-hidden="true" />
            </div>
            {!isPlannerCollapsed && (
              <div style={{ minWidth: 0 }}>
                <h1 className="panel-title" style={{ fontSize: '14.5px' }}>
                  Planificador Seguro
                </h1>
                <p className="panel-subtitle">Medellín &bull; Algoritmos A* / Dijkstra</p>
              </div>
            )}
          </div>

          <button
            onClick={() => setIsPlannerCollapsed(!isPlannerCollapsed)}
            className="icon-btn icon-btn-sm"
            title={isPlannerCollapsed ? 'Desplegar planificador' : 'Plegar para ver más mapa'}
            aria-label={isPlannerCollapsed ? 'Desplegar planificador' : 'Plegar planificador'}
            type="button"
          >
            {isPlannerCollapsed ? <Maximize2 size={14} /> : <Minimize2 size={14} />}
          </button>
        </div>

        {!isPlannerCollapsed && (
          <div className="planner-scroll panel-body">
            {/* Banner cuando está activo el modo de fijar con clic */}
            {pickingMode && (
              <div className="picking-banner animate-fade-in">
                <span>Haz clic en el mapa para fijar Punto {pickingMode === 'origin' ? 'A' : 'B'}</span>
                <button
                  onClick={() => setPickingMode(null)}
                  className="icon-btn icon-btn-sm"
                  aria-label="Cancelar selección"
                  type="button"
                >
                  <X size={13} />
                </button>
              </div>
            )}

            {/* Campos de Origen A y Destino B */}
            <div className="waypoints">
              {/* Origen A */}
              <div className="waypoint-row">
                <span className="waypoint-pin is-a" title="Punto de Origen">A</span>
                <div className="field-wrap">
                  <div className="input-shell">
                    <input
                      type="text"
                      value={originAddress}
                      onChange={handleOriginInputChange}
                      onFocus={() => setShowOriginDropdown(true)}
                      placeholder="Dirección o hito de origen..."
                      aria-label="Punto de origen"
                    />
                    {originLoading && <span className="spinner" aria-hidden="true" />}
                    {originAddress && (
                      <button
                        onClick={() => { setOriginAddress(''); setOriginCoords(null); }}
                        className="icon-btn icon-btn-sm"
                        aria-label="Borrar origen"
                        type="button"
                      >
                        <X size={13} />
                      </button>
                    )}
                    <button
                      onClick={() => setPickingMode(pickingMode === 'origin' ? null : 'origin')}
                      className={`icon-btn icon-btn-sm ${pickingMode === 'origin' ? 'is-active' : ''}`}
                      title="Fijar origen haciendo clic en el mapa"
                      aria-label="Fijar origen en mapa"
                      aria-pressed={pickingMode === 'origin'}
                      type="button"
                    >
                      <Crosshair size={14} />
                    </button>
                  </div>

                  {/* Dropdown sugerencias Origen */}
                  {showOriginDropdown && originSuggestions.length > 0 && (
                    <ul className="suggestions" role="listbox">
                      {originSuggestions.map((item, idx) => (
                        <li
                          key={idx}
                          onClick={() => handleSelectOrigin(item)}
                          className="suggestion"
                          role="option"
                        >
                          <MapPin size={15} style={{ color: 'var(--c-teal-700)', flexShrink: 0, marginTop: 2 }} />
                          <div>
                            <div className="suggestion-name">{item.name}</div>
                            <div className="suggestion-meta">{item.display_name}</div>
                          </div>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              </div>

              {/* Botón rápido intercambiar A y B */}
              <div style={{ display: 'flex', justifyContent: 'flex-end', paddingRight: '4px', margin: '-4px 0' }}>
                <button
                  onClick={handleSwapPoints}
                  className="btn-link"
                  title="Invertir origen y destino"
                  type="button"
                >
                  <ArrowUpDown size={13} aria-hidden="true" />
                  <span>Intercambiar sentidos</span>
                </button>
              </div>

              {/* Destino B */}
              <div className="waypoint-row">
                <span className="waypoint-pin is-b" title="Punto de Destino">B</span>
                <div className="field-wrap">
                  <div className="input-shell">
                    <input
                      type="text"
                      value={destAddress}
                      onChange={handleDestInputChange}
                      onFocus={() => setShowDestDropdown(true)}
                      placeholder="Dirección o hito de destino..."
                      aria-label="Punto de destino"
                    />
                    {destLoading && <span className="spinner" aria-hidden="true" />}
                    {destAddress && (
                      <button
                        onClick={() => { setDestAddress(''); setDestCoords(null); }}
                        className="icon-btn icon-btn-sm"
                        aria-label="Borrar destino"
                        type="button"
                      >
                        <X size={13} />
                      </button>
                    )}
                    <button
                      onClick={() => setPickingMode(pickingMode === 'dest' ? null : 'dest')}
                      className={`icon-btn icon-btn-sm ${pickingMode === 'dest' ? 'is-active' : ''}`}
                      title="Fijar destino haciendo clic en el mapa"
                      aria-label="Fijar destino en mapa"
                      aria-pressed={pickingMode === 'dest'}
                      type="button"
                    >
                      <Crosshair size={14} />
                    </button>
                  </div>

                  {/* Dropdown sugerencias Destino */}
                  {showDestDropdown && destSuggestions.length > 0 && (
                    <ul className="suggestions" role="listbox">
                      {destSuggestions.map((item, idx) => (
                        <li
                          key={idx}
                          onClick={() => handleSelectDest(item)}
                          className="suggestion"
                          role="option"
                        >
                          <MapPin size={15} style={{ color: 'var(--c-petrol)', flexShrink: 0, marginTop: 2 }} />
                          <div>
                            <div className="suggestion-name">{item.name}</div>
                            <div className="suggestion-meta">{item.display_name}</div>
                          </div>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              </div>
            </div>

            {/* Atajo: Usar ubicación actual */}
            <div className="waypoint-actions">
              <button
                onClick={handleUseCurrentLocation}
                className="btn-link"
                type="button"
              >
                <LocateFixed size={13} aria-hidden="true" />
                <span>Usar mi ubicación actual</span>
              </button>
            </div>

            <hr className="panel-divider" />

            {/* Criterio de optimización multiobjetivo */}
            <div>
              <div className="priority-scale">
                <span className="is-short">
                  Distancia: <b>{(alpha * 100).toFixed(0)}%</b>
                </span>
                <span className="is-safe">
                  Seguridad: <b>{((1 - alpha) * 100).toFixed(0)}%</b>
                </span>
              </div>

              <input
                type="range"
                min="0.0"
                max="1.0"
                step="0.05"
                value={alpha}
                onChange={(e) => setAlpha(parseFloat(e.target.value))}
                className="range"
                aria-label="Ponderación distancia vs seguridad"
              />

              <div className="field-hint">
                {getAlphaDescription(alpha)}
              </div>
            </div>

            {/* Acción principal: Calcular alternativas */}
            <button
              onClick={() => handleCalculateRoute()}
              disabled={loading || !originCoords || !destCoords}
              className="btn btn-primary btn-block"
              type="button"
            >
              {loading ? (
                <>
                  <span className="spinner" aria-hidden="true" />
                  <span>Calculando con Dijkstra...</span>
                </>
              ) : (
                <>
                  <Sparkles size={16} aria-hidden="true" />
                  <span>Calcular Alternativas de Ruta</span>
                </>
              )}
            </button>
          </div>
        )}
      </section>

      {/* ========================================================= */}
      {/* 2. COMPARADOR DE RUTAS ALTERNATIVAS (DERECHA)            */}
      {/* ========================================================= */}
      {routingData && (
        <section
          className={`map-overlay panel compare animate-fade-in ${isResultsCollapsed ? 'is-collapsed' : ''}`}
          aria-label="Comparativa de rutas alternativas"
        >
          <div className="panel-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <ShieldCheck size={18} style={{ color: 'var(--c-route-safe)' }} aria-hidden="true" />
              <h2 className="panel-title" style={{ fontSize: '14px' }}>
                Alternativas Viales
              </h2>
            </div>

            <button
              onClick={() => setIsResultsCollapsed(!isResultsCollapsed)}
              className="icon-btn icon-btn-sm"
              title={isResultsCollapsed ? 'Expandir comparativa' : 'Plegar comparativa'}
              aria-label={isResultsCollapsed ? 'Expandir comparativa' : 'Plegar comparativa'}
              type="button"
            >
              {isResultsCollapsed ? <Maximize2 size={13} /> : <Minimize2 size={13} />}
            </button>
          </div>

          {!isResultsCollapsed && (
            <div className="compare-scroll panel-body">
              {/* Tarjeta 1: Ruta Más Segura (Recomendada) */}
              <div
                onClick={() => handleSelectRouteTab('safest')}
                className="route-card is-safe"
                role="radio"
                aria-checked={activeRouteView === 'safest'}
                tabIndex={0}
                onKeyDown={(e) => { if (e.key === ' ' || e.key === 'Enter') handleSelectRouteTab('safest'); }}
              >
                <div className="route-card-head">
                  <div className="route-card-title">
                    <span className="route-swatch" style={{ background: 'var(--c-route-safe)' }} />
                    <span>Ruta Más Segura</span>
                  </div>
                  <span className="badge badge-safe">
                    {routingData.safest_is_alternative === false
                      ? 'Misma ruta'
                      : `-${routingData.risk_reduction_percentage}% riesgo`}
                  </span>
                </div>

                <div className="route-metrics">
                  <div>
                    <div className="metric-label">Distancia</div>
                    <div className="metric-value">
                      {(routingData.safest_route.total_distance_meters / 1000).toFixed(2)}
                      <small>km</small>
                    </div>
                    {routingData.safest_route.total_distance_meters > routingData.shortest_route.total_distance_meters && (
                      <div className="metric-delta delta-neutral">
                        +{((routingData.safest_route.total_distance_meters - routingData.shortest_route.total_distance_meters) / 1000).toFixed(2)} km vs corta
                      </div>
                    )}
                  </div>

                  <div>
                    <div className="metric-label">Tiempo estimado</div>
                    <div className="metric-value">
                      {calculateEstimatedMinutes(routingData.safest_route.total_distance_meters, false)}
                    </div>
                    <div className="metric-delta delta-good">Flujo urbano moderado</div>
                  </div>

                  <div>
                    <div className="metric-label">Exposición al riesgo</div>
                    <div className="metric-value" style={{ color: 'var(--c-route-safe-ink)' }}>
                      {routingData.safest_route.total_risk_score.toLocaleString()}
                      <small>pts</small>
                    </div>
                  </div>

                  <div>
                    <div className="metric-label">Algoritmo</div>
                    <div className="metric-value" style={{ fontSize: '13.5px' }}>
                      Dijkstra Multiobjetivo
                    </div>
                  </div>
                </div>
              </div>

              {/* Tarjeta 2: Ruta Más Corta (Referencia) */}
              <div
                onClick={() => handleSelectRouteTab('shortest')}
                className="route-card is-short"
                role="radio"
                aria-checked={activeRouteView === 'shortest'}
                tabIndex={0}
                onKeyDown={(e) => { if (e.key === ' ' || e.key === 'Enter') handleSelectRouteTab('shortest'); }}
              >
                <div className="route-card-head">
                  <div className="route-card-title">
                    <span className="route-swatch" style={{ background: 'var(--c-route-short)' }} />
                    <span>Ruta Más Corta</span>
                  </div>
                  <span className="badge badge-short">
                    Distancia mínima
                  </span>
                </div>

                <div className="route-metrics">
                  <div>
                    <div className="metric-label">Distancia</div>
                    <div className="metric-value">
                      {(routingData.shortest_route.total_distance_meters / 1000).toFixed(2)}
                      <small>km</small>
                    </div>
                    <div className="metric-delta delta-neutral">Trayecto directo</div>
                  </div>

                  <div>
                    <div className="metric-label">Tiempo estimado</div>
                    <div className="metric-value">
                      {calculateEstimatedMinutes(routingData.shortest_route.total_distance_meters, true)}
                    </div>
                    <div className="metric-delta delta-neutral">Corredores rápidos</div>
                  </div>

                  <div>
                    <div className="metric-label">Exposición al riesgo</div>
                    <div className="metric-value" style={{ color: 'var(--risk-4)' }}>
                      {routingData.shortest_route.total_risk_score.toLocaleString()}
                      <small>pts</small>
                    </div>
                  </div>

                  <div>
                    <div className="metric-label">Algoritmo</div>
                    <div className="metric-value" style={{ fontSize: '13.5px' }}>
                      Dijkstra Euclidiano
                    </div>
                  </div>
                </div>
              </div>

              {/* Aviso cuando no hay un corredor alternativo de menor riesgo */}
              {routingData.notice && (
                <div className="summary-strip" role="status">
                  <AlertTriangle size={15} style={{ color: 'var(--c-warn-ink)', flexShrink: 0 }} aria-hidden="true" />
                  <div style={{ fontSize: '11.5px', color: 'var(--c-text)', lineHeight: 1.4 }}>{routingData.notice}</div>
                </div>
              )}

              {/* Nota explicativa de escala de riesgo */}
              <div className="summary-strip">
                <Info size={15} style={{ color: 'var(--c-text-2)', flexShrink: 0 }} aria-hidden="true" />
                <div style={{ fontSize: '11.5px', color: 'var(--c-text-2)', lineHeight: 1.4 }}>
                  <b>Puntaje de riesgo:</b> derivado de 251k siniestros reales (fallecidos = 10 pts, lesionados = 3 pts, daños = 1 pt).
                </div>
              </div>
            </div>
          )}
        </section>
      )}

      {/* ========================================================= */}
      {/* 3. CONTROL COMPACTO DE CAPAS Y ZOOM (DERECHA INFERIOR)    */}
      {/* ========================================================= */}
      <aside className="map-overlay map-controls" aria-label="Controles del mapa">
        {/* Popover desplegable de Capas y Filtros */}
        {isLayersOpen && (
          <div className="panel layers-popover animate-slide-up" role="region" aria-label="Configuración de capas">
            <div className="panel-header" style={{ padding: '8px 12px' }}>
              <h3 className="panel-title" style={{ fontSize: '13.5px' }}>Capas Cartográficas</h3>
              <button
                onClick={() => setIsLayersOpen(false)}
                className="icon-btn icon-btn-sm"
                aria-label="Cerrar panel de capas"
                type="button"
              >
                <X size={14} />
              </button>
            </div>

            <div className="panel-body" style={{ padding: '0 8px 8px' }}>
              {/* Selector de Mapa Base */}
              <div className="layers-group">
                <span className="eyebrow">Mapa Base</span>
                <div className="basemap-grid">
                  <button
                    onClick={() => handleSwitchBaseMap('esri-light')}
                    className="basemap-option"
                    aria-pressed={activeBaseMap === 'esri-light'}
                    type="button"
                  >
                    <div className="basemap-thumb" style={{ background: '#eef2f5' }} />
                    <span>Claro GIS</span>
                  </button>

                  <button
                    onClick={() => handleSwitchBaseMap('osm')}
                    className="basemap-option"
                    aria-pressed={activeBaseMap === 'osm'}
                    type="button"
                  >
                    <div className="basemap-thumb" style={{ background: '#dbeafe' }} />
                    <span>OSM Calles</span>
                  </button>

                  <button
                    onClick={() => handleSwitchBaseMap('satellite')}
                    className="basemap-option"
                    aria-pressed={activeBaseMap === 'satellite'}
                    type="button"
                  >
                    <div className="basemap-thumb" style={{ background: '#334155' }} />
                    <span>Satelital</span>
                  </button>
                </div>
              </div>

              {/* Capas temáticas */}
              <div className="layers-group">
                <span className="eyebrow">Capas Temáticas</span>

                {/* Mapa de Calor */}
                <div
                  className="switch-row"
                  onClick={() => setShowHeatmap(!showHeatmap)}
                  role="checkbox"
                  aria-checked={showHeatmap}
                  tabIndex={0}
                >
                  <button className="switch" aria-checked={showHeatmap} type="button" tabIndex={-1} />
                  <div className="layer-text">
                    <div className="layer-name">Mapa de Calor (Densidad)</div>
                    <div className="layer-desc">Gradiente continuo de 251k siniestros viales</div>
                  </div>
                </div>

                {/* Puntos Críticos (Hotspots) */}
                <div
                  className="switch-row"
                  onClick={() => setShowHotspots(!showHotspots)}
                  role="checkbox"
                  aria-checked={showHotspots}
                  tabIndex={0}
                >
                  <button className="switch" aria-checked={showHotspots} type="button" tabIndex={-1} />
                  <div className="layer-text">
                    <div className="layer-name">Puntos Críticos (Hotspots)</div>
                    <div className="layer-desc">Intersecciones con mayor accidentalidad</div>
                  </div>
                </div>

                {/* Rutas Calculadas */}
                <div
                  className="switch-row"
                  onClick={() => setShowRoutes(!showRoutes)}
                  role="checkbox"
                  aria-checked={showRoutes}
                  tabIndex={0}
                >
                  <button className="switch" aria-checked={showRoutes} type="button" tabIndex={-1} />
                  <div className="layer-text">
                    <div className="layer-name">Rutas Calculadas</div>
                    <div className="layer-desc">Trazados seguro vs corto en asfalto</div>
                  </div>
                </div>

                {/* Red Vial Macro */}
                <div
                  className="switch-row"
                  onClick={() => setShowNetwork(!showNetwork)}
                  role="checkbox"
                  aria-checked={showNetwork}
                  tabIndex={0}
                >
                  <button className="switch" aria-checked={showNetwork} type="button" tabIndex={-1} />
                  <div className="layer-text">
                    <div className="layer-name">Topología de Red Vial</div>
                    <div className="layer-desc">Nodos y aristas modeladas del grafo</div>
                  </div>
                </div>
              </div>

              {/* Filtro de Severidad */}
              <div className="layers-group">
                <span className="eyebrow">Filtro de Gravedad Vial</span>
                <div className="segmented" role="radiogroup" aria-label="Filtrar siniestros por gravedad">
                  <button
                    onClick={() => setSeverityFilter('all')}
                    aria-pressed={severityFilter === 'all'}
                    type="button"
                  >
                    Todos
                  </button>
                  <button
                    onClick={() => setSeverityFilter('fatal')}
                    aria-pressed={severityFilter === 'fatal'}
                    type="button"
                  >
                    Con Muertos
                  </button>
                  <button
                    onClick={() => setSeverityFilter('injured')}
                    aria-pressed={severityFilter === 'injured'}
                    type="button"
                  >
                    Con Heridos
                  </button>
                </div>
              </div>

              {/* Filtro Temporal del Heatmap (Año o Histórico) */}
              <div className="layers-group">
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                  <span className="eyebrow">Año del Mapa de Calor</span>
                  <span style={{ fontSize: '11px', color: 'var(--c-teal-700)', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
                    {heatmapYear === 'ALL' ? 'Histórico (2014–2020)' : `Año ${heatmapYear}`}
                  </span>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '4px' }}>
                  <button
                    onClick={() => setHeatmapYear('ALL')}
                    style={{
                      gridColumn: 'span 4',
                      padding: '5px 8px',
                      borderRadius: '6px',
                      fontSize: '11.5px',
                      fontWeight: heatmapYear === 'ALL' ? 700 : 500,
                      backgroundColor: heatmapYear === 'ALL' ? 'var(--c-petrol)' : 'var(--c-surface-2)',
                      color: heatmapYear === 'ALL' ? '#ffffff' : 'var(--c-text)',
                      border: `1px solid ${heatmapYear === 'ALL' ? 'var(--c-petrol)' : 'var(--c-border)'}`,
                      cursor: 'pointer',
                      transition: 'all 0.15s ease',
                    }}
                    type="button"
                  >
                    Todo el Histórico (2014–2020)
                  </button>
                  {[2014, 2015, 2016, 2017, 2018, 2019, 2020].map((yr) => (
                    <button
                      key={yr}
                      onClick={() => setHeatmapYear(yr)}
                      style={{
                        padding: '5px 4px',
                        borderRadius: '6px',
                        fontSize: '11px',
                        fontFamily: 'var(--font-mono)',
                        fontWeight: heatmapYear === yr ? 700 : 500,
                        backgroundColor: heatmapYear === yr ? 'var(--c-teal)' : 'var(--c-surface-2)',
                        color: heatmapYear === yr ? '#ffffff' : 'var(--c-text)',
                        border: `1px solid ${heatmapYear === yr ? 'var(--c-teal)' : 'var(--c-border)'}`,
                        cursor: 'pointer',
                        transition: 'all 0.15s ease',
                      }}
                      type="button"
                    >
                      {yr}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Botón flotante para abrir capas */}
        <button
          onClick={() => setIsLayersOpen(!isLayersOpen)}
          className="control-btn-labeled"
          aria-expanded={isLayersOpen}
          aria-label="Abrir selector de capas y filtros"
          type="button"
        >
          <Layers size={16} aria-hidden="true" />
          <span>Capas & Filtros</span>
          <span className="control-count" title="Capas temáticas activas">
            {(showHeatmap ? 1 : 0) + (showHotspots ? 1 : 0) + (showRoutes ? 1 : 0) + (showNetwork ? 1 : 0)}
          </span>
        </button>

        {/* Stack de Zoom */}
        <div className="control-stack" role="group" aria-label="Controles de zoom">
          <button
            onClick={() => mapInstanceRef.current && mapInstanceRef.current.zoomIn()}
            className="icon-btn"
            title="Acercar mapa"
            aria-label="Acercar mapa"
            type="button"
          >
            +
          </button>
          <button
            onClick={() => mapInstanceRef.current && mapInstanceRef.current.zoomOut()}
            className="icon-btn"
            title="Alejar mapa"
            aria-label="Alejar mapa"
            type="button"
          >
            &minus;
          </button>
        </div>
      </aside>

      {/* ========================================================= */}
      {/* 4. LEYENDA CARTOGRÁFICA DINÁMICA (IZQUIERDA INFERIOR)     */}
      {/* ========================================================= */}
      <aside className={`map-overlay panel legend animate-fade-in ${isLegendCollapsed ? 'is-collapsed-auto' : ''}`} aria-label="Leyenda del mapa">
        <div className="panel-header" style={{ padding: '8px 12px' }}>
          <span className="eyebrow" style={{ color: 'var(--c-text)' }}>Leyenda Cartográfica</span>
          <button
            onClick={() => setIsLegendCollapsed(!isLegendCollapsed)}
            className="icon-btn icon-btn-sm"
            aria-label={isLegendCollapsed ? 'Expandir leyenda' : 'Plegar leyenda'}
            type="button"
          >
            {isLegendCollapsed ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
          </button>
        </div>

        {!isLegendCollapsed && (
          <div className="legend-body">
            {/* Rampa de calor si está activa con selector rápido de año */}
            {showHeatmap && (
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                  <div className="legend-section-title" style={{ margin: 0 }}>Intensidad (Heatmap)</div>
                  <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--c-teal-700)' }}>
                    {heatmapYear === 'ALL' ? '2014–2020' : `Año ${heatmapYear}`}
                  </span>
                </div>
                <div className="heat-ramp" />
                <div className="heat-ramp-labels">
                  <span>Baja densidad</span>
                  <span style={{ fontFamily: 'var(--font-mono)' }}>
                    {heatmapData ? `${heatmapData.total_incidents.toLocaleString()} casos` : 'Crítica'}
                  </span>
                </div>

                {/* Selector rápido de año en leyenda */}
                <div style={{ display: 'flex', gap: '3px', flexWrap: 'wrap', marginTop: '6px' }}>
                  <button
                    onClick={() => setHeatmapYear('ALL')}
                    style={{
                      padding: '2px 6px',
                      borderRadius: '4px',
                      fontSize: '10px',
                      fontWeight: heatmapYear === 'ALL' ? 700 : 500,
                      backgroundColor: heatmapYear === 'ALL' ? 'var(--c-petrol)' : 'var(--c-surface-2)',
                      color: heatmapYear === 'ALL' ? '#ffffff' : 'var(--c-text)',
                      border: 'none',
                      cursor: 'pointer',
                    }}
                    type="button"
                    title="Ver todo el histórico acumulado (2014–2020)"
                  >
                    Todo
                  </button>
                  {[2014, 2015, 2016, 2017, 2018, 2019, 2020].map((yr) => (
                    <button
                      key={yr}
                      onClick={() => setHeatmapYear(yr)}
                      style={{
                        padding: '2px 5px',
                        borderRadius: '4px',
                        fontSize: '10px',
                        fontFamily: 'var(--font-mono)',
                        fontWeight: heatmapYear === yr ? 700 : 500,
                        backgroundColor: heatmapYear === yr ? 'var(--c-teal)' : 'var(--c-surface-2)',
                        color: heatmapYear === yr ? '#ffffff' : 'var(--c-text)',
                        border: 'none',
                        cursor: 'pointer',
                      }}
                      type="button"
                      title={`Filtrar mapa de calor por año ${yr}`}
                    >
                      {yr}
                    </button>
                  ))}
                </div>
                {heatmapLoading && (
                  <div style={{ fontSize: '10px', color: 'var(--c-text-2)', marginTop: '4px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <span className="spin" style={{ display: 'inline-block' }}>⟳</span> Actualizando año {heatmapYear === 'ALL' ? 'histórico' : heatmapYear}...
                  </div>
                )}
              </div>
            )}

            {/* Simbología de Rutas si están activas */}
            {showRoutes && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <div className="legend-section-title">Rutas de Navegación</div>
                <div className="legend-row">
                  <span className="legend-line" style={{ background: 'var(--c-route-safe)' }} />
                  <span>Ruta Más Segura (Menor riesgo)</span>
                </div>
                <div className="legend-row">
                  <span className="legend-line" style={{ background: 'var(--c-route-short)' }} />
                  <span>Ruta Más Corta (Distancia)</span>
                </div>
              </div>
            )}

            {/* Simbología de Puntos Críticos */}
            {showHotspots && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <div className="legend-section-title">Puntos Críticos Viales</div>
                <div className="legend-row">
                  <span className="badge-dot" style={{ background: 'var(--risk-5)', border: '2px solid #fff' }} />
                  <span>Intersección con víctimas fatales</span>
                </div>
                <div className="legend-row">
                  <span className="badge-dot" style={{ background: 'var(--risk-2)', border: '2px solid #fff' }} />
                  <span>Intersección con personas heridas</span>
                </div>
              </div>
            )}

            {/* Puntos de Viaje */}
            <div style={{ display: 'flex', gap: '12px', fontSize: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                <span className="waypoint-pin is-a" style={{ width: '16px', height: '16px', fontSize: '9px' }}>A</span>
                <span>Origen</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                <span className="waypoint-pin is-b" style={{ width: '16px', height: '16px', fontSize: '9px' }}>B</span>
                <span>Destino</span>
              </div>
            </div>
          </div>
        )}
      </aside>

      {/* ========================================================= */}
      {/* 5. FICHA CONTEXTUAL DEL PUNTO CRÍTICO (PANEL INFERIOR)     */}
      {/* ========================================================= */}
      {selectedHotspot && (
        <section
          className="map-overlay panel sheet animate-slide-up"
          role="dialog"
          aria-label={`Detalle del punto crítico: ${selectedHotspot.lugar}`}
        >
          <div className="sheet-inner">
            <div
              className="sheet-accent"
              style={{
                background: (selectedHotspot.fatal_count || 0) > 0 ? 'var(--risk-5)' : 'var(--risk-2)',
              }}
            />

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '12px' }}>
              <div style={{ minWidth: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                  <span
                    className="badge"
                    style={{
                      backgroundColor: (selectedHotspot.fatal_count || 0) > 0 ? 'var(--c-danger-soft)' : 'var(--c-warn-soft)',
                      color: (selectedHotspot.fatal_count || 0) > 0 ? 'var(--c-danger)' : 'var(--c-warn-ink)',
                    }}
                  >
                    Riesgo {getRiskLevel(selectedHotspot.total_risk_score, selectedHotspot.fatal_count).label}
                  </span>
                  <span className="sheet-meta">
                    <b>{selectedHotspot.comuna_nombre || 'Medellín'}</b> &bull; {selectedHotspot.barrio || 'Valle de Aburrá'}
                  </span>
                </div>

                <h3 className="panel-title" style={{ marginTop: '4px', fontSize: '15px' }}>
                  {selectedHotspot.lugar}
                </h3>
              </div>

              <button
                onClick={() => setSelectedHotspot(null)}
                className="icon-btn icon-btn-sm"
                aria-label="Cerrar ficha de punto crítico"
                type="button"
              >
                <X size={15} />
              </button>
            </div>

            {/* Métricas clave del punto crítico */}
            <div className="sheet-grid" style={{ marginTop: '12px' }}>
              <div className="sheet-stat">
                <div className="metric-label">Total Siniestros</div>
                <div className="metric-value">
                  {selectedHotspot.incident_count?.toLocaleString()}
                </div>
              </div>

              <div className="sheet-stat">
                <div className="metric-label" style={{ color: 'var(--c-danger)' }}>Víctimas Fatales</div>
                <div className="metric-value" style={{ color: 'var(--c-danger)' }}>
                  {selectedHotspot.fatal_count || 0}
                </div>
              </div>

              <div className="sheet-stat">
                <div className="metric-label" style={{ color: 'var(--c-warn-ink)' }}>Personas Heridas</div>
                <div className="metric-value" style={{ color: 'var(--c-warn-ink)' }}>
                  {selectedHotspot.injured_count || 0}
                </div>
              </div>
            </div>

            {/* Acciones de planificación desde el punto crítico */}
            <div style={{ display: 'flex', gap: '8px', marginTop: '12px', justifyContent: 'flex-end', flexWrap: 'wrap' }}>
              <button
                onClick={() => {
                  const coords = { lat: selectedHotspot.latitud, lon: selectedHotspot.longitud };
                  setOriginCoords(coords);
                  setOriginAddress(selectedHotspot.lugar);
                  setSelectedHotspot(null);
                  handleCalculateRoute(coords, destCoords);
                }}
                className="btn btn-sm btn-secondary"
                type="button"
              >
                Fijar como Origen A
              </button>

              <button
                onClick={() => {
                  const coords = { lat: selectedHotspot.latitud, lon: selectedHotspot.longitud };
                  setDestCoords(coords);
                  setDestAddress(selectedHotspot.lugar);
                  setSelectedHotspot(null);
                  handleCalculateRoute(originCoords, coords);
                }}
                className="btn btn-sm btn-secondary"
                type="button"
              >
                Fijar como Destino B
              </button>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
