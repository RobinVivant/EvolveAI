import os

class Config:
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    DOCKER_IMAGE = "meta-agent-env"
    MAX_TOKENS = 1024
    TEMPERATURE = 0
