from flask import Flask, request
import requests

app = Flask(__name__)

# Target URL to forward requests to
TARGET_URL = "https://example.com"

@app.route("/", methods=["GET"])
def forward_request():
    # Forward the request to the target URL
    response = requests.get(TARGET_URL, params=request.args)

    # Return the response from the target server
    return response.content, response.status_code, response.headers.items()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
