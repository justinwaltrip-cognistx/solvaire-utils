"""
data dir: ./crown_royal_processing_converted

Get distribution of pages in each file in the directory. Ignore non-PDF files.
"""

import os
from PyPDF2 import PdfReader
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import logging

# Setup logging
logging.basicConfig(level=logging.ERROR)


def count_pages(file_info):
    """Count pages in a single PDF file"""
    file_path, filename = file_info
    try:
        reader = PdfReader(file_path)
        return filename, len(reader.pages)
    except Exception as e:
        logging.error(f"Error processing {filename}: {e}")
        return filename, None


def get_pdf_page_distribution(data_dir, max_workers=4):
    """Get page distribution for all PDFs in directory using parallel processing"""

    # Get list of PDF files with full paths
    pdf_files = [
        (os.path.join(data_dir, f), f)
        for f in os.listdir(data_dir)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:
        print("No PDF files found in directory")
        return

    # Process PDFs in parallel with progress bar
    page_counts = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(
            tqdm(
                executor.map(count_pages, pdf_files),
                total=len(pdf_files),
                desc="Processing PDFs",
            )
        )

    # Collect results
    page_counts = {filename: pages for filename, pages in results if pages is not None}

    # Print results
    print("\nPage distribution:")
    for file, pages in sorted(page_counts.items()):
        print(f"{file}: {pages} pages")

    # Print summary statistics
    if page_counts:
        total_pages = sum(page_counts.values())
        avg_pages = total_pages / len(page_counts)
        print(f"\nTotal PDFs processed: {len(page_counts)}")
        print(f"Failed PDFs: {len(pdf_files) - len(page_counts)}")
        print(f"Total pages: {total_pages}")
        print(f"Average pages per PDF: {avg_pages:.1f}")


if __name__ == "__main__":
    data_dir = "./crown_royal_processing_converted"
    get_pdf_page_distribution(data_dir)
