#!/usr/bin/env python3

import argparse
import logging
import os
from PyPDF2 import PdfFileReader

logger = logging.getLogger(__name__)

class PdfHashExtractor:
    """
    Extracts hash and encryption information from a PDF file

    Attributes:
    - `file_name`: PDF file path.
    - `strict`: Boolean that controls whether an error is raised, if a PDF
        has problems e.g. Multiple definitions in encryption dictionary
        for a specific key. Defaults to `False`.
    - `algorithm`: Encryption algorithm used by the standard security handler
    - `length`: The length of the encryption key, in bits. Defaults to 40.
    - `permissions`: User access permissions
    - `revision`: Revision of the standard security handler
    """

    def __init__(self, file_name: str, strict: bool = False):
        self.file_name = file_name

        with open(file_name, "rb") as doc:
            self.pdf = PdfFileReader(doc, strict=strict)
            self.encrypt_dict = self.pdf.getEncryptionDictionary()

            if not self.encrypt_dict:
                raise RuntimeError("File not encrypted")

            self.algorithm: int = self.encrypt_dict.get("/Filter", "Unknown")
            self.revision: int = self.encrypt_dict.get("/R", -1)
            self.length: int = self.encrypt_dict.get("/Length", 40)
            self.permissions: int = self.encrypt_dict.get("/P", -1)
            self.encrypt_metadata: int = int(self.encrypt_dict.get("/EncryptMetadata", False))
            self.document_id = self.pdf.trailer['/ID'][0].original_bytes.hex()

    def parse(self) -> str:
        """
        Parse PDF encryption information into a formatted string
        """
        fields = [
            f"${self.file_name}${self.algorithm}",
            self.revision,
            self.length,
            self.permissions,
            self.encrypt_metadata,
            len(self.document_id),
            self.document_id,
            "32*00000000000000000000000000000000",
            "32*00000000000000000000000000000000"
        ]
        return "*".join(map(str, fields))

def search_pdf_files(directory):
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Hash Extractor")
    parser.add_argument(
        "directory", help="Directory containing PDF files to extract information from"
    )
    args = parser.parse_args()

    pdf_files = search_pdf_files(args.directory)

    for filename in pdf_files:
        try:
            extractor = PdfHashExtractor(filename)
            pdf_hash = extractor.parse()
            print(pdf_hash)

        except Exception as error:
            logger.error("%s : %s", filename, error, exc_info=True)
