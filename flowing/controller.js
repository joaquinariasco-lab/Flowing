import json
from jsonschema import Draft7Validator, ValidationError

# You must implement this
# def get_ai_response(prompt: str, api_key: str) -> str:
#     ...

def get_validated_ai_response(
    prompt: str,
    schema: dict,
    api_key: str,
    max_retries: int = 3
) -> dict:
    """
    Validates and enforces schema on AI output.
    Retries until valid or max_retries reached.

    :param prompt: Original developer prompt
    :param schema: JSON schema provided by developer
    :param api_key: API key
    :param max_retries: Max retry attempts
    :return: Valid structured output (dict)
    """

    validator = Draft7Validator(schema)

    attempt = 0
    last_error = None

    while attempt < max_retries:
        attempt += 1

        try:
            structured_prompt = f"""
Return ONLY valid JSON matching this schema:
{json.dumps(schema)}

User request:
{prompt}
"""

            raw_output = get_ai_response(structured_prompt, api_key)

            try:
                parsed = json.loads(raw_output)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format")

            errors = list(validator.iter_errors(parsed))

            if not errors:
                return parsed
            else:
                last_error = [e.message for e in errors]
                print(f"Validation failed (attempt {attempt}): {last_error}")

        except Exception as err:
            last_error = str(err)
            print(f"Attempt {attempt} failed: {last_error}")

    raise Exception(
        f"Failed to generate valid response after {max_retries} attempts.\n"
        f"Last error: {last_error}"
    )
