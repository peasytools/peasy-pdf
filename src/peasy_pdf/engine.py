"""peasy-pdf — PDF manipulation engine powered by pypdf.

21 operations: merge, split, rotate, reorder, reverse, delete pages,
extract pages, odd/even filter, duplicate pages, insert blank pages,
compress, resize, crop, flatten, extract text, get/set/strip metadata,
info, encrypt, and decrypt.

All functions accept ``bytes | Path`` input. PDF-producing functions
return ``bytes``. Info/text functions return structured data.
"""

from __future__ import annotations

import io
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

# ── Types ─────────────────────────────────────────────────────────

PdfInput = bytes | Path | str
"""A PDF source: raw bytes, a ``pathlib.Path``, or a string file path."""

PageSize = Literal[
    "a3",
    "a4",
    "a5",
    "letter",
    "legal",
    "tabloid",
]

OddEvenMode = Literal["odd", "even"]


@dataclass(frozen=True)
class PdfInfo:
    """Basic information about a PDF file."""

    pages: int
    encrypted: bool
    title: str
    author: str
    subject: str
    creator: str
    producer: str
    size_bytes: int


@dataclass(frozen=True)
class PdfMetadata:
    """PDF document metadata."""

    title: str = ""
    author: str = ""
    subject: str = ""
    keywords: str = ""
    creator: str = ""
    producer: str = ""


@dataclass(frozen=True)
class PageTextResult:
    """Text extracted from a single page."""

    page: int  # 1-indexed
    text: str


@dataclass(frozen=True)
class ExtractedText:
    """Text extracted from an entire PDF."""

    pages: list[PageTextResult] = field(default_factory=list)
    full_text: str = ""


# ── Page sizes in points (72 dpi) ────────────────────────────────

_PAGE_SIZES: dict[str, tuple[float, float]] = {
    "a3": (841.89, 1190.55),
    "a4": (595.28, 841.89),
    "a5": (419.53, 595.28),
    "letter": (612.0, 792.0),
    "legal": (612.0, 1008.0),
    "tabloid": (792.0, 1224.0),
}


# ── Internal helpers ──────────────────────────────────────────────


def _read(source: PdfInput, password: str | None = None) -> PdfReader:
    """Read a PDF from bytes, Path, or string path."""
    if isinstance(source, bytes):
        reader = PdfReader(io.BytesIO(source))
    elif isinstance(source, (Path, str)):
        reader = PdfReader(str(source))
    else:
        msg = f"Expected bytes, Path, or str, got {type(source).__name__}"
        raise TypeError(msg)
    if reader.is_encrypted:
        if password is None:
            msg = "PDF is encrypted — provide a password"
            raise ValueError(msg)
        reader.decrypt(password)
    return reader


def _write(writer: PdfWriter) -> bytes:
    """Serialize a PdfWriter to bytes."""
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


def _source_size(source: PdfInput) -> int:
    """Get the byte size of the source."""
    if isinstance(source, bytes):
        return len(source)
    return Path(source).stat().st_size


def _parse_pages(spec: str, total: int) -> list[int]:
    """Parse a 1-indexed page spec like ``'1,3,5-7'`` into 0-indexed indices.

    Supports:
    - Single pages: ``'1,3,5'``
    - Ranges: ``'2-5'``
    - Mixed: ``'1,3-5,8'``
    - ``'all'`` for every page
    """
    if spec.strip().lower() == "all":
        return list(range(total))
    indices: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = max(1, int(start_s))
            end = min(total, int(end_s))
            indices.extend(range(start - 1, end))
        else:
            page = int(part)
            if 1 <= page <= total:
                indices.append(page - 1)
    return indices


# ── Core operations ───────────────────────────────────────────────


