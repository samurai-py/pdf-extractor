import logging
from dataclasses import asdict
import httpx

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from pydantic import BaseModel, HttpUrl

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

async def fetch_pdf_from_url(url: str) -> bytes:
    """Fetch PDF file from a given URL and return its content as bytes."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            if response.headers['Content-Type'] != 'application/pdf':
                logger.error("The provided URL does not point to a PDF file.")
                raise HTTPException(status_code=400, detail="The provided URL does not point to a PDF file")
            return response.content
    except httpx.RequestError as exc:
        logger.error(f"Error downloading the PDF from the provided URL: {exc}")
        raise HTTPException(status_code=500, detail="An error occurred while downloading the PDF")

async def read_pdf_file(file: UploadFile) -> bytes:
    """Read and return the content of an uploaded PDF file."""
    if not file.filename.endswith('.pdf'):
        logger.error("The uploaded file is not a PDF.")
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    return await file.read()

async def extract_data_from_pdf(pdf_bytes: bytes) -> ExtractedDataModel:
    """Extract data from a PDF file given its content as bytes."""
    try:
        extractor = PDFExtractor(pdf_bytes)
        extracted_data = extractor.extract_data()
        logger.info("Successfully extracted data from the PDF.")
        return extracted_data
    except Exception as e:
        logger.exception("Error processing the PDF.")
        raise HTTPException(status_code=500, detail="An error occurred while processing the PDF") from e

@app.post("/process-pdf/", response_model=ExtractedDataModel)
async def process_pdf(file: UploadFile = File(None), url: HttpUrl = Form(None)):
    """
    Processes a PDF file uploaded directly or from a provided URL and extracts specific information.

    Args:
        file (UploadFile): The PDF file to be processed.
        url (HttpUrl): The URL to download the PDF file from.

    Returns:
        JSONResponse: Extracted data from the PDF.
    """
    if not file and not url:
        logger.error("No file or URL provided.")
        raise HTTPException(status_code=400, detail="Either a file or a URL must be provided")

    pdf_bytes = None

    if file:
        pdf_bytes = await read_pdf_file(file)
    elif url:
        pdf_bytes = await fetch_pdf_from_url(str(url))

    extracted_data = await extract_data_from_pdf(pdf_bytes)
    return asdict(extracted_data)
