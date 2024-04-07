import unittest
from unittest.mock import patch
import time

from measure import measure_notebook_elapsed_time, print_notebook_elapsed_time

class TestMeasureNotebookElapsedTime(unittest.TestCase):

    @patch('time.time', side_effect=[0, 10])
    def test_measure_notebook_elapsed_time(self, mock_time):
        # Arrange
        start_time = 0

        # Act
        elapsed_time = measure_notebook_elapsed_time(start_time)

        # Assert
        self.assertEqual(elapsed_time, 10)

    # Add more test cases for different scenarios

class TestPrintNotebookElapsedTime(unittest.TestCase):

    @patch('builtins.print')
    def test_print_notebook_elapsed_time_seconds(self, mock_print):
        # Arrange
        elapsed_time = 30

        # Act
        print_notebook_elapsed_time(elapsed_time)

        # Assert
        mock_print.assert_called_once_with("Elapsed time in the notebook: 30.00 seconds")

    # Add more test cases for different scenarios

if __name__ == '__main__':
    unittest.main()
