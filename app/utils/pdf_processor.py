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
                "description": "",
                "from": "",
                "until": "",
                "amount": ""
            }
        ]
        }

        # Separando a linha em suas partes distintas
        line_14 = lines[14]
        dates = re.findall(r'[a-zA-Z]{3} \d{1,2}, \d{4}', line_14)
        money = re.findall(r'\b(?:USD|\$)\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?\b', line_14)

        # Removendo as datas e o valor monetário da descrição
        description = line_14
        for date in dates:
            description = description.replace(date, "")
        for m in money:
            description = description.replace(m, "")

        # Definindo os valores extraídos nos detalhes da fatura
        invoice_details["payments"][0]["description"] = description.replace("USD", "").strip()

        # Definindo os valores extraídos nos detalhes da fatura
        if dates:
            invoice_details["payments"][0]["from"] = dates[0]
            if len(dates) > 1:
                invoice_details["payments"][0]["until"] = dates[1]
            else:
                invoice_details["payments"][0]["until"] = ""
        else:
            invoice_details["payments"][0]["from"] = ""
            invoice_details["payments"][0]["until"] = ""

        invoice_details["payments"][0]["amount"] = money[0] if money else ""

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
