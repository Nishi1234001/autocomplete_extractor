# Autocomplete API Name Extraction


## Overview
This project extracts all possible names from an autocomplete API using a breadth-first search (BFS) strategy. The goal is to systematically explore the API's autocomplete functionality, handle rate limiting, and compile a unique list of names.

## Methodology
- **BFS Strategy:**  
  We start with all single letters and expand branches that return the maximum number of results (i.e., saturated branches).
- **API Rate Limiting:**  
  A delay (`REQUEST_DELAY = 0.5` seconds) is used between requests to avoid hitting the API rate limits.
- **Data Aggregation:**  
  Names are collected in a set to remove duplicates and are then saved to `collected_names.txt`.

## Findings
- **Total API Requests Made:** 572 requests  
- **Total Unique Names Collected:** 242 names

## Usage Instructions
1. Ensure you have Python installed.
2. Install dependencies: `pip install requests`
3. Run the script: `python extract_names.py`
4. The output will be saved in `collected_names.txt`.

## Challenges
- Handling rate limiting by implementing a delay between requests.
- Ensuring completeness by expanding saturated prefixes.

