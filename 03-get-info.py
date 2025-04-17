import os
from collections import Counter
from pathlib import Path

def analyze_file_types(directory):
    # Initialize a Counter to store file extensions and their counts
    extension_counts = Counter()
    
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Get the file extension (converted to lowercase for consistency)
            extension = Path(file).suffix.lower()
            extension_counts[extension] += 1
    
    # Print results in Markdown format
    print("# File Types Found")
    print("| Extension | Count |")
    print("|-----------|-------|")
    for ext, count in extension_counts.most_common():
        if ext:  # If there is an extension
            print(f"| `{ext}` | {count} |")
        else:  # For files with no extension
            print(f"| No extension | {count} |")

# Usage
try:
    analyze_file_types("./crown_royal_processing")
except Exception as e:
    print(f"Error analyzing directory: {e}")