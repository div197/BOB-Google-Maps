"""Tests for export module."""

import json
import tempfile
from pathlib import Path
import pytest
from bob_core.export import JSONExporter, CSVExporter, export_data


def test_json_exporter():
    """Test JSON export functionality."""
    data = [
        {"name": "Test Business", "rating": "4.5", "reviews": [{"content": "Good"}]},
        {"name": "Another Business", "rating": "3.0", "reviews": []}
    ]
    
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        exporter = JSONExporter(f.name)
        output_path = exporter.export(data)
        
        # Verify file was created
        assert output_path.exists()
        
        # Verify content
        with open(output_path, 'r', encoding='utf-8') as rf:
            exported_data = json.load(rf)
        
        assert len(exported_data) == 2
        assert exported_data[0]["name"] == "Test Business"


def test_csv_exporter():
    """Test CSV export functionality."""
    data = [
        {"name": "Test Business", "rating": "4.5", "info": {"address": "123 Main St"}},
        {"name": "Another Business", "rating": "3.0", "info": {"address": "456 Oak Ave"}}
    ]
    
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        exporter = CSVExporter(f.name)
        output_path = exporter.export(data)
        
        # Verify file was created
        assert output_path.exists()
        
        # Verify content (basic check)
        content = output_path.read_text(encoding='utf-8')
        assert "Test Business" in content
        assert "123 Main St" in content


def test_export_data_auto_format():
    """Test auto-format detection."""
    data = [{"name": "Test", "value": 123}]
    
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        output_path = export_data(data, f.name, format="auto")
        assert output_path.exists()
        
        # Verify it's valid JSON
        with open(output_path, 'r', encoding='utf-8') as rf:
            exported_data = json.load(rf)
        assert len(exported_data) == 1


def test_flatten_dict():
    """Test dictionary flattening for CSV."""
    exporter = CSVExporter("dummy.csv")
    
    nested_dict = {
        "name": "Test",
        "info": {"address": "123 Main", "phone": "555-1234"},
        "reviews": [{"content": "Good"}, {"content": "Bad"}]
    }
    
    flattened = exporter._flatten_dict(nested_dict)
    
    assert "name" in flattened
    assert "info_address" in flattened
    assert "info_phone" in flattened
    assert "reviews_0_content" in flattened 