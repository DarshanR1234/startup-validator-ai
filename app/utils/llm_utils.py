import json
import time
from typing import Type, TypeVar, Any

from pydantic import BaseModel
from groq import Groq, RateLimitError, BadRequestError

from app.config.settings import settings


T = TypeVar("T", bound=BaseModel)

_client = None


def get_groq_client() -> Groq:
    global _client

    if _client is None:
        _client = Groq(
            api_key=settings.groq_api_key
        )

    return _client


def to_strict_json_schema(
    model_cls: Type[T],
) -> dict:
    schema = model_cls.model_json_schema()

    def _make_strict(node):
        if isinstance(node, dict):

            if "properties" in node:
                node["additionalProperties"] = False
                node["required"] = list(
                    node["properties"].keys()
                )

            for value in node.values():
                _make_strict(value)

        elif isinstance(node, list):

            for item in node:
                _make_strict(item)

    _make_strict(schema)

    return schema


def sanitize_data_for_model(
    model_cls: Type[T],
    data: Any,
) -> dict:

    if not isinstance(data, dict):
        data = {}

    for field_name, field_info in model_cls.model_fields.items():

        annotation = field_info.annotation
        annotation_str = str(annotation)

        if (
            field_name not in data
            or data[field_name] is None
        ):

            if "list" in annotation_str.lower():
                data[field_name] = []

            elif (
                "int" in annotation_str.lower()
                or "float" in annotation_str.lower()
            ):
                data[field_name] = 0

            elif "dict" in annotation_str.lower():
                data[field_name] = {}

            else:
                data[field_name] = ""

            continue

        value = data[field_name]

        # String expected but list received
        if annotation is str and isinstance(
            value,
            list,
        ):
            data[field_name] = "\n".join(
                str(item)
                for item in value
            )

        # String expected but number/bool received
        elif annotation is str and isinstance(
            value,
            (int, float, bool),
        ):
            data[field_name] = str(value)

        # Integer expected but string received
        elif annotation is int and isinstance(
            value,
            str,
        ):
            try:
                data[field_name] = int(value)

            except ValueError:
                data[field_name] = 0

        # List fields
        elif (
            hasattr(annotation, "__origin__")
            and annotation.__origin__ is list
        ):

            if not isinstance(value, list):
                value = [value]

            args = getattr(
                annotation,
                "__args__",
                (),
            )

            if (
                args
                and isinstance(args[0], type)
                and issubclass(args[0], BaseModel)
            ):

                item_cls = args[0]
                new_list = []

                for item in value:

                    if isinstance(item, str):

                        if "claim" in item_cls.model_fields:
                            new_list.append(
                                {
                                    "claim": item,
                                    "source": "",
                                }
                            )

                        elif "name" in item_cls.model_fields:
                            new_list.append(
                                {
                                    "name": item,
                                    "priority": 1,
                                }
                            )

                        elif "reason" in item_cls.model_fields:
                            new_list.append(
                                {
                                    "reason": item
                                }
                            )

                        else:
                            new_list.append({})

                    elif isinstance(item, dict):

                        new_list.append(
                            sanitize_data_for_model(
                                item_cls,
                                item,
                            )
                        )

                    else:
                        new_list.append(item)

                data[field_name] = new_list

            else:

                data[field_name] = [
                    str(item)
                    for item in value
                ]

        # Nested Pydantic model
        elif (
            isinstance(annotation, type)
            and issubclass(annotation, BaseModel)
        ):

            if isinstance(value, dict):

                data[field_name] = (
                    sanitize_data_for_model(
                        annotation,
                        value,
                    )
                )

            else:

                data[field_name] = (
                    sanitize_data_for_model(
                        annotation,
                        {}
                    )
                )

    return data


def _is_daily_limit_error(
    error: Exception,
) -> bool:

    message = str(error).lower()

    return (
        "tokens per day" in message
        or "tpd" in message
        or "daily limit" in message
    )


