# DO NOT USE AS IS
# Create and move to a working directory
WORK_DIR="crown_royal_processing"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# Download with progress
echo "Downloading zip file..."
# TODO uncomment
# aws s3 cp s3://crown-royal/CrownRoyalFiberCusts01.zip ./

# Unzip with progress feedback
echo "Extracting files..."
unzip -o CrownRoyalFiberCusts01.zip | pv -l >/dev/null

# Upload back to S3 with progress
echo "Uploading files to S3..."
aws s3 cp crown_royal_processing/ s3://crown-royal/CrownRoyalFiberCusts01/ \
    --recursive

echo "Process complete!"
