from app.schemas.agent_outputs import IdeaAnalysis
from app.utils.llm_utils import invoke_structured_llm


def analyze_startup_idea(
    startup_idea: str,
) -> IdeaAnalysis:

    system_prompt = (
        "You analyze startup ideas. "
        "Return only valid structured output. "
        "Keep every field concise."
    )

    user_prompt = f"""
STARTUP IDEA:
{startup_idea}

Extract:

- problem
- proposed_solution
- target_industry
- target_customer
- business_model
- key_value_proposition
- assumptions

Rules:

- Use only information supported by the startup idea.
- Do not invent facts.
- If something is genuinely missing, use "Not specified".
- Keep each field to one concise sentence.
- assumptions should contain at most 3 short items.
- Return ONLY the structured output.
"""

    return invoke_structured_llm(
        model_cls=IdeaAnalysis,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=1024,
        response_mode="json_object",
    )