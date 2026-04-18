import requests

def get_ai_response(prompt: str, api_key: str) -> str:
    """
    Sends a prompt to the AI API and returns the response.

    :param prompt: The developer's input prompt
    :param api_key: The developer's API key
    :return: AI response as string
    """

    if not prompt or not isinstance(prompt, str):
        raise ValueError("Invalid prompt")

    if not api_key:
        raise ValueError("API key is required")

    try:
        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": "gpt-5.3",
                "input": prompt
            }
        )

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

        data = response.json()

        # Normalize response safely
        try:
            output = data["output"][0]["content"][0]["text"]
        except (KeyError, IndexError, TypeError):
            raise ValueError("Invalid response format from API")

        if not output:
            raise ValueError("Empty response from API")

        return output

    except Exception as error:
        print(f"AI request failed: {str(error)}")
        raise
