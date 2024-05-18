from fastapi import FastAPI, File, UploadFile, HTTPException
from .utils.pdf_processor import extract_pdf_data

app = FastAPI()

@app.post("/process-pdf/")
async def process_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        extracted_data = extract_pdf_data(await file.read())
        return extracted_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
