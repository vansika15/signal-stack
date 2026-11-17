from app.services.ranking_service import RankingService

def test_ranking_calculation_high_priority():
    result = RankingService.calculate_ranking(
        strategic_relevance="High",
        business_impact="High",
        urgency="Immediate",
        source_reliability="High",
        evidence_strength="High",
        verification_status="Verified"
    )
    assert "score" in result
    assert "breakdown" in result
    assert result["score"] >= 90.0
    assert "components" in result["breakdown"]
    assert "strategic_relevance" in result["breakdown"]["components"]
    assert "business_impact" in result["breakdown"]["components"]

def test_ranking_calculation_low_priority():
    result = RankingService.calculate_ranking(
        strategic_relevance="Low",
        business_impact="Low",
        urgency="Watchlist",
        source_reliability="Low",
        evidence_strength="Low",
        verification_status="Unverified"
    )
    assert result["score"] < 40.0
