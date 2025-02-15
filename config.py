import redis
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
    """Handle incoming configuration updates."""
    data = json.loads(message['data'])
    algorithm = data['algorithm']
    backend_servers = data['backend_servers']
    # Update local memory
    config_cache['algorithm'] = algorithm
    config_cache['backend_servers'] = backend_servers
    print("Updated config cache:", config_cache)

# Subscribe to the Redis channel
pubsub = redis_client.pubsub()
pubsub.subscribe(**{REDIS_CHANNEL: handle_config_update})

print("Listening for config updates...")
for message in pubsub.listen():
    if message['type'] == 'message':
        handle_config_update(message)