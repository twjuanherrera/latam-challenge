import datetime  # For working with dates
from typing import List, Tuple  # For type annotations
from google.cloud import bigquery  # For interacting with BigQuery
from processing import process_bigquery_results  # External function for processing results
import memory_profiler  # Module for memory profiling # type: ignore

# Decorator to profile memory usage of the function
@memory_profiler.profile
def q1_memory(client: bigquery.Client, query: str) -> List[Tuple[datetime.date, str]]:
    """
    Executes a BigQuery query, profiles its memory usage, and returns extracted date-string pairs.

    Args:
        client: BigQuery client object.
        query: BigQuery SQL query string.

    Returns:
        List of tuples containing date and string pairs extracted from BigQuery results.
    """

    # Delegate query execution and data extraction to the external function:
    # - Assumes 'process_bigquery_results' handles query execution, result processing,
    #   and extraction of date-string pairs.
    return process_bigquery_results(client, query)
