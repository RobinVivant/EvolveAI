import requests
import time
import logging
import json


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
            try:
                return response_json['choices'][0]['message']['content'], latency
            except (KeyError, IndexError) as e:
                logging.error(f"Error parsing LLM response: {str(e)}")
                raise ValueError("Unexpected response format from LLM")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending request to LLM: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON response: {str(e)}")
            raise ValueError("Invalid JSON response from LLM")
