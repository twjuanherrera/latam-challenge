import unittest
from unittest.mock import MagicMock, patch
from google.cloud import storage
from io import BytesIO

from ingest import upload_drive_file_to_cloud_storage

class TestUploadDriveFileToCloudStorage(unittest.TestCase):

    @patch('google.cloud.storage.Blob')
    def test_upload_drive_file_to_cloud_storage_file_already_exists(self, mock_blob):
        # Arrange
        bucket = MagicMock(spec=storage.Bucket)
        bucket.blob.return_value.exists.return_value = True
        bucket.blob.return_value.download_as_string.return_value = b'{}'

        downloaded = BytesIO(b'{}')
        zip_file_name = 'test.zip'
        folder_name = 'test_folder'

        with patch('builtins.print') as mock_print:
            # Act
            result = upload_drive_file_to_cloud_storage(bucket, folder_name, downloaded, zip_file_name)

            # Assert
            mock_print.assert_called_once_with(f"File '{zip_file_name}' already exists on cloud storage with exact matching size, skipping upload.")
            self.assertEqual(result, bucket.blob.return_value)

    # Add more test cases for different scenarios

if __name__ == '__main__':
    unittest.main()
