import json
import os
import statistics
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns


def load_page_counts(json_file):
    """Load the saved page count data"""
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
            return data["page_counts"]
    except FileNotFoundError:
        print(f"Error: Could not find {json_file}")
        return None


def analyze_outliers(page_counts, std_dev_threshold=2):
    """Analyze page counts and identify outliers"""
    if not page_counts:
        return None

    pages_list = list(page_counts.values())
    mean_pages = statistics.mean(pages_list)
    stdev_pages = statistics.stdev(pages_list) if len(pages_list) > 1 else 0
    threshold = mean_pages + (std_dev_threshold * stdev_pages)

    # Sort files by page count and identify outliers
    sorted_files = sorted(page_counts.items(), key=lambda x: x[1], reverse=True)
    outliers = [(f, p) for f, p in sorted_files if p > threshold]

    return {
        "mean": mean_pages,
        "stdev": stdev_pages,
        "threshold": threshold,
        "outliers": outliers,
        "all_files": sorted_files,
    }


def plot_distribution(page_counts, stats, output_file="page_distribution.png"):
    """Create a histogram of page counts with outlier threshold marked"""
    plt.figure(figsize=(12, 6))
    sns.histplot(list(page_counts.values()), bins=30)
    plt.axvline(
        x=stats["threshold"],
        color="r",
        linestyle="--",
        label=f'Outlier Threshold ({stats["threshold"]:.1f} pages)',
    )
    plt.title("Distribution of PDF Page Counts")
    plt.xlabel("Number of Pages")
    plt.ylabel("Count")
    plt.legend()
    plt.savefig(output_file)
    plt.close()
    print(f"\nDistribution plot saved as: {output_file}")


def main():
    # Load the data
    json_file = "pdf_page_counts_crown_royal_processing_converted.json"  # Adjust filename if needed
    page_counts = load_page_counts(json_file)

    if not page_counts:
        return

    # Analyze the data
    stats = analyze_outliers(page_counts)

    # Prepare the summary data
    summary_data = []
    for filename, pages in stats["outliers"]:
        std_devs_above_mean = (pages - stats["mean"]) / stats["stdev"]
        summary_data.append(
            [
                filename,
                pages,
                f"{std_devs_above_mean:.1f}",
                f"{(pages - stats['mean']):.1f}",
            ]
        )

    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Mean pages: {stats['mean']:.1f}")
    print(f"Standard deviation: {stats['stdev']:.1f}")
    print(f"Outlier threshold: {stats['threshold']:.1f}")
    print(f"\nFound {len(stats['outliers'])} potential outliers")

    # Print outlier details in a nice table
    if summary_data:
        print("\nPotential outliers (sorted by page count):")
        headers = ["Filename", "Pages", "Std Devs Above Mean", "Pages Above Mean"]
        print(tabulate(summary_data, headers=headers, tablefmt="grid"))

        # Create a list of commands to remove outliers
        print("\nTo remove these files, you can use the following commands:")
        print("\nBash commands:")
        for filename, _ in stats["outliers"]:
            print(f'rm "{filename}"')

        print("\nPython commands:")
        print("import os")
        for filename, _ in stats["outliers"]:
            print(f'os.remove("{filename}")')

    # Plot the distribution
    plot_distribution(page_counts, stats)

    # Print percentile information
    pages_list = list(page_counts.values())
    percentiles = [50, 75, 90, 95, 99]
    print("\nPercentile Information:")
    for p in percentiles:
        value = statistics.quantiles(pages_list, n=100)[p - 1]
        print(f"{p}th percentile: {value:.1f} pages")


if __name__ == "__main__":
    main()
