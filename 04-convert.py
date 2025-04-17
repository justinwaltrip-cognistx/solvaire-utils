"""
data dir: ./crown_royal_processing
out dir: ./crown_royal_processing_converted

Loop through all files in the data directory and convert them to the desired format.

Should remain as is: .pdf, .doc, and .docx
Should be converted to pdf: .rtf, .ps, .png, .tif, .pptx, .xlsx, and .xlsm
"""
import os
import subprocess
from pathlib import Path
import win32com.client
from PIL import Image

def convert_to_pdf(input_path, output_path):
    # Get file extension
    file_ext = input_path.suffix.lower()
    
    try:
        if file_ext in ['.png', '.tif']:
            # Convert image files to PDF
            image = Image.open(input_path)
            rgb_image = image.convert('RGB')
            rgb_image.save(output_path, 'PDF')
            
        elif file_ext in ['.rtf']:
            # Convert RTF to PDF using Word
            word = win32com.client.Dispatch('Word.Application')
            doc = word.Documents.Open(input_path)
            doc.SaveAs(output_path, FileFormat=17)  # 17 represents PDF format
            doc.Close()
            word.Quit()
            
        elif file_ext in ['.pptx']:
            # Convert PowerPoint to PDF
            powerpoint = win32com.client.Dispatch('PowerPoint.Application')
            presentation = powerpoint.Presentations.Open(input_path)
            presentation.SaveAs(output_path, 32)  # 32 represents PDF format
            presentation.Close()
            powerpoint.Quit()
            
        elif file_ext in ['.xlsx', '.xlsm']:
            # Convert Excel to PDF
            excel = win32com.client.Dispatch('Excel.Application')
            workbook = excel.Workbooks.Open(input_path)
            workbook.ExportAsFixedFormat(0, output_path)  # 0 represents PDF format
            workbook.Close()
            excel.Quit()
            
        elif file_ext in ['.ps']:
            # Convert PostScript to PDF using Ghostscript
            subprocess.run(['gs', '-sDEVICE=pdfwrite', '-dNOPAUSE', '-dBATCH', 
                          f'-sOutputFile={output_path}', input_path])
    
    except Exception as e:
        print(f"Error converting {input_path}: {str(e)}")

def main():
    # Define directories
    data_dir = Path('./crown_royal_processing')
    out_dir = Path('./crown_royal_processing_converted')
    
    # Create output directory if it doesn't exist
    out_dir.mkdir(exist_ok=True)
    
    # File extensions that should remain as is
    keep_extensions = {'.pdf', '.doc', '.docx'}
    
    # File extensions that should be converted to PDF
    convert_extensions = {'.rtf', '.ps', '.png', '.tif', '.pptx', '.xlsx', '.xlsm'}
    
    # Process all files in the data directory
    for file_path in data_dir.glob('*'):
        if not file_path.is_file():
            continue
            
        file_ext = file_path.suffix.lower()
        
        if file_ext in keep_extensions:
            # Copy file as is
            output_path = out_dir / file_path.name
            output_path.write_bytes(file_path.read_bytes())
            
        elif file_ext in convert_extensions:
            # Convert file to PDF
            output_path = out_dir / (file_path.stem + '.pdf')
            convert_to_pdf(file_path, output_path)
            
        else:
            print(f"Skipping unsupported file: {file_path}")

if __name__ == "__main__":
    main()