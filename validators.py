from typing import Dict, List
from models import Achievement, Metric

class DataValidator:
    @staticmethod
    def validate_achievement(data: Dict) -> None:
        Achievement(**data)
    
    @staticmethod
    def validate_metrics(metrics: List[Dict]) -> None:
        for metric in metrics:
            Metric(**metric)