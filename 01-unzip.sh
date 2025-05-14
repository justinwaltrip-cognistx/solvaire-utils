set -ex

# Create separate directories for zip and extracted files
DOWNLOAD_DIR="downloads"
EXTRACT_DIR="extracted_files"
ZIP_FILE="SmallCellCusts02_FlattenedPortfolios.zip"
mkdir -p "$DOWNLOAD_DIR" "$EXTRACT_DIR"

# Download with progress
echo "Downloading zip file..."
aws s3 cp s3://crown-royal/$ZIP_FILE "$DOWNLOAD_DIR/"

# Unzip with progress feedback
echo "Extracting files..."
unzip -o "$DOWNLOAD_DIR/$ZIP_FILE" -d "$EXTRACT_DIR" | pv -l >/dev/null
