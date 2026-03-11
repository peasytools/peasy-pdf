"""Tests for peasy_pdf.engine — 21 PDF operations."""

from __future__ import annotations

import io
from pathlib import Path

import pypdf
import pytest
from pypdf import PdfReader, PdfWriter

from peasy_pdf import engine

# ── Fixtures ──────────────────────────────────────────────────────


def _make_pdf(pages: int = 3, text: str = "Hello Page") -> bytes:
    """Create a simple test PDF with N pages."""
    writer = PdfWriter()
    for _i in range(pages):
        writer.add_blank_page(width=595.28, height=841.89)
    if text:
        writer.add_metadata({"/Title": "Test PDF", "/Author": "Pytest"})
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


def _page_count(data: bytes) -> int:
    """Count pages in PDF bytes."""
    return len(PdfReader(io.BytesIO(data)).pages)


@pytest.fixture
def sample_pdf() -> bytes:
    return _make_pdf(3)


@pytest.fixture
def five_page_pdf() -> bytes:
    return _make_pdf(5)


@pytest.fixture
def tmp_pdf(tmp_path: Path) -> Path:
    p = tmp_path / "test.pdf"
    p.write_bytes(_make_pdf(3))
    return p


# ── merge ─────────────────────────────────────────────────────────


class TestMerge:
    def test_merge_two(self, sample_pdf: bytes) -> None:
        result = engine.merge(sample_pdf, sample_pdf)
        assert _page_count(result) == 6

    def test_merge_three(self, sample_pdf: bytes) -> None:
        result = engine.merge(sample_pdf, sample_pdf, sample_pdf)
        assert _page_count(result) == 9

    def test_merge_path(self, tmp_pdf: Path) -> None:
        result = engine.merge(tmp_pdf, tmp_pdf)
        assert _page_count(result) == 6

    def test_merge_requires_two(self, sample_pdf: bytes) -> None:
        with pytest.raises(ValueError, match="at least 2"):
            engine.merge(sample_pdf)


# ── split ─────────────────────────────────────────────────────────


class TestSplit:
    def test_split_default_individual(self, sample_pdf: bytes) -> None:
        parts = engine.split(sample_pdf)
        assert len(parts) == 3
        assert all(_page_count(p) == 1 for p in parts)

    def test_split_every(self, five_page_pdf: bytes) -> None:
        parts = engine.split(five_page_pdf, every=2)
        assert len(parts) == 3  # 2+2+1
        assert _page_count(parts[0]) == 2
        assert _page_count(parts[2]) == 1

    def test_split_ranges(self, five_page_pdf: bytes) -> None:
        parts = engine.split(five_page_pdf, ranges="1-2,3-5")
        assert len(parts) == 2
        assert _page_count(parts[0]) == 2
        assert _page_count(parts[1]) == 3


# ── rotate ────────────────────────────────────────────────────────


class TestRotate:
    def test_rotate_all(self, sample_pdf: bytes) -> None:
        result = engine.rotate(sample_pdf, angle=90)
        assert _page_count(result) == 3

    def test_rotate_specific_pages(self, sample_pdf: bytes) -> None:
        result = engine.rotate(sample_pdf, angle=180, pages="1,3")
        assert _page_count(result) == 3

    def test_rotate_invalid_angle(self, sample_pdf: bytes) -> None:
        with pytest.raises(ValueError, match="multiple of 90"):
            engine.rotate(sample_pdf, angle=45)


# ── reorder ───────────────────────────────────────────────────────


class TestReorder:
    def test_reorder(self, sample_pdf: bytes) -> None:
        result = engine.reorder(sample_pdf, order="3,1,2")
        assert _page_count(result) == 3

    def test_reorder_duplicate(self, sample_pdf: bytes) -> None:
        result = engine.reorder(sample_pdf, order="1,1,1")
        assert _page_count(result) == 3


# ── reverse ───────────────────────────────────────────────────────


class TestReverse:
    def test_reverse(self, sample_pdf: bytes) -> None:
        result = engine.reverse(sample_pdf)
        assert _page_count(result) == 3


# ── delete_pages ──────────────────────────────────────────────────


