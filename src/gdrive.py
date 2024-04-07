import logging  # For logging messages
from google.colab import drive, auth  # For accessing Google Drive and authentication # type: ignore
from googleapiclient.discovery import build  # For building Google API service objects # type: ignore
import io  # For working with bytes streams
from googleapiclient.http import MediaIoBaseDownload  # For downloading media files from Google APIs # type: ignore
from typing import Any  # For type hints

def authenticate_google_drive() -> None:
    """Authenticates the user with Google Drive using their Colab credentials.

    This function attempts to authenticate the user with Google Drive. If
    successful, it allows access to the user's Drive for operations like
    mounting or downloading files.

    Args:
        None

    Returns:
        None

    Raises:
        Exception: If there's an error during authentication.

    Assumptions:
        - The user has a Google account associated with their Colab environment.
        - The user has the necessary permissions to access their Google Drive.
    """

    try:
        auth.authenticate_user()
    except Exception as e:
        logging.error(f"Error authenticating to Google Drive: {e}")
        raise

def mount_google_drive(
    mount_point: str = '/content/drive'
) -> None:
  """Mounts Google Drive to the specified mount point.

  This function mounts the user's Google Drive to the specified directory
  within the Colab environment. This allows users to interact with their
  Drive files directly through the file system.

  Args:
      mount_point (str, optional): The path to mount Google Drive. Defaults to '/content/drive'.

  Raises:
      RuntimeError: If there's an error mounting the drive.

  Assumptions:
      - The user has already authenticated with Google Drive (using `authenticate_google_drive`).
      - The user has the necessary permissions to mount their Drive.
  """
  logging.info(f"Attempting to mount Google Drive to {mount_point}")
  try:
    drive.mount(mount_point, force_remount=True)
    logging.info(f"Successfully mounted Google Drive to {mount_point}")
  except Exception as e:
    logging.error(f"Error mounting Google Drive: {e}")
    raise RuntimeError(f"Error mounting Google Drive: {e}")

def download_file_from_drive(
    drive_service: Any, file_id: str
) -> io.BytesIO:
    """Downloads a file from Google Drive.

  This function downloads a specific file from the user's Google Drive
  given its ID. The downloaded content is returned as a BytesIO object.

  Args:
      drive_service (Any): The Google Drive service resource obtained using the `build` function.
      file_id (str): The ID of the file to download.

  Returns:
      io.BytesIO: The downloaded file content as a BytesIO object.

  Raises:
      Exception: If there's an error downloading the file.

  Assumptions:
      - The user has already authenticated with Google Drive (using `authenticate_google_drive`).
      - The provided `drive_service` object is a valid Google Drive service resource.
      - The user has permission to access the file specified by `file_id`.
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
