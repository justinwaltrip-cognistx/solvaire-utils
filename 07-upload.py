# # just upload the first three files from ./crown_royal_processing_converted to "sqr-bucket-194-prod" bucket at "unzipped/sync_test/CrownRoyalFiberCusts01"
# # - crown_royal_processing_converted/BCCZ0000000370_(Counter-signed) Colo_Supp_O066855.pdf
# # - crown_royal_processing_converted/BCCZ0000000372_10 20171012-ConsentToAssignment.pdf
# # - crown_royal_processing_converted/BCCZ0000000373_11 20171012-LightowerOGSFullDocRenewal.pdf
# aws s3 cp './crown_royal_processing_converted/BCCZ0000000370_(Counter-signed) Colo_Supp_O066855.pdf' 's3://sqr-bucket-194-prod/unzipped/sync_test/CrownRoyalFiberCusts01/BCCZ0000000370_(Counter-signed) Colo_Supp_O066855/BCCZ0000000370_(Counter-signed) Colo_Supp_O066855.pdf'
# aws s3 cp './crown_royal_processing_converted/BCCZ0000000372_10 20171012-ConsentToAssignment.pdf' 's3://sqr-bucket-194-prod/unzipped/sync_test/CrownRoyalFiberCusts01/BCCZ0000000372_10 20171012-ConsentToAssignment/BCCZ0000000372_10 20171012-ConsentToAssignment.pdf'
# aws s3 cp './crown_royal_processing_converted/BCCZ0000000373_11 20171012-LightowerOGSFullDocRenewal.pdf' 's3://sqr-bucket-194-prod/unzipped/sync_test/CrownRoyalFiberCusts01/BCCZ0000000373_11 20171012-LightowerOGSFullDocRenewal/CrownRoyalFiberCusts01/BCCZ0000000373_11 20171012-LightowerOGSFullDocRenewal.pdf'

# upload ./crown_royal_processing_converted to "sqr-bucket-194-prod" bucket at "unzipped/sync"
# - each <file> should be uploaded to "sqr-bucket-194-prod" bucket at "unzipped/sync/CrownRoyalFiberCusts01/<file>/<file>.<ext>"
import os
import boto3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def upload_file(file_path, bucket_name, base_prefix):
    """Upload a single file to S3"""
    try:
        s3_client = boto3.client("s3")
        file_name = os.path.basename(file_path)
        name_without_ext = os.path.splitext(file_name)[0]
        ext = os.path.splitext(file_name)[1]

        # Construct the S3 key
        s3_key = f"{base_prefix}/CrownRoyalFiberCusts01/{name_without_ext}/{file_name}"

        print(f"Uploading {file_path} to s3://{bucket_name}/{s3_key}")
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"Successfully uploaded {file_name}")
        return True
    except Exception as e:
        print(f"Error uploading {file_name}: {str(e)}")
        return False


def main():
    # Configuration
    source_dir = "./crown_royal_processing_converted"
    bucket_name = "sqr-bucket-194-prod"
    base_prefix = "unzipped/sync"
    max_workers = 5  # Adjust based on your needs

    # Create list of files to upload
    files_to_upload = []
    for file in os.listdir(source_dir):
        if os.path.isfile(os.path.join(source_dir, file)):
            files_to_upload.append(os.path.join(source_dir, file))

    # Upload files in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(upload_file, file_path, bucket_name, base_prefix)
            for file_path in files_to_upload
        ]

        # Wait for all uploads to complete
        results = [future.result() for future in futures]

    # Print summary
    successful = sum(results)
    failed = len(results) - successful
    print(f"\nUpload Summary:")
    print(f"Successfully uploaded: {successful}")
    print(f"Failed uploads: {failed}")


if __name__ == "__main__":
    main()
