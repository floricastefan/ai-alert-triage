# AI-Powered SOC Alert Triage & Threat Intelligence Assistant

A Security Operations Center (SOC) Tier 1 triage assistant that processes simulated security alerts, enriches Indicators of Compromise (IOCs) via external Threat Intelligence APIs, and generates structured incident triage reports using Google Gemini.

## Overview

In a SOC environment, analysts spend significant time manually querying IP addresses and file hashes across threat intelligence platforms when investigating alerts. Using a dataset of simulated alerts, this project automates the IOC lookup and initial triage analysis in four steps:

1. **Alert Ingestion:** Reads simulated security alerts (Windows Security Event Logs, Suricata IDS, Microsoft Defender for Endpoint, Firewall logs) from `resources/sample_alerts.json`.
2. **Threat Intelligence Enrichment:** Extracts IP addresses and SHA-256 file hashes from each alert and queries **AbuseIPDB** (for IP reputation) and **VirusTotal** (for file hash analysis).
3. **LLM Triage Analysis:** Combines the raw alert context with the Threat Intelligence findings and prompts **Google Gemini** to act as a Tier 1 SOC Analyst.
4. **Report Generation:** Produces a structured Markdown triage report in `reports/triage_report.md` containing an executive summary, MITRE ATT&CK mapping, severity assessment, and actionable next steps for Tier 2 analysts.

## Project Structure

```text
ai-alert-triage/
├── backend/
│   ├── alert_loader.py   # Loads alerts from the JSON dataset
│   ├── threat_intel.py   # Queries AbuseIPDB and VirusTotal v3 APIs
│   ├── ai_analyzer.py    # Sends enriched alert context to Google Gemini
│   └── main.py           # Orchestrates the pipeline and writes the Markdown report
├── reports/
│   └── triage_report.md  # Generated SOC triage report
├── resources/
│   └── sample_alerts.json # Simulated SOC alerts dataset
├── .env.example          # Template for required API keys
└── requirements.txt      # Python dependencies
```

## Prerequisites

- Python 3.10+
- Free API keys for:
  - [AbuseIPDB](https://www.abuseipdb.com/)
  - [VirusTotal](https://www.virustotal.com/)
  - [Google AI Studio (Gemini API)](https://aistudio.google.com/)

## Setup & Usage

1. **Clone the repository and activate the virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   Copy `.env.example` to `.env` and add your API keys:
   ```ini
   ABUSEIPDB_API_KEY=your_abuseipdb_api_key_here
   VIRUSTOTAL_API_KEY=your_virustotal_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the triage pipeline:**
   ```bash
   python backend/main.py
   ```

5. **View the output:**
   Open `reports/triage_report.md` to review the generated triage assessments.
