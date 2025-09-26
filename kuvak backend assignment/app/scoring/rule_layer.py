# app/scoring/rule_layer.py

def role_score(role: str) -> int:
    if not role:
        return 0
    decision_makers = ["CEO", "Founder", "Head", "Director", "Chief"]
    influencers = ["Manager", "Lead", "VP", "Vice President", "Principal"]
    role_lower = role.lower()
    if any(dm.lower() in role_lower for dm in decision_makers):
        return 20
    elif any(inf.lower() in role_lower for inf in influencers):
        return 10
    return 0

def industry_score(industry: str, target_industries: list) -> int:
    if not industry:
        return 0
    # Exact match gives full points
    if any(industry.strip().lower() == t.strip().lower() for t in target_industries):
        return 20
    # Partial/adjacent match gives partial points
    if any(t.strip().lower() in industry.strip().lower() or industry.strip().lower() in t.strip().lower() for t in target_industries):
        return 10
    return 0

def data_completeness(lead: dict) -> int:
    required = ["name", "role", "company", "industry", "location", "linkedin_bio"]
    return 10 if all(lead.get(k) and str(lead.get(k)).strip() for k in required) else 0
