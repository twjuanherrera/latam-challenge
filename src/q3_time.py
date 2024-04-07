from typing import List, Tuple  # For type annotations
from google.cloud import bigquery  # For interacting with BigQuery
from processing import process_bigquery_results  # External function for processing results
import line_profiler  # Module for line-by-line profiling # type: ignore

# Decorator for line-by-line profiling of the function's execution time
@line_profiler.profile
def q3_time(client: bigquery.Client, query: str) -> List[Tuple[str, int]]:
    """
    Executes a BigQuery query, profiles its execution time line-by-line,
    and returns extracted date-string pairs.

    Args:
        client: BigQuery client object.
        query: BigQuery SQL query string.

    Returns:
        List of tuples containing date-string pairs extracted from BigQuery results.
    """

    # Delegate query execution and data extraction to the external function:
    # - Assumes 'process_bigquery_results' handles query execution, result processing,
    #   and extraction of date-string pairs.
    # - The decorator will profile the execution time of each line within this function,
    #   including the time spent within 'process_bigquery_results'.
    return process_bigquery_results(client, query)
