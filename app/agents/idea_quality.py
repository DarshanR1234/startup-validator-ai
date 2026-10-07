def is_idea_valid(idea_analysis: dict) -> tuple[bool, str]:

    def valid(field: str) -> bool:
        value = str(
            idea_analysis.get(field, "")
        ).strip().lower()

        return bool(
            value
            and value != "not specified"
        )

    problem = valid("problem")
    solution = valid("proposed_solution")
    customer = valid("target_customer")

    # A startup idea is usable when it has
    # a concrete solution and a target customer.
    if solution and customer:
        return True, ""

    return (
        False,
        "Startup idea is too vague. "
        "Please specify the problem, solution, "
        "and target customer.",
    )