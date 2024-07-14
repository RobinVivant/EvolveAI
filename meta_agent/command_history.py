from collections import deque
from llm_client import LLMClient
from config import Config


class CommandHistory:
    def __init__(self, api_key):
        self.history = deque(maxlen=Config.MAX_HISTORY_ITEMS)
        self.summary_client = LLMClient(api_key, Config.OPENROUTER_SUMMARY_MODEL)

    def add_command(self, command, output, reasoning):
        summary = self.summarize(command, output, reasoning)
        self.history.append(summary)

    def summarize(self, command, output, reasoning):
        prompt = f"""Summarize the following command execution in a concise manner:
Command: {command}
Output: {output}
Reasoning: {reasoning}
Provide a brief summary that captures the essence of the command, its output, and the reasoning behind it."""

        messages = [
            {"role": "system", "content": "You are a helpful AI assistant that summarizes command executions."},
            {"role": "user", "content": prompt}
        ]

        summary = self.summary_client.send_request(messages)
        return summary

    def get_history(self):
        return list(self.history)
