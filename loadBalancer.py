from flask import Flask, request
import requests
import mysql.connector
import threading
import time


machines = []
app = Flask(__name__)

# Target: Forward to receiving server
TARGET_URL = "http://127.0.0.1:5001"

def fetch_settings():
    print("Fetching healthy machines from DB...", flush=True)
    global machines
    while True :
        print("OK")
        mydb = mysql.connector.connect(
            host="localhost",
            username="root",
            password="root",
            database="LoadBalancerDB"
        )

        
        cursor = mydb.cursor()
        query = ("SELECT ip_address, port FROM machines "
            "WHERE status='healthy'")

        cursor.execute(query)
        
        ip_hosts = []
        ip_ports = []
        for (ip_address, port) in cursor:
            ip_hosts.append(ip_address)
            ip_ports.append(port)
        

        machines = [[ip_hosts[0],ip_ports[0]], [ip_hosts[1],ip_ports[1]]]
        print(machines)
        print("http://"+str(machines[0][0])+":"+str(machines[0][1]))
        time.sleep(10)



@app.route("/", methods=["GET"])
def forward_request():
    global machines
    try:
        for machine in machines:
            # Forward the request to the receiving server
            print("http://"+str(machine[0])+":"+str(machine[1]))
            response = requests.get("http://"+str(machine[0])+":"+str(machine[1]), params=request.args)
            
            # Add code to send to machines in a load balanced way
            # Fetch from DB or somehow get information in a hashtable and go through the loop 
            # Pull Data from DB on periodic basis 
            # Round robin method 
            



            # Debug print to check forwarding
            print(f"Forwarded request to {TARGET_URL}, received status: {response.status_code}")

            # Return the same response back to the client
            return response.content, response.status_code, response.headers.items()
        
    except Exception as e:
        print(f"Error forwarding request: {e}")
        return "Error forwarding request", 500

if __name__ == "__main__":
    thread = threading.Thread(target=fetch_settings, daemon=True)
    thread.start()
    time.sleep(3)

    app.run(port=5000, debug=True)

