import re
import io
from typing import List, Optional
from dataclasses import dataclass
import pdfplumber

@dataclass
class PaymentDetails:
    """Class representing payment details."""
    description: str
    from_date: str
    until_date: str
    amount: str


@dataclass
class InvoiceDetails:
    """Class representing invoice details."""
    date: str
    id: str
    payment_due: str
    payments: List[PaymentDetails]


@dataclass
class CustomerData:
    """Class representing customer data."""
    name: str
    street: str
    postcode: str
    country: str


@dataclass
class RecipientBankDetails:
    """Class representing recipient bank details."""
    bank_account_name: str
    bank_name: str
    account_number: str
    swift_code: str
    bank_address: str


@dataclass
class ExtractedData:
    """Class representing extracted data."""
    customer: CustomerData
    invoice_details: InvoiceDetails
    recipient_bank_details: RecipientBankDetails


class PDFExtractor:
    """Class for extracting data from a PDF."""
    def __init__(self, pdf_bytes: bytes):
        self.pdf_bytes = pdf_bytes
        self.text = self._extract_text()
        self.lines = self.text.split('\n')

    def _extract_text(self) -> str:
        """Extracts text from the PDF."""
        with pdfplumber.open(io.BytesIO(self.pdf_bytes)) as pdf:
            page = pdf.pages[0]
            return page.extract_text()

    def extract_data(self) -> ExtractedData:
        """Extracts data from the PDF."""
        customer_data = self._extract_customer_data()
        invoice_details = self._extract_invoice_details()
        recipient_bank_details = self._extract_bank_details()

        return ExtractedData(
            customer=customer_data,
            invoice_details=invoice_details,
            recipient_bank_details=recipient_bank_details
        )

    def _extract_customer_data(self) -> CustomerData:
        """Extracts customer data from the PDF."""
        return CustomerData(
            name=' '.join(self.lines[6].split()[:2]),
            street=self.lines[7].strip(),
            postcode=self.lines[8].strip(),
            country=self.lines[9].strip()
        )

    def _extract_invoice_details(self) -> InvoiceDetails:
        """Extracts invoice details from the PDF."""
        return InvoiceDetails(
            date=self._extract_value(r'Invoice date:\s*(.*?)\n'),
            id=self._extract_value(r'Invoice number:\s*(.*?)\n'),
            payment_due=self._extract_value(r'Payment due:\s*(.*?)\n'),
            payments=[self._extract_payment_details(self.lines[14])]
        )

    def _extract_payment_details(self, line: str) -> PaymentDetails:
        """Extracts payment details from a line of text."""
        
        dates = re.findall(r'[a-zA-Z]{3} \d{1,2}, \d{4}', line)
        money = re.findall(r'(USD\s*\$?\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', line)

        description = line
        for date in dates:
            description = description.replace(date, "")
        for m in money:
            description = description.replace(m, "")

        return PaymentDetails(
            description=description.strip(),
            from_date=dates[0] if dates else "",
            until_date=dates[1] if len(dates) > 1 else "",
            amount=money[0] if money else ""
        )

    def _extract_bank_details(self) -> RecipientBankDetails:
        """Extracts recipient bank details from the PDF."""
        return RecipientBankDetails(
            bank_account_name=self._extract_value(r'Bank account name:\s*(.*?)\n'),
            bank_name=self._extract_value(r'Name of Bank:\s*(.*?)\n'),
            account_number=self._extract_value(r'Bank account number:\s*(.*?)\n'),
            swift_code=self._extract_value(r'Bank SWIFT code:\s*(.*?)\n'),
            bank_address=self._extract_value(r'Bank address:\s*(.*?)\n')
        )

    def _extract_value(self, pattern: str) -> Optional[str]:
        """Extracts a value based on a regex pattern."""
        match = re.search(pattern, self.text)
        return match.group(1).strip() if match else None
