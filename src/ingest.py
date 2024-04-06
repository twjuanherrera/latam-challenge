#TODO: authenticate_google_drive, download_file_from_drive must be on gdrive feature
#TODO: decompress_zip_file must be in common feature

from google.colab import auth
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload
from google.cloud import storage
import zipfile
from typing import Any

def authenticate_google_drive() -> None:
    """Authenticates to Google Drive using the user's credentials.

    Args:
        None
    """
    try:
        auth.authenticate_user()
    except Exception as e:
        logging.error(f"Error authenticating to Google Drive: {e}")
        raise


def download_file_from_drive(
    drive_service: Any, file_id: str
) -> io.BytesIO:
    """Downloads a file from Google Drive.

    Args:
        drive_service (Any): The Google Drive service resource (in the build function returns Any).
        file_id (str): The ID of the file to download.

    Returns:
        io.BytesIO: The downloaded file content as a BytesIO object.
    """
    downloaded: io.BytesIO = io.BytesIO()
    try:
        request = drive_service.files().get_media(fileId=file_id)
        downloader = MediaIoBaseDownload(downloaded, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f'Downloading {int(status.progress() * 100)}%')
        downloaded.seek(0)
        return downloaded
    except Exception as e:
        print(f"Error downloading file: {e}")
        raise


def upload_file_to_cloud_storage(
    bucket: storage.Bucket, folder_name: str, downloaded: io.BytesIO, zip_file_name: str
) -> storage.Blob:
    """Uploads a file to Google Cloud Storage.

    Args:
        bucket (Bucket): Google Cloud Storage bucket.
        folder_name (str): The name of the folder within the bucket where the file will be uploaded.
        downloaded (io.BytesIO): The downloaded file to upload.
        zip_file_name (str): The name of the file to be uploaded.

    Returns:
        google.cloud.storage.Blob: The uploaded blob object.
    """
    folder_blob: storage.Blob = bucket.blob(f"{folder_name}/")

    # Check and create folder if it doesn't exist
    if not folder_blob.exists():
        folder_blob.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')

    # Upload the file to the specified folder
    blob: storage.Blob = bucket.blob(f'{folder_name}/{zip_file_name}')
    blob.upload_from_file(downloaded, content_type='application/zip')

    print(f'File uploaded to gs://{bucket.name}/{blob.name}')
    return blob


def decompress_zip_file(
    bucket: storage.Bucket, folder_name: str, zip_file_name: str
) -> str:
    """Decompresses a ZIP file stored in Google Cloud Storage.

    Args:
        bucket (Bucket): Google Cloud Storage bucket where the ZIP file is stored.
        folder_name (str): The name of the folder within the bucket where the ZIP file is located.
        zip_file_name (str): The name of the ZIP file

    Returns:
        str: The unzipped file name.
    """

    json_file_name: str = ''
    blob_name: str = ''

    try:
        zip_blob: storage.Blob = bucket.blob(f'{folder_name}/{zip_file_name}')
        with zipfile.ZipFile(io.BytesIO(zip_blob.download_as_string()), 'r') as z:
            for file_info in z.infolist():
                with z.open(file_info) as file:
                    blob_name: str = f'{folder_name}/{file_info.filename}'
                    json_file_name: str = file_info.filename
                    json_blob: storage.Blob = bucket.blob(blob_name)
                    json_blob.upload_from_file(file)
        print(f'File decompressed in gs://{bucket.name}/{blob_name}')
    except zipfile.BadZipFile:
        logging.warning(f'The file in gs://{bucket.name}/{folder_name}/{zip_file_name} is not a valid ZIP file.')
    except Exception as e:
        logging.error(f'Error decompressing file: {e}')
    finally:
        return json_file_name