def merge(*sources: PdfInput, password: str | None = None) -> bytes:
    """Merge multiple PDFs into one.

    Args:
        *sources: Two or more PDF inputs (bytes, Path, or str).
        password: Password for encrypted PDFs.

    Returns:
        Merged PDF as bytes.
    """
    if len(sources) < 2:
        msg = "merge() requires at least 2 PDF sources"
        raise ValueError(msg)
    writer = PdfWriter()
    for src in sources:
        reader = _read(src, password)
        for page in reader.pages:
            writer.add_page(page)
    return _write(writer)


def split(
    source: PdfInput,
    ranges: str = "",
    *,
    every: int = 0,
    password: str | None = None,
) -> list[bytes]:
    """Split a PDF into parts.

    Args:
        source: PDF input.
        ranges: Comma-separated ranges like ``'1-3,4-6'``.
            Each range produces one output PDF.
        every: Split every N pages (alternative to ranges).
        password: Password for encrypted PDFs.

    Returns:
        List of PDF byte strings, one per split.
    """
    reader = _read(source, password)
    total = len(reader.pages)

    if every > 0:
        groups: list[list[int]] = []
        for start in range(0, total, every):
            groups.append(list(range(start, min(start + every, total))))
    elif ranges:
        groups = []
        for rng in ranges.split(","):
            rng = rng.strip()
            if "-" in rng:
                s, e = rng.split("-", 1)
                start_idx = max(0, int(s) - 1)
                end_idx = min(total, int(e))
                groups.append(list(range(start_idx, end_idx)))
            else:
                page = int(rng)
                if 1 <= page <= total:
                    groups.append([page - 1])
        if not groups:
            msg = "No valid page ranges specified"
            raise ValueError(msg)
    else:
        # Default: split into individual pages
        groups = [[i] for i in range(total)]

    results: list[bytes] = []
    for group in groups:
        writer = PdfWriter()
        for idx in group:
            writer.add_page(reader.pages[idx])
        results.append(_write(writer))
    return results


def rotate(
    source: PdfInput,
    angle: int = 90,
    pages: str = "all",
    *,
    password: str | None = None,
) -> bytes:
    """Rotate pages in a PDF.

    Args:
        source: PDF input.
        angle: Rotation angle (90, 180, 270, or -90).
        pages: Page spec like ``'1,3,5-7'`` or ``'all'``.
        password: Password for encrypted PDFs.

    Returns:
        PDF with rotated pages as bytes.
    """
    if angle % 90 != 0:
        msg = f"Angle must be a multiple of 90, got {angle}"
        raise ValueError(msg)
    reader = _read(source, password)
    writer = PdfWriter()
    total = len(reader.pages)
    target_indices = set(_parse_pages(pages, total))
    for i, page in enumerate(reader.pages):
        if i in target_indices:
            page = page.rotate(angle)
        writer.add_page(page)
    return _write(writer)


def reorder(
    source: PdfInput,
    order: str,
    *,
    password: str | None = None,
) -> bytes:
    """Reorder pages in a PDF.

    Args:
        source: PDF input.
        order: Comma-separated 1-indexed page numbers in desired order,
            e.g. ``'3,1,2'``.
        password: Password for encrypted PDFs.

    Returns:
        Reordered PDF as bytes.
    """
    reader = _read(source, password)
    total = len(reader.pages)
    indices = _parse_pages(order, total)
    writer = PdfWriter()
    for idx in indices:
        writer.add_page(reader.pages[idx])
    return _write(writer)


def reverse(source: PdfInput, *, password: str | None = None) -> bytes:
    """Reverse the page order of a PDF.

    Args:
        source: PDF input.
        password: Password for encrypted PDFs.

    Returns:
        PDF with reversed page order as bytes.
    """
    reader = _read(source, password)
    writer = PdfWriter()
    for page in reversed(reader.pages):
        writer.add_page(page)
    return _write(writer)


