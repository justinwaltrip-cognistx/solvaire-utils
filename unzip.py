import boto3
import zipfile
import io
import os
from botocore.exceptions import ClientError
from tqdm import tqdm


def get_file_size(s3_client, bucket, key):
    """Get file size from S3"""
    response = s3_client.head_object(Bucket=bucket, Key=key)
    return response["ContentLength"]


def download_with_progress(s3_client, bucket, key, file_obj):
    """Download from S3 with progress bar"""
    file_size = get_file_size(s3_client, bucket, key)
    with tqdm(total=file_size, unit="B", unit_scale=True, desc="Downloading") as pbar:
        s3_client.download_fileobj(
            bucket,
            key,
            file_obj,
            Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
        )


def upload_with_progress(s3_client, bucket, key, file_content):
    """Upload to S3 with progress bar"""
    content_size = len(file_content)
    with tqdm(
        total=content_size, unit="B", unit_scale=True, desc=f"Uploading {key}"
    ) as pbar:
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=file_content,
            Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
        )


def process_s3_zip(bucket_name, zip_key, chunk_size=8192):
    """
    Stream and process zip from S3 with progress indicators
    """
    s3_client = boto3.client("s3")
    try:
        # Create a streaming buffer
        zip_buffer = io.BytesIO()

        # Download zip file with progress bar
        download_with_progress(s3_client, bucket_name, zip_key, zip_buffer)

        # Reset buffer position
        zip_buffer.seek(0)

        # Open zip file from buffer
        with zipfile.ZipFile(zip_buffer) as zip_ref:
            # List all files in zip
            file_list = zip_ref.namelist()
            print(f"Found {len(file_list)} files in zip")

            # Process each file in zip
            for file_name in file_list:
                print(f"\nProcessing {file_name}")

                # Stream the file content
                with zip_ref.open(file_name) as file:
                    # Read file in chunks to avoid memory issues
                    content = io.BytesIO()
                    while True:
                        chunk = file.read(chunk_size)
                        if not chunk:
                            break
                        content.write(chunk)

                    content.seek(0)
                    file_content = content.read()

                # Upload path will be same as zip path but without .zip extension
                upload_key = os.path.join(os.path.dirname(zip_key), file_name)

                # Upload file with progress bar
                upload_with_progress(s3_client, bucket_name, upload_key, file_content)

                print(f"Successfully uploaded {file_name}")

    except ClientError as e:
        print(f"AWS Error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    # Parse S3 path
    s3_path = "s3://crown-royal/CrownRoyalFiberCusts01.zip"
    bucket = s3_path.split("/")[2]
    key = "/".join(s3_path.split("/")[3:])

    # Process the zip file
    process_s3_zip(bucket, key)
