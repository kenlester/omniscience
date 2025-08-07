import collections

class InMemoryQueue:
    """
    A simple in-memory queue implementation using collections.deque
    for efficient and thread-safe appends and pops from either side.
    """
    def __init__(self):
        self._queue = collections.deque()

    def publish(self, message):
        """Adds a message to the right end of the queue."""
        self._queue.append(message)

    def consume(self):
        """Removes and returns a message from the left end of the queue."""
        if not self.is_empty():
            return self._queue.popleft()
        return None

    def is_empty(self):
        """Returns True if the queue is empty, False otherwise."""
        return len(self._queue) == 0

    def __len__(self):
        """Returns the number of items in the queue."""
        return len(self._queue)

# --- Instantiate the queues required by the OMNISCIENCE program ---

# Queue for URLs to be crawled by the Crawler Swarm
crawl_queue = InMemoryQueue()

# Queue for product page URLs to be processed by the Extractor Swarm
extraction_queue = InMemoryQueue()
