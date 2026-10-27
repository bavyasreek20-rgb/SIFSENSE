from app.analyzer import analyze_report


def test_high_risk_phrase_is_flagged():
    result = analyze_report("Worker entered a confined space without gas test.")
    assert result["classification"] == "SIF-Potential"
    assert result["severity_score"] >= 50
    assert len(result["evidence"]) >= 1
    assert "Confined space" in result["life_saving_rules"]


def test_unmatched_report_does_not_claim_detected_precursor():
    result = analyze_report("Housekeeping observation: papers were arranged neatly.")
    assert result["severity_score"] == 0
    assert result["classification"] == "Non-SIF-Potential"
    assert result["evidence"] == []


def test_rule_mapping_is_explainable():
    result = analyze_report("A suspended load moved above the work area.")
    assert any(item["phrase"] == "suspended load" for item in result["evidence"])
    assert "Lifting operations" in result["life_saving_rules"]


def test_score_is_capped():
    result = analyze_report(
        "confined space without gas test; no fall protection; "
        "lockout tagout not applied; line of fire; gas leak"
    )
    assert result["severity_score"] <= 100
