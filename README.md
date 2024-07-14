# Meta-Agent Application

This application implements a meta-agent that can process queries, solve complex problems, and continuously improve its capabilities. The meta-agent operates within a Docker container, providing a secure and isolated environment for executing commands and solving problems.

## How It Works

The Meta-Agent application consists of several key components:

1. **Query Processing**: The agent accepts natural language queries through a Flask API endpoint.

2. **LLM Integration**: It uses the OpenRouter API to interact with large language models for processing queries and generating responses.

3. **Command Execution**: The agent can execute shell commands within the Docker container and capture their output.

4. **Feedback Loop**: A recursive feedback mechanism allows the agent to refine its responses and solve complex problems through multiple iterations.

5. **Command History**: The agent maintains a history of executed commands, which informs future decision-making.

6. **Dynamic System Prompt**: The system prompt is generated dynamically, incorporating container information and command history.

## Setup and Running

### Prerequisites

1. Install Docker on your system.
2. Install Poetry for Python dependency management.

### Setup

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```
   poetry install
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root with the following content:
     ```
     OPENROUTER_API_KEY=your_openrouter_api_key
     OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
     OPENROUTER_SUMMARY_MODEL=anthropic/claude-3-haiku
     ```
   Replace `your_openrouter_api_key` with your actual OpenRouter API key.

### Building and Running the Docker Container

1. Build the Docker image:
   ```
   docker build -t meta-agent-env .
   ```

2. Run the Docker container:
   ```
   docker run -p 5000:5000 --env-file .env meta-agent-env
   ```

This command starts the container, maps port 5000 from the container to the host, and loads the environment variables from the `.env` file.

## Usage

Once the container is running, you can interact with the Meta-Agent by sending POST requests to `http://localhost:5000/query` with a JSON body containing the query:

```json
{
    "query": "Your query here"
}
```

The application will process the query using the Meta-Agent and return a response.

## Configuration

The application uses the following environment variables for configuration:

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)
- `OPENROUTER_MODEL`: The model to use for main queries (default: 'anthropic/claude-3.5-sonnet')
- `OPENROUTER_SUMMARY_MODEL`: The model to use for summarization (default: 'anthropic/claude-3-haiku')
- `DOCKER_IMAGE`: The Docker image to use for the container (default: 'meta-agent-env')
- `MAX_RECURSION_DEPTH`: Maximum depth for the feedback loop (default: 3)
- `MAX_HISTORY_ITEMS`: Maximum number of items in the command history (default: 10)

You can set these environment variables in the `.env` file or modify them in the `config.py` file.

## Security Considerations

- The application runs in a Docker container to provide isolation from the host system.
- User inputs are processed through the LLM to prevent direct injection of malicious commands.
- The Docker container runs with limited permissions to minimize potential risks.

## Future Improvements

- Implement more sophisticated error handling and logging.
- Add support for more external tools and APIs within the container.
- Enhance the command history management and summarization capabilities.
- Implement a more advanced system prompt update mechanism.
- Add user authentication and rate limiting for the API endpoint.
