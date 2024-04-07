import unittest
from unittest.mock import MagicMock, patch
from google.cloud import bigquery
import datetime

from q1_time import q1_time

class TestQ1Time(unittest.TestCase):

    @patch('processing.process_bigquery_results')
    @patch('line_profiler.profile')
    def test_q1_time(self, mock_profile, mock_process_bigquery_results):
        # Arrange
        client = MagicMock(spec=bigquery.Client)
        query = "SELECT * FROM table"

        mock_process_bigquery_results.return_value = [(datetime.date(2023, 1, 1), 'username1'), (datetime.date(2023, 1, 2), 'username2')]

        # Act
        result = q1_time(client, query)

        # Assert
        self.assertEqual(result, [(datetime.date(2023, 1, 1), 'username1'), (datetime.date(2023, 1, 2), 'username2')])

    # Add more test cases for different scenarios

if __name__ == '__main__':
    unittest.main()
