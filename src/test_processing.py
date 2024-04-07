import unittest
from unittest.mock import MagicMock, patch
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

from processing import process_bigquery_results

class TestProcessBigQueryResults(unittest.TestCase):

    @patch('google.cloud.bigquery.Client.query')
    def test_process_bigquery_results_found_results(self, mock_query):
        # Arrange
        client = MagicMock(spec=bigquery.Client)
        query = "SELECT * FROM table"

        mock_results = MagicMock()
        mock_results.__iter__.return_value = [('2023-01-01', 'username1'), ('2023-01-02', 'username2')]
        mock_query.return_value.result.return_value = mock_results

        # Act
        result = process_bigquery_results(client, query)

        # Assert
        self.assertEqual(result, [('2023-01-01', 'username1'), ('2023-01-02', 'username2')])

    # Add more test cases for different scenarios

if __name__ == '__main__':
    unittest.main()
