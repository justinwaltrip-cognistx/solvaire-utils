# Create separate directories for zip and extracted files
DOWNLOAD_DIR="downloads"
EXTRACT_DIR="extracted_files"
mkdir -p "$DOWNLOAD_DIR" "$EXTRACT_DIR"

# Download with progress
echo "Downloading zip file..."
aws s3 cp s3://crown-royal/SmallCellCusts02.zip "$DOWNLOAD_DIR/"

# Unzip with progress feedback
echo "Extracting files..."
unzip -o "$DOWNLOAD_DIR/SmallCellCusts02.zip" -d "$EXTRACT_DIR" | pv -l >/dev/null
