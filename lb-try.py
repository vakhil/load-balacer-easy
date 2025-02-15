from flask import Flask, request, jsonify
import requests
import json
import redis

app = Flask(__name__)

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def get_config():
    return {
        "destination_url": redis_client.get("destination_url"),
        "backend_ip": redis_client.get("backend_ip"),
        "algorithm": redis_client.get("algorithm")
    }

@app.route("/forward", methods=["POST"])
def forward_request():
    destination_url = get_config["destination_url"]
    
    if not destination_url:
        return jsonify({"error": "No destination URL configured"}), 500
    
    try:
        response = requests.post(destination_url, json=request.json)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
