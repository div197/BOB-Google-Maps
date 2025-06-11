"""bob_core.export

Data export utilities for various formats (CSV, Excel, JSON).
"""
from __future__ import annotations

import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from datetime import datetime

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

__all__ = [
    "CSVExporter",
    "JSONExporter", 
    "ExcelExporter",
    "export_data"
]


class BaseExporter:
    """Base class for data exporters."""
    
    def __init__(self, output_path: Union[str, Path]):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
    
    def export(self, data: List[Dict[str, Any]], **kwargs) -> Path:
        """Export data to file. Override in subclasses."""
        raise NotImplementedError


class JSONExporter(BaseExporter):
    """Export data to JSON format."""
    
    def export(self, data: List[Dict[str, Any]], indent: int = 2, **kwargs) -> Path:
        """Export to JSON file."""
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent, default=str)
        return self.output_path


class CSVExporter(BaseExporter):
    """Export data to CSV format."""
    
    def export(self, data: List[Dict[str, Any]], **kwargs) -> Path:
        """Export to CSV file."""
        if not data:
            return self.output_path
        
        # Flatten nested data for CSV
        flattened_data = []
        for item in data:
            flat_item = self._flatten_dict(item)
            flattened_data.append(flat_item)
        
        # Get all unique keys
        all_keys = set()
        for item in flattened_data:
            all_keys.update(item.keys())
        
        with open(self.output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
            writer.writeheader()
            writer.writerows(flattened_data)
        
        return self.output_path
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
        """Flatten nested dictionary for CSV export."""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Convert lists to comma-separated strings
                if v and isinstance(v[0], dict):
                    # For list of dicts, create numbered columns
                    for i, item in enumerate(v[:5]):  # Limit to first 5 items
                        if isinstance(item, dict):
                            items.extend(self._flatten_dict(item, f"{new_key}_{i}", sep=sep).items())
                        else:
                            items.append((f"{new_key}_{i}", str(item)))
                else:
                    items.append((new_key, ', '.join(str(x) for x in v)))
            else:
                items.append((new_key, v))
        
        return dict(items)


class ExcelExporter(BaseExporter):
    """Export data to Excel format (requires pandas)."""
    
    def export(self, data: List[Dict[str, Any]], sheet_name: str = "Data", **kwargs) -> Path:
        """Export to Excel file."""
        if not PANDAS_AVAILABLE:
            raise ImportError("pandas required for Excel export. Install with: pip install pandas openpyxl")
        
        # Flatten data similar to CSV
        csv_exporter = CSVExporter(self.output_path)
        flattened_data = []
        for item in data:
            flat_item = csv_exporter._flatten_dict(item)
            flattened_data.append(flat_item)
        
        df = pd.DataFrame(flattened_data)
        
        # Ensure .xlsx extension
        if not self.output_path.suffix == '.xlsx':
            self.output_path = self.output_path.with_suffix('.xlsx')
        
        with pd.ExcelWriter(self.output_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        return self.output_path


def export_data(
    data: List[Dict[str, Any]], 
    output_path: Union[str, Path], 
    format: str = "auto",
    **kwargs
) -> Path:
    """
    Export data to specified format.
    
    Parameters
    ----------
    data : List[Dict[str, Any]]
        Data to export
    output_path : Union[str, Path]
        Output file path
    format : str
        Export format: "json", "csv", "excel", or "auto" (detect from extension)
    **kwargs
        Additional arguments passed to exporter
        
    Returns
    -------
    Path
        Path to exported file
    """
    output_path = Path(output_path)
    
    # Auto-detect format from extension
    if format == "auto":
        ext = output_path.suffix.lower()
        if ext == ".json":
            format = "json"
        elif ext == ".csv":
            format = "csv"
        elif ext in [".xlsx", ".xls"]:
            format = "excel"
        else:
            format = "json"  # Default fallback
    
    # Select appropriate exporter
    if format == "json":
        exporter = JSONExporter(output_path)
    elif format == "csv":
        exporter = CSVExporter(output_path)
    elif format == "excel":
        exporter = ExcelExporter(output_path)
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    return exporter.export(data, **kwargs) 