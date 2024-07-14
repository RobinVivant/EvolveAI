import os

class Config:
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
    OPENROUTER_MODEL = os.environ.get('OPENROUTER_MODEL', 'openai/gpt-4')
    DOCKER_IMAGE = os.environ.get('DOCKER_IMAGE', 'meta-agent-env')
    MAX_TOKENS = 1024
    TEMPERATURE = 0
