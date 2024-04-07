import logging  # Library for logging events
from typing import Any  # Library for type annotations
from google.cloud import bigquery  # Library for interacting with BigQuery
from google.api_core.exceptions import NotFound  # For handling potential resource not found errors (not actively used here)

# Function for authenticating with BigQuery
def authenticate_bigquery(project_id: str) -> bigquery.Client:
    """
    Authenticates to BigQuery and returns the client object.

    Args:
        project_id (str): Your GCP project ID.

    Returns:
        bigquery.Client: The BigQuery client object for subsequent interactions.
    """

    # Create a BigQuery client using the provided project ID
    try:
        client: bigquery.Client = bigquery.Client(project_id)
    except Exception as e:  # Handle potential authentication errors
        logging.error(f"Authentication to BigQuery failed: {e}")
        raise  # Re-raise the exception to propagate it for appropriate handling

    # Log a message indicating successful authentication
    logging.info(f"Authenticated to BigQuery using project ID '{project_id}'.")

    return client  # Return the authenticated client for further operations

def create_dataset(
    client: bigquery.Client, dataset_name: str, mode: str = "create"
) -> None:
    """
    Creates a BigQuery dataset, handling existence checks and potential overwriting.

    Args:
        client (bigquery.Client): BigQuery client object.
        dataset_name (str): Name of the dataset to create.
        mode (Optional[str], optional): Action to take if the dataset already exists ('create' or 'overwrite'). Defaults to 'create'.

    Raises:
        Exception: For unexpected errors during dataset creation, existence check, or overwrite operation.
    """

    dataset_ref: bigquery.DatasetReference = client.dataset(dataset_name)
    try:
        # Check dataset existence
        client.get_dataset(dataset_ref)
        if mode == "overwrite":
            logging.info(f"Dataset '{dataset_name}' already exists, overwriting...")
            try:
                # Attempt to delete the existing dataset with contents
                client.delete_dataset(dataset_ref, delete_contents=True)
                logging.info(f"Dataset '{dataset_name}' deleted for overwrite.")
            except Exception as e:  # Handle potential delete errors during overwrite
                logging.error(f"Failed to delete existing dataset '{dataset_name}' for overwrite: {e}")
                raise  # Re-raise to propagate the error
            client.create_dataset(dataset_ref)
            logging.info(f"Dataset '{dataset_name}' overwritten.")
        else:
            logging.info(f"Dataset '{dataset_name}' already exists (skipping creation).")
    except NotFound:
        logging.info(f"Dataset '{dataset_name}' not found, creating...")
        client.create_dataset(dataset_ref)
        logging.info(f"Dataset '{dataset_name}' created.")
    except Exception as e:
        logging.error(f"Error creating dataset '{dataset_name}': {e}")
        raise

def create_table(
    client: bigquery.Client,
    dataset_name: str,
    table_name: str,
    mode: str = "create",  # Default mode is "create"
) -> None:
    """
    Creates a BigQuery table, handling existence checks and potential overwriting.
    Infers table schema from data upon creation.

    Args:
        client (bigquery.Client): BigQuery client object.
        dataset_name (str): Name of the dataset containing the table.
        table_name (str): Name of the table to create.
        mode (str, optional): Action to take if the table exists ('create' or 'overwrite'). Defaults to 'create'.

    Raises:
        Exception: For unexpected errors during table creation, existence check, or overwrite operation.
    """

    # Create references to the dataset and table
    dataset_ref = client.dataset(dataset_name)
    table_ref = dataset_ref.table(table_name)

    try:
        # Check if the table already exists
        client.get_table(table_ref)
        logging.info(f"Table '{table_name}' already exists.")

        if mode == "overwrite":
            # Overwrite the existing table:
            logging.info(f"Overwriting table '{table_name}'...")
            client.delete_table(table_ref)  # Delete the existing table

            # Create a new empty table with the same name (schema inferred by BigQuery upon data insertion)
            table = bigquery.Table(table_ref)
            client.create_table(table)
            logging.info(f"Table '{table_name}' overwritten.")
    except NotFound:
        # Table doesn't exist, create it:
        logging.info(f"Table '{table_name}' not found, creating...")
        table = bigquery.Table(table_ref)
        client.create_table(table)
        logging.info(f"Table '{table_name}' created.")
    except Exception as e:
        # Log any unexpected errors and re-raise the exception
        logging.error(f"Error creating table '{table_name}': {e}")
        raise

def load_data_from_storage(
    client: bigquery.Client,
    source_uri: str,
    dataset_name: str,
    table_name: str,
    json_file_name: str
) -> None:
    """
    Loads newline-delimited JSON data from Cloud Storage to a BigQuery table.
    Infers table schema from data and ignores unknown values.

    Args:
        client (bigquery.Client): BigQuery client object.
        source_uri (str): URI of the data file in Cloud Storage (excluding the filename).
        dataset_name (str): Name of the dataset containing the table.
        table_name (str): Name of the table to load data into.
        json_file_name (str): Name of the JSON file in the bucket.

    Raises:
        Exception: For unexpected errors during data loading.
    """

    job_config = bigquery.LoadJobConfig()

    # Set job configuration properties (type hints for these properties are not supported):
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON  # Specify data format
    job_config.autodetect = True  # Auto-detect schema from data
    job_config.ignore_unknown_values = True  # Ignore unknown values during loading

    # Construct the full URI for the JSON file:
    full_source_uri = source_uri + json_file_name

    # Initiate the load job:
    load_job = client.load_table_from_uri(
        full_source_uri,  # Load from the full URI
        client.dataset(dataset_name).table(table_name),  # Destination table
        job_config=job_config  # Apply the specified job configuration
    )

    try:
        load_job.result()  # Wait for the load job to complete
        logging.info(f"Data loaded from '{full_source_uri}' to table '{dataset_name}.{table_name}'.")
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise
