import fitz  # PyMuPDF
import os
import glob
from typing import List, Dict

def extract_text_blocks_from_pdf(pdf_path: str) -> List[Dict]:
    """
    Extracts text blocks from a PDF file using PyMuPDF.
    Returns a list of dictionaries containing the text, page number, and block coordinates.
    """
    doc = fitz.open(pdf_path)
    all_blocks = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Extract blocks: (x0, y0, x1, y1, text, block_no, block_type)
        # block_type == 0 means text block, 1 means image block
        blocks = page.get_text("blocks")
        
        for b in blocks:
            if b[6] == 0:  # Only process text blocks
                text = b[4].strip()
                if text:
                    # Clean up hyphens at the end of lines
                    text = text.replace("-\n", "")
                    
                    block_info = {
                        "text": text,
                        "page": page_num + 1,
                        "bbox": b[:4]
                    }
                    all_blocks.append(block_info)
                    
    return all_blocks

def parse_all_pdfs(input_dir: str = "data/raw") -> Dict[str, List[Dict]]:
    """
    Parses all PDFs in the specified directory.
    """
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    parsed_data = {}
    
    print(f"Found {len(pdf_files)} PDFs in {input_dir}. Parsing...")
    
    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        print(f"Parsing {filename}...")
        blocks = extract_text_blocks_from_pdf(pdf_path)
        parsed_data[filename] = blocks
        
    print(f"Successfully parsed {len(pdf_files)} PDFs.")
    return parsed_data

if __name__ == "__main__":
    # Test the parser on downloaded PDFs
    data = parse_all_pdfs()
    
    if data:
        # Print a sample from the first PDF
        first_pdf = list(data.keys())[0]
        print(f"\nSample extracted block from {first_pdf}:")
        print(data[first_pdf][10] if len(data[first_pdf]) > 10 else data[first_pdf][0])
