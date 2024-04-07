import unittest
from unittest.mock import MagicMock, patch
from google.cloud import bigquery
import datetime

from q1_memory import q1_memory

class TestQ1Memory(unittest.TestCase):

    @patch('processing.process_bigquery_results')
    @patch('memory_profiler.profile')
    def test_q1_memory(self, mock_profile, mock_process_bigquery_results):
        # Arrange
        client = MagicMock(spec=bigquery.Client)
        query = "SELECT * FROM table"

        mock_process_bigquery_results.return_value = [(datetime.date(2023, 1, 1), 'username1'), (datetime.date(2023, 1, 2), 'username2')]

        # Act
        result = q1_memory(client, query)

        # Assert
        self.assertEqual(result, [(datetime.date(2023, 1, 1), 'username1'), (datetime.date(2023, 1, 2), 'username2')])

    # Add more test cases for different scenarios

if __name__ == '__main__':
    unittest.main()
