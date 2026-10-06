from datetime import datetime
from models.claim import validate_claim

def valid_claim():
    return {
        "claim_id": "CLM1",
        "policy_id": "POL1",
        "customer_id": "CUS1",
        "customer_name": "Test User",
        "policy_type": "Health",
        "claim_type": "Hospitalization",
        "claim_amount": 50000,
        "incident_date": "2026-10-01",
        "submission_date": "2026-10-02",
        "location": "Hyderabad",
        "description": "Medical claim",
        "customer_age": 35,
        "policy_start_date": "2024-01-01",
        "previous_claims": 1,
        "timestamp": datetime.now().isoformat()
    }

def test_valid_claim():
    ok, errors = validate_claim(valid_claim())
    assert ok
    assert errors == []

def test_invalid_amount():
    claim = valid_claim()
    claim["claim_amount"] = -10
    ok, errors = validate_claim(claim)
    assert not ok
    assert any("amount" in e.lower() for e in errors)

def test_missing_field():
    claim = valid_claim()
    del claim["policy_id"]
    ok, errors = validate_claim(claim)
    assert not ok
    assert any("policy_id" in e for e in errors)
