from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

META_AGENT_URL = 'http://meta-agent:5000/query'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_query = request.json.get('query')
    response = requests.post(META_AGENT_URL, json={'query': user_query})
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
