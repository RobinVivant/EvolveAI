import os
import docker
from flask import Flask, request, jsonify
from meta_agent import MetaAgent

app = Flask(__name__)
meta_agent = MetaAgent()

@app.route('/query', methods=['POST'])
def process_query():
    query = request.json.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    response = meta_agent.process_query(query)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
