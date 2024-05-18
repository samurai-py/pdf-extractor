import pdfplumber
import re
import io

def extract_pdf_data(pdf_bytes):
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        # Selecionando a primeira página do PDF
        page = pdf.pages[0]
        text = page.extract_text()

        # Extraindo informações específicas do texto
        lines = text.split('\n')
        customer_data = {
            "name": ' '.join(lines[6].split()[:2]),
            "street": lines[7].strip(),
            "postcode": lines[8].strip(),
            "country": lines[9].strip()
        }

        invoice_details = {
            "date": extract_value(text, r'Invoice date:\s*(.*?)\n'),
            "id": extract_value(text, r'Invoice number:\s*(.*?)\n'),
            "payment_due": extract_value(text, r'Payment due:\s*(.*?)\n'),
            "payments": [
                {
                    "description": extract_value(text, r'Description\n(.*?)\n'),
                    "from": extract_value(text, r'From (.*?) '),
                    "until": extract_value(text, r'Until (.*?)\n'),
                    "amount": extract_value(text, r'Amount\n(.*?)\n')
                }
            ]
        }

        recipient_bank_details = {
            "bank_account_name": extract_value(text, r'Bank account name:*(.*?)\n'),
            "bank_name": extract_value(text, r'Name of Bank:*(.*?)\n'),
            "account_number": extract_value(text, r'Bank account number:*(.*?)\n'),
            "swift_code": extract_value(text, r'Bank SWIFT code:*(.*?)\n'),
            "bank_address": extract_value(text, r'Bank address:*(.*?)\n')
        }

        return {
            "customer": customer_data,
            "invoice_details": invoice_details,
            "recipient_bank_details": recipient_bank_details
        }

def extract_value(text, pattern):
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None
