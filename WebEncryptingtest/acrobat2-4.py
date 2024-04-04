#!/usr/bin/env python3

import argparse
import os
import PyPDF2

class PdfHashExtractor:
    """
    Extracts hash and encryption information from a PDF file

    Attributes:
    - `file_name`: PDF file path.
    """

    def __init__(self, file_name: str):
        self.file_name = file_name

    def parse(self) -> str:
        """
        Parse PDF encryption information into a formatted string for John
        """
        try:
            with open(self.file_name, "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                encrypt_dict = pdf_reader.getEncryptionDictionary()

                if not encrypt_dict:
                    raise RuntimeError("File not encrypted")

                algorithm = encrypt_dict.get("/V")
                length = encrypt_dict.get("/Length", 40)
                permissions = encrypt_dict["/P"]
                revision = encrypt_dict["/R"]

                document_id = pdf_reader.trailer.get("/ID")[0]
                encrypt_metadata = pdf_reader.encrypt_metadata

                passwords = self.get_passwords(pdf_reader)

                fields = [
                    f"$pdf${algorithm}",
                    revision,
                    length,
                    permissions,
                    encrypt_metadata,
                    len(document_id),
                    document_id.hex(),
                    passwords,
                ]
                return "*".join(map(str, fields))

        except PyPDF2.utils.PdfReadError as error:
            raise RuntimeError(f"Error reading PDF: {error}")

    def get_passwords(self, pdf_reader) -> str:
        """
        Creates a string consisting of the hexidecimal string of the
        /U, /O, /UE and /OE entries and their corresponding byte string length
        """
        passwords = []
        keys = ("udata", "odata", "oeseed", "ueseed")
        max_key_length = 48  # Maximum key length for encryption revision 5

        for key in keys:
            data = pdf_reader.decrypt_info[key]

            if data:
                data = data[:max_key_length]
                passwords.extend([str(len(data)), data.hex()])

        return "*".join(passwords)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Hash Extractor")
    parser.add_argument(
        "pdf_files", nargs="+", help="PDF file(s) to extract information from"
    )
    args = parser.parse_args()

    for pdf_file in args.pdf_files:
        try:
            extractor = PdfHashExtractor(pdf_file)
            pdf_hash = extractor.parse()
            print(pdf_hash)

        except RuntimeError as error:
            print(f"Error processing {pdf_file}: {error}")
