# Meta-Agent Application

This application implements a meta-agent that can process queries, solve complex problems, and continuously improve its capabilities.

## Setup

1. Install Docker on your system.
2. Install Poetry for Python dependency management.
3. Clone this repository.
4. Run `poetry install` to install the required dependencies.
5. Set the OPENAI_API_KEY environment variable with your OpenAI API key.

## Running the Application

1. Build the Docker image: `docker build -t meta-agent-env .`
2. Run the application: `poetry run python meta_agent/main.py`

The application will start a Flask server that listens for queries on port 5000.

## Usage

Send a POST request to `http://localhost:5000/query` with a JSON body containing the query:

```json
{
    "query": "Your query here"
}
```

The application will process the query and return a response.

## Security Considerations

- The application runs in a Docker container to provide isolation from the host system.
- User inputs are sanitized to prevent injection attacks.
- The Docker container has limited permissions to minimize potential risks.

## Future Improvements

- Implement more sophisticated error handling and logging.
- Add support for more external tools and APIs.
- Implement a more advanced system prompt update mechanism.
