from models.risk import calculate_risk_score, classify_claim

def test_high_amount_increases_risk():
    claim = {
        "claim_amount": 150000,
        "previous_claims": 0,
        "policy_start_date": "2020-01-01",
        "incident_date": "2026-10-01"
    }
    score, reasons = calculate_risk_score(claim)
    assert score >= 40
    assert reasons

def test_multiple_conditions_can_be_high():
    claim = {
        "claim_amount": 200000,
        "previous_claims": 6,
        "policy_start_date": "2026-09-20",
        "incident_date": "2026-10-01"
    }
    score, _ = calculate_risk_score(claim)
    assert score >= 80

def test_classification():
    assert classify_claim(10, True) == ("LOW", "APPROVED")
    assert classify_claim(45, True) == ("MEDIUM", "REVIEW")
    assert classify_claim(70, True) == ("HIGH", "REVIEW")
    assert classify_claim(90, True) == ("FRAUD_SUSPECTED", "FRAUD_SUSPECTED")
    assert classify_claim(10, False) == ("REJECTED", "REJECTED")
