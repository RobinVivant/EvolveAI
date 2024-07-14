import os


class Config:
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY must be set in environment variables")
    OPENROUTER_MODEL = os.environ.get('OPENROUTER_MODEL', 'anthropic/claude-3.5-sonnet')
    OPENROUTER_SUMMARY_MODEL = os.environ.get('OPENROUTER_SUMMARY_MODEL', 'anthropic/claude-3-haiku')
    DOCKER_IMAGE = os.environ.get('DOCKER_IMAGE', 'meta-agent-env')
    MAX_RECURSION_DEPTH = int(os.environ.get('MAX_RECURSION_DEPTH', 3))
    MAX_HISTORY_ITEMS = int(os.environ.get('MAX_HISTORY_ITEMS', 10))
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
