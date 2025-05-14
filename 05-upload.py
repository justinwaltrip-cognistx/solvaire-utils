import os
import boto3
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from tqdm import tqdm

SMALL_CELL_CUSTS_PREFIX = "SmallCellCusts02_FlattenedPortfolios"


def upload_file(file_path, bucket_name, base_prefix):
    """Upload a single file to S3"""
    try:
        s3_client = boto3.client("s3")
        file_name = os.path.basename(file_path)
        name_without_ext = os.path.splitext(file_name)[0]
        s3_key = (
            f"{base_prefix}/{SMALL_CELL_CUSTS_PREFIX}/{name_without_ext}/{file_name}"
        )
        s3_client.upload_file(file_path, bucket_name, s3_key)
        return True
    except Exception as e:
        print(f"Error uploading {file_name}: {str(e)}")
        return False


def main(num_files=None):
    # Configuration
    source_dir = "./supported_files"
    bucket_name = "sqr-bucket-194-prod"
    base_prefix = "unzipped/sync"
    max_workers = 5

    # Create list of files to upload
    all_files = []
    for file in os.listdir(source_dir):
        if os.path.isfile(os.path.join(source_dir, file)):
            all_files.append(os.path.join(source_dir, file))

    # If num_files is specified and less than total files, randomly sample
    if num_files and num_files < len(all_files):
        files_to_upload = random.sample(all_files, num_files)
        print(
            f"Randomly selected {num_files} files out of {len(all_files)} total files"
        )
    else:
        files_to_upload = all_files
        print(f"Uploading all {len(files_to_upload)} files")

    # Upload files in parallel with progress bar
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(upload_file, file_path, bucket_name, base_prefix): file_path
            for file_path in files_to_upload
        }

        # Use tqdm to display progress
        results = []
        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Uploading files"
        ):
            results.append(future.result())

    # Print summary
    successful = sum(results)
    failed = len(results) - successful
    print(f"\nUpload Summary:")
    print(f"Successfully uploaded: {successful}")
    print(f"Failed uploads: {failed}")


if __name__ == "__main__":
    import argparse

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Upload files to S3")
    parser.add_argument(
        "--num-files",
        type=int,
        help="Number of files to upload (optional)",
        default=None,
    )

    # Parse arguments
    args = parser.parse_args()

    # Run main with specified number of files (or None for all files)
    main(args.num_files)
