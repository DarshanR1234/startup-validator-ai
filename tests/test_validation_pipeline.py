from app.graph.graph import build_startup_validation_graph


def test_startup_validation_pipeline():

    startup_idea = """
    I want to build an AI-powered platform that helps
    small restaurants predict food demand and reduce food waste.
    """

    graph = build_startup_validation_graph()

    initial_state = {
        "startup_idea": startup_idea
    }

    config = {
        "configurable": {
            "thread_id": "test-validation-pipeline"
        }
    }

    result = graph.invoke(
        initial_state,
        config=config
    )

    assert "scoring_result" in result

    scoring_result = result["scoring_result"]

    assert "overall_score" in scoring_result
    assert "verdict" in scoring_result

    assert 0 <= scoring_result["overall_score"] <= 100