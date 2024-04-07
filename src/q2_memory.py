from typing import List, Tuple  # For type annotations
from google.cloud import bigquery  # For interacting with BigQuery
from processing import process_bigquery_results  # External function for processing results
import memory_profiler  # Module for memory profiling # type: ignore

# Decorator to profile memory usage of the function
@memory_profiler.profile
def q2_memory(client: bigquery.Client, query: str) -> List[Tuple[str, int]]:
    """
    Executes a BigQuery query, profiles its memory usage, extracts string-integer pairs,
    and handles potential conversion errors.

    Args:
        client: BigQuery client object.
        query: BigQuery SQL query string.

    Returns:
        List of tuples containing string-integer pairs extracted from BigQuery results.
        Returns an empty list if data conversion fails.
    """

    try:
        # Delegate query execution and data extraction to the external function:
        results = process_bigquery_results(client, query)

        # Extract string-integer pairs, validating data format:
        # - Assumes 'process_bigquery_results' returns a list of iterables with two elements.
        # - Attempts to convert the second element of each row to an integer.
        return [(row[0], int(row[1])) for row in results]

    except ValueError as e:
        # Handle potential errors during data conversion:
        print(f"Error converting data to string and integer pairs: {e}")
        return []  # Return an empty list to signal the error
