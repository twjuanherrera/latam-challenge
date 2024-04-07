import unittest
from unittest.mock import MagicMock, patch
from google.cloud import bigquery

from q2_memory import q2_memory

class TestQ2Memory(unittest.TestCase):

    @patch('processing.process_bigquery_results')
    @patch('memory_profiler.profile')
    def test_q2_memory(self, mock_profile, mock_process_bigquery_results):
        # Arrange
        client = MagicMock(spec=bigquery.Client)
        query = "SELECT * FROM table"

        mock_process_bigquery_results.return_value = [('string1', '10'), ('string2', '20')]

        # Act
        result = q2_memory(client, query)

        # Assert
        self.assertEqual(result, [('string1', 10), ('string2', 20)])

    # Add more test cases for different scenarios

if __name__ == '__main__':
    unittest.main()
