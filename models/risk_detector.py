
import re


def detect_risks(text, clauses=None):
    """
    Identify potential contract issues using rule-based checks.

    These checks identify wording that may need review.
    They do not determine whether a contract is legally valid.
    """

    risks = []

    if not text or not text.strip():
        return risks

    lower_text = re.sub(r"\s+", " ", text.lower())

    def add_risk(level, title, evidence, reason, recommendation):
        risks.append({
            "risk_level": level,
            "title": title,
            "evidence": evidence,
            "reason": reason,
            "recommendation": recommendation
        })

    # ==========================================
    # RULE 1: UNLIMITED LIABILITY
    # ==========================================

    if re.search(
        r"\bunlimited liability\b|"
        r"\bwithout limitation of liability\b|"
        r"\bno limit on liability\b",
        lower_text
    ):
        add_risk(
            "HIGH",
            "Potential Unlimited Liability",
            "Wording indicating unlimited liability was detected.",
            "A party may have substantial financial exposure.",
            "Ask a qualified lawyer to review liability limits, exclusions and exceptions."
        )

    # ==========================================
    # RULE 2: BROAD INDEMNIFICATION
    # ==========================================

    if re.search(
        r"\bindemnif\w*.{0,150}\b(all claims|any and all claims|"
        r"all losses|any and all losses)\b",
        lower_text
    ):
        add_risk(
            "HIGH",
            "Potentially Broad Indemnification",
            "Broad indemnification wording was detected.",
            "The indemnifying party may have extensive responsibilities.",
            "Review covered claims, exclusions, procedures and financial limits."
        )

    # ==========================================
    # RULE 3: TERMINATION WITHOUT NOTICE
    # ==========================================

    termination_found = bool(re.search(
        r"\b(terminate|termination|terminates|terminated)\b",
        lower_text
    ))

    notice_found = bool(re.search(
        r"\b\d+\s*(business\s*)?(days?|weeks?|months?)"
        r"\s*(prior\s+)?(written\s+)?notice\b|"
        r"\bnotice\s+period\b",
        lower_text
    ))

    if termination_found and not notice_found:
        add_risk(
            "MEDIUM",
            "Termination Notice Not Detected",
            "Termination wording exists, but a notice period was not identified.",
            "The procedure or timing for ending the agreement may need clarification.",
            "Review termination rights, notice requirements and any exceptions."
        )

    # ==========================================
    # RULE 4: MISSING CONFIDENTIALITY PROVISION
    # ==========================================

    confidentiality_found = bool(re.search(
        r"\b(confidential|confidentiality|non-disclosure|"
        r"proprietary information)\b",
        lower_text
    ))

    if not confidentiality_found:
        add_risk(
            "MEDIUM",
            "Confidentiality Provision Not Detected",
            "No confidentiality-related wording was identified.",
            "The document may not explicitly address protection of confidential information.",
            "Consider whether confidentiality obligations are needed."
        )

    # ==========================================
    # RULE 5: MISSING PAYMENT PROVISION
    # ==========================================

    payment_found = bool(re.search(
        r"\b(payment|payments|salary|compensation|"
        r"remuneration|fees|fee|invoice|consideration)\b",
        lower_text
    ))

    if not payment_found:
        add_risk(
            "MEDIUM",
            "Payment Provision Not Detected",
            "No payment-related wording was identified.",
            "Financial obligations may not be clearly documented.",
            "Review whether payment amounts, due dates and payment conditions should be included."
        )

    # ==========================================
    # RULE 6: MISSING DISPUTE RESOLUTION
    # ==========================================

    dispute_found = bool(re.search(
        r"\b(arbitration|mediation|dispute resolution|"
        r"dispute settlement|resolution of disputes|"
        r"courts of competent jurisdiction|jurisdiction)\b",
        lower_text
    ))

    if not dispute_found:
        add_risk(
            "MEDIUM",
            "Dispute Resolution Not Detected",
            "No dispute resolution wording was identified.",
            "The contract may not clearly explain how disagreements are handled.",
            "Consider reviewing appropriate dispute resolution procedures."
        )

    # ==========================================
    # RULE 7: MISSING GOVERNING LAW
    # ==========================================

    governing_law_found = bool(re.search(
        r"\b(governing law|governed by the laws|"
        r"governed by the law|laws of [a-z ]+|"
        r"law of [a-z ]+)\b",
        lower_text
    ))

    if not governing_law_found:
        add_risk(
            "MEDIUM",
            "Governing Law Not Detected",
            "No governing law wording was identified.",
            "The applicable legal framework may not be clearly specified.",
            "Check whether a governing law provision is appropriate."
        )

    # ==========================================
    # RULE 8: BROAD CONFIDENTIALITY WORDING
    # ==========================================

    if re.search(
        r"\bkeep all.{0,60}information confidential\b|"
        r"\bkeep all information secret\b",
        lower_text
    ):
        add_risk(
            "LOW",
            "Broad Confidentiality Obligation",
            "Broad confidentiality wording was detected.",
            "The scope of protected information may need clarification.",
            "Review permitted disclosures, exceptions, exclusions and duration."
        )

    # ==========================================
    # RULE 9: LIABILITY CAP NOT DETECTED
    # ==========================================

    liability_found = bool(re.search(
        r"\b(liability|liable|damages|indemnification|indemnify)\b",
        lower_text
    ))

    liability_cap_found = bool(re.search(
        r"\b(cap on liability|limitation of liability|"
        r"liability shall not exceed|aggregate liability|"
        r"maximum liability|liability cap)\b",
        lower_text
    ))

    if liability_found and not liability_cap_found:
        add_risk(
            "MEDIUM",
            "Liability Cap Not Detected",
            "Liability-related wording exists, but an explicit financial cap was not identified.",
            "The agreement may not clearly establish a maximum financial exposure.",
            "Review whether liability limits and appropriate exceptions are required."
        )

    # ==========================================
    # RULE 10: RENEWAL WITHOUT NOTICE DETAILS
    # ==========================================

    renewal_found = bool(re.search(
        r"\b(auto(?:matic)?\s+renewal|renewal|renew automatically)\b",
        lower_text
    ))

    renewal_notice_found = bool(re.search(
        r"\b\d+\s*(days?|weeks?|months?)\s*(prior\s+)?"
        r"(written\s+)?notice\b",
        lower_text
    ))

    if renewal_found and not renewal_notice_found:
        add_risk(
            "LOW",
            "Renewal Notice Details Not Detected",
            "Renewal wording exists, but a notice period was not identified.",
            "The procedure for preventing or changing renewal may need clarification.",
            "Review renewal duration, automatic renewal and cancellation notice requirements."
        )

    return risks


# ==========================================
# TEST RISK DETECTOR
# ==========================================

if __name__ == "__main__":

    sample_text = """
    EMPLOYMENT AGREEMENT

    This agreement is made between ABC Technologies Pvt Ltd
    and John Smith on 1 January 2026.

    PAYMENT CLAUSE:
    The company shall pay the employee a monthly salary
    of INR 50000.

    CONFIDENTIALITY CLAUSE:
    The employee must keep all company information confidential.

    TERMINATION CLAUSE:
    Either party may terminate this agreement by providing
    30 days written notice.

    LIABILITY CLAUSE:
    The employee shall be responsible for damages caused
    by intentional misconduct.
    """

    print("\n========== LEGAL RISK DETECTION TEST ==========\n")

    detected_risks = detect_risks(sample_text, [])

    if detected_risks:

        for index, risk in enumerate(detected_risks, start=1):

            print(f"\nRisk {index}: {risk['title']}")
            print("Level:", risk["risk_level"])
            print("Evidence:", risk["evidence"])
            print("Reason:", risk["reason"])
            print("Recommendation:", risk["recommendation"])
            print("-" * 60)

    else:
        print("No potential risks detected.")

    print("\nTotal potential issues:", len(detected_risks))
    print("Risk detection test completed!")
