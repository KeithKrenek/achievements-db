from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
import yaml
from docx import Document
from jinja2 import Template
from models import Achievement
from exceptions import DatabaseError

class BaseExporter(ABC):
    @abstractmethod
    def export(self, achievements: List[Dict], output_path: str):
        pass

class JSONExporter(BaseExporter):
    def export(self, achievements: List[Dict], output_path: str):
        with open(output_path, 'w') as f:
            json.dump(achievements, f, indent=2)

class DocxExporter(BaseExporter):
    def export(self, achievements: List[Dict], output_path: str):
        doc = Document()
        # ... [previous implementation] ...
        pass  # Keeping for brevity, actual implementation remains the same

class ExportManager:
    def __init__(self):
        self.exporters = {
            'json': JSONExporter(),
            'docx': DocxExporter()
        }
    
    def export(self, 
               achievements: List[Dict],
               format: str,
               output_path: str):
        if format not in self.exporters:
            raise ValueError(f"Unsupported format: {format}")
        
        self.exporters[format].export(achievements, output_path)