import logging
from google.colab import drive

def mount_google_drive(
    mount_point: str = '/content/drive'
) -> None:
  """Mounts Google Drive to the specified mount point.

  Args:
      mount_point (str, optional): The path to mount Google Drive. Defaults to '/content/drive'.

  Raises:
      RuntimeError: If there's an error mounting the drive.
  """
  logging.info(f"Attempting to mount Google Drive to {mount_point}")
  try:
    drive.mount(mount_point, force_remount=True)
    logging.info(f"Successfully mounted Google Drive to {mount_point}")
  except Exception as e:
    logging.error(f"Error mounting Google Drive: {e}")
    raise RuntimeError(f"Error mounting Google Drive: {e}")