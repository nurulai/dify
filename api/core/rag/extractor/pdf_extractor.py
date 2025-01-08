"""Abstract interface for document loader implementations with image-based text extraction."""

from collections.abc import Iterator
from typing import Optional, cast
import io
import pytesseract
from pdf2image import convert_from_bytes

from core.rag.extractor.blob.blob import Blob
from core.rag.extractor.extractor_base import BaseExtractor
from core.rag.models.document import Document
from extensions.ext_storage import storage


class PdfExtractor(BaseExtractor):
    """Load pdf files by converting pages to images and using OCR.

    Args:
        file_path: Path to the file to load.
        file_cache_key: Optional key for caching extracted text.
        dpi: Resolution for rendering PDF pages (default: 200).
        language: OCR language(s) to use (default: 'eng').
    """

    def __init__(
        self, 
        file_path: str, 
        file_cache_key: Optional[str] = None,
        dpi: int = 200,
        language: str = 'eng'
    ):
        """Initialize with file path and optional parameters."""
        self._file_path = file_path
        self._file_cache_key = file_cache_key
        self._dpi = dpi
        self._language = language

    def extract(self) -> list[Document]:
        """Extract text from PDF pages using image conversion and OCR."""
        if self._file_cache_key:
            try:
                text = cast(bytes, storage.load(self._file_cache_key)).decode("utf-8")
                return [Document(page_content=text)]
            except FileNotFoundError:
                pass

        documents = list(self.load())
        text_list = []
        for document in documents:
            text_list.append(document.page_content)
        text = "\n\n".join(text_list)

        # save plaintext file for caching
        if self._file_cache_key:
            storage.save(self._file_cache_key, text.encode("utf-8"))

        return documents

    def load(self) -> Iterator[Document]:
        """Lazy load given path as pages."""
        blob = Blob.from_path(self._file_path)
        yield from self.parse(blob)

    def parse(self, blob: Blob) -> Iterator[Document]:
        """Lazily parse the blob by converting pages to images and performing OCR."""
        with blob.as_bytes_io() as file_path:
            # Convert PDF pages to images
            images = convert_from_bytes(
                file_path.read(),
                dpi=self._dpi,
                fmt='PNG'
            )
            
            for page_number, image in enumerate(images):
                # Perform OCR on the image
                content = pytesseract.image_to_string(
                    image,
                    lang=self._language
                )
                
                metadata = {
                    "source": blob.source,
                    "page": page_number,
                    "dpi": self._dpi,
                    "ocr_language": self._language
                }
                
                yield Document(page_content=content, metadata=metadata)

    @staticmethod
    def get_available_languages() -> list[str]:
        """Get list of available OCR languages."""
        return pytesseract.get_languages()