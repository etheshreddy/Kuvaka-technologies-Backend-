# app/scoring/pipeline.py
from .rule_layer import role_score, industry_score, data_completeness
from .ai_layer import ai_score

def score_lead(lead: dict, offer: dict, target_industries: list):
    """
    Produce a scored lead dict combining rule-based points (max 50) and AI points (max 50).
    """
    # Rule layer
    r_points = (
        role_score(lead.get("role", "")) +
        industry_score(lead.get("industry", ""), target_industries) +
        data_completeness(lead)
    )
    if r_points > 50:
        r_points = 50

    # AI layer
    ai = ai_score(lead, offer)
    ai_points = ai.get("points", 0)

    total = r_points + ai_points
    # Clamp total to 0..100
    total = max(0, min(100, total))

    return {
        "name": lead.get("name", ""),
        "role": lead.get("role", ""),
        "company": lead.get("company", ""),
        "intent": ai.get("intent", "Low"),
        "score": total,
        "reasoning": ai.get("reasoning", "")
    }
