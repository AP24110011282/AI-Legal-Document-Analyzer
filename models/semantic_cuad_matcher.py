
import re

from sentence_transformers import SentenceTransformer, util


# ==========================================
# 1. MODEL CONFIGURATION
# ==========================================

MODEL_NAME = "all-MiniLM-L6-v2"

DEFAULT_THRESHOLD = 0.52
MINIMUM_SCORE_GAP = 0.025

print("Loading CUAD semantic matching model...")

MODEL = SentenceTransformer(MODEL_NAME)


# ==========================================
# 2. CUAD 41 CONTRACT CATEGORIES
# ==========================================

CATEGORIES = {
    "Affiliate License-Licensee":
        "A license granted to an affiliate of the licensee.",

    "Affiliate License-Licensor":
        "A license granted by an affiliate of the licensor.",

    "Agreement Date":
        "The date when the contract is signed or executed.",

    "Anti-Assignment":
        "Restrictions on assigning or transferring contractual rights.",

    "Audit Rights":
        "Rights to inspect or audit financial records and accounts.",

    "Cap On Liability":
        "The maximum financial liability allowed under the contract.",

    "Change Of Control":
        "Provisions concerning changes in company ownership or control.",

    "Competitive Restriction Exception":
        "Exceptions to restrictions on competition.",

    "Covenant Not To Sue":
        "An agreement not to file a lawsuit or legal claim.",

    "Document Name":
        "The official name or title of the contract.",

    "Effective Date":
        "The date on which the contract becomes effective.",

    "Expiration Date":
        "The date on which the agreement expires or reaches its end.",

    "Exclusivity":
        "Requirements for exclusive business relationships.",

    "Governing Law":
        "The country or state laws governing the contract.",

    "Insurance":
        "Requirements for insurance policies and coverage.",

    "Ip Ownership Assignment":
        "Transfer of intellectual property ownership.",

    "Irrevocable Or Perpetual License":
        "A license that is permanent or cannot be revoked.",

    "Joint Ip Ownership":
        "Shared ownership of intellectual property.",

    "License Grant":
        "Permission to use intellectual property.",

    "Liquidated Damages":
        "Pre-agreed financial compensation for breach of contract.",

    "Minimum Commitment":
        "Minimum purchase or payment obligations.",

    "Most Favored Nation":
        "A requirement to provide terms as favorable as those offered to another party.",

    "No-Solicit Of Customers":
        "Restrictions on soliciting customers.",

    "No-Solicit Of Employees":
        "Restrictions on recruiting employees.",

    "Non-Compete":
        "Restrictions preventing a party from competing.",

    "Non-Disparagement":
        "Restrictions on negative statements about another party.",

    "Non-Transferable License":
        "A license that cannot be transferred.",

    "Notice Period To Terminate Renewal":
        "Advance notice required to terminate an agreement or prevent contract renewal.",

    "Parties":
        "Names and identities of organizations or individuals entering the contract.",

    "Post-Termination Services":
        "Services required after termination of the agreement.",

    "Price Restrictions":
        "Restrictions on prices, fees or resale pricing.",

    "Renewal Term":
        "Duration and conditions of contract renewal.",

    "Revenue/Profit Sharing":
        "Sharing revenue, income or profits between parties.",

    "Rofr/Rofo/Rofn":
        "Rights of first refusal, first offer or first negotiation.",

    "Source Code Escrow":
        "Depositing software source code with an escrow agent.",

    "Termination For Convenience":
        "The right to terminate an agreement without proving a breach or cause.",

    "Third Party Beneficiary":
        "Rights granted to third parties under a contract.",

    "Uncapped Liability":
        "Liability that has no contractual financial cap.",

    "Unlimited/All-You-Can-Eat-License":
        "Unlimited use of licensed products or services.",

    "Volume Restriction":
        "Restrictions on quantities or usage volumes.",

    "Warranty Duration":
        "The period during which warranties remain valid."
}


# ==========================================
# 3. PREPARE CATEGORY EMBEDDINGS
# ==========================================

print("Preparing CUAD category embeddings...")

CATEGORY_NAMES = list(CATEGORIES.keys())

CATEGORY_DESCRIPTIONS = list(CATEGORIES.values())

CATEGORY_EMBEDDINGS = MODEL.encode(
    CATEGORY_DESCRIPTIONS,
    convert_to_tensor=True,
    normalize_embeddings=True
)

print("CUAD semantic matcher ready.")
print("Total categories:", len(CATEGORY_NAMES))


# ==========================================
# 4. TEXT NORMALIZATION
# ==========================================

