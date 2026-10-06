from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any

REQUIRED_FIELDS = [
    "claim_id", "policy_id", "customer_id", "customer_name",
    "policy_type", "claim_type", "claim_amount", "incident_date",
    "submission_date", "location", "description", "customer_age",
    "policy_start_date", "previous_claims", "timestamp"
]

@dataclass
class Claim:
    claim_id: str
    policy_id: str
    customer_id: str
    customer_name: str
    policy_type: str
    claim_type: str
    claim_amount: float
    incident_date: str
    submission_date: str
    location: str
    description: str
    customer_age: int
    policy_start_date: str
    previous_claims: int
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def parse_date(value: str):
    return datetime.strptime(value, "%Y-%m-%d").date()

def validate_claim(data: dict) -> tuple[bool, list[str]]:
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in data or data[field] in (None, ""):
            errors.append(f"Missing field: {field}")
    if errors:
        return False, errors

    try:
        amount = float(data["claim_amount"])
        if amount <= 0:
            errors.append("Claim amount must be greater than zero")
    except (TypeError, ValueError):
        errors.append("Claim amount must be numeric")

    try:
        age = int(data["customer_age"])
        if not 0 < age <= 120:
            errors.append("Customer age is invalid")
    except (TypeError, ValueError):
        errors.append("Customer age must be an integer")

    try:
        previous = int(data["previous_claims"])
        if previous < 0:
            errors.append("Previous claims cannot be negative")
    except (TypeError, ValueError):
        errors.append("Previous claims must be an integer")

    for field in ("incident_date", "submission_date", "policy_start_date"):
        try:
            parse_date(str(data[field]))
        except ValueError:
            errors.append(f"Invalid date: {field}")

    try:
        datetime.fromisoformat(str(data["timestamp"]).replace("Z", "+00:00"))
    except ValueError:
        errors.append("Invalid timestamp")

    return len(errors) == 0, errors
