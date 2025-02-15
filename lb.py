from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import requests
import redis
import threading
import json

# Redis setup
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_CHANNEL = 'config_updates'

# Initialize Redis connection
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# Local memory to store configurations
config_cache = {}

def handle_config_update(message):
    """Handle incoming configuration updates from Redis."""
    if message['type'] == 'message':
        data = json.loads(message['data'])
        algorithm = data.get('algorithm')
        backend_servers = data.get('backend_servers')
        # Update local memory
        config_cache['algorithm'] = algorithm
        config_cache['backend_servers'] = backend_servers
        print("Updated config cache:", config_cache)

def start_redis_subscriber():
    """Start a Redis subscriber in a separate thread."""
    pubsub = redis_client.pubsub()
    pubsub.subscribe(REDIS_CHANNEL)
    print("Redis subscriber started. Listening for config updates...")
    for message in pubsub.listen():
        handle_config_update(message)

class ForwardingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests and forward them to Google."""
        # Parse the URL and query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # Forward the request to Google
        google_url = 'https://www.google.com/search'
        google_response = requests.get(google_url, params=query_params)

        # Log the current configuration (for demonstration purposes)
        print("Current config cache:", config_cache)

        # Send the response from Google back to the client
        self.send_response(google_response.status_code)
        self.send_header('Content-type', google_response.headers['Content-Type'])
        self.end_headers()
        self.wfile.write(google_response.content)

def run(server_class=HTTPServer, handler_class=ForwardingHandler, port=8080):
    """Start the HTTP server."""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    # Start the Redis subscriber in a separate thread
    redis_thread = threading.Thread(target=start_redis_subscriber, daemon=True)
    redis_thread.start()

    # Start the HTTP server
    run()