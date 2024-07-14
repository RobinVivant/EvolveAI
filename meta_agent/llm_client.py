import requests


class LLMClient:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model

    def send_request(self, messages):
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "messages": messages
            }
        )
        response_json = response.json()
        return response_json['choices'][0]['message']['content']
