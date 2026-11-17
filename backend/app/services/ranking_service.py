import datetime
from typing import Dict, Any

class RankingService:
    """
    Explainable 6-Factor Multi-Criteria Scoring Model
    Calculates a strategic score from 0.0 to 100.0 based on:
    1. Strategic Relevance (Weight: 25%)
    2. Business Impact (Weight: 25%)
    3. Action Urgency (Weight: 20%)
    4. Credibility & Evidence (Weight: 15%)
    5. Recency (Weight: 10%)
    6. Information Novelty (Weight: 5%)
    """

    WEIGHTS = {
        "relevance": 0.25,
        "impact": 0.25,
        "urgency": 0.20,
        "credibility": 0.15,
        "recency": 0.10,
        "novelty": 0.05
    }

    LEVEL_SCORES = {
        "High": 1.0,
        "Medium": 0.6,
        "Low": 0.25
    }

    URGENCY_SCORES = {
        "Immediate": 1.0,
        "Short-Term": 0.75,
        "Medium-Term": 0.45,
        "Watchlist": 0.20
    }

    VERIFICATION_SCORES = {
        "Verified": 1.0,
        "Pending Verification": 0.65,
        "Unverified": 0.30
    }

    @classmethod
    def calculate_ranking(
        cls,
        strategic_relevance: str = "High",
        business_impact: str = "High",
        urgency: str = "Short-Term",
        source_reliability: str = "High",
        evidence_strength: str = "High",
        verification_status: str = "Verified",
        publication_date: datetime.datetime = None,
        discovery_date: datetime.datetime = None,
        is_novel: bool = True
    ) -> Dict[str, Any]:
        # 1. Relevance
        rel_factor = cls.LEVEL_SCORES.get(strategic_relevance, 0.6)
        
        # 2. Impact
        impact_factor = cls.LEVEL_SCORES.get(business_impact, 0.6)
        
        # 3. Urgency
        urg_factor = cls.URGENCY_SCORES.get(urgency, 0.5)
        
        # 4. Credibility (combination of source reliability, evidence strength, verification)
        rel_score = cls.LEVEL_SCORES.get(source_reliability, 0.6)
        ev_score = cls.LEVEL_SCORES.get(evidence_strength, 0.6)
        ver_score = cls.VERIFICATION_SCORES.get(verification_status, 0.65)
        cred_factor = (rel_score * 0.4) + (ev_score * 0.4) + (ver_score * 0.2)
        
        # 5. Recency
        effective_date = publication_date or discovery_date or datetime.datetime.utcnow()
        days_old = max(0, (datetime.datetime.utcnow() - effective_date).days)
        if days_old <= 2:
            recency_factor = 1.0
        elif days_old <= 7:
            recency_factor = 0.85
        elif days_old <= 14:
            recency_factor = 0.65
        elif days_old <= 30:
            recency_factor = 0.40
        else:
            recency_factor = 0.20
            
        # 6. Novelty
        novelty_factor = 1.0 if is_novel else 0.5

        # Weighted calculation (0 - 100 scale)
        weighted_sum = (
            (rel_factor * cls.WEIGHTS["relevance"]) +
            (impact_factor * cls.WEIGHTS["impact"]) +
            (urg_factor * cls.WEIGHTS["urgency"]) +
            (cred_factor * cls.WEIGHTS["credibility"]) +
            (recency_factor * cls.WEIGHTS["recency"]) +
            (novelty_factor * cls.WEIGHTS["novelty"])
        )
        total_score = round(weighted_sum * 100, 1)

        breakdown = {
            "total_score": total_score,
            "components": {
                "strategic_relevance": {
                    "score": round(rel_factor * 100, 1),
                    "weight": cls.WEIGHTS["relevance"],
                    "contribution": round(rel_factor * cls.WEIGHTS["relevance"] * 100, 1)
                },
                "business_impact": {
                    "score": round(impact_factor * 100, 1),
                    "weight": cls.WEIGHTS["impact"],
                    "contribution": round(impact_factor * cls.WEIGHTS["impact"] * 100, 1)
                },
                "action_urgency": {
                    "score": round(urg_factor * 100, 1),
                    "weight": cls.WEIGHTS["urgency"],
                    "contribution": round(urg_factor * cls.WEIGHTS["urgency"] * 100, 1)
                },
                "credibility": {
                    "score": round(cred_factor * 100, 1),
                    "weight": cls.WEIGHTS["credibility"],
                    "contribution": round(cred_factor * cls.WEIGHTS["credibility"] * 100, 1)
                },
                "recency": {
                    "score": round(recency_factor * 100, 1),
                    "weight": cls.WEIGHTS["recency"],
                    "contribution": round(recency_factor * cls.WEIGHTS["recency"] * 100, 1)
                },
                "novelty": {
                    "score": round(novelty_factor * 100, 1),
                    "weight": cls.WEIGHTS["novelty"],
                    "contribution": round(novelty_factor * cls.WEIGHTS["novelty"] * 100, 1)
                }
            },
            "explanation": (
                f"Ranked {total_score}/100. Relevance contributes {round(rel_factor * cls.WEIGHTS['relevance'] * 100, 1)} pts "
                f"due to {strategic_relevance} strategic alignment; Business Impact contributes {round(impact_factor * cls.WEIGHTS['impact'] * 100, 1)} pts. "
                f"Assessed as {urgency} urgency from {verification_status} evidence."
            )
        }

        return {
            "score": total_score,
            "breakdown": breakdown
        }
