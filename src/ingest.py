# Import libraries for working with Google Cloud Storage and file-like objects
import io # For working with inputs and outputs (downloaded file content)
from google.cloud import storage  # For working with Google Cloud Storage

def upload_drive_file_to_cloud_storage(
    bucket: storage.Bucket, 
    folder_name: str, 
    downloaded: io.BytesIO, 
    zip_file_name: str
) -> storage.Blob:
    """Uploads a file to Google Cloud Storage.

    This function uploads a file provided as a BytesIO object to a specified folder
    within a Google Cloud Storage bucket with a conditional check.

    Args:
        bucket (storage.Bucket): The Google Cloud Storage bucket where the file will be uploaded.
        folder_name (str): The name of the folder within the bucket to upload the file to.
        downloaded (io.BytesIO): The BytesIO object containing the file data to upload.
        zip_file_name (str): The name of the file to be uploaded.

    Returns:
        storage.Blob: The uploaded blob object representing the uploaded file in Cloud Storage.

    Assumptions:
        - The user has authenticated with Google Cloud and has permission to access and write to the specified bucket.
        - The `downloaded` object is a valid BytesIO object containing the file data.

    Suggestions for Improvement:
        - Error Handling: Implement checks for potential errors during upload (e.g., network errors, permission issues). Use `try-except` blocks with informative error messages.
        - Progress Reporting: For large files, consider adding progress reporting mechanisms using third-party libraries or manual tracking.
        - Variable Naming: Use more descriptive variable names (e.g., `uploaded_file` instead of `downloaded`).
        - Type Annotations: Consider adding type annotations for clarity and potential type checking.
        - Folder Creation: Explore alternative methods like `Blob.make_dirs()`.
        - Logging: Use a logging library for structured logging instead of `print` statements.
    """

    # Create a blob object referencing the folder path within the bucket
    folder_blob: storage.Blob = bucket.blob(f"{folder_name}/")

    # Check if the folder exists. If not, create an empty file object to serve as a placeholder.
    if not folder_blob.exists():
        try:
            folder_blob.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')
            print(f"Folder '{folder_name}' created in bucket gs://{bucket.name}")  # Informational message
        except Exception as e:  # Catch potential errors during folder creation
            print(f"Error creating folder: {e}")
            raise  # Re-raise the exception for further handling

    # Create a blob object referencing the specific file to be uploaded within the folder
    blob: storage.Blob = bucket.blob(f'{folder_name}/{zip_file_name}')

    # Download as string and get the size if the ZIP blob exists in the bucket
    if blob.exists():
        existing_blob_data: str = blob.download_as_string()
        existing_blob_size: int = len(existing_blob_data)

    # Check if a blob with the same name and size already exists
    if blob.exists() and existing_blob_size == len(downloaded.getvalue()):
        print(f"File '{zip_file_name}' already exists on cloud storage with exact matching size, skipping upload.")
    else:
        # Upload the file if conditions aren't met
        try:
            blob.upload_from_string(downloaded.getvalue(), content_type='application/zip')
            print(f'File uploaded to gs://{bucket.name}/{blob.name}')
        except Exception as e:  # Catch potential errors during upload
            print(f"Error uploading file: {e}")
            raise  # Re-raise the exception for further handling

    # Return the uploaded blob object
    return blob
