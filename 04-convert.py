import os
import subprocess
from pathlib import Path
from PIL import Image
from tqdm import tqdm


def convert_to_pdf(input_path, output_path):
    file_ext = input_path.suffix.lower()
    try:
        if file_ext in [".png", ".tif"]:
            # Convert image files to PDF using Pillow
            image = Image.open(input_path)
            rgb_image = image.convert("RGB")
            rgb_image.save(output_path, "PDF")

        elif file_ext in [".rtf", ".pptx", ".xlsx", ".xlsm"]:
            # Convert office documents using LibreOffice
            subprocess.run(
                [
                    "soffice",
                    "--headless",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    str(output_path.parent),
                    str(input_path),
                ]
            )

        elif file_ext in [".ps"]:
            # Convert PostScript to PDF using Ghostscript
            subprocess.run(
                [
                    "gs",
                    "-sDEVICE=pdfwrite",
                    "-dNOPAUSE",
                    "-dBATCH",
                    f"-sOutputFile={output_path}",
                    str(input_path),
                ]
            )

    except Exception as e:
        print(f"Error converting {input_path}: {str(e)}")


def main():
    data_dir = Path("./crown_royal_processing")
    out_dir = Path("./crown_royal_processing_converted")
    out_dir.mkdir(exist_ok=True)

    keep_extensions = {".pdf", ".doc", ".docx"}
    convert_extensions = {".rtf", ".ps", ".png", ".tif", ".pptx", ".xlsx", ".xlsm"}

    files = list(data_dir.glob("*"))

    for file_path in tqdm(files, desc="Processing files", unit="file"):
        if not file_path.is_file():
            continue

        file_ext = file_path.suffix.lower()
        if file_ext in keep_extensions:
            output_path = out_dir / file_path.name
            output_path.write_bytes(file_path.read_bytes())

        elif file_ext in convert_extensions:
            output_path = out_dir / (file_path.stem + ".pdf")
            convert_to_pdf(file_path, output_path)

        else:
            print(f"Skipping unsupported file: {file_path}")


if __name__ == "__main__":
    main()