def normalize_text(text):

    text = str(text).replace("\r", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================
# 5. REMOVE CLAUSE HEADINGS
# ==========================================

def remove_clause_headings(text):

    headings = [
        "PAYMENT CLAUSE",
        "CONFIDENTIALITY CLAUSE",
        "TERMINATION CLAUSE",
        "LIABILITY CLAUSE",
        "GOVERNING LAW CLAUSE",
        "INSURANCE CLAUSE",
        "AUDIT RIGHTS CLAUSE",
        "RENEWAL CLAUSE"
    ]

    for heading in headings:

        text = re.sub(
            r"\b" + re.escape(heading) + r"\s*:",
            "",
            text,
            flags=re.IGNORECASE
        )

    return text.strip()


# ==========================================
# 6. SENTENCE SPLITTING
# ==========================================

def split_sentences(document_text):

    text = normalize_text(document_text)

    text = remove_clause_headings(text)

    sentences = re.split(
        r"(?<=[.!?])\s+(?=[A-Z0-9])",
        text
    )

    cleaned_sentences = []

    seen = set()

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence) < 25:
            continue

        key = sentence.lower()

        if key not in seen:

            seen.add(key)

            cleaned_sentences.append(sentence)

    return cleaned_sentences


# ==========================================
# 7. RULE-ASSISTED CATEGORY DETECTION
# ==========================================

def detect_rule_categories(sentence):

    text = sentence.lower()

    detected = []

    rules = {

        "Governing Law": [
            r"\bgoverned by the laws?\b",
            r"\bgoverning law\b",
            r"\blaws? of [a-z][a-z\s-]*",
            r"\bconstrued in accordance with the laws?\b"
        ],

        "Expiration Date": [
            r"\bexpiration date\b",
            r"\bexpiry date\b",
            r"\bexpires on\b",
            r"\bexpires at\b",
            r"\bshall expire\b",
            r"\bwill expire\b",
            r"\bexpiration\b"
        ],

        "Liquidated Damages": [
            r"\bliquidated damages\b",
            r"\bpre-agreed damages\b",
            r"\bpredetermined damages\b",
            r"\bagreed amount of damages\b",
            r"\bfixed amount of damages\b",
            r"\bspecified amount of damages\b"
        ],

        "Cap On Liability": [
            r"\bmaximum liability\b",
            r"\bliability shall not exceed\b",
            r"\bliability will not exceed\b",
            r"\btotal liability\b.{0,100}\bshall not exceed\b",
            r"\baggregate liability\b",
            r"\bliability is limited to\b",
            r"\blimitation of liability\b",
            r"\bliability cap\b"
        ],

        "Uncapped Liability": [
            r"\bunlimited liability\b",
            r"\buncapped liability\b",
            r"\bwithout limitation\b",
            r"\bwithout any liability cap\b",
            r"\bno limit on liability\b",
            r"\bliability\b.{0,100}\bshall be unlimited\b"
        ],

        "Termination For Convenience": [
            r"\bterminate\b.{0,100}\bfor convenience\b",
            r"\btermination\b.{0,100}\bfor convenience\b",
            r"\bterminate\b.{0,100}\bwithout cause\b",
            r"\bterminate\b.{0,100}\bwithout reason\b",
            r"\btermination\b.{0,100}\bat its discretion\b"
        ],

        "Notice Period To Terminate Renewal": [
            r"\bnotice\b.{0,120}\b(terminate|termination|renew|renewal)\b",
            r"\b(terminate|termination|renew|renewal)\b.{0,120}\bnotice\b"
        ]
    }

    for category, patterns in rules.items():

        if any(
            re.search(pattern, text)
            for pattern in patterns
        ):

            detected.append(category)

    # Prevent an uncapped liability clause
    # from also being classified as a liability cap.

    if "Uncapped Liability" in detected:

        detected = [
            category for category in detected
            if category != "Cap On Liability"
        ]

    # Do not classify a termination-for-convenience
    # sentence as a notice-period clause merely because
    # it also mentions notice.

    if "Termination For Convenience" in detected:

        detected = [
            category for category in detected
            if category != "Notice Period To Terminate Renewal"
        ]

    return detected


# ==========================================
# 8. CATEGORY VALIDATION
# ==========================================

