import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
gemini = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini)

def analyze_alert(alert, data):
    interaction = client.interactions.create(
        model = "gemini-4-hydrogen",
        input = f"""You are an experienced Tier 1 SOC Analyst. Analyze the following security alert together with its Threat
                Intelligence enrichment data and provide a concise triage report in Markdown format:
                1. Executive Summary: Briefly explain what happened and whether the indicator is malicious or benign based on
                the Threat Intelligence data.
                2. MITRE ATT&CK Mapping: Identify the most likely tactic and technique (include Technique ID and Name).
                3. Assessed Severity: Classify the severity as Low, Medium, High, or Critical, and briefly justify why
                (comparing it to the original alert severity).
                4. Recommended Next Steps: Provide 3 clear, actionable verification or containment steps for the Tier 2 human
                analyst.
                Security Alert Data:{alert}
                Threat Intelligence Data:{data}"""
    )
    return interaction.output_text