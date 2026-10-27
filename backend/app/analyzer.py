"""Transparent baseline analyzer for demonstration only.

Weights and mappings are illustrative heuristics, not a validated safety model.
Review and adapt them with qualified HSE professionals before any real use.
"""
import re
from typing import Dict, List

# Curated demo lexicon. Keep phrases specific enough to reduce false positives.
# Rule names are illustrative labels, not an authoritative rule-compliance decision.
PRECURSORS = [
    {"phrase": "confined space without gas test", "category": "Confined space", "weight": 10,
     "rules": ["Confined space"]},
    {"phrase": "entered a confined space without", "category": "Confined space", "weight": 10,
     "rules": ["Confined space"]},
    {"phrase": "working at height without fall protection", "category": "Working at height", "weight": 10,
     "rules": ["Working at height"]},
    {"phrase": "no fall protection", "category": "Working at height", "weight": 9,
     "rules": ["Working at height"]},
    {"phrase": "lockout tagout not applied", "category": "Energy isolation", "weight": 10,
     "rules": ["Energy isolation"]},
    {"phrase": "energy source was not isolated", "category": "Energy isolation", "weight": 10,
     "rules": ["Energy isolation"]},
    {"phrase": "line of fire", "category": "Line of fire", "weight": 8,
     "rules": ["Line of fire"]},
    {"phrase": "suspended load", "category": "Lifting operations", "weight": 8,
     "rules": ["Lifting operations"]},
    {"phrase": "vehicle near miss", "category": "Driving", "weight": 7,
     "rules": ["Driving"]},
    {"phrase": "exceeded speed limit", "category": "Driving", "weight": 7,
     "rules": ["Driving"]},
    {"phrase": "gas leak", "category": "Hazardous atmosphere", "weight": 8,
     "rules": ["Confined space", "Energy isolation"]},
    {"phrase": "high pressure release", "category": "Pressure release", "weight": 9,
     "rules": ["Energy isolation"]},
    {"phrase": "bypassed safety interlock", "category": "Safety system bypass", "weight": 9,
     "rules": ["Energy isolation"]},
    {"phrase": "excavation without permit", "category": "Ground disturbance", "weight": 9,
     "rules": ["Ground disturbance"]},
    {"phrase": "electrical panel exposed", "category": "Electrical hazard", "weight": 8,
     "rules": ["Energy isolation"]},
]

DISCLAIMER = (
    "Prototype triage only. This heuristic result is not a probability or a safety decision. "
    "A qualified HSE professional must review the original report."
)


def analyze_report(report_text: str) -> Dict:
    """Return explainable phrase matches, score, triage label, and rule hints."""
    normalized = re.sub(r"\s+", " ", report_text.lower()).strip()
    evidence: List[Dict] = []
    rules = set()
    total_weight = 0

    for item in PRECURSORS:
        phrase = item["phrase"]
        if phrase in normalized:
            evidence.append({
                "phrase": phrase,
                "category": item["category"],
                "severity_weight": item["weight"],
                "matched_text": phrase,
            })
            total_weight += item["weight"]
            rules.update(item["rules"])

    # Cap score at 100; this is a heuristic index, not a calibrated probability.
    score = min(100, total_weight * 10)
    classification = "SIF-Potential" if score >= 50 else "Non-SIF-Potential"
    if classification == "SIF-Potential":
        recommendation = (
            "Prioritize for prompt review by the HSE team. Verify the context, controls, "
            "and required corrective actions before making any operational decision."
        )
    elif evidence:
        recommendation = (
            "Review the matched precursor and surrounding context during routine HSE review. "
            "Do not treat a low score as proof that the report is safe."
        )
    else:
        recommendation = (
            "No configured precursor phrase was matched. Manually review the report; "
            "the baseline may miss relevant risks expressed in different wording."
        )

    return {
        "classification": classification,
        "severity_score": score,
        "evidence": evidence,
        "life_saving_rules": sorted(rules),
        "recommendation": recommendation,
        "disclaimer": DISCLAIMER,
    }