def validate_category(category, sentence):

    text = sentence.lower()

    if category == "Expiration Date":

        return any(
            re.search(pattern, text)
            for pattern in [
                r"\bexpiration date\b",
                r"\bexpiry date\b",
                r"\bexpires on\b",
                r"\bexpires at\b",
                r"\bshall expire\b",
                r"\bwill expire\b",
                r"\bexpiration\b"
            ]
        )

    elif category == "Liquidated Damages":

        return any(
            phrase in text
            for phrase in [
                "liquidated damages",
                "pre-agreed damages",
                "predetermined damages",
                "agreed amount of damages",
                "fixed amount of damages",
                "specified amount of damages"
            ]
        )

    elif category == "Governing Law":

        return any(
            re.search(pattern, text)
            for pattern in [
                r"\bgoverned by the laws?\b",
                r"\bgoverning law\b",
                r"\blaws? of [a-z][a-z\s-]*",
                r"\bconstrued in accordance with the laws?\b"
            ]
        )

    elif category == "Notice Period To Terminate Renewal":

        return (
            bool(re.search(r"\bnotice\b", text))
            and bool(
                re.search(
                    r"\b(terminate|termination|renew|renewal)\b",
                    text
                )
            )
            and "for convenience" not in text
            and "without cause" not in text
            and "without reason" not in text
        )

    elif category == "Termination For Convenience":

        return (
            bool(
                re.search(
                    r"\b(terminate|termination)\b",
                    text
                )
            )
            and any(
                phrase in text
                for phrase in [
                    "for convenience",
                    "without cause",
                    "without reason",
                    "at its discretion"
                ]
            )
        )

    elif category == "Cap On Liability":

        return any(
            re.search(pattern, text)
            for pattern in [
                r"\bmaximum liability\b",
                r"\bliability shall not exceed\b",
                r"\bliability will not exceed\b",
                r"\btotal liability\b.{0,100}\bshall not exceed\b",
                r"\baggregate liability\b",
                r"\bliability is limited to\b",
                r"\blimitation of liability\b",
                r"\bliability cap\b"
            ]
        )

    elif category == "Uncapped Liability":

        return any(
            re.search(pattern, text)
            for pattern in [
                r"\bunlimited liability\b",
                r"\buncapped liability\b",
                r"\bwithout limitation\b",
                r"\bwithout any liability cap\b",
                r"\bno limit on liability\b",
                r"\bliability\b.{0,100}\bshall be unlimited\b"
            ]
        )

    return True


# ==========================================
# 9. SEMANTIC CLAUSE DETECTION
# ==========================================

def detect_semantic_clauses(
    document_text,
    threshold=DEFAULT_THRESHOLD,
    minimum_score_gap=MINIMUM_SCORE_GAP
):

    if not document_text or not document_text.strip():
        return []

    sentences = split_sentences(document_text)

    if not sentences:
        return []

    print("Analyzing document sentences...")

    sentence_embeddings = MODEL.encode(
        sentences,
        convert_to_tensor=True,
        normalize_embeddings=True
    )

    similarities = util.cos_sim(
        sentence_embeddings,
        CATEGORY_EMBEDDINGS
    )

    best_category_matches = {}

    for index, sentence in enumerate(sentences):

        scores = similarities[index]

        # RULE-ASSISTED DETECTION

        rule_categories = detect_rule_categories(sentence)

        for category in rule_categories:

            if not validate_category(category, sentence):
                continue

            category_index = CATEGORY_NAMES.index(category)

            category_score = float(scores[category_index])

            result = {
                "category": category,
                "sentence": sentence,
                "similarity": round(category_score, 3),
                "score_gap": None,
                "matching_method": "rule-assisted semantic"
            }

            existing = best_category_matches.get(category)

            if (
                existing is None
                or category_score > existing["similarity"]
            ):

                best_category_matches[category] = result

        # SEMANTIC MATCHING

        best_indices = scores.argsort(descending=True)

        best_index = int(best_indices[0])

        best_score = float(scores[best_index])

        second_score = float(scores[int(best_indices[1])])

        score_gap = best_score - second_score

        category = CATEGORY_NAMES[best_index]

        # Skip competing semantic classification when
        # an explicit rule has matched this sentence.

        if rule_categories:
            continue

        if not validate_category(category, sentence):
            continue

        if best_score < threshold:
            continue

        if score_gap < minimum_score_gap:
            continue

        result = {
            "category": category,
            "sentence": sentence,
            "similarity": round(best_score, 3),
            "score_gap": round(score_gap, 3),
            "matching_method": "semantic"
        }

        existing = best_category_matches.get(category)

        if (
            existing is None
            or best_score > existing["similarity"]
        ):

            best_category_matches[category] = result

    # SORT RESULTS BY DOCUMENT ORDER

    results = list(best_category_matches.values())

    sentence_positions = {
        sentence: index
        for index, sentence in enumerate(sentences)
    }

    results.sort(
        key=lambda item: sentence_positions[item["sentence"]]
    )

    return results


# ==========================================
# 10. TEST SEMANTIC MATCHER
# ==========================================

if __name__ == "__main__":

    sample_text = """
    SERVICE AGREEMENT

    This agreement expires on 31 December 2026.

    Either party may terminate this agreement by providing
    30 days written notice.

    This agreement shall be governed by the laws of India.

    The total liability of either party shall not exceed
    INR 500000.

    The supplier shall pay liquidated damages of INR 10000
    for each day of delay.

    Either party may terminate this agreement for convenience
    without cause by providing written notice.

    The liability of the supplier shall be unlimited.
    """

    print("\n========== CUAD MATCHING TEST ==========\n")

    results = detect_semantic_clauses(sample_text)

    if results:

        for result in results:

            print("Category:", result["category"])

            print("Sentence:", result["sentence"])

            print("Similarity:", result["similarity"])

            print("Matching Method:", result["matching_method"])

            print("-" * 50)

    else:

        print("No sufficiently strong matches detected.")

    print("\nTotal matches:", len(results))

    print("\nCUAD categories:", len(CATEGORIES))

    print("\nSemantic matching test completed!")
