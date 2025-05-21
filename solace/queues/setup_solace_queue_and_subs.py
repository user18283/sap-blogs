import requests
import argparse
import json
import csv
import urllib3
from requests.auth import HTTPBasicAuth

# Disable insecure HTTPS warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Read parameters
print("reading parameters")
parser = argparse.ArgumentParser(description="Simple login script")
parser.add_argument('--password', required=True, help='Password')
parser.add_argument('--url', required=True, help='SEMP URL')
args = parser.parse_args()

# Connection Properties
SOLACE_BASE_URL = args.url
SOLACE_USERNAME ="mission-control-manager"
SOLACE_PASSWORD = args.password
SOLACE_VPN = "test"


def get_vpn_info():
    """Get information about the Message VPN"""
    endpoint = f"{SOLACE_BASE_URL}/config/msgVpns/{SOLACE_VPN}"

    response = requests.get(
        endpoint,
        auth=HTTPBasicAuth(SOLACE_USERNAME, SOLACE_PASSWORD),
        verify=False  # For production, set to True and use proper certificates
    )

    if response.status_code == 200:
        vpn_info = response.json()
        print(f"VPN Information for '{SOLACE_VPN}':")
        print(json.dumps(vpn_info, indent=2))
        return vpn_info
    else:
        print(f"Failed to retrieve VPN info: {response.status_code}")
        print(response.text)
        return None


def create_queue(queue_name):
    """Create a new queue in the Message VPN"""
    endpoint = f"{SOLACE_BASE_URL}/config/msgVpns/{SOLACE_VPN}/queues"

    queue_data = {
        "queueName": queue_name,
        "accessType": "exclusive",
        "egressEnabled": True,
        "ingressEnabled": True,
        "permission": "consume",
        "maxMsgSpoolUsage": 1000
    }

    response = requests.post(
        endpoint,
        auth=HTTPBasicAuth(SOLACE_USERNAME, SOLACE_PASSWORD),
        json=queue_data,
        verify=False
    )

    if response.status_code in [200, 201]:
        print(f"Queue '{queue_name}' created successfully!")
        return True
    else:
        print(f"Failed to create queue: {response.status_code}")
        print(response.text)
        return False


def add_topic_subscription(queue_name, topic_name):
    """Add a topic subscription to a queue"""
    endpoint = f"{SOLACE_BASE_URL}/config/msgVpns/{SOLACE_VPN}/queues/{queue_name}/subscriptions"

    subscription_data = {
        "subscriptionTopic": topic_name
    }

    response = requests.post(
        endpoint,
        auth=HTTPBasicAuth(SOLACE_USERNAME, SOLACE_PASSWORD),
        json=subscription_data,
        verify=False
    )

    if response.status_code in [200, 201]:
        print(f"Topic '{topic_name}' subscribed to queue '{queue_name}' successfully!")
        return True
    else:
        print(f"Failed to add subscription: {response.status_code}")
        print(response.text)
        return False


def process_csv_file(csv_filename):
    """Process the CSV file to create queues and topic subscriptions"""
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            queue_name = row[0].strip()  # The first column is the queue name
            topics = [topic.strip() for topic in row[1:]]  # The rest are topic names

            # Create queue if it doesn't exist
            if create_queue(queue_name):
                # Subscribe the queue to the topics
                for topic in topics:
                    add_topic_subscription(queue_name, topic)


def main():

    print("Solace SEMP API Client (Port 943)")
    print("================================")

    # Read and process the CSV file
    csv_filename = "input.csv"
    process_csv_file(csv_filename)

if __name__ == "__main__":
    main()