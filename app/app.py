import logging

from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, HTTPException

from .utils.pdf_processor import extract_pdf_data

# Logger configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)

app = FastAPI()

class ExtractedData(BaseModel):
    customer: dict
    invoice_details: dict
    recipient_bank_details: dict

@app.post("/process-pdf/", response_model=ExtractedData)
async def process_pdf(file: UploadFile = File(...)):
    """
    Processes a PDF file and extracts specific information.

    Args:
        file (UploadFile): The PDF file to be processed.

    Returns:
        JSONResponse: Extracted data from the PDF.
    """

    if not file.filename.endswith('.pdf'):
        logger.error("O arquivo enviado não é um PDF.")
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        pdf_bytes = await file.read()
        extracted_data = extract_pdf_data(pdf_bytes)
        logger.info("Dados extraídos com sucesso do PDF.")
        return extracted_data
    except Exception as e:
        logger.exception("Erro ao processar o PDF.")
        raise HTTPException(status_code=500, detail="An error occurred while processing the PDF") from e