class TestDeletePages:
    def test_delete_single(self, sample_pdf: bytes) -> None:
        result = engine.delete_pages(sample_pdf, pages="2")
        assert _page_count(result) == 2

    def test_delete_range(self, five_page_pdf: bytes) -> None:
        result = engine.delete_pages(five_page_pdf, pages="2-4")
        assert _page_count(result) == 2

    def test_delete_all_raises(self, sample_pdf: bytes) -> None:
        with pytest.raises(ValueError, match="Cannot delete all"):
            engine.delete_pages(sample_pdf, pages="1-3")


# ── extract_pages ─────────────────────────────────────────────────


class TestExtractPages:
    def test_extract_single(self, sample_pdf: bytes) -> None:
        result = engine.extract_pages(sample_pdf, pages="2")
        assert _page_count(result) == 1

    def test_extract_range(self, five_page_pdf: bytes) -> None:
        result = engine.extract_pages(five_page_pdf, pages="2-4")
        assert _page_count(result) == 3


# ── odd_even ──────────────────────────────────────────────────────


class TestOddEven:
    def test_odd(self, five_page_pdf: bytes) -> None:
        result = engine.odd_even(five_page_pdf, mode="odd")
        assert _page_count(result) == 3  # pages 1,3,5

    def test_even(self, five_page_pdf: bytes) -> None:
        result = engine.odd_even(five_page_pdf, mode="even")
        assert _page_count(result) == 2  # pages 2,4


# ── duplicate_pages ───────────────────────────────────────────────


class TestDuplicatePages:
    def test_duplicate_all(self, sample_pdf: bytes) -> None:
        result = engine.duplicate_pages(sample_pdf, copies=2)
        assert _page_count(result) == 6  # 3 pages x 2 copies

    def test_duplicate_specific(self, sample_pdf: bytes) -> None:
        result = engine.duplicate_pages(sample_pdf, pages="1", copies=3)
        assert _page_count(result) == 5  # page1x3 + page2x1 + page3x1

    def test_duplicate_invalid_copies(self, sample_pdf: bytes) -> None:
        with pytest.raises(ValueError, match="copies must be >= 1"):
            engine.duplicate_pages(sample_pdf, copies=0)


# ── insert_blank ──────────────────────────────────────────────────


class TestInsertBlank:
    def test_insert_at_end(self, sample_pdf: bytes) -> None:
        result = engine.insert_blank(sample_pdf)
        assert _page_count(result) == 4

    def test_insert_after_page(self, sample_pdf: bytes) -> None:
        result = engine.insert_blank(sample_pdf, after="1")
        assert _page_count(result) == 4

    def test_insert_multiple(self, sample_pdf: bytes) -> None:
        result = engine.insert_blank(sample_pdf, after="1,2", count=2)
        assert _page_count(result) == 7  # 3 + 2x2


# ── compress ──────────────────────────────────────────────────────


class TestCompress:
    def test_compress(self, sample_pdf: bytes) -> None:
        result = engine.compress(sample_pdf)
        assert isinstance(result, bytes)
        assert _page_count(result) == 3


# ── resize ────────────────────────────────────────────────────────


class TestResize:
    def test_resize_a4(self, sample_pdf: bytes) -> None:
        result = engine.resize(sample_pdf, size="a4")
        assert _page_count(result) == 3

    def test_resize_letter(self, sample_pdf: bytes) -> None:
        result = engine.resize(sample_pdf, size="letter")
        assert _page_count(result) == 3

    def test_resize_specific_pages(self, sample_pdf: bytes) -> None:
        result = engine.resize(sample_pdf, size="a5", pages="1")
        assert _page_count(result) == 3


# ── crop ──────────────────────────────────────────────────────────


class TestCrop:
    def test_crop(self, sample_pdf: bytes) -> None:
        result = engine.crop(sample_pdf, left=50, top=50, right=50, bottom=50)
        assert _page_count(result) == 3

    def test_crop_specific_pages(self, sample_pdf: bytes) -> None:
        result = engine.crop(sample_pdf, left=10, pages="1")
        assert _page_count(result) == 3


# ── flatten ───────────────────────────────────────────────────────


