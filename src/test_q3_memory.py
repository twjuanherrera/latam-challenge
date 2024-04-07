import unittest
from unittest.mock import MagicMock, patch
from google.cloud import bigquery

from q3_memory import q3_memory

class TestQ3Memory(unittest.TestCase):

    @patch('processing.process_bigquery_results')
    @patch('memory_profiler.profile')
    def test_q3_memory(self, mock_profile, mock_process_bigquery_results):
        # Arrange
        client = MagicMock(spec=bigquery.Client)
        query = "SELECT * FROM table"

        mock_process_bigquery_results.return_value = [('string1', '10'), ('string2', '20')]

        # Act
        result = q3_memory(client, query)

        # Assert
        self.assertEqual(result, [('string1', 10), ('string2', 20)])

    # Add more test cases for different scenarios

if __name__ == '__main__':
    unittest.main()
