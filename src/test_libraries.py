import unittest
from unittest.mock import patch, mock_open
import subprocess
import sys
from importlib.machinery import ModuleSpec

from libraries import check_requirements, install_requirements

class TestCheckRequirements(unittest.TestCase):

    @patch('builtins.open', mock_open(read_data="numpy\npandas\nmatplotlib\n"))
    @patch('importlib.util.find_spec')
    def test_check_requirements_all_installed(self, mock_find_spec):
        # Arrange
        mock_find_spec.return_value = ModuleSpec('numpy', None)

        # Act
        result = check_requirements("requirements.txt")

        # Assert
        self.assertTrue(result)

    # Add more test cases for different scenarios

class TestInstallRequirements(unittest.TestCase):

    @patch('subprocess.run')
    @patch('libraries.check_requirements')
    def test_install_requirements_not_installed(self, mock_check_requirements, mock_subprocess_run):
        # Arrange
        mock_check_requirements.return_value = False

        # Act
        install_requirements("requirements.txt")

        # Assert
        mock_subprocess_run.assert_called_once_with([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

    # Add more test cases for different scenarios

if __name__ == '__main__':
    unittest.main()