class TestFlatten:
    def test_flatten(self, sample_pdf: bytes) -> None:
        result = engine.flatten(sample_pdf)
        assert _page_count(result) == 3


# ── extract_text ──────────────────────────────────────────────────


class TestExtractText:
    def test_extract_text(self, sample_pdf: bytes) -> None:
        result = engine.extract_text(sample_pdf)
        assert len(result.pages) == 3
        assert isinstance(result.full_text, str)

    def test_extract_text_specific_pages(self, sample_pdf: bytes) -> None:
        result = engine.extract_text(sample_pdf, pages="1")
        assert len(result.pages) == 1
        assert result.pages[0].page == 1


# ── metadata ──────────────────────────────────────────────────────


class TestMetadata:
    def test_get_metadata(self, sample_pdf: bytes) -> None:
        meta = engine.get_metadata(sample_pdf)
        assert meta.title == "Test PDF"
        assert meta.author == "Pytest"

    def test_set_metadata(self, sample_pdf: bytes) -> None:
        result = engine.set_metadata(sample_pdf, title="New Title", author="New Author")
        meta = engine.get_metadata(result)
        assert meta.title == "New Title"
        assert meta.author == "New Author"

    def test_strip_metadata(self, sample_pdf: bytes) -> None:
        result = engine.strip_metadata(sample_pdf)
        meta = engine.get_metadata(result)
        assert meta.title == ""
        assert meta.author == ""


# ── info ──────────────────────────────────────────────────────────


class TestInfo:
    def test_info(self, sample_pdf: bytes) -> None:
        result = engine.info(sample_pdf)
        assert result.pages == 3
        assert result.encrypted is False
        assert result.title == "Test PDF"
        assert result.size_bytes > 0

    def test_info_path(self, tmp_pdf: Path) -> None:
        result = engine.info(tmp_pdf)
        assert result.pages == 3


# ── encrypt / decrypt ─────────────────────────────────────────────


class TestEncryptDecrypt:
    def test_encrypt(self, sample_pdf: bytes) -> None:
        encrypted = engine.encrypt(sample_pdf, user_password="secret")
        reader = PdfReader(io.BytesIO(encrypted))
        assert reader.is_encrypted

    def test_encrypt_decrypt_roundtrip(self, sample_pdf: bytes) -> None:
        encrypted = engine.encrypt(sample_pdf, user_password="secret")
        decrypted = engine.decrypt(encrypted, password="secret")
        assert _page_count(decrypted) == 3

    def test_decrypt_wrong_password(self, sample_pdf: bytes) -> None:
        encrypted = engine.encrypt(sample_pdf, user_password="secret")
        with pytest.raises(pypdf.errors.PdfReadError):
            engine.decrypt(encrypted, password="wrong")


# ── _parse_pages ──────────────────────────────────────────────────


class TestParsePages:
    def test_single(self) -> None:
        assert engine._parse_pages("2", 5) == [1]  # 0-indexed

    def test_range(self) -> None:
        assert engine._parse_pages("2-4", 5) == [1, 2, 3]

    def test_mixed(self) -> None:
        assert engine._parse_pages("1,3-5", 5) == [0, 2, 3, 4]

    def test_all(self) -> None:
        assert engine._parse_pages("all", 5) == [0, 1, 2, 3, 4]

    def test_out_of_range(self) -> None:
        assert engine._parse_pages("10", 5) == []

    def test_clamp_range(self) -> None:
        assert engine._parse_pages("3-100", 5) == [2, 3, 4]


# ── Input types ───────────────────────────────────────────────────


class TestInputTypes:
    def test_bytes_input(self, sample_pdf: bytes) -> None:
        result = engine.info(sample_pdf)
        assert result.pages == 3

    def test_path_input(self, tmp_pdf: Path) -> None:
        result = engine.info(tmp_pdf)
        assert result.pages == 3

    def test_str_input(self, tmp_pdf: Path) -> None:
        result = engine.info(str(tmp_pdf))
        assert result.pages == 3

    def test_invalid_input(self) -> None:
        with pytest.raises(TypeError, match="Expected bytes"):
            engine.info(123)  # type: ignore[arg-type]