def invoke_structured_llm(
    model_cls: Type[T],
    system_prompt: str,
    user_prompt: str,
    max_retries: int = 3,
    retry_delay: float = 4.0,
    max_tokens: int = 1536,
    response_mode: str = "json_object",
) -> T:

    client = get_groq_client()

    strict_schema = to_strict_json_schema(
        model_cls
    )

    name = model_cls.__name__

    required_keys = list(
        strict_schema.get(
            "properties",
            {}
        ).keys()
    )

    keys_str = ", ".join(
        required_keys
    )

    enhanced_system_prompt = (
        f"{system_prompt}\n\n"
        "CRITICAL INSTRUCTIONS:\n"
        f"- Respond ONLY with a valid JSON object matching the '{name}' schema.\n"
        f"- Include ALL top-level properties: {keys_str}.\n"
        "- Every required property MUST be present.\n"
        "- Do not omit any criterion.\n"
        "- Array fields must contain realistic items.\n"
        "- String fields must contain text.\n"
        "- Numeric values for string fields must be returned as strings.\n"
        "- Do not use markdown.\n"
        "- Do not add explanations outside JSON."
    )

    last_exception = None

    for attempt in range(
        1,
        max_retries + 1,
    ):

        try:

            prompt_chars = (
                len(enhanced_system_prompt)
                + len(user_prompt)
            )

            print(
                f"[LLM] {name} | "
                f"prompt_chars={prompt_chars} | "
                f"max_tokens={max_tokens}"
            )

            if response_mode == "json_object":

                format_spec = {
                    "type": "json_object"
                }

            else:

                format_spec = {
                    "type": "json_schema",
                    "json_schema": {
                        "name": name.lower(),
                        "strict": True,
                        "schema": strict_schema,
                    },
                }

            response = client.chat.completions.create(
                model=settings.development_model,

                messages=[
                    {
                        "role": "system",
                        "content": enhanced_system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],

                temperature=0,

                max_tokens=max_tokens,

                include_reasoning=False,

                response_format=format_spec,
            )

            usage = getattr(
                response,
                "usage",
                None,
            )

            if usage:

                print(
                    f"[LLM USAGE] {name} | "
                    f"prompt={getattr(usage, 'prompt_tokens', '?')} | "
                    f"completion={getattr(usage, 'completion_tokens', '?')} | "
                    f"total={getattr(usage, 'total_tokens', '?')}"
                )

            content = (
                response
                .choices[0]
                .message
                .content
            )

            if not content:
                raise ValueError(
                    "Groq returned empty content."
                )

            content_clean = content.strip()

            if content_clean.startswith("```json"):
                content_clean = content_clean[7:]

            elif content_clean.startswith("```"):
                content_clean = content_clean[3:]

            if content_clean.endswith("```"):
                content_clean = content_clean[:-3]

            content_clean = content_clean.strip()

            data = json.loads(
                content_clean
            )

            if not isinstance(data, dict):
                raise ValueError(
                    "Groq response is not a JSON object."
                )

            sanitized_data = (
                sanitize_data_for_model(
                    model_cls,
                    data,
                )
            )

            return model_cls.model_validate(
                sanitized_data
            )

        except RateLimitError as exc:

            last_exception = exc

            if _is_daily_limit_error(exc):

                print(
                    f"[LLM Daily Limit] "
                    f"{name} cannot continue. "
                    f"Daily token limit exhausted."
                )

                break

            wait_time = (
                retry_delay
                * (1.5 ** (attempt - 1))
            )

            print(
                f"[LLM Rate Limit] "
                f"Retrying {name} in "
                f"{wait_time:.1f}s "
                f"(Attempt {attempt}/{max_retries})..."
            )

            time.sleep(wait_time)

        except BadRequestError as exc:

            last_exception = exc

            print(
                f"[LLM Bad Request] "
                f"{name}: {exc}"
            )

            break

        except (
            ValueError,
            json.JSONDecodeError,
        ) as exc:

            last_exception = exc

            print(
                f"[LLM Error] "
                f"Retrying {name} "
                f"(Attempt {attempt}/{max_retries}): "
                f"{exc}"
            )

            time.sleep(2.0)

        except Exception as exc:

            last_exception = exc

            print(
                f"[LLM Exception] "
                f"Retrying {name} "
                f"(Attempt {attempt}/{max_retries}): "
                f"{exc}"
            )

            time.sleep(2.0)

    raise RuntimeError(
        f"Failed to generate structured output "
        f"for {name} after {max_retries} attempts. "
        f"Last error: {last_exception}"
    ) from last_exception