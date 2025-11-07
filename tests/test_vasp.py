import sys, os
import pytest
import pandas as pd
from main import normalize_vasp_response, read_codes

def test_normalize_vasp_response_basic(tmp_path):
    """Testa se a função normaliza corretamente os dados de tracking"""
    raw_data = {
        "service": {"serviceBarCode": "TEST123"},
        "currentEvent": {
            "eventDescriptionPT": "ENTREGUE",
            "eventDate": "2025-11-05T15:30:00Z"
        },
        "clientEvents": [
            {
                "eventDate": "2025-11-03T08:15:00Z",
                "createdDateUtc": "03/11/2025 08:15",
                "eventDescriptionPT": "RECOLHIDA",
                "depotName": "Centro Lisboa",
                "incidencePT": "Encomenda recolhida pelo motorista"
            }
        ]
    }

    result = normalize_vasp_response(raw_data, "TEST123", snapshot_dir=tmp_path)
    assert result["number"] == "TEST123"
    assert result["status"] == "ok"
    assert result["current_state"] == "ENTREGUE"
    assert len(result["events"]) == 1
    assert "raw_json_snapshot_path" in result
    assert "raw_html_snapshot_path" in result

def test_no_events_returns_not_found(tmp_path):
    raw_data = {
        "service": {"serviceBarCode": "X000"},
        "currentEvent": {"eventDescriptionPT": "DESCONHECIDO", "eventDate": "2025-11-05T12:00:00Z"},
        "clientEvents": []
    }
    result = normalize_vasp_response(raw_data, "X000", snapshot_dir=tmp_path)
    assert result["status"] == "not_found"
    assert result["events"] == []

def test_missing_optional_fields(tmp_path):
    raw_data = {
        "service": {"serviceBarCode": "TEST123"},
        "currentEvent": {"eventDescriptionPT": "EM DISTRIBUIÇÃO"},
        "clientEvents": [
            {"eventDate": "2025-11-03T10:00:00Z", "eventDescriptionPT": "RECOLHIDA"}
        ]
    }
    result = normalize_vasp_response(raw_data, "TEST123", snapshot_dir=tmp_path)
    assert result["current_state"] == "EM DISTRIBUIÇÃO"
    assert "location" in result["events"][0]

def test_events_sorted_by_timestamp(tmp_path):
    raw_data = {
        "service": {"serviceBarCode": "TESTSORT"},
        "clientEvents": [
            {"eventDate": "2025-11-04T10:00:00Z", "eventDescriptionPT": "SEGUNDO"},
            {"eventDate": "2025-11-03T09:00:00Z", "eventDescriptionPT": "PRIMEIRO"}
        ]
    }
    result = normalize_vasp_response(raw_data, "TESTSORT", snapshot_dir=tmp_path)
    assert result["events"][0]["state"] == "PRIMEIRO"
    assert result["events"][1]["state"] == "SEGUNDO"

def test_read_codes_txt(tmp_path):
    f = tmp_path / "codes.txt"
    f.write_text("123452222221\n67890223124141\n")
    codes = read_codes(str(f))
    assert codes == ["123452222221", "67890223124141"]

def test_read_codes_csv(tmp_path):
    df = pd.DataFrame({"codigo": ["A", "B", "C"]})
    f = tmp_path / "codes.csv"
    df.to_csv(f, index=False)
    codes = read_codes(str(f))
    assert codes == ["A", "B", "C"]
