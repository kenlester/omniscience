from message_queue.queues import crawl_queue

def test_crawl_queue():
    """
    A simple test to verify the functionality of the crawl_queue.
    """
    print("--- Testing Crawl Queue ---")

    # Sample URLs to be discovered
    sample_urls = [
        "http://example-retailer.com/products/widget-a",
        "http://another-store.com/items/gadget-b",
        "http://shop-o-rama.com/product/thingamajig-c"
    ]

    print(f"Queue is empty: {crawl_queue.is_empty()}")
    print(f"Initial queue size: {len(crawl_queue)}")

    print("\nPublishing sample URLs to the queue...")
    for url in sample_urls:
        crawl_queue.publish(url)
        print(f"Published: {url}")

    print(f"\nQueue is empty: {crawl_queue.is_empty()}")
    print(f"Queue size after publishing: {len(crawl_queue)}")

    print("\nConsuming messages from the queue...")
    consumed_urls = []
    while not crawl_queue.is_empty():
        message = crawl_queue.consume()
        print(f"Consumed: {message}")
        consumed_urls.append(message)

    print(f"\nQueue is empty: {crawl_queue.is_empty()}")
    print(f"Final queue size: {len(crawl_queue)}")

    print("\n--- Verification ---")
    print(f"Original URLs match consumed URLs: {sample_urls == consumed_urls}")
    if sample_urls != consumed_urls:
        print("Error: The consumed URLs do not match the published URLs or are not in the correct FIFO order.")
    else:
        print("Success: Queue is working as expected.")

if __name__ == "__main__":
    test_crawl_queue()
