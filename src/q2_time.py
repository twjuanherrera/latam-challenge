from typing import List, Tuple
import datetime
from google.cloud import bigquery
from processing import process_bigquery_results
import line_profiler

@line_profiler.profile
def q2_time(
    client: bigquery.Client,
    query: str
) -> List[Tuple[str, int]]:
    """
    Executes a BigQuery SQL query and returns a list of tuples containing dates and strings extracted from the results.

    Args:
        client (bigquery.Client): A BigQuery client object.
        query (str): The BigQuery SQL query to be executed.

    Returns:
        List[Tuple[datetime.date, str]]: A list of tuples where each tuple contains a datetime.date object and a string.
    """

    return process_bigquery_results(client, query)
