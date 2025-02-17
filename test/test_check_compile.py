from src.agrtool.check_compile_error import check_unchecked # type: ignore
import pytest

def test_check_unchecked_unchecked(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    p = d / "compile_errortester.txt"
    p.write_text("unchecked ... unchecked\nunchecked\n", encoding="utf-8")
    check_unchecked(d)
    assert len(list(d.iterdir())) == 0

def test_check_unchecked_real(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    p = d / "compile_errortester.txt"
    p.write_text("\n\n\n", encoding="utf-8")
    check_unchecked(d)
    assert len(list(d.iterdir())) == 1


def test_check_unchecked_str(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    p = d / "compile_errortester.txt"
    p.write_text("\n\n\n", encoding="utf-8")
    check_unchecked(str(d))
    assert len(list(d.iterdir())) == 1