import os
from pathlib import Path
from tqdm import tqdm
from collections import defaultdict

def check_duplicates(source_dir, auto_rename=False):
    filename_dict = defaultdict(list)
    # If auto_rename is True, this will store the new paths
    renamed_files = []
    
    # Collect all files
    for file_path in source_dir.rglob("*"):
        if file_path.is_file():
            filename_dict[file_path.name].append(file_path)

    has_duplicates = False
    for filename, paths in filename_dict.items():
        if len(paths) > 1:
            has_duplicates = True
            print(f"\nDuplicate found for '{filename}' in:")
            for path in paths:
                print(f"  - {path}")
            
            if auto_rename:
                # Rename files using parent folder name
                for path in paths:
                    parent_folder = path.parent.name
                    new_name = f"{parent_folder} - {path.name}"
                    new_path = path.parent / new_name
                    try:
                        path.rename(new_path)
                        renamed_files.append((str(path), str(new_path)))
                        print(f"Renamed to: {new_path}")
                    except Exception as e:
                        print(f"Error renaming {path}: {str(e)}")

    if auto_rename and renamed_files:
        print("\nSuccessfully renamed files:")
        for old_path, new_path in renamed_files:
            print(f"  {old_path} -> {new_path}")
            
    return has_duplicates

def main(auto_rename=False):
    # Define source and destination directories
    source_dir = Path("./extracted_files")
    dest_dir = Path("./supported_files")
    
    # Check for duplicates first
    print("Checking for duplicate filenames...")
    has_duplicates = check_duplicates(source_dir, auto_rename)
    
    if has_duplicates and not auto_rename:
        print("\nPlease resolve duplicate filenames before proceeding.")
        return
    
    print("Proceeding with file copying...")
    
    # Create destination directory if it doesn't exist
    dest_dir.mkdir(exist_ok=True)
    
    # Define supported file extensions (case-insensitive)
    supported_extensions = {".pdf", ".doc", ".docx"}
    
    # Get list of all files recursively
    files = list(source_dir.rglob("*"))
    
    # Process each file
    for file_path in tqdm(files, desc="Processing files", unit="file"):
        if not file_path.is_file():
            continue
            
        file_ext = file_path.suffix.lower()
        if file_ext in supported_extensions:
            output_path = dest_dir / file_path.name
            try:
                output_path.write_bytes(file_path.read_bytes())
            except Exception as e:
                print(f"Error copying {file_path}: {str(e)}")
        else:
            print(f"Skipping unsupported file: {file_path}")

if __name__ == "__main__":
    # Add flag for auto-renaming
    auto_rename = True  # Set to True to enable auto-renaming
    main(auto_rename)