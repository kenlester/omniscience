import json
from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists

def get_project_id():
    """Reads the project ID from the GCP credentials file."""
    try:
        with open('gcp_creds.json', 'r') as f:
            creds = json.load(f)
        return creds['project_id']
    except FileNotFoundError:
        print("Error: gcp_creds.json not found. Make sure to provide the credentials.")
        exit(1)
    except KeyError:
        print("Error: 'project_id' not found in gcp_creds.json.")
        exit(1)

def create_topic_if_not_exists(publisher, topic_path):
    """Creates a Pub/Sub topic if it doesn't already exist."""
    try:
        print(f"Attempting to create topic: {topic_path}...")
        publisher.create_topic(request={"name": topic_path})
        print(f"Topic created: {topic_path}")
    except AlreadyExists:
        print(f"Topic already exists: {topic_path}")
    except Exception as e:
        print(f"An error occurred while creating topic {topic_path}: {e}")
        raise

def create_subscription_if_not_exists(subscriber, topic_path, subscription_path):
    """Creates a Pub/Sub subscription if it doesn't already exist."""
    try:
        print(f"Attempting to create subscription: {subscription_path}...")
        subscriber.create_subscription(
            request={"name": subscription_path, "topic": topic_path}
        )
        print(f"Subscription created: {subscription_path}")
    except AlreadyExists:
        print(f"Subscription already exists: {subscription_path}")
    except Exception as e:
        print(f"An error occurred while creating subscription {subscription_path}: {e}")
        raise

def main():
    """Main function to set up all GCP resources."""
    project_id = get_project_id()

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    # Define topic and subscription names
    topics = {
        "CRAWL_QUEUE": "CRAWL_QUEUE_sub",
        "EXTRACTION_QUEUE": "EXTRACTION_QUEUE_sub"
    }

    print("--- Starting GCP Pub/Sub Resource Setup ---")
    for topic_id, sub_id in topics.items():
        topic_path = publisher.topic_path(project_id, topic_id)
        subscription_path = subscriber.subscription_path(project_id, sub_id)

        create_topic_if_not_exists(publisher, topic_path)
        create_subscription_if_not_exists(subscriber, topic_path, subscription_path)

    print("\n--- GCP Pub/Sub Resource Setup Complete ---")

if __name__ == "__main__":
    main()
