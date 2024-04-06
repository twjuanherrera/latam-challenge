from typing import List, Tuple
import datetime
import processing
from google.cloud import bigquery

def q1_time(
    client: bigquery.Client,
    query: str
) -> List[Tuple[datetime.date, str]]:
    return process_bigquery_results(client, query)