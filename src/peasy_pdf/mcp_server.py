"""peasy-pdf MCP server — Expose PDF tools to AI assistants.

Run::

    uvx --from "peasy-pdf[mcp]" python -m peasy_pdf.mcp_server

Configure in Claude Desktop / Cursor / Windsurf::

    {
        "mcpServers": {
            "peasy-pdf": {
                "command": "uvx",
                "args": ["--from", "peasy-pdf[mcp]", "python", "-m", "peasy_pdf.mcp_server"]
            }
        }
    }
"""

from __future__ import annotations

import base64

from mcp.server.fastmcp import FastMCP

from peasy_pdf import engine

mcp = FastMCP("peasy-pdf")


def _b64_to_bytes(b64: str) -> bytes:
    """Decode base64-encoded PDF data."""
    return base64.b64decode(b64)


def _bytes_to_b64(data: bytes) -> str:
    """Encode PDF bytes to base64."""
    return base64.b64encode(data).decode("ascii")


@mcp.tool()
def pdf_merge(files_b64: list[str]) -> str:
    """Merge multiple PDFs into one.

    files_b64: List of base64-encoded PDF files.
    Returns: Base64-encoded merged PDF.
    """
    sources = [_b64_to_bytes(f) for f in files_b64]
    result = engine.merge(*sources)
    return _bytes_to_b64(result)


@mcp.tool()
def pdf_split(file_b64: str, ranges: str = "", every: int = 0) -> list[str]:
    """Split a PDF into parts.

    file_b64: Base64-encoded PDF.
    ranges: Comma-separated ranges like '1-3,4-6'.
    every: Split every N pages.
    Returns: List of base64-encoded PDF parts.
    """
    source = _b64_to_bytes(file_b64)
    parts = engine.split(source, ranges=ranges, every=every)
    return [_bytes_to_b64(p) for p in parts]


@mcp.tool()
def pdf_rotate(file_b64: str, angle: int = 90, pages: str = "all") -> str:
    """Rotate pages in a PDF.

    file_b64: Base64-encoded PDF.
    angle: Rotation angle (90, 180, 270).
    pages: Page spec like '1,3,5-7' or 'all'.
    Returns: Base64-encoded rotated PDF.
    """
    result = engine.rotate(_b64_to_bytes(file_b64), angle=angle, pages=pages)
    return _bytes_to_b64(result)


@mcp.tool()
def pdf_compress(file_b64: str) -> str:
    """Compress a PDF to reduce file size.

    file_b64: Base64-encoded PDF.
    Returns: Base64-encoded compressed PDF.
    """
    result = engine.compress(_b64_to_bytes(file_b64))
    return _bytes_to_b64(result)


@mcp.tool()
def pdf_extract_text(file_b64: str, pages: str = "all") -> str:
    """Extract text from a PDF.

    file_b64: Base64-encoded PDF.
    pages: Page spec like '1-3' or 'all'.
    Returns: Extracted text.
    """
    result = engine.extract_text(_b64_to_bytes(file_b64), pages=pages)
    return result.full_text


@mcp.tool()
def pdf_info(file_b64: str) -> dict[str, object]:
    """Get PDF information (page count, metadata, size).

    file_b64: Base64-encoded PDF.
    Returns: Dict with pages, encrypted, title, author, etc.
    """
    result = engine.info(_b64_to_bytes(file_b64))
    return {
        "pages": result.pages,
        "encrypted": result.encrypted,
        "title": result.title,
        "author": result.author,
        "subject": result.subject,
        "size_bytes": result.size_bytes,
    }


@mcp.tool()
def pdf_metadata(
    file_b64: str,
    title: str | None = None,
    author: str | None = None,
    subject: str | None = None,
    keywords: str | None = None,
) -> str:
    """Set PDF metadata. Returns base64-encoded PDF with updated metadata.

    file_b64: Base64-encoded PDF.
    title, author, subject, keywords: Metadata fields to set.
    """
    result = engine.set_metadata(
        _b64_to_bytes(file_b64),
        title=title,
        author=author,
        subject=subject,
        keywords=keywords,
    )
    return _bytes_to_b64(result)


@mcp.tool()
def pdf_encrypt(file_b64: str, password: str) -> str:
    """Encrypt a PDF with password protection.

    file_b64: Base64-encoded PDF.
    password: Password to set.
    Returns: Base64-encoded encrypted PDF.
    """
    result = engine.encrypt(_b64_to_bytes(file_b64), user_password=password)
    return _bytes_to_b64(result)


@mcp.tool()
def pdf_decrypt(file_b64: str, password: str) -> str:
    """Decrypt a password-protected PDF.

    file_b64: Base64-encoded PDF.
    password: Password to decrypt.
    Returns: Base64-encoded decrypted PDF.
    """
    result = engine.decrypt(_b64_to_bytes(file_b64), password=password)
    return _bytes_to_b64(result)


@mcp.tool()
def pdf_delete_pages(file_b64: str, pages: str) -> str:
    """Delete specific pages from a PDF.

    file_b64: Base64-encoded PDF.
    pages: Page spec of pages to remove, e.g. '2,5-7'.
    Returns: Base64-encoded PDF with pages removed.
    """
    result = engine.delete_pages(_b64_to_bytes(file_b64), pages=pages)
    return _bytes_to_b64(result)


@mcp.tool()
def pdf_extract_pages(file_b64: str, pages: str) -> str:
    """Extract specific pages from a PDF.

    file_b64: Base64-encoded PDF.
    pages: Page spec of pages to keep, e.g. '1,3-5'.
    Returns: Base64-encoded PDF with only specified pages.
    """
    result = engine.extract_pages(_b64_to_bytes(file_b64), pages=pages)
    return _bytes_to_b64(result)


@mcp.tool()
def pdf_reverse(file_b64: str) -> str:
    """Reverse the page order of a PDF.

    file_b64: Base64-encoded PDF.
    Returns: Base64-encoded reversed PDF.
    """
    result = engine.reverse(_b64_to_bytes(file_b64))
    return _bytes_to_b64(result)


if __name__ == "__main__":
    mcp.run()
