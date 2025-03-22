import requests
import time
import string
from collections import deque

# Base URL for the autocomplete API.
BASE_URL = "http://35.200.185.69:8000/v1/autocomplete?query="

# The maximum number of results the API returns (indicating saturation).
MAX_RESULTS = 10

# Delay between requests to handle rate limiting (in seconds).
REQUEST_DELAY = 0.5

# Set a maximum prefix length to avoid endless exploration.
MAX_PREFIX_LENGTH = 6

def query_api(prefix):
    """
    Query the API for a given prefix and return the results and count.
    """
    url = BASE_URL + prefix
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return data.get("results", []), data.get("count", 0)
    except Exception as e:
        print(f"Error querying prefix '{prefix}': {e}")
        return [], 0

def main():
    # Initialize the BFS queue with single lowercase letters.
    queue = deque(string.ascii_lowercase)
    collected_names = set()
    total_requests = 0

    while queue:
        prefix = queue.popleft()
        results, count = query_api(prefix)
        total_requests += 1

        # Add returned names to our collection.
        collected_names.update(results)

        # Expand the branch only if saturated and prefix length is less than MAX_PREFIX_LENGTH.
        if count == MAX_RESULTS and len(prefix) < MAX_PREFIX_LENGTH:
            for char in string.ascii_lowercase:
                new_prefix = prefix + char
                queue.append(new_prefix)

        # Print progress (optional)
        print(f"Queried: {prefix} | Count: {count} | Total Names: {len(collected_names)}")
        
        # Wait to avoid hitting rate limits.
        time.sleep(REQUEST_DELAY)

    print("\n--- Extraction Complete ---")
    print(f"Total API Requests Made: {total_requests}")
    print(f"Total Unique Names Collected: {len(collected_names)}")

    return collected_names  # Ensure `collected_names` is returned

if __name__ == "__main__":
    collected_names = main()  # Retrieve `collected_names`

    # Save results to a file
    with open("collected_names.txt", "w") as f:
        for name in sorted(collected_names):
            f.write(name + "\n")

    print("Results saved to collected_names.txt")


