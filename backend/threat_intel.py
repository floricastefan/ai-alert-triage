import os
import requests
from dotenv import load_dotenv

load_dotenv()

abuseipdb = os.getenv("ABUSEIPDB_API_KEY")
virustotal = os.getenv("VIRUSTOTAL_API_KEY")

def get_ip(ip):
    url = 'https://api.abuseipdb.com/api/v2/check'
    querystring = {
        'ipAddress': ip,
        'maxAgeInDays': '90'
    }

    headers = {
        "Accept": "application/json",
        "Key": abuseipdb,
    }
    response = requests.request(method='GET', url=url, headers=headers, params=querystring)

    return response.json()["data"]

def get_hash(file_hash):
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"

    headers = {
        "Accept": "application/json",
        "x-apikey": virustotal,
    }
    response = requests.request(method='GET', url=url, headers=headers)

    return response.json()["data"]["attributes"]["last_analysis_stats"]




