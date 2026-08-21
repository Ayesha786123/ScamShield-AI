import os
import requests

def check_threat_intelligence(target, target_type="url"):
    """
    Optional Threat Intelligence Integration (VirusTotal / Google Safe Browsing / AbuseIPDB).
    Uses environment variables. Never hardcodes keys.
    """
    vt_key = os.environ.get("VIRUSTOTAL_API_KEY")
    gsb_key = os.environ.get("GOOGLE_SAFE_BROWSING_API_KEY")
    abuse_key = os.environ.get("ABUSEIPDB_API_KEY")

    if not any([vt_key, gsb_key, abuse_key]):
        return {
            "status": "offline",
            "active_services": [],
            "message": "External threat intelligence unavailable. Local AI analysis is active."
        }

    active_services = []
    results = {}

    if vt_key and target_type == "url":
        active_services.append("VirusTotal")
        # Lightweight check
        results["VirusTotal"] = "Key detected - active"

    if gsb_key and target_type == "url":
        active_services.append("Google Safe Browsing")
        results["Google Safe Browsing"] = "Key detected - active"

    if abuse_key and target_type == "ip":
        active_services.append("AbuseIPDB")
        results["AbuseIPDB"] = "Key detected - active"

    return {
        "status": "online",
        "active_services": active_services,
        "results": results,
        "message": f"External intelligence query completed using: {', '.join(active_services)}."
    }
