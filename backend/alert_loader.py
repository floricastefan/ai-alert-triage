import json
from pathlib import Path

parent = Path(__file__).parent.parent
sample_alerts = parent / "resources" / "sample_alerts.json"

def get_alerts():
    with open(sample_alerts, 'r') as f:
        alerts = json.load(f)

    return alerts