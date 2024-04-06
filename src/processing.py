from google.api_core.exceptions import BadRequest, NotFound  # Specific exceptions
from google.cloud import bigquery
from typing import List, Tuple,  Any

def process_bigquery_results(
    client: bigquery.Client, query: str
) -> List[Tuple[Any, Any]]:
    """
    Executes a BigQuery query, handles results, and performs data conversion.

    Args:
        client: BigQuery client object.
        query: BigQuery SQL query string.

    Returns:
        A list of tuples containing the extracted data (date and username).

    Raises:
        NotFound: If the query returns no results.
        Exception: For other unexpected errors during query execution or processing.
    """

    extracted_data: List[Tuple[str, str]] = []

    try:
        query_job: bigquery.QueryJob = client.query(query)
        results = query_job.result() # Type notation not possible for this

        if not results:
            raise NotFound("No results found for the query.")

        extracted_data = [(row[0], row[1]) for row in results]

    except BadRequest as e:
        print(f"BigQuery error: {e}")
        raise
    except NotFound as e:
        print(f"Query returned no results: {e}")
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        return extracted_data
