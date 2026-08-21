from datetime import datetime

def generate_markdown_report(result_dict, scanner_type="Message"):
    """
    Generates downloadable Markdown security report.
    """
    score = result_dict.get("risk_score", 0)
    level = result_dict.get("risk_level", "SAFE")
    category = result_dict.get("category", "General")
    confidence = result_dict.get("confidence", 85)
    explanation = result_dict.get("explanation", "")
    recommendation = result_dict.get("recommendation", "")
    indicators = result_dict.get("indicators", [])
    scam_dna = result_dict.get("scam_dna", {})
    attack_chain = result_dict.get("attack_chain", [])

    report = f"""# 🛡️ ScamShield AI - Threat Intelligence Report

**Generated At:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Scanner Module:** {scanner_type.title()} Scanner  
**Assessment Result:** {level} RISK ({score}/100)  
**Confidence Score:** {confidence}%  
**Scam Category:** {category}  

---

## 📊 Executive Summary
{explanation}

---

## ⚠️ Flagged Risk Indicators
"""
    if indicators:
        for ind in indicators:
            report += f"- {ind}\n"
    else:
        report += "- No elevated risk indicators flagged.\n"

    report += """
---

## 🧬 Scam DNA Profile
"""
    if isinstance(scam_dna, dict):
        for k, v in scam_dna.items():
            key_name = str(k).replace("_", " ").title()
            report += f"- **{key_name}:** {v}\n"

    report += """
---

## 🔗 Attack Escalation Chain
"""
    if isinstance(attack_chain, list):
        for step in attack_chain:
            report += f"1. **{step.get('title', 'Step')}**: {step.get('desc', '')}\n"

    report += f"""
---

## 🛡️ Recommended Safety Actions
{recommendation}

---
*Report generated automatically by ScamShield AI V2 Security SaaS.*
"""
    return report
