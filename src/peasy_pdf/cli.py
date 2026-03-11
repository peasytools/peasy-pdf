"""peasy-pdf CLI — PDF manipulation from the command line.

Usage::

    peasy-pdf merge file1.pdf file2.pdf -o merged.pdf
    peasy-pdf split doc.pdf --every 5 -o split_
    peasy-pdf rotate doc.pdf --angle 90 -o rotated.pdf
    peasy-pdf compress doc.pdf -o compressed.pdf
    peasy-pdf info doc.pdf
    peasy-pdf text doc.pdf --pages 1-3
    peasy-pdf encrypt doc.pdf --password secret -o encrypted.pdf
    peasy-pdf decrypt encrypted.pdf --password secret -o decrypted.pdf
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from peasy_pdf import engine

app = typer.Typer(
    name="peasy-pdf",
    help="PDF toolkit — 21 tools from peasypdf.com",
    no_args_is_help=True,
)
console = Console()


def _write_output(data: bytes, output: Path) -> None:
    """Write PDF bytes to file."""
    output.write_bytes(data)
    size_kb = len(data) / 1024
    console.print(f"[green]✓[/green] Written {output} ({size_kb:.1f} KB)")


@app.command()
def merge(
    files: Annotated[list[Path], typer.Argument(help="PDF files to merge")],
    output: Annotated[Path, typer.Option("-o", "--output")] = Path("merged.pdf"),
    password: Annotated[str | None, typer.Option("--password", "-p")] = None,
) -> None:
    """Merge multiple PDFs into one."""
    result = engine.merge(*files, password=password)
    _write_output(result, output)


@app.command()
def split(
    file: Annotated[Path, typer.Argument(help="PDF file to split")],
    ranges: Annotated[str | None, typer.Option("--ranges", "-r")] = None,
    every: Annotated[int, typer.Option("--every", "-e")] = 0,
    output: Annotated[str, typer.Option("-o", "--output")] = "split_",
    password: Annotated[str | None, typer.Option("--password", "-p")] = None,
) -> None:
    """Split a PDF into parts."""
    parts = engine.split(file, ranges=ranges or "", every=every, password=password)
    for i, part in enumerate(parts, 1):
        out_path = Path(f"{output}{i:03d}.pdf")
        _write_output(part, out_path)
    console.print(f"[green]✓[/green] Split into {len(parts)} files")


@app.command()
def rotate(
    file: Annotated[Path, typer.Argument(help="PDF file")],
    angle: Annotated[int, typer.Option("--angle", "-a")] = 90,
    pages: Annotated[str, typer.Option("--pages")] = "all",
    output: Annotated[Path, typer.Option("-o", "--output")] = Path("rotated.pdf"),
    password: Annotated[str | None, typer.Option("--password", "-p")] = None,
) -> None:
    """Rotate pages in a PDF."""
    result = engine.rotate(file, angle=angle, pages=pages, password=password)
    _write_output(result, output)


@app.command()
def reorder(
    file: Annotated[Path, typer.Argument(help="PDF file")],
    order: Annotated[str, typer.Option("--order", help="Page order, e.g. '3,1,2'")],
    output: Annotated[Path, typer.Option("-o", "--output")] = Path("reordered.pdf"),
    password: Annotated[str | None, typer.Option("--password", "-p")] = None,
) -> None:
    """Reorder pages in a PDF."""
    result = engine.reorder(file, order=order, password=password)
    _write_output(result, output)


@app.command(name="reverse")
def reverse_cmd(
    file: Annotated[Path, typer.Argument(help="PDF file")],
    output: Annotated[Path, typer.Option("-o", "--output")] = Path("reversed.pdf"),
    password: Annotated[str | None, typer.Option("--password", "-p")] = None,
) -> None:
    """Reverse the page order of a PDF."""
    result = engine.reverse(file, password=password)
    _write_output(result, output)


@app.command()
def delete(
    file: Annotated[Path, typer.Argument(help="PDF file")],
    pages: Annotated[str, typer.Option("--pages", help="Pages to delete, e.g. '2,5-7'")],
    output: Annotated[Path, typer.Option("-o", "--output")] = Path("trimmed.pdf"),
    password: Annotated[str | None, typer.Option("--password", "-p")] = None,
) -> None:
    """Delete specific pages from a PDF."""
    result = engine.delete_pages(file, pages=pages, password=password)
    _write_output(result, output)


@app.command(name="extract")
def extract_cmd(
    file: Annotated[Path, typer.Argument(help="PDF file")],
    pages: Annotated[str, typer.Option("--pages", help="Pages to extract, e.g. '1,3-5'")],
    output: Annotated[Path, typer.Option("-o", "--output")] = Path("extracted.pdf"),
    password: Annotated[str | None, typer.Option("--password", "-p")] = None,
) -> None:
    """Extract specific pages from a PDF."""
    result = engine.extract_pages(file, pages=pages, password=password)
    _write_output(result, output)


@app.command()
def compress(
    file: Annotated[Path, typer.Argument(help="PDF file")],
    output: Annotated[Path, typer.Option("-o", "--output")] = Path("compressed.pdf"),
    password: Annotated[str | None, typer.Option("--password", "-p")] = None,
) -> None:
    """Compress a PDF to reduce file size."""
    original_size = file.stat().st_size
    result = engine.compress(file, password=password)
    _write_output(result, output)
    ratio = (1 - len(result) / original_size) * 100 if original_size > 0 else 0
    console.print(f"  Size reduction: {ratio:.1f}%")


@app.command()
def resize(
    file: Annotated[Path, typer.Argument(help="PDF file")],
    size: Annotated[str, typer.Option("--size", "-s")] = "a4",
    pages: Annotated[str, typer.Option("--pages")] = "all",
    output: Annotated[Path, typer.Option("-o", "--output")] = Path("resized.pdf"),
    password: Annotated[str | None, typer.Option("--password", "-p")] = None,
) -> None:
    """Resize pages to a standard size (a3, a4, a5, letter, legal, tabloid)."""
    result = engine.resize(file, size=size, pages=pages, password=password)  # type: ignore[arg-type]
    _write_output(result, output)


@app.command()
def crop(
    file: Annotated[Path, typer.Argument(help="PDF file")],
    left: Annotated[float, typer.Option("--left")] = 0,
    bottom: Annotated[float, typer.Option("--bottom")] = 0,
    right: Annotated[float, typer.Option("--right")] = 0,
    top: Annotated[float, typer.Option("--top")] = 0,
    pages: Annotated[str, typer.Option("--pages")] = "all",
    output: Annotated[Path, typer.Option("-o", "--output")] = Path("cropped.pdf"),
    password: Annotated[str | None, typer.Option("--password", "-p")] = None,
) -> None:
    """Crop pages by removing margins (in points)."""
    result = engine.crop(
        file, left=left, bottom=bottom, right=right, top=top, pages=pages, password=password
    )
    _write_output(result, output)


@app.command()
def flatten(
    file: Annotated[Path, typer.Argument(help="PDF file")],
    output: Annotated[Path, typer.Option("-o", "--output")] = Path("flattened.pdf"),
    password: Annotated[str | None, typer.Option("--password", "-p")] = None,
) -> None:
    """Flatten PDF form fields (make non-editable)."""
    result = engine.flatten(file, password=password)
    _write_output(result, output)


@app.command()
def text(
    file: Annotated[Path, typer.Argument(help="PDF file")],
    pages: Annotated[str, typer.Option("--pages")] = "all",
    password: Annotated[str | None, typer.Option("--password", "-p")] = None,
) -> None:
    """Extract text from a PDF."""
    result = engine.extract_text(file, pages=pages, password=password)
    for pr in result.pages:
        console.print(f"\n[bold]── Page {pr.page} ──[/bold]")
        console.print(pr.text)


@app.command()
def info(
    file: Annotated[Path, typer.Argument(help="PDF file")],
    password: Annotated[str | None, typer.Option("--password", "-p")] = None,
) -> None:
    """Show PDF information."""
    result = engine.info(file, password=password)
    table = Table(title=str(file))
    table.add_column("Property", style="cyan")
    table.add_column("Value")
    table.add_row("Pages", str(result.pages))
    table.add_row("Size", f"{result.size_bytes / 1024:.1f} KB")
    table.add_row("Encrypted", "Yes" if result.encrypted else "No")
    table.add_row("Title", result.title or "(none)")
    table.add_row("Author", result.author or "(none)")
    table.add_row("Subject", result.subject or "(none)")
    table.add_row("Creator", result.creator or "(none)")
    table.add_row("Producer", result.producer or "(none)")
    console.print(table)


@app.command()
def metadata(
    file: Annotated[Path, typer.Argument(help="PDF file")],
    title: Annotated[str | None, typer.Option("--title")] = None,
    author: Annotated[str | None, typer.Option("--author")] = None,
    subject: Annotated[str | None, typer.Option("--subject")] = None,
    keywords: Annotated[str | None, typer.Option("--keywords")] = None,
    strip: Annotated[bool, typer.Option("--strip", help="Remove all metadata")] = False,
    output: Annotated[Path, typer.Option("-o", "--output")] = Path("metadata.pdf"),
    password: Annotated[str | None, typer.Option("--password", "-p")] = None,
) -> None:
    """Get or set PDF metadata. Use --strip to remove all metadata."""
    if strip:
        result = engine.strip_metadata(file, password=password)
        _write_output(result, output)
    elif any(v is not None for v in [title, author, subject, keywords]):
        result = engine.set_metadata(
            file,
            title=title,
            author=author,
            subject=subject,
            keywords=keywords,
            password=password,
        )
        _write_output(result, output)
    else:
        meta = engine.get_metadata(file, password=password)
        table = Table(title="Metadata")
        table.add_column("Field", style="cyan")
        table.add_column("Value")
        table.add_row("Title", meta.title or "(none)")
        table.add_row("Author", meta.author or "(none)")
        table.add_row("Subject", meta.subject or "(none)")
        table.add_row("Keywords", meta.keywords or "(none)")
        table.add_row("Creator", meta.creator or "(none)")
        table.add_row("Producer", meta.producer or "(none)")
        console.print(table)


@app.command(name="encrypt")
def encrypt_cmd(
    file: Annotated[Path, typer.Argument(help="PDF file")],
    user_password: Annotated[str, typer.Option("--password", "-p", help="User password")],
    owner_password: Annotated[str | None, typer.Option("--owner")] = None,
    output: Annotated[Path, typer.Option("-o", "--output")] = Path("encrypted.pdf"),
    source_password: Annotated[str | None, typer.Option("--source-password")] = None,
) -> None:
    """Encrypt a PDF with password protection."""
    result = engine.encrypt(
        file,
        user_password=user_password,
        owner_password=owner_password,
        password=source_password,
    )
    _write_output(result, output)


@app.command(name="decrypt")
def decrypt_cmd(
    file: Annotated[Path, typer.Argument(help="PDF file")],
    password: Annotated[str, typer.Option("--password", "-p", help="PDF password")],
    output: Annotated[Path, typer.Option("-o", "--output")] = Path("decrypted.pdf"),
) -> None:
    """Decrypt a password-protected PDF."""
    result = engine.decrypt(file, password=password)
    _write_output(result, output)


if __name__ == "__main__":
    app()
