import unittest
from unittest.mock import MagicMock
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import logging
import storage

class TestStorageFunctions(unittest.TestCase):
    def test_authenticate_bigquery_success(self):
        client_mock = MagicMock()
        bigquery_mock = MagicMock(return_value=client_mock)

        with unittest.mock.patch('storage.bigquery.Client', bigquery_mock):
            client = storage.authenticate_bigquery("project_id")

        self.assertEqual(client, client_mock)

    def test_authenticate_bigquery_failure(self):
        bigquery_mock = MagicMock(side_effect=Exception("Authentication failed"))

        with unittest.mock.patch('storage.bigquery.Client', bigquery_mock):
            with self.assertRaises(Exception):
                storage.authenticate_bigquery("project_id")

    def test_create_dataset_exists_skip(self):
        client_mock = MagicMock()
        client_mock.get_dataset.side_effect = NotFound()

        with unittest.mock.patch('storage.client', client_mock):
            storage.create_dataset(client_mock, "dataset_name", "create")

        client_mock.get_dataset.assert_called_once()

    def test_create_dataset_exists_overwrite(self):
        client_mock = MagicMock()
        client_mock.get_dataset.return_value = "dummy_dataset"
        client_mock.delete_dataset = MagicMock()
        client_mock.create_dataset = MagicMock()

        with unittest.mock.patch('storage.client', client_mock):
            storage.create_dataset(client_mock, "dataset_name", "overwrite")

        client_mock.get_dataset.assert_called_once()
        client_mock.delete_dataset.assert_called_once_with("dummy_dataset", delete_contents=True)
        client_mock.create_dataset.assert_called_once()

    def test_create_table_exists_skip(self):
        client_mock = MagicMock()
        client_mock.get_table.side_effect = NotFound()

        with unittest.mock.patch('storage.client', client_mock):
            storage.create_table(client_mock, "dataset_name", "table_name", "create")

        client_mock.get_table.assert_called_once()

    def test_create_table_exists_overwrite(self):
        client_mock = MagicMock()
        client_mock.get_table.return_value = "dummy_table"
        client_mock.delete_table = MagicMock()
        client_mock.create_table = MagicMock()

        with unittest.mock.patch('storage.client', client_mock):
            storage.create_table(client_mock, "dataset_name", "table_name", "overwrite")

        client_mock.get_table.assert_called_once()
        client_mock.delete_table.assert_called_once_with("dummy_table")
        client_mock.create_table.assert_called_once()

    def test_load_data_from_storage(self):
        client_mock = MagicMock()
        client_mock.dataset.return_value.table.return_value = "table_ref"
        client_mock.load_table_from_uri.return_value.result.side_effect = None

        with unittest.mock.patch('storage.client', client_mock):
            storage.load_data_from_storage(client_mock, "source_uri", "dataset_name", "table_name", "json_file_name")

        client_mock.load_table_from_uri.assert_called_once_with(
            "source_urijson_file_name",
            "table_ref",
            job_config=unittest.mock.ANY
        )
        client_mock.load_table_from_uri.return_value.result.assert_called_once()

if __name__ == '__main__':
    unittest.main()
