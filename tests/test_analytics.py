"""
Pruebas del endpoint de analítica cruzada y de la normalización de la base SQLite.
"""

from fastapi.testclient import TestClient
from app.main import app
from app.services.db_builder import fix_text, normalize_class, normalize_place, normalize_severity

client = TestClient(app)


def test_text_normalization():
    assert fix_text("BelÃ©n") == "Belén"
    assert fix_text("Bel\xE9n") == "Belén"
    assert normalize_severity("SOLO DA\XF1OS") == "SOLO DAÑOS"
    assert normalize_severity("SOLO DAñOS") == "SOLO DAÑOS"
    assert normalize_class("CA\ufffd\xadDA DE OCUPANTE") == "CAIDA OCUPANTE"
    assert normalize_place("SN") == "Sin información"


def test_analytics_unfiltered_is_consistent():
    data = client.get("/api/v1/incidents/analytics").json()
    total = data["total_incidents"]
    assert total > 0
    assert set(data["by_severity"]) <= {"SOLO DAÑOS", "CON HERIDOS", "CON MUERTOS"}
    assert sum(data["by_severity"].values()) == total
    assert sum(data["by_year"].values()) == total
    assert sum(data["by_hour"]) == total
    assert len(data["by_hour"]) == 24 and len(data["by_weekday"]) == 7 and len(data["by_month"]) == 12
    assert sum(c["count"] for c in data["communes"]) == total


def test_analytics_filters_combine():
    full = client.get("/api/v1/incidents/analytics").json()
    sub = client.get(
        "/api/v1/incidents/analytics",
        params={"anio": 2019, "gravedad": "CON HERIDOS", "comuna": "La Candelaria"},
    ).json()
    assert 0 < sub["total_incidents"] < full["total_incidents"]
    assert list(sub["by_year"]) == ["2019"]
    assert list(sub["by_severity"]) == ["CON HERIDOS"]
    assert [c["comuna"] for c in sub["communes"]] == ["La Candelaria"]


def test_severity_filter_matches_normalized_label():
    # Antes de la normalización este filtro devolvía 0 por la codificación corrupta
    data = client.get("/api/v1/incidents/analytics", params={"gravedad": "SOLO DAÑOS"}).json()
    assert data["total_incidents"] > 100_000
