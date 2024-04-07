import unittest
from unittest.mock import MagicMock, patch
from google.cloud import bigquery

from q2_time import q2_time

class TestQ2Time(unittest.TestCase):

    @patch('processing.process_bigquery_results')
    @patch('line_profiler.profile')
    def test_q2_time(self, mock_profile, mock_process_bigquery_results):
        # Arrange
        client = MagicMock(spec=bigquery.Client)
        query = "SELECT * FROM table"

        mock_process_bigquery_results.return_value = [('string1', '10'), ('string2', '20')]

        # Act
        result = q2_time(client, query)

        # Assert
        self.assertEqual(result, [('string1', 10), ('string2', 20)])

    # Add more test cases for different scenarios

if __name__ == '__main__':
    unittest.main()
