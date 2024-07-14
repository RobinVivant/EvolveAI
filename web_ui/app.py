from flask import Flask, render_template, request, jsonify
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

META_AGENT_URL = 'http://meta-agent:5000/query'
META_AGENT_TIMEOUT = 300  # 5 minutes timeout

app.logger.info(f"Meta-agent URL: {META_AGENT_URL}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_query = request.json.get('query')
    try:
        app.logger.info(f"Sending request to meta-agent: {user_query}")
        response = requests.post(META_AGENT_URL, json={'query': user_query}, timeout=META_AGENT_TIMEOUT)
        response.raise_for_status()
        app.logger.info("Received response from meta-agent")
        try:
            return jsonify(response.json())
        except ValueError:
            app.logger.error("Error decoding JSON from meta-agent response")
            return jsonify({"error": "Invalid response from meta-agent"}), 500
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error connecting to meta-agent: {str(e)}", exc_info=True)
        if isinstance(e, requests.exceptions.Timeout):
            return jsonify({"error": "Request to meta-agent timed out."}), 504
        return jsonify({"error": "Unable to connect to meta-agent service."}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
