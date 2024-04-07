import typing  # Import for type hints
from google.api_core.exceptions import BadRequest, NotFound  # Specific exceptions for BigQuery API # type: ignore
from google.cloud import bigquery  # Client for interacting with BigQuery

def process_bigquery_results(
    client: bigquery.Client, query: str
) -> typing.List[typing.Tuple[str, str]]:
    """Executes a BigQuery query, handles results, and extracts date and username pairs.

    Args:
        client: The BigQuery client object.
        query: The BigQuery SQL query string to execute.

    Returns:
        A list of tuples containing the extracted date and username pairs.

    Raises:
        NotFound: If the query returns no results.
        Exception: For other unexpected errors during query execution or processing.
    """

    extracted_data: typing.List[typing.Tuple[str, str]] = []  # Initialize empty list

    try:
        query_job: bigquery.QueryJob = client.query(query)  # Submit the query
        results = query_job.result()  # Await query completion and fetch results

        if not results:
            raise NotFound("No results found for the query.")  # Raise specific exception

        # Extract date and username from each row
        extracted_data = [(row[0], row[1]) for row in results]

    except BadRequest as e:
        print(f"BigQuery error: {e}")  # Print error message for debugging
        raise  # Re-raise for further handling
    except NotFound as e:
        print(f"Query returned no results: {e}")  # Log message for clarity
        raise  # Propagate the exception for appropriate action
    except Exception as e:
        print(f"Error: {e}")  # Catch general errors for logging
        raise  # Re-raise for troubleshooting

    finally:
        return extracted_data  # Always return the extracted data, even with exceptions
