from google.cloud import pubsub_v1
import json

def get_project_id():
    """Reads the project ID from the GCP credentials file."""
    try:
        with open('gcp_creds.json', 'r') as f:
            creds = json.load(f)
        return creds['project_id']
    except (FileNotFoundError, KeyError):
        # As a fallback, use the hardcoded project ID.
        print("Warning: Could not read project_id from gcp_creds.json. Using hardcoded ID.")
        return 'omniscience-468322'

class PubSubQueue:
    """
    A wrapper for a Google Cloud Pub/Sub topic to provide a simple
    publishing interface.
    """

    def __init__(self, topic_id):
        self.publisher = pubsub_v1.PublisherClient()
        self.project_id = get_project_id()
        self.topic_path = self.publisher.topic_path(self.project_id, topic_id)
        print(f"PubSubQueue initialized for topic: {self.topic_path}")

    def publish(self, message):
        """
        Publishes a message to the Pub/Sub topic.
        The message will be JSON-encoded if it is not a string.
        """
        if not isinstance(message, str):
            message = json.dumps(message)

        # Data must be a bytestring.
        data = message.encode("utf-8")

        # The publish method returns a future.
        future = self.publisher.publish(self.topic_path, data)

        # Calling result() on the future blocks until the message is published
        # and raises an exception on failure.
        try:
            future.result()
            print(f"Successfully published message to {self.topic_path}")
        except Exception as e:
            print(f"Failed to publish message to {self.topic_path}: {e}")
            raise

    def __repr__(self):
        return f"<PubSubQueue(topic_path='{self.topic_path}')>"

def consume_one_message(subscription_id):
    """
    Pulls a single message from a Pub/Sub subscription.

    Args:
        subscription_id (str): The ID of the subscription to pull from.

    Returns:
        str: The message data as a string, or None if no message is available.
    """
    subscriber = pubsub_v1.SubscriberClient()
    project_id = get_project_id()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    print(f"Pulling one message from {subscription_path}...")

    # The pull method returns a PullResponse object.
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1}
    )

    if not response.received_messages:
        print("No messages received.")
        return None

    received_message = response.received_messages[0]
    message_data = received_message.message.data.decode("utf-8")

    print(f"Received message: {message_data}")

    # Acknowledge the message so it's not delivered again.
    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [received_message.ack_id]}
    )
    print("Message acknowledged.")

    return message_data

# --- Instantiate the queues required by the OMNISCIENCE program ---

# Queue for URLs to be crawled by the Crawler Swarm
crawl_queue = PubSubQueue(topic_id="CRAWL_QUEUE")

# Queue for product page URLs to be processed by the Extractor Swarm
extraction_queue = PubSubQueue(topic_id="EXTRACTION_QUEUE")
