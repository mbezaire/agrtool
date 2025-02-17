from src.agrtool.cleanupfiles import clean_name, clean_files  # type: ignore
import pytest

def test_clean_name_mac():
    assert clean_name("MyFile-1.java") == "MyFile.java"
    assert clean_name("MyProgram2-21.java") == "MyProgram2.java"
    assert clean_name("MyFile-1-2.java") == "MyFile.java"
    assert clean_name("MyFile-1-2.py") == "MyFile.py"
    assert clean_name("MyFile-1.txt") == "MyFile.txt"

def test_clean_name_pc():
    assert clean_name("MyFile (1).java") == "MyFile.java"
    assert clean_name("MyProgram2 (2).java") == "MyProgram2.java"
    assert clean_name("MyFile (1) (2).java") == "MyFile.java"
    assert clean_name("MyFile (1) (2).txt") == "MyFile.txt"
    assert clean_name("MyFile (12).csv") == "MyFile.csv"
    assert clean_name("MyFile (12)-1.py") == "MyFile.py"
    assert clean_name("MyFile-1 (12).py") == "MyFile.py"


def test_clean_files(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    files = ["MyClass (1).java","data-1.txt","DontChange-1.xls", "MyOther.java", "MixedUp2-1 (2).java"]
    better = [d / "MyClass.java", d / "data.txt", d / "DontChange-1.xls", d / "MyOther.java", d / "MixedUp2.java"]
    better.sort()
    for file in files:
        p = d / file
        p.write_text("nothing", encoding="utf-8")
    
    clean_files(d)
    actual = list(d.iterdir())
    actual.sort()
    assert actual == better