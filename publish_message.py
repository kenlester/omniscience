import sys
from message_queue.queues import PubSubQueue

def main():
    """
    A command-line utility to publish a message to a GCP Pub/Sub topic.

    Usage:
        python publish_message.py <topic_id> "<message>"
    """
    if len(sys.argv) != 3:
        print("Usage: python publish_message.py <topic_id> \"<message>\"")
        sys.exit(1)

    topic_id = sys.argv[1]
    message = sys.argv[2]

    print(f"Attempting to publish to topic: {topic_id}")

    try:
        queue = PubSubQueue(topic_id=topic_id)
        queue.publish(message)
        print("Message published successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
