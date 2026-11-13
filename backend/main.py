import alert_loader
import threat_intel
import ai_analyzer
from pathlib import Path

parent = Path(__file__).parent.parent
triage_report = parent / "reports" / "triage_report.md"
alerts = alert_loader.get_alerts()

for alert in alerts:
    print(alert["alert_id"])
    for indicator in alert["indicators"]:
        if indicator["type"] == "ip":
            value = threat_intel.get_ip(indicator["value"])
            report = ai_analyzer.analyze_alert(alert, value)
        if indicator["type"] == "hash":
            value = threat_intel.get_hash(indicator["value"])
            report = ai_analyzer.analyze_alert(alert, value)

        with open(triage_report, "a") as f:
            f.write(report + "\n\n---\n\n")