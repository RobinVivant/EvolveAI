import logging

from flask import Flask, request, jsonify

from config import Config
from meta_agent import MetaAgent

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

if not Config.OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set in the environment variables.")

meta_agent = MetaAgent(Config.OPENROUTER_API_KEY, Config.OPENROUTER_MODEL)


@app.route('/query', methods=['POST'])
def process_query():
    query = request.json.get('query')
    if not query:
        logging.warning("Received request with no query")
        return jsonify({"error": "No query provided"}), 400

    try:
        response = meta_agent.process_query(query)
        return jsonify({"response": response})
    except Exception as e:
        logging.exception(f"Error processing query: {str(e)}")
        return jsonify({"error": f"An error occurred while processing the query: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
