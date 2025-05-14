import os
import boto3
import random
import shutil
import zipfile
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


def copy_file_to_dir(file_path, dest_dir):
    """Copy a single file to destination directory"""
    try:
        file_name = os.path.basename(file_path)
        name_without_ext = os.path.splitext(file_name)[0]

        # Create subdirectory structure
        new_dir = os.path.join(dest_dir, name_without_ext)
        os.makedirs(new_dir, exist_ok=True)

        # Copy file to new location
        shutil.copy2(file_path, os.path.join(new_dir, file_name))
        return True
    except Exception as e:
        print(f"Error copying {file_name}: {str(e)}")
        return False


def create_zip_file(source_dir, zip_name):
    """Create a zip file from the source directory"""
    try:
        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
        return True
    except Exception as e:
        print(f"Error creating zip file: {str(e)}")
        return False


def main(num_files=None, local_only=False):
    # Configuration
    source_dir = "./supported_files"
    bucket_name = "sqr-bucket-194-prod"
    base_prefix = "unzipped/sync"
    max_workers = 5
    local_dest_dir = "./output_files"
    zip_name = "output_files.zip"

    # Create list of files to process
    all_files = []
    for file in os.listdir(source_dir):
        if os.path.isfile(os.path.join(source_dir, file)):
            all_files.append(os.path.join(source_dir, file))

    # If num_files is specified and less than total files, randomly sample
    if num_files and num_files < len(all_files):
        files_to_process = random.sample(all_files, num_files)
        print(
            f"Randomly selected {num_files} files out of {len(all_files)} total files"
        )
    else:
        files_to_process = all_files
        print(f"Processing all {len(files_to_process)} files")

    if local_only:
        # Create local directory structure and copy files
        os.makedirs(local_dest_dir, exist_ok=True)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(copy_file_to_dir, file_path, local_dest_dir): file_path
                for file_path in files_to_process
            }

            results = []
            for future in tqdm(
                as_completed(futures), total=len(futures), desc="Copying files"
            ):
                results.append(future.result())

        # Create zip file
        print("\nCreating zip file...")
        if create_zip_file(local_dest_dir, zip_name):
            print(f"Successfully created {zip_name}")
        else:
            print("Failed to create zip file")

        # Print summary
        successful = sum(results)
        failed = len(results) - successful
        print(f"\nCopy Summary:")
        print(f"Successfully copied: {successful}")
        print(f"Failed copies: {failed}")

    else:
        # Upload files to S3
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    upload_file, file_path, bucket_name, base_prefix
                ): file_path
                for file_path in files_to_process
            }

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
    parser = argparse.ArgumentParser(
        description="Process files (upload to S3 or create local zip)"
    )
    parser.add_argument(
        "--num-files",
        type=int,
        help="Number of files to process (optional)",
        default=None,
    )
    parser.add_argument(
        "--local-only",
        action="store_true",
        help="Create local directory structure and zip file instead of uploading to S3",
    )

    # Parse arguments
    args = parser.parse_args()

    # Run main with specified options
    main(args.num_files, args.local_only)
