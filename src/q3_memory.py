from typing import List, Tuple  # For type annotations
from google.cloud import bigquery  # For interacting with BigQuery
from processing import process_bigquery_results  # External function for processing results
import memory_profiler  # Module for memory profiling # type: ignore

@memory_profiler.profile  # Decorator to profile memory usage
def q3_memory(client: bigquery.Client, query: str) -> List[Tuple[str, int]]:
   """
   Executes a BigQuery query, profiles its memory usage, extracts string-integer pairs,
   and considers memory-efficient return strategies for large datasets.

   Args:
       client: BigQuery client object.
       query: BigQuery SQL query string.

   Returns:
       List of tuples containing string-integer pairs extracted from BigQuery results.
       Might suggest alternative return strategies (streaming or pagination) for large results.
   """

   try:
       # Delegate query execution and data extraction to the external function:
       results = process_bigquery_results(client, query)

       # Extract string-integer pairs, validating data format:
       formatted_results = [(row[0], int(row[1])) for row in results]

       # Consider memory-efficient return strategies based on result size:
       if len(formatted_results) > 1000:  # Adjust threshold as needed
           print("Warning: Returning a large dataset. Consider using streaming or pagination for memory optimization.")
           # Potentially explore implementation of streaming or pagination techniques here

       return formatted_results

   except ValueError as e:
       print(f"Error converting data to string and integer pairs: {e}")
       return []  # Return an empty list to signal the error
