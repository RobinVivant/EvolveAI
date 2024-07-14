import requests
import time


class LLMClient:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model

    def send_request(self, messages):
        start_time = time.time()
        try:
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
            response.raise_for_status()
            end_time = time.time()
            latency = end_time - start_time
            response_json = response.json()
            return response_json['choices'][0]['message']['content'], latency
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending request to LLM: {str(e)}")
            raise
