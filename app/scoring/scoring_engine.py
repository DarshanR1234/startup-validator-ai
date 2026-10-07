from typing import Any


WEIGHTS = {
    "market_demand": 0.20,
    "customer_need": 0.20,
    "competition": 0.15,
    "business_potential": 0.15,
    "pricing_potential": 0.10,
    "feasibility": 0.10,
    "mvp_clarity": 0.10,
}


def calculate_validation_score(evaluation: Any) -> dict:
    """
    Calculate the deterministic startup validation score.

    Each criterion is scored from 0 to 10.
    The final score is converted to a 0-100 scale.
    """

    weighted_scores = {}

    for criterion, weight in WEIGHTS.items():
        criterion_score = getattr(evaluation, criterion).score

        weighted_scores[criterion] = (
            criterion_score / 10
        ) * (weight * 100)

    overall_score = round(
        sum(weighted_scores.values()),
        2
    )

    verdict = get_verdict(overall_score)

    return {
        "weighted_scores": weighted_scores,
        "overall_score": overall_score,
        "verdict": verdict,
    }


def get_verdict(score: float) -> str:

    if score < 40:
        return "High Risk"

    if score < 60:
        return "Weak Potential"

    if score < 75:
        return "Moderate Potential"

    if score < 90:
        return "Strong Potential"

    return "Excellent Potential"