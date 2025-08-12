import json
from google.cloud import pubsub_v1
from google.api_core.exceptions import NotFound

def get_project_id():
    """Reads the project ID from the GCP credentials file."""
    try:
        with open('gcp_creds.json', 'r') as f:
            creds = json.load(f)
        return creds['project_id']
    except (FileNotFoundError, KeyError):
        print("Warning: gcp_creds.json not found or missing project_id. Using hardcoded ID.")
        return 'omniscience-468322'

def delete_subscription_if_exists(subscriber, subscription_path):
    """Deletes a Pub/Sub subscription if it exists."""
    try:
        subscriber.delete_subscription(request={"subscription": subscription_path})
        print(f"Subscription deleted: {subscription_path}")
    except NotFound:
        print(f"Subscription not found, skipping: {subscription_path}")
    except Exception as e:
        print(f"An error occurred while deleting subscription {subscription_path}: {e}")
        raise

def delete_topic_if_exists(publisher, topic_path):
    """Deletes a Pub/Sub topic if it exists."""
    try:
        publisher.delete_topic(request={"topic": topic_path})
        print(f"Topic deleted: {topic_path}")
    except NotFound:
        print(f"Topic not found, skipping: {topic_path}")
    except Exception as e:
        print(f"An error occurred while deleting topic {topic_path}: {e}")
        raise

def main():
    """Main function to tear down all GCP resources."""
    project_id = get_project_id()

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()

    # Define topic and subscription names
    topics = {
        "CRAWL_QUEUE": "CRAWL_QUEUE_sub",
        "EXTRACTION_QUEUE": "EXTRACTION_QUEUE_sub"
    }

    print("--- Starting GCP Pub/Sub Resource Teardown ---")
    for topic_id, sub_id in topics.items():
        topic_path = publisher.topic_path(project_id, topic_id)
        subscription_path = subscriber.subscription_path(project_id, sub_id)

        # Subscriptions must be deleted before their topics
        delete_subscription_if_exists(subscriber, subscription_path)
        delete_topic_if_exists(publisher, topic_path)

    print("\n--- GCP Pub/Sub Resource Teardown Complete ---")

if __name__ == "__main__":
    main()
