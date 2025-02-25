from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def receive_request():
    print("Hello, World!")  # Prints to terminal when a request is received
    return "Received!", 200

if __name__ == "__main__":
    app.run(port=5005, debug=True)
