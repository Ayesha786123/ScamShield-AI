from src.explainability import generate_explanation
from src.scam_dna import generate_scam_dna
from src.attack_chain import generate_attack_chain
from src.copilot import generate_copilot_recommendations


def get_risk_level(score):
    """
    Strict Risk Thresholds:
    SAFE = 0-19
    LOW = 20-39
    MEDIUM = 40-59
    HIGH = 60-79
    CRITICAL = 80-100
    """
    score = int(score)
    if score <= 19:
        return "SAFE"
    elif score <= 39:
        return "LOW"
    elif score <= 59:
        return "MEDIUM"
    elif score <= 79:
        return "HIGH"
    else:
        return "CRITICAL"


def format_unified_result(risk_score, confidence, category, indicators, raw_text="", scanner_type="message", extra_data=None):
    """
    Format scanner output into standard V2 unified dictionary format.
    """
    score = min(max(int(risk_score), 0), 100)
    level = get_risk_level(score)
    conf = min(max(int(confidence), 0), 100)
    
    explanation = generate_explanation(score, level, category, indicators)
    recommendations = generate_copilot_recommendations(level, category, indicators)
    recommendation_str = "; ".join(recommendations)
    
    scam_dna = generate_scam_dna(category, level, indicators, text=raw_text)
    attack_chain = generate_attack_chain(category, level, indicators, text=raw_text)

    result = {
        "risk_score": score,
        "risk_level": level,
        "confidence": conf,
        "category": category,
        "indicators": indicators,
        "recommendation": recommendation_str,
        "explanation": explanation,
        "scam_dna": scam_dna,
        "attack_chain": attack_chain
    }

    if extra_data and isinstance(extra_data, dict):
        result.update(extra_data)

    return result
