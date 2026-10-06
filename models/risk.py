from datetime import datetime

def calculate_risk_score(claim: dict) -> tuple[int, list[str]]:
    score = 0
    reasons = []
    amount = float(claim["claim_amount"])
    previous = int(claim["previous_claims"])

    if amount > 100000:
        score += 40
        reasons.append("Claim amount exceeds ₹100,000")
    elif amount > 75000:
        score += 20
        reasons.append("High claim amount")

    if previous >= 5:
        score += 30
        reasons.append("Five or more previous claims")
    elif previous >= 3:
        score += 15
        reasons.append("Multiple previous claims")

    try:
        policy_start = datetime.strptime(claim["policy_start_date"], "%Y-%m-%d").date()
        incident = datetime.strptime(claim["incident_date"], "%Y-%m-%d").date()
        if (incident - policy_start).days <= 30:
            score += 25
            reasons.append("Incident occurred within 30 days of policy start")
    except ValueError:
        score += 50
        reasons.append("Invalid policy or incident date")

    if amount > 150000:
        score += 20
        reasons.append("Unusually high claim amount")

    return min(score, 100), reasons

def classify_claim(score: int, valid: bool) -> tuple[str, str]:
    if not valid:
        return "REJECTED", "REJECTED"
    if score >= 80:
        return "FRAUD_SUSPECTED", "FRAUD_SUSPECTED"
    if score >= 60:
        return "HIGH", "REVIEW"
    if score >= 30:
        return "MEDIUM", "REVIEW"
    return "LOW", "APPROVED"
