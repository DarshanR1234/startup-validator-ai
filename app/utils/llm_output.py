import json
from typing import Any


def parse_json_response(content: str) -> dict[str, Any]:
    """
    Safely parse an LLM JSON response.
    """

    if not content:
        raise ValueError("LLM returned an empty response.")

    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM returned invalid JSON: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError(
            "LLM response must be a JSON object."
        )

    return data


def ensure_list(
    data: dict[str, Any],
    field: str,
) -> None:
    """
    Ensure a field exists and is a list.
    Missing fields become empty lists.
    """

    value = data.get(field)

    if value is None:
        data[field] = []

    elif not isinstance(value, list):
        data[field] = [value]


def ensure_string(
    data: dict[str, Any],
    field: str,
    default: str = "",
) -> None:
    """
    Ensure a field exists and is a string.
    """

    value = data.get(field)

    if value is None:
        data[field] = default

    elif not isinstance(value, str):
        data[field] = str(value)