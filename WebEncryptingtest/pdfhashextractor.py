import argparse
import logging
import os

from pyhanko.pdf_utils.misc import PdfReadError
from pyhanko.pdf_utils.reader import PdfFileReader

class PdfHashExtractor:

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
        
        #Pasar el tipo de encryptacion en un string final.
        
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

def main():
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, 'documento.pdf')
    
    with open(file_path, 'r') as config_file:
        file_name = config_file.read().strip()

    extractor = PdfHashExtractor(file_name)
    hash_string = extractor.parse()
    print(hash_string)

if __name__ == "__main__":
    main()


