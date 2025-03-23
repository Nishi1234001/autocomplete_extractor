import argparse
import requests
import time
import string
from collections import deque

# The maximum number of results the API returns (indicating saturation).
MAX_RESULTS = 10

# Standard delay between requests (in seconds).
REQUEST_DELAY = 0.5

# Reduced delay when no results are returned.
NO_RESULT_DELAY = 0.1

# Set a maximum prefix length to avoid endless exploration.
MAX_PREFIX_LENGTH = 6

def query_api(prefix, base_url):
    """
    Query the API for a given prefix using the given base URL and return the results and count.
    """
    url = base_url + prefix
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return data.get("results", []), data.get("count", 0)
    except Exception as e:
        print(f"Error querying prefix '{prefix}': {e}")
        return [], 0

def extract_names(base_url):
    """
    Run the BFS extraction process using the provided base URL.
    Returns the set of collected unique names.
    """
    queue = deque(string.ascii_lowercase)
    collected_names = set()
    total_requests = 0

    while queue:
        prefix = queue.popleft()
        results, count = query_api(prefix, base_url)
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

        # Use a shorter delay if count is 0 to speed up execution.
        delay = NO_RESULT_DELAY if count == 0 else REQUEST_DELAY
        time.sleep(delay)

    print("\n--- Extraction Complete ---")
    print(f"Total API Requests Made: {total_requests}")
    print(f"Total Unique Names Collected: {len(collected_names)}")
    return collected_names

def main():
    # Use argparse to get the version parameter from the command line.
    parser = argparse.ArgumentParser(description="Extract names from an autocomplete API.")
    parser.add_argument(
        "--version",
        type=str,
        default="v1",
        help="API version to use (e.g., v1, v2, v3). Default is v1."
    )
    args = parser.parse_args()

    # Construct the base URL using the provided version.
    base_url = f"http://35.200.185.69:8000/{args.version}/autocomplete?query="
    print(f"Using base URL: {base_url}")

    # Extract names using the provided base URL.
    collected_names = extract_names(base_url)

    # Save results to a file named according to the version.
    output_file = f"collected_names_{args.version}.txt"
    with open(output_file, "w") as f:
        for name in sorted(collected_names):
            f.write(name + "\n")

    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()