def delete_pages(
    source: PdfInput,
    pages: str,
    *,
    password: str | None = None,
) -> bytes:
    """Delete specific pages from a PDF.

    Args:
        source: PDF input.
        pages: Page spec of pages to remove, e.g. ``'2,5-7'``.
        password: Password for encrypted PDFs.

    Returns:
        PDF with specified pages removed as bytes.
    """
    reader = _read(source, password)
    total = len(reader.pages)
    to_remove = set(_parse_pages(pages, total))
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        if i not in to_remove:
            writer.add_page(page)
    if len(writer.pages) == 0:
        msg = "Cannot delete all pages"
        raise ValueError(msg)
    return _write(writer)


def extract_pages(
    source: PdfInput,
    pages: str,
    *,
    password: str | None = None,
) -> bytes:
    """Extract specific pages from a PDF.

    Args:
        source: PDF input.
        pages: Page spec of pages to keep, e.g. ``'1,3-5'``.
        password: Password for encrypted PDFs.

    Returns:
        PDF containing only the specified pages as bytes.
    """
    reader = _read(source, password)
    total = len(reader.pages)
    indices = _parse_pages(pages, total)
    writer = PdfWriter()
    for idx in indices:
        writer.add_page(reader.pages[idx])
    return _write(writer)


def odd_even(
    source: PdfInput,
    mode: OddEvenMode = "odd",
    *,
    password: str | None = None,
) -> bytes:
    """Extract odd or even pages from a PDF.

    Args:
        source: PDF input.
        mode: ``'odd'`` for pages 1,3,5,... or ``'even'`` for 2,4,6,...
        password: Password for encrypted PDFs.

    Returns:
        PDF containing only the selected pages as bytes.
    """
    reader = _read(source, password)
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        page_num = i + 1  # 1-indexed
        if (mode == "odd" and page_num % 2 == 1) or (mode == "even" and page_num % 2 == 0):
            writer.add_page(page)
    if len(writer.pages) == 0:
        msg = f"No {mode} pages found"
        raise ValueError(msg)
    return _write(writer)


def duplicate_pages(
    source: PdfInput,
    pages: str = "all",
    copies: int = 2,
    *,
    password: str | None = None,
) -> bytes:
    """Duplicate specific pages in a PDF.

    Args:
        source: PDF input.
        pages: Page spec of pages to duplicate, e.g. ``'1,3'``.
        copies: Number of copies of each page (including original).
        password: Password for encrypted PDFs.

    Returns:
        PDF with duplicated pages as bytes.
    """
    if copies < 1:
        msg = f"copies must be >= 1, got {copies}"
        raise ValueError(msg)
    reader = _read(source, password)
    total = len(reader.pages)
    dup_set = set(_parse_pages(pages, total))
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        repeat = copies if i in dup_set else 1
        for _ in range(repeat):
            writer.add_page(page)
    return _write(writer)


def insert_blank(
    source: PdfInput,
    after: str = "",
    *,
    count: int = 1,
    width: float = 595.28,
    height: float = 841.89,
    password: str | None = None,
) -> bytes:
    """Insert blank pages into a PDF.

    Args:
        source: PDF input.
        after: Page spec for where to insert blanks, e.g. ``'2,5'``.
            Empty string inserts at the end.
        count: Number of blank pages to insert at each position.
        width: Page width in points (default A4).
        height: Page height in points (default A4).
        password: Password for encrypted PDFs.

    Returns:
        PDF with blank pages inserted as bytes.
    """
    reader = _read(source, password)
    total = len(reader.pages)
    insert_after = set(_parse_pages(after, total)) if after else set()
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        writer.add_page(page)
        if i in insert_after:
            for _ in range(count):
                writer.add_blank_page(width=width, height=height)
    if not after:
        # Insert at the end
        for _ in range(count):
            writer.add_blank_page(width=width, height=height)
    return _write(writer)


def compress(source: PdfInput, *, password: str | None = None) -> bytes:
    """Compress a PDF by removing redundancies and compressing streams.

    Args:
        source: PDF input.
        password: Password for encrypted PDFs.

    Returns:
        Compressed PDF as bytes.
    """
    reader = _read(source, password)
    writer = PdfWriter()
    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)
    if reader.metadata:
        writer.add_metadata(reader.metadata)
    return _write(writer)


