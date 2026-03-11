# peasy-pdf

[![PyPI](https://img.shields.io/pypi/v/peasy-pdf)](https://pypi.org/project/peasy-pdf/)
[![Python](https://img.shields.io/pypi/pyversions/peasy-pdf)](https://pypi.org/project/peasy-pdf/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![pypdf](https://img.shields.io/badge/powered_by-pypdf-blue)](https://pypdf.readthedocs.io/)

Python PDF toolkit with 21 operations for everyday document tasks. Merge multiple PDFs into one, split documents by page ranges, compress file size, rotate pages, extract text, encrypt with passwords, reorder, crop, resize, flatten forms, and manage PDF metadata -- all through a clean, consistent API. Every function accepts `bytes`, `Path`, or `str` and returns `bytes`, making it easy to chain operations or integrate into web services.

Built for [PeasyPDF](https://peasypdf.com), a free online PDF toolkit with 25 browser-based tools for merging, splitting, compressing, converting, and securing PDF documents. The site processes files entirely client-side for privacy, while the Python package brings the same capabilities to scripts, pipelines, and AI assistants.

> **Try the interactive tools at [peasypdf.com](https://peasypdf.com)** -- [PDF Tools](https://peasypdf.com/), [PDF Glossary](https://peasypdf.com/glossary/), [PDF Guides](https://peasypdf.com/guides/).

<p align="center">
  <img src="demo.gif" alt="peasy-pdf demo — merge, split, compress PDFs in Python" width="800">
</p>

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [What You Can Do](#what-you-can-do)
  - [Page Manipulation](#page-manipulation)
  - [Document Operations](#document-operations)
  - [Text & Metadata](#text--metadata)
  - [Security](#security)
- [Page Specs](#page-specs)
- [Input Flexibility](#input-flexibility)
- [Command-Line Interface](#command-line-interface)
- [MCP Server (Claude, Cursor, Windsurf)](#mcp-server-claude-cursor-windsurf)
- [REST API Client](#rest-api-client)
- [API Reference](#api-reference)
- [Learn More About PDF](#learn-more-about-pdf)
- [Also Available](#also-available)
- [Peasy Developer Tools](#peasy-developer-tools)
- [License](#license)

## Install

```bash
pip install peasy-pdf                # Core engine (pypdf)
pip install "peasy-pdf[cli]"         # + Command-line interface (typer, rich)
pip install "peasy-pdf[mcp]"         # + MCP server for AI assistants
pip install "peasy-pdf[api]"         # + HTTP client for peasypdf.com API
pip install "peasy-pdf[all]"         # Everything
```

Or run instantly without installing:

```bash
uvx --from "peasy-pdf[cli]" peasy-pdf info document.pdf
```

## Quick Start

```python
from peasy_pdf import merge, split, rotate, compress, info, extract_text

# Merge two PDF reports into a single document
merged = merge("report_q1.pdf", "report_q2.pdf")

# Split a PDF into chunks of 5 pages each
chunks = split("handbook.pdf", every=5)

# Rotate all pages 90 degrees clockwise
rotated = rotate("landscape.pdf", angle=90)

# Compress a PDF to reduce file size for email
compressed = compress("large-scan.pdf")

# Get PDF info — page count, title, encryption status
pdf_info = info("document.pdf")
print(f"Pages: {pdf_info.pages}, Title: {pdf_info.title}")

# Extract text from specific pages for indexing
text = extract_text("contract.pdf", pages="1-3")
print(text.full_text)
```

## What You Can Do

### Page Manipulation

PDFs are structured as sequences of independent page objects, which makes page-level operations straightforward -- you can rearrange, duplicate, or remove pages without touching the content streams. peasy-pdf provides 10 page manipulation functions that cover the most common document assembly tasks, from combining multiple files into one to extracting specific pages for review.

| Function | Description | Key Parameters |
|----------|-------------|----------------|
| `merge()` | Combine multiple PDFs into a single document | `*sources` (2+ PDF inputs) |
| `split()` | Split by page ranges or every N pages | `ranges`, `every` |
| `rotate()` | Rotate pages by 90, 180, or 270 degrees | `angle`, `pages` |
| `reorder()` | Rearrange pages in any sequence | `order` (e.g. `"3,1,2"`) |
| `reverse()` | Reverse the entire page order | -- |
| `delete_pages()` | Remove specific pages from a document | `pages` |
| `extract_pages()` | Extract specific pages into a new PDF | `pages` |
| `odd_even()` | Filter odd or even pages (duplex printing) | `mode` (`"odd"` or `"even"`) |
| `duplicate_pages()` | Duplicate pages for handouts or forms | `pages`, `copies` |
| `insert_blank()` | Insert blank pages at specific positions | `after`, `count`, `width`, `height` |

```python
from peasy_pdf import merge, split, reorder, reverse, extract_pages, odd_even

# Merge a cover page with a report body
combined = merge("cover.pdf", "body.pdf")

# Split a 100-page book into 10-page chapters
chapters = split("book.pdf", every=10)

# Split by explicit ranges — pages 1-5 and pages 6-10 as separate files
parts = split("book.pdf", ranges="1-5,6-10")

# Reorder pages — put page 3 first, then 1, then 2
reordered = reorder("slides.pdf", order="3,1,2")

# Reverse a document for back-to-front printing
reversed_doc = reverse("handout.pdf")

# Extract only the executive summary (pages 2-4)
summary = extract_pages("annual_report.pdf", pages="2-4")

# Get odd pages for single-sided duplex printing
front_sides = odd_even("booklet.pdf", mode="odd")
```

Learn more: [PeasyPDF Tools](https://peasypdf.com/) · [PDF Glossary](https://peasypdf.com/glossary/)

### Document Operations

Beyond page-level assembly, PDF documents often need structural transformations. Compression reduces file size by re-encoding content streams with Flate (zlib) compression -- particularly effective on PDFs generated by scanners or design tools that leave streams uncompressed. Resizing scales page content to standard paper sizes (A3, A4, A5, Letter, Legal, Tabloid) while preserving aspect ratio. Cropping trims margins by adjusting the MediaBox coordinates, measured in PDF points (72 points per inch). Flattening bakes interactive form fields (AcroForm) into the page content, producing a static document that renders identically everywhere.

| Function | Description | Key Parameters |
|----------|-------------|----------------|
| `compress()` | Compress content streams with Flate encoding | -- |
| `resize()` | Scale pages to standard sizes (A4, Letter, etc.) | `size`, `pages` |
| `crop()` | Crop page margins by trimming edges | `left`, `bottom`, `right`, `top`, `pages` |
| `flatten()` | Flatten form fields into static content | -- |

Supported page sizes:

| Size | Dimensions (points) | Common Use |
|------|---------------------|------------|
| `a3` | 841.89 x 1190.55 | Posters, large-format printing |
| `a4` | 595.28 x 841.89 | International standard (210 x 297 mm) |
| `a5` | 419.53 x 595.28 | Booklets, notebooks |
| `letter` | 612 x 792 | US standard (8.5 x 11 in) |
| `legal` | 612 x 1008 | US legal documents (8.5 x 14 in) |
| `tabloid` | 792 x 1224 | US tabloid / ledger (11 x 17 in) |

```python
from peasy_pdf import compress, resize, crop, flatten

# Compress a scanned PDF — Flate-encodes uncompressed content streams
compressed = compress("scanned_invoice.pdf")

# Resize a Letter-size document to A4 for international distribution
resized = resize("us_report.pdf", size="a4")

# Resize only the first page to Letter
resized_first = resize("mixed.pdf", size="letter", pages="1")

# Crop 36 points (0.5 inch) from each edge to remove scan borders
cropped = crop("scan.pdf", left=36, right=36, top=36, bottom=36)

# Flatten a filled PDF form so fields become static text
flat = flatten("filled_form.pdf")
```

Learn more: [PeasyPDF](https://peasypdf.com/) · [PDF Guides](https://peasypdf.com/guides/) · [PDF Glossary](https://peasypdf.com/glossary/)

### Text & Metadata

Every PDF can carry two kinds of non-visual information: text content embedded in page streams, and document-level metadata. Text extraction reads the text operators from each page's content stream and assembles them into readable strings -- useful for full-text search indexing, content analysis, or feeding documents into LLM pipelines. The `extract_text()` function returns per-page results plus a combined full-text string.

PDF metadata follows the Info Dictionary standard defined in the PDF specification (ISO 32000). The six standard fields -- Title, Author, Subject, Keywords, Creator, and Producer -- appear in file properties dialogs and are indexed by search engines and document management systems. The XMP (Extensible Metadata Platform) standard extends this with richer schemas like Dublin Core, but the Info Dictionary remains the most widely used format. peasy-pdf provides `get_metadata()`, `set_metadata()`, and `strip_metadata()` for complete metadata lifecycle management.

| Function | Description | Returns |
|----------|-------------|---------|
| `extract_text()` | Extract text with per-page breakdown | `ExtractedText` |
| `info()` | Get page count, encryption status, metadata, file size | `PdfInfo` |
| `get_metadata()` | Read all 6 standard metadata fields | `PdfMetadata` |
| `set_metadata()` | Update specific metadata fields (preserves others) | `bytes` |
| `strip_metadata()` | Remove all metadata for privacy | `bytes` |

```python
from peasy_pdf import extract_text, info, get_metadata, set_metadata, strip_metadata

# Extract text from a contract — per-page results for clause analysis
text = extract_text("contract.pdf", pages="1-5")
for page in text.pages:
    print(f"Page {page.page}: {len(page.text)} chars")
print(text.full_text[:200])  # First 200 characters of combined text

# Get document info — page count, title, encryption status, file size
pdf_info = info("annual_report.pdf")
print(f"Pages: {pdf_info.pages}")
print(f"Encrypted: {pdf_info.encrypted}")
print(f"Size: {pdf_info.size_bytes:,} bytes")
print(f"Producer: {pdf_info.producer}")

# Read PDF metadata fields (Title, Author, Subject, Keywords, Creator, Producer)
meta = get_metadata("report.pdf")
print(f"Title: {meta.title}, Author: {meta.author}")

# Update document title and author for proper cataloging
updated = set_metadata("draft.pdf", title="Q4 Financial Report", author="Finance Team")

# Strip all metadata before sharing externally — removes PII from file properties
clean = strip_metadata("internal_memo.pdf")
```

Learn more: [PeasyPDF](https://peasypdf.com/) · [PDF Guides](https://peasypdf.com/guides/) · [PDF Glossary](https://peasypdf.com/glossary/)

### Security

PDF encryption uses the standard security handler defined in ISO 32000. The specification defines two passwords: the **user password** (required to open the document) and the **owner password** (grants full access including printing, copying, and editing). When you call `encrypt()`, pypdf applies 128-bit AES encryption by default. The `decrypt()` function removes encryption entirely, producing an unprotected PDF that anyone can open.

Permission flags in the PDF spec control what actions are allowed even after the document is opened: printing, content copying, form filling, annotation, and page extraction. While these flags are advisory (PDF viewers enforce them voluntarily), they are the standard mechanism for controlling document distribution in enterprise workflows.

| Function | Description | Key Parameters |
|----------|-------------|----------------|
| `encrypt()` | Add password protection with AES encryption | `user_password`, `owner_password` |
| `decrypt()` | Remove password protection | `password` |

```python
from peasy_pdf import encrypt, decrypt

# Encrypt a confidential report with a user password
protected = encrypt("financials.pdf", user_password="secret123")

# Encrypt with separate user and owner passwords
# User password to open, owner password for full access (print, copy, edit)
protected = encrypt(
    "board_minutes.pdf",
    user_password="view-only",
    owner_password="admin-access",
)

# Decrypt a password-protected PDF to remove restrictions
unlocked = decrypt("protected.pdf", password="secret123")
```

Learn more: [PeasyPDF](https://peasypdf.com/) · [PDF Guides](https://peasypdf.com/guides/)

## Page Specs

All page-aware functions use a 1-indexed page spec string. This syntax lets you target individual pages, ranges, or combinations without converting to zero-based indices yourself.

| Spec | Meaning | Example |
|------|---------|---------|
| `"1"` | Single page | Page 1 only |
| `"1,3,5"` | Multiple pages | Pages 1, 3, and 5 |
| `"2-5"` | Page range | Pages 2, 3, 4, and 5 |
| `"1,3-5,8"` | Mixed | Pages 1, 3, 4, 5, and 8 |
| `"all"` | Every page | All pages (default) |

```python
from peasy_pdf import rotate, extract_pages, delete_pages

# Rotate only page 1
rotated = rotate("doc.pdf", pages="1", angle=90)

# Extract pages 1, 3, and 5-7 into a new PDF
subset = extract_pages("doc.pdf", pages="1,3,5-7")

# Delete the last page (page 10 of a 10-page doc)
trimmed = delete_pages("doc.pdf", pages="10")

# All pages is the default for most functions
rotated_all = rotate("doc.pdf", angle=180)  # pages="all" implied
```

## Input Flexibility

Every function accepts `bytes`, `Path`, or `str` (file path). This makes peasy-pdf work seamlessly with file systems, HTTP responses, databases, and in-memory buffers.

```python
from pathlib import Path
from peasy_pdf import info

# String file path
result = info("document.pdf")

# pathlib.Path
result = info(Path("documents") / "report.pdf")

# Raw bytes from an HTTP response or database BLOB
pdf_bytes = response.content
result = info(pdf_bytes)

# Chain operations — output bytes feed directly into the next function
from peasy_pdf import compress, encrypt
compressed = compress("large.pdf")
protected = encrypt(compressed, user_password="secret")
```

All PDF-producing functions return `bytes`, so you can write results to disk, return them from a web endpoint, or pass them to another peasy-pdf function:

```python
from peasy_pdf import merge, compress
from pathlib import Path

# Merge, compress, and save in one pipeline
result = compress(merge("part1.pdf", "part2.pdf"))
Path("final.pdf").write_bytes(result)
```

## Command-Line Interface

```bash
pip install "peasy-pdf[cli]"
```

Every operation is available as a CLI subcommand:

```bash
# Merge multiple PDFs
peasy-pdf merge file1.pdf file2.pdf -o merged.pdf

# Split every 5 pages
peasy-pdf split doc.pdf --every 5 -o split_

# Split by ranges
peasy-pdf split doc.pdf --ranges "1-3,4-6" -o chapter_

# Rotate all pages 90 degrees
peasy-pdf rotate doc.pdf --angle 90 -o rotated.pdf

# Compress to reduce file size
peasy-pdf compress doc.pdf -o compressed.pdf

# Get document info
peasy-pdf info doc.pdf

# Extract text from specific pages
peasy-pdf text doc.pdf --pages 1-3

# Encrypt with a password
peasy-pdf encrypt doc.pdf --password secret -o encrypted.pdf

# Decrypt a protected PDF
peasy-pdf decrypt encrypted.pdf --password secret -o decrypted.pdf

# Update metadata
peasy-pdf metadata doc.pdf --title "New Title" --author "Author" -o updated.pdf
```

## MCP Server (Claude, Cursor, Windsurf)

peasy-pdf includes a Model Context Protocol server that exposes all 21 PDF operations to AI assistants.

```bash
pip install "peasy-pdf[mcp]"
```

**Claude Desktop** (`claude_desktop_config.json`):

```json
{
    "mcpServers": {
        "peasy-pdf": {
            "command": "uvx",
            "args": ["--from", "peasy-pdf[mcp]", "python", "-m", "peasy_pdf.mcp_server"]
        }
    }
}
```

**Cursor** (`.cursor/mcp.json`):

```json
{
    "mcpServers": {
        "peasy-pdf": {
            "command": "uvx",
            "args": ["--from", "peasy-pdf[mcp]", "python", "-m", "peasy_pdf.mcp_server"]
        }
    }
}
```

**Windsurf** (`~/.windsurf/mcp.json`):

```json
{
    "mcpServers": {
        "peasy-pdf": {
            "command": "uvx",
            "args": ["--from", "peasy-pdf[mcp]", "python", "-m", "peasy_pdf.mcp_server"]
        }
    }
}
```

## REST API Client

The API client connects to the [PeasyPDF developer API](https://peasypdf.com/developers/) for server-side processing and tool discovery.

```python
from peasy_pdf.api import PeasyPdfAPI

# Initialize the API client
api = PeasyPdfAPI()

# List all available PDF tools
tools = api.list_tools()
for tool in tools:
    print(f"{tool['name']}: {tool['description']}")

# Search the PDF glossary
results = api.search("compress")

# Get tool details
tool = api.get_tool("merge-pdf")
```

Full API documentation at [peasypdf.com/developers/](https://peasypdf.com/developers/).
OpenAPI 3.1.0 spec: [peasypdf.com/api/openapi.json](https://peasypdf.com/api/openapi.json).

## API Reference

### Core Functions

| Function | Parameters | Returns | Description |
|----------|-----------|---------|-------------|
| `merge(*sources, password)` | `*sources: PdfInput` | `bytes` | Merge 2+ PDFs into one document |
| `split(source, ranges, every, password)` | `source: PdfInput` | `list[bytes]` | Split by ranges or every N pages |
| `rotate(source, angle, pages, password)` | `angle: int`, `pages: str` | `bytes` | Rotate pages by 90/180/270 degrees |
| `reorder(source, order, password)` | `order: str` | `bytes` | Reorder pages (e.g. `"3,1,2"`) |
| `reverse(source, password)` | -- | `bytes` | Reverse the page order |
| `delete_pages(source, pages, password)` | `pages: str` | `bytes` | Remove specific pages |
| `extract_pages(source, pages, password)` | `pages: str` | `bytes` | Extract specific pages |
| `odd_even(source, mode, password)` | `mode: "odd" \| "even"` | `bytes` | Filter odd or even pages |
| `duplicate_pages(source, pages, copies, password)` | `pages: str`, `copies: int` | `bytes` | Duplicate pages N times |
| `insert_blank(source, after, count, width, height, password)` | `after: str`, `count: int` | `bytes` | Insert blank pages at positions |
| `compress(source, password)` | -- | `bytes` | Compress content streams |
| `resize(source, size, pages, password)` | `size: PageSize` | `bytes` | Resize to A3/A4/A5/Letter/Legal/Tabloid |
| `crop(source, left, bottom, right, top, pages, password)` | margins in points | `bytes` | Crop page margins |
| `flatten(source, password)` | -- | `bytes` | Flatten form fields (AcroForm removal) |
| `extract_text(source, pages, password)` | `pages: str` | `ExtractedText` | Extract text with per-page breakdown |
| `info(source, password)` | -- | `PdfInfo` | Page count, metadata, encryption, size |
| `get_metadata(source, password)` | -- | `PdfMetadata` | Read 6 standard metadata fields |
| `set_metadata(source, title, author, ..., password)` | keyword args | `bytes` | Update metadata (preserves others) |
| `strip_metadata(source, password)` | -- | `bytes` | Remove all metadata |
| `encrypt(source, user_password, owner_password, password)` | passwords | `bytes` | Add AES password protection |
| `decrypt(source, password)` | `password: str` | `bytes` | Remove password protection |

### Data Classes

| Class | Fields | Description |
|-------|--------|-------------|
| `PdfInfo` | `pages`, `encrypted`, `title`, `author`, `subject`, `creator`, `producer`, `size_bytes` | Document information |
| `PdfMetadata` | `title`, `author`, `subject`, `keywords`, `creator`, `producer` | Metadata fields (all `str`) |
| `ExtractedText` | `pages: list[PageTextResult]`, `full_text: str` | Extracted text with breakdown |
| `PageTextResult` | `page: int`, `text: str` | Text from a single page (1-indexed) |

### Type Aliases

| Type | Definition | Description |
|------|-----------|-------------|
| `PdfInput` | `bytes \| Path \| str` | Any PDF source |
| `PageSize` | `Literal["a3", "a4", "a5", "letter", "legal", "tabloid"]` | Standard paper sizes |
| `OddEvenMode` | `Literal["odd", "even"]` | Page filter mode |

## Learn More About PDF

- **Tools**: [PeasyPDF Tools](https://peasypdf.com/)
- **Guides**: [PDF Glossary](https://peasypdf.com/glossary/) · [PDF Guides](https://peasypdf.com/guides/)
- **API**: [Developer Docs](https://peasypdf.com/developers/) · [OpenAPI Spec](https://peasypdf.com/api/openapi.json)

## Also Available

| Platform | Install | Link |
|----------|---------|------|
| **npm** | `npm install peasy-pdf` | [npm](https://www.npmjs.com/package/peasy-pdf) |
| **MCP** | `uvx --from "peasy-pdf[mcp]" python -m peasy_pdf.mcp_server` | [Config](#mcp-server-claude-cursor-windsurf) |

## Peasy Developer Tools

Part of the [Peasy](https://peasytools.com) open-source developer tools ecosystem.

| Package | PyPI | npm | Description |
|---------|------|-----|-------------|
| **peasy-pdf** | [PyPI](https://pypi.org/project/peasy-pdf/) | [npm](https://www.npmjs.com/package/peasy-pdf) | PDF merge, split, compress, 21 operations -- [peasypdf.com](https://peasypdf.com) |
| peasy-image | [PyPI](https://pypi.org/project/peasy-image/) | [npm](https://www.npmjs.com/package/peasy-image) | Image resize, crop, convert, compress, 20 operations -- [peasyimage.com](https://peasyimage.com) |
| peasy-css | [PyPI](https://pypi.org/project/peasy-css/) | [npm](https://www.npmjs.com/package/peasy-css) | CSS gradients, shadows, flexbox, grid generators -- [peasycss.com](https://peasycss.com) |
| peasy-compress | [PyPI](https://pypi.org/project/peasy-compress/) | [npm](https://www.npmjs.com/package/peasy-compress) | ZIP, TAR, gzip, brotli archive operations -- [peasytools.com](https://peasytools.com) |
| peasy-document | [PyPI](https://pypi.org/project/peasy-document/) | [npm](https://www.npmjs.com/package/peasy-document) | Markdown, HTML, CSV, JSON conversions -- [peasytools.com](https://peasytools.com) |
| peasy-audio | [PyPI](https://pypi.org/project/peasy-audio/) | -- | Audio convert, trim, merge, normalize -- [peasyaudio.com](https://peasyaudio.com) |
| peasy-video | [PyPI](https://pypi.org/project/peasy-video/) | -- | Video trim, resize, GIF conversion -- [peasyvideo.com](https://peasyvideo.com) |
| peasy-convert | [PyPI](https://pypi.org/project/peasy-convert/) | -- | Unified CLI for all Peasy tools -- [peasytools.com](https://peasytools.com) |
| peasy-mcp | [PyPI](https://pypi.org/project/peasy-mcp/) | -- | Unified MCP server for AI assistants -- [peasytools.com](https://peasytools.com) |

## License

MIT
