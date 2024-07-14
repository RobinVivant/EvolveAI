from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

META_AGENT_URL = 'http://meta-agent:5000/query'
META_AGENT_TIMEOUT = 300  # 5 minutes timeout

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_query = request.json.get('query')
    try:
        response = requests.post(META_AGENT_URL, json={'query': user_query}, timeout=META_AGENT_TIMEOUT)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error connecting to meta-agent: {str(e)}")
        return jsonify({"error": "Unable to connect to meta-agent service. The request may have timed out."}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
