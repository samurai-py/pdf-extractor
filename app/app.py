import logging
from dataclasses import asdict

from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel

from .utils.pdf_processor import PDFExtractor


# Logger configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)

app = FastAPI()

class ExtractedDataModel(BaseModel):
    customer: dict
    invoice_details: dict
    recipient_bank_details: dict

@app.post("/process-pdf/", response_model=ExtractedDataModel)
async def process_pdf(file: UploadFile = File(...)):
    """
    Processes a PDF file and extracts specific information.

    Args:
        file (UploadFile): The PDF file to be processed.

    Returns:
        JSONResponse: Extracted data from the PDF.
    """
    if not file.filename.endswith('.pdf'):
        logger.error("Uploaded file is not a PDF.")
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        pdf_bytes = await file.read()
        extractor = PDFExtractor(pdf_bytes)
        extracted_data = extractor.extract_data()
        logger.info("Successfully extracted data from the PDF.")
        return asdict(extracted_data)
    except Exception as e:
        logger.exception("Error processing the PDF.")
        raise HTTPException(status_code=500, detail="An error occurred while processing the PDF") from e