def resize(
    source: PdfInput,
    size: PageSize = "a4",
    pages: str = "all",
    *,
    password: str | None = None,
) -> bytes:
    """Resize pages in a PDF to a standard page size.

    Scales content to fit the target size while preserving aspect ratio.

    Args:
        source: PDF input.
        size: Target page size.
        pages: Page spec of pages to resize, e.g. ``'1,3-5'`` or ``'all'``.
        password: Password for encrypted PDFs.

    Returns:
        Resized PDF as bytes.
    """
    target_w, target_h = _PAGE_SIZES[size]
    reader = _read(source, password)
    total = len(reader.pages)
    target_indices = set(_parse_pages(pages, total))
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        if i in target_indices:
            mb = page.mediabox
            cur_w = float(mb.width)
            cur_h = float(mb.height)
            if cur_w > 0 and cur_h > 0:
                sx = target_w / cur_w
                sy = target_h / cur_h
                scale = min(sx, sy)
                page.scale(float(scale), float(scale))
                page.mediabox = RectangleObject((0.0, 0.0, target_w, target_h))
        writer.add_page(page)
    return _write(writer)


def crop(
    source: PdfInput,
    left: float = 0,
    bottom: float = 0,
    right: float = 0,
    top: float = 0,
    pages: str = "all",
    *,
    password: str | None = None,
) -> bytes:
    """Crop pages by removing margins (in points, 72 dpi).

    Args:
        source: PDF input.
        left: Points to crop from the left edge.
        bottom: Points to crop from the bottom edge.
        right: Points to crop from the right edge.
        top: Points to crop from the top edge.
        pages: Page spec of pages to crop.
        password: Password for encrypted PDFs.

    Returns:
        Cropped PDF as bytes.
    """
    reader = _read(source, password)
    total = len(reader.pages)
    target_indices = set(_parse_pages(pages, total))
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        if i in target_indices:
            mb = page.mediabox
            page.mediabox = RectangleObject(
                (
                    float(mb.left) + left,
                    float(mb.bottom) + bottom,
                    float(mb.right) - right,
                    float(mb.top) - top,
                )
            )
        writer.add_page(page)
    return _write(writer)


def flatten(source: PdfInput, *, password: str | None = None) -> bytes:
    """Flatten PDF form fields, making them non-editable.

    Args:
        source: PDF input.
        password: Password for encrypted PDFs.

    Returns:
        Flattened PDF as bytes.
    """
    reader = _read(source, password)
    writer = PdfWriter()
    writer.append(reader)
    # Flatten all form fields by removing the AcroForm
    if "/AcroForm" in writer._root_object:
        del writer._root_object["/AcroForm"]
    return _write(writer)


# ── Text extraction ───────────────────────────────────────────────


def extract_text(
    source: PdfInput,
    pages: str = "all",
    *,
    password: str | None = None,
) -> ExtractedText:
    """Extract text from a PDF.

    Args:
        source: PDF input.
        pages: Page spec of pages to extract text from.
        password: Password for encrypted PDFs.

    Returns:
        Extracted text with per-page breakdown.
    """
    reader = _read(source, password)
    total = len(reader.pages)
    indices = _parse_pages(pages, total)
    page_results: list[PageTextResult] = []
    all_text: list[str] = []
    for idx in indices:
        text = reader.pages[idx].extract_text() or ""
        page_results.append(PageTextResult(page=idx + 1, text=text))
        all_text.append(text)
    return ExtractedText(pages=page_results, full_text="\n\n".join(all_text))


# ── Metadata ──────────────────────────────────────────────────────


