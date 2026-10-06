from database.database import initialize_database, get_all_claims

def main():
    initialize_database()
    claims = get_all_claims()

    print("\n" + "=" * 65)
    print("REAL-TIME INSURANCE CLAIM PROCESSING REPORT")
    print("=" * 65)

    if not claims:
        print("No claims processed yet.")
        return

    total = len(claims)
    approved = sum(c["status"] == "APPROVED" for c in claims)
    rejected = sum(c["status"] == "REJECTED" for c in claims)
    fraud = sum(c["status"] == "FRAUD_SUSPECTED" for c in claims)
    high = sum(c["risk_level"] == "HIGH" for c in claims)
    total_amount = sum(c["claim_amount"] for c in claims)
    avg_amount = total_amount / total
    avg_risk = sum(c["risk_score"] for c in claims) / total

    print(f"Total claims processed : {total}")
    print(f"Approved claims        : {approved}")
    print(f"Rejected claims        : {rejected}")
    print(f"Fraud suspected        : {fraud}")
    print(f"High-risk claims       : {high}")
    print(f"Total claim amount     : ₹{total_amount:,.2f}")
    print(f"Average claim amount   : ₹{avg_amount:,.2f}")
    print(f"Average risk score     : {avg_risk:.2f}")

    print("\n" + "-" * 65)
    print(f"{'Claim ID':<12}{'Amount':>14}{'Risk':>8}{'Level':<18}{'Status':<18}")
    print("-" * 65)
    for c in claims[-20:]:
        print(
            f"{c['claim_id']:<12}"
            f"₹{c['claim_amount']:>12,.0f}"
            f"{c['risk_score']:>8}"
            f"{c['risk_level']:<18}"
            f"{c['status']:<18}"
        )
    print("-" * 65)

if __name__ == "__main__":
    main()
