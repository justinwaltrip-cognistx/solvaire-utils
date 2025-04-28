import os
from PyPDF2 import PdfReader
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import logging
import statistics
import json
from datetime import datetime

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


def save_results(data, output_file):
    """Save results to JSON file"""
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)
    print(f"\nResults saved to: {output_file}")


def load_results(output_file):
    """Load results from JSON file"""
    try:
        with open(output_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def analyze_and_display_results(page_counts, pdf_files_count):
    """Analyze and display the results"""
    if not page_counts:
        print("No valid PDFs processed")
        return

    # Calculate statistics
    pages_list = list(page_counts.values())
    mean_pages = statistics.mean(pages_list)
    stdev_pages = statistics.stdev(pages_list) if len(pages_list) > 1 else 0

    # Sort files by page count
    sorted_files = sorted(page_counts.items(), key=lambda x: x[1], reverse=True)

    # Print results
    print("\nFiles sorted by page count (highlighting potential outliers):")
    print("-" * 70)
    print(f"{'Filename':<50} {'Pages':>8} {'Status':>10}")
    print("-" * 70)

    for filename, pages in sorted_files:
        status = ""
        if pages > mean_pages + (2 * stdev_pages):
            status = "OUTLIER"
        print(f"{filename:<50} {pages:>8} {status:>10}")

    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Total PDFs processed: {len(page_counts)}")
    print(f"Failed PDFs: {pdf_files_count - len(page_counts)}")
    print(f"Total pages: {sum(pages_list)}")
    print(f"Average pages: {mean_pages:.1f}")
    print(f"Standard deviation: {stdev_pages:.1f}")
    print(f"Minimum pages: {min(pages_list)}")
    print(f"Maximum pages: {max(pages_list)}")

    # Suggest threshold
    threshold = mean_pages + (2 * stdev_pages)
    print(f"\nSuggested outlier threshold (mean + 2*std): {threshold:.1f} pages")
    print("Files above this threshold might be candidates for removal.")


def get_pdf_page_distribution(data_dir, max_workers=4, force_recount=False):
    """Get page distribution for all PDFs in directory using parallel processing"""
    # Create output filename based on directory name
    output_file = f"pdf_page_counts_{os.path.basename(data_dir)}.json"

    # Try to load existing results unless force_recount is True
    if not force_recount:
        existing_results = load_results(output_file)
        if existing_results:
            print("Loading existing results from file...")
            analyze_and_display_results(
                existing_results["page_counts"], existing_results["total_pdf_files"]
            )
            return

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

    # Save results
    results_data = {
        "page_counts": page_counts,
        "total_pdf_files": len(pdf_files),
        "timestamp": datetime.now().isoformat(),
    }
    save_results(results_data, output_file)

    # Display results
    analyze_and_display_results(page_counts, len(pdf_files))


if __name__ == "__main__":
    data_dir = "./supported_files"
    # Set force_recount=True if you want to recount pages regardless of existing results
    get_pdf_page_distribution(data_dir, force_recount=True)
