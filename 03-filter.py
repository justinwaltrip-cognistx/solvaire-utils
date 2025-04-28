import os
from pathlib import Path
from tqdm import tqdm
from collections import defaultdict


def check_duplicates(source_dir):
    # Dictionary to store filename occurrences
    filename_dict = defaultdict(list)

    # Recursively get all files
    for file_path in source_dir.rglob("*"):
        if file_path.is_file():
            filename_dict[file_path.name].append(str(file_path))

    # Check for duplicates
    has_duplicates = False
    for filename, paths in filename_dict.items():
        if len(paths) > 1:
            has_duplicates = True
            print(f"\nDuplicate found for '{filename}' in:")
            for path in paths:
                print(f"  - {path}")

    return has_duplicates


def main():
    # Define source and destination directories
    source_dir = Path("./extracted_files")
    dest_dir = Path("./supported_files")

    # Check for duplicates first
    print("Checking for duplicate filenames...")
    if check_duplicates(source_dir):
        print("\nPlease resolve duplicate filenames before proceeding.")
        return

    print("No duplicates found. Proceeding with file copying...")

    # Create destination directory if it doesn't exist
    dest_dir.mkdir(exist_ok=True)

    # Define supported file extensions (case-insensitive)
    supported_extensions = {".pdf", ".doc", ".docx"}

    # Get list of all files recursively
    files = list(source_dir.rglob("*"))

    # Process each file
    for file_path in tqdm(files, desc="Processing files", unit="file"):
        # Skip if not a file
        if not file_path.is_file():
            continue

        # Get file extension in lowercase
        file_ext = file_path.suffix.lower()

        # Copy file if extension is supported
        if file_ext in supported_extensions:
            output_path = dest_dir / file_path.name
            try:
                output_path.write_bytes(file_path.read_bytes())
            except Exception as e:
                print(f"Error copying {file_path}: {str(e)}")
        else:
            print(f"Skipping unsupported file: {file_path}")


if __name__ == "__main__":
    main()
