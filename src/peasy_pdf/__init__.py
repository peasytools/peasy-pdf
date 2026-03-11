"""peasy-pdf — Python PDF toolkit powered by pypdf.

21 PDF operations: merge, split, rotate, compress, extract text,
encrypt, decrypt, reorder, reverse, delete pages, extract pages,
odd/even filter, duplicate pages, insert blank pages, resize, crop,
flatten, get/set/strip metadata, and info.

Usage::

    from peasy_pdf import merge, split, info, extract_text

    merged = merge("file1.pdf", "file2.pdf")
    parts = split("doc.pdf", every=5)

    pdf_info = info("doc.pdf")
    print(pdf_info.pages)    # 42
    print(pdf_info.title)    # "Annual Report"

    text = extract_text("doc.pdf", pages="1-3")
    print(text.full_text)
"""

from peasy_pdf.engine import (
    ExtractedText,
    OddEvenMode,
    PageSize,
    PageTextResult,
    PdfInfo,
    PdfInput,
    PdfMetadata,
    compress,
    crop,
    decrypt,
    delete_pages,
    duplicate_pages,
    encrypt,
    extract_pages,
    extract_text,
    flatten,
    get_metadata,
    info,
    insert_blank,
    merge,
    odd_even,
    reorder,
    resize,
    reverse,
    rotate,
    set_metadata,
    split,
    strip_metadata,
)

__version__ = "0.1.0"

__all__ = [
    "ExtractedText",
    "OddEvenMode",
    "PageSize",
    "PageTextResult",
    "PdfInfo",
    "PdfInput",
    "PdfMetadata",
    "compress",
    "crop",
    "decrypt",
    "delete_pages",
    "duplicate_pages",
    "encrypt",
    "extract_pages",
    "extract_text",
    "flatten",
    "get_metadata",
    "info",
    "insert_blank",
    "merge",
    "odd_even",
    "reorder",
    "resize",
    "reverse",
    "rotate",
    "set_metadata",
    "split",
    "strip_metadata",
]