def get_metadata(source: PdfInput, *, password: str | None = None) -> PdfMetadata:
    """Get PDF document metadata.

    Args:
        source: PDF input.
        password: Password for encrypted PDFs.

    Returns:
        PDF metadata.
    """
    reader = _read(source, password)
    meta = reader.metadata
    if meta is None:
        return PdfMetadata()
    return PdfMetadata(
        title=str(meta.get("/Title", "") or ""),
        author=str(meta.get("/Author", "") or ""),
        subject=str(meta.get("/Subject", "") or ""),
        keywords=str(meta.get("/Keywords", "") or ""),
        creator=str(meta.get("/Creator", "") or ""),
        producer=str(meta.get("/Producer", "") or ""),
    )


def set_metadata(
    source: PdfInput,
    *,
    title: str | None = None,
    author: str | None = None,
    subject: str | None = None,
    keywords: str | None = None,
    creator: str | None = None,
    producer: str | None = None,
    password: str | None = None,
) -> bytes:
    """Set PDF document metadata.

    Only non-None values are updated; existing values are preserved.

    Args:
        source: PDF input.
        title: Document title.
        author: Document author.
        subject: Document subject.
        keywords: Document keywords.
        creator: Creator application.
        producer: Producer application.
        password: Password for encrypted PDFs.

    Returns:
        PDF with updated metadata as bytes.
    """
    reader = _read(source, password)
    writer = PdfWriter()
    writer.append(reader)
    updates: dict[str, str] = {}
    if title is not None:
        updates["/Title"] = title
    if author is not None:
        updates["/Author"] = author
    if subject is not None:
        updates["/Subject"] = subject
    if keywords is not None:
        updates["/Keywords"] = keywords
    if creator is not None:
        updates["/Creator"] = creator
    if producer is not None:
        updates["/Producer"] = producer
    if updates:
        writer.add_metadata(updates)
    return _write(writer)


def strip_metadata(source: PdfInput, *, password: str | None = None) -> bytes:
    """Remove all metadata from a PDF.

    Args:
        source: PDF input.
        password: Password for encrypted PDFs.

    Returns:
        PDF with all metadata removed as bytes.
    """
    reader = _read(source, password)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    # Write without copying metadata
    return _write(writer)


# ── Info ──────────────────────────────────────────────────────────


def info(source: PdfInput, *, password: str | None = None) -> PdfInfo:
    """Get basic information about a PDF.

    Args:
        source: PDF input.
        password: Password for encrypted PDFs.

    Returns:
        PDF info including page count, encryption status, and metadata.
    """
    reader = _read(source, password)
    meta = reader.metadata
    return PdfInfo(
        pages=len(reader.pages),
        encrypted=reader.is_encrypted,
        title=str(meta.get("/Title", "") or "") if meta else "",
        author=str(meta.get("/Author", "") or "") if meta else "",
        subject=str(meta.get("/Subject", "") or "") if meta else "",
        creator=str(meta.get("/Creator", "") or "") if meta else "",
        producer=str(meta.get("/Producer", "") or "") if meta else "",
        size_bytes=_source_size(source),
    )


# ── Encryption ────────────────────────────────────────────────────


def encrypt(
    source: PdfInput,
    user_password: str,
    owner_password: str | None = None,
    *,
    password: str | None = None,
) -> bytes:
    """Encrypt a PDF with password protection.

    Args:
        source: PDF input.
        user_password: Password required to open the PDF.
        owner_password: Password for full access (defaults to user_password).
        password: Password for an already-encrypted source PDF.

    Returns:
        Encrypted PDF as bytes.
    """
    reader = _read(source, password)
    writer = PdfWriter()
    writer.append(reader)
    writer.encrypt(
        user_password=user_password,
        owner_password=owner_password or user_password,
    )
    return _write(writer)


def decrypt(
    source: PdfInput,
    password: str,
) -> bytes:
    """Decrypt a password-protected PDF.

    Args:
        source: PDF input (must be encrypted).
        password: Password to decrypt the PDF.

    Returns:
        Decrypted PDF as bytes.
    """
    reader = _read(source, password)
    writer = PdfWriter()
    writer.append(reader)
    return _write(writer)
