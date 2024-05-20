import re
import io
from typing import Dict, List, Union

import pdfplumber


def extract_pdf_data(pdf_bytes: bytes) -> Dict[str, Union[Dict[str, str], List[Dict[str, str]]]]:
    """
    Extracts data from a PDF file.

    Args:
        pdf_bytes (bytes): The PDF file content as bytes.

    Returns:
        dict: A dictionary containing extracted data.
            - 'customer': A dictionary containing customer data.
            - 'invoice_details': A dictionary containing invoice details.
            - 'recipient_bank_details': A dictionary containing recipient bank details.
    """
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
        lines = text.split('\n')

        customer_data = extract_customer_data(lines)
        invoice_details = extract_invoice_details(lines, text)
        recipient_bank_details = extract_bank_details(text)

        return {
            "customer": customer_data,
            "invoice_details": invoice_details,
            "recipient_bank_details": recipient_bank_details
        }
    

def extract_customer_data(lines: List[str]) -> Dict[str, str]:
    """
    Extracts customer data from the lines.

    Args:
        lines (List[str]): The lines of text extracted from the PDF.

    Returns:
        dict: A dictionary containing customer data.
            - 'name': The customer's name.
            - 'street': The customer's street address.
            - 'postcode': The customer's postcode.
            - 'country': The customer's country.
    """
    return {
        "name": ' '.join(lines[6].split()[:2]),
        "street": lines[7].strip(),
        "postcode": lines[8].strip(),
        "country": lines[9].strip()
    }


def extract_invoice_details(lines: List[str], text: str) -> Dict[str, Union[str, List[Dict[str, str]]]]:
    """
    Extracts invoice details from the lines and text.

    Args:
        lines (List[str]): The lines of text extracted from the PDF.
        text (str): The extracted text from the PDF.

    Returns:
        dict: A dictionary containing invoice details.
            - 'date': The invoice date.
            - 'id': The invoice number.
            - 'payment_due': The payment due date.
            - 'payments': A list of payment details dictionaries.
    """
    invoice_details = {
        "date": extract_value(text, r'Invoice date:\s*(.*?)\n'),
        "id": extract_value(text, r'Invoice number:\s*(.*?)\n'),
        "payment_due": extract_value(text, r'Payment due:\s*(.*?)\n'),
        "payments": [
            extract_payment_details(lines[14])
        ]
    }
    return invoice_details


def extract_payment_details(line: str) -> Dict[str, str]:
    """
    Extracts payment details from a line.

    Args:
        line (str): The line containing payment details.

    Returns:
        dict: A dictionary containing payment details.
            - 'description': The payment description.
            - 'from': The start date of the payment period.
            - 'until': The end date of the payment period.
            - 'amount': The payment amount.
    """
    dates = re.findall(r'[a-zA-Z]{3} \d{1,2}, \d{4}', line)
    money = re.findall(r'\b(?:USD|\$)\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?\b', line)

    description = line
    for date in dates:
        description = description.replace(date, "")
    for m in money:
        description = description.replace(m, "")

    return {
        "description": description.replace("USD", "").strip(),
        "from": dates[0] if dates else "",
        "until": dates[1] if len(dates) > 1 else "",
        "amount": money[0] if money else ""
    }


def extract_bank_details(text: str) -> Dict[str, str]:
    """
    Extracts recipient bank details from the text.

    Args:
        text (str): The extracted text from the PDF.

    Returns:
        dict: A dictionary containing recipient bank details.
            - 'bank_account_name': The bank account name.
            - 'bank_name': The name of the bank.
            - 'account_number': The bank account number.
            - 'swift_code': The bank SWIFT code.
            - 'bank_address': The bank address.
    """
    return {
        "bank_account_name": extract_value(text, r'Bank account name:\s*(.*?)\n'),
        "bank_name": extract_value(text, r'Name of Bank:\s*(.*?)\n'),
        "account_number": extract_value(text, r'Bank account number:\s*(.*?)\n'),
        "swift_code": extract_value(text, r'Bank SWIFT code:\s*(.*?)\n'),
        "bank_address": extract_value(text, r'Bank address:\s*(.*?)\n')
    }


def extract_value(text: str, pattern: str) -> Union[str, None]:
    """
    Extracts a value from the text using a regular expression pattern.

    Args:
        text (str): The text to extract the value from.
        pattern (str): The regular expression pattern.

    Returns:
        str or None: The extracted value or None if no match is found.
    """
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None
