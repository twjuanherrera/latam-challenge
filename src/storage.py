import logging
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

def authenticate_bigquery(
    project_id: str
) -> bigquery.Client:
    """Authenticates to BigQuery and returns the client object.

    Args:
        project_id (str): Your GCP project ID.

    Returns:
        bigquery.Client: BigQuery client object.
    """

    return bigquery.Client(project_id)


def create_dataset(
    client: bigquery.Client, dataset_name: str, mode: str = 'create'
) -> None:
    """
    Creates a BigQuery dataset if it doesn't exist.

    Args:
        client (bigquery.Client): BigQuery client object.
        dataset_name (str): Name of the dataset to create.
        mode (Optional[str], optional): Action to take if the dataset already exists ('create' or 'overwrite'). Defaults to 'create'.

    Raises:
        Exception: For unexpected errors during dataset creation or existence check.
    """

    dataset_ref: bigquery.DatasetReference = client.dataset(dataset_name)
    try:
        client.get_dataset(dataset_ref)
        if mode == 'overwrite':
            logging.info(f"Dataset '{dataset_name}' already exists, overwriting...")
            client.delete_dataset(dataset_ref, delete_contents=True)
            client.create_dataset(dataset_ref)
            logging.info(f"Dataset '{dataset_name}' overwritten.")
        else:
            logging.info(f"Dataset '{dataset_name}' already exists.")
    except NotFound:
        logging.info(f"Dataset '{dataset_name}' not found, creating...")
        client.create_dataset(dataset_ref)
        logging.info(f"Dataset '{dataset_name}' created.")
    except Exception as e:
        logging.error(f"Error creating dataset '{dataset_name}': {e}")
        raise


def create_table(
    client: bigquery.Client, dataset_name: str, table_name: str, mode: str = 'create'
) -> None:
    """
    Creates a BigQuery table if it doesn't exist.

    Args:
        client (bigquery.Client): BigQuery client object.
        dataset_name (str): Name of the dataset containing the table.
        table_name (str): Name of the table to create.
        mode (Optional[str], optional): Action to take if the table already exists ('create' or 'overwrite'). Defaults to 'create'.

    Raises:
        Exception: For unexpected errors during table creation or existence check.
    """

    dataset_ref: bigquery.DatasetReference = client.dataset(dataset_name)
    table_ref: bigquery.TableReference = dataset_ref.table(table_name)
    try:
        client.get_table(table_ref)
        logging.info(f"Table '{table_name}' already exists.")
        if mode == 'overwrite':
            logging.info(f"Overwriting table '{table_name}'...")
            client.delete_table(table_ref)
            table: bigquery.Table = bigquery.Table(table_ref)
            client.create_table(table) # Empty schema for BigQuery to infer
            logging.info(f"Table '{table_name}' overwritten.")
    except NotFound:
        logging.info(f"Table '{table_name}' not found, creating...")
        table: bigquery.Table = bigquery.Table(table_ref)
        client.create_table(table) # Empty schema for BigQuery to infer
        logging.info(f"Table '{table_name}' created.")
    except Exception as e:
        logging.error(f"Error creating table '{table_name}': {e}")
        raise

def load_data_from_storage(
    client: bigquery.Client, source_uri: str, dataset_name: str, table_name: str, json_file_name: str
) -> None:
    """
    Loads data from Cloud Storage (newline-delimited JSON) to BigQuery table.

    Args:
        client (bigquery.Client): BigQuery client object.
        source_uri (str): URI of the data file in Cloud Storage.
        dataset_name (str): Name of the dataset containing the table.
        table_name (str): Name of the table to load data into.
        json_file_name (str): Name of the JSON file in the Bucket
    Raises:
        Exception: For unexpected errors during data loading.
    """

    job_config: bigquery.LoadJobConfig = bigquery.LoadJobConfig()

    # Only way to set job_config properties is without type notation
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.autodetect = True  # Auto-detect schema
    job_config.ignore_unknown_values = True  # Ignore unknown values

    load_job = client.load_table_from_uri(
        source_uri + json_file_name,
        client.dataset(dataset_name).table(table_name),
        job_config=job_config
    )
    try:
        load_job.result()  # Wait for load completion
        logging.info(f"Data loaded from '{source_uri}' to table '{dataset_name}.{table_name}'.")
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise