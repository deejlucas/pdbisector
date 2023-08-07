import os
import pytest
import shutil

from pdbisector import parsing

def mock_extract_major_versions(vrsts):
        return [0, 1, 2, 2, 2]


def test_extract_vrsts():
    assert parsing.extract_vrsts([]) == []
    assert parsing.extract_vrsts(["v0.1.0.rst", "v1.2.0.rst", "v1.12.0.rst"]) == ["v0.1.0", "v1.2.0", "v1.12.0"]
    assert parsing.extract_vrsts(["v0.1.0.rst", "foo", "rst", "v1.12.0"]) == ["v0.1.0"]


def test_get_max_major(monkeypatch):
    monkeypatch.setattr(
        parsing,
        "extract_major_versions",
        mock_extract_major_versions
    )

    assert(parsing.get_max_major(["v0.2.0", "v1.1.0", "v2.0.0", "v2.2.0", "v2.12.0"]) == 2)


def test_get_minor(monkeypatch):
    monkeypatch.setattr(
        parsing,
        "extract_major_versions",
        mock_extract_major_versions
    )
    assert(parsing.get_max_minor(["v0.2.0", "v1.1.0", "v2.0.0", "v2.2.0", "v2.12.0"], 2) == 12)


def test_get_version_numbers(monkeypatch):
    def mocklistdir():
        return 
    monkeypatch.setattr(
        parsing.os,
        "listdir",
        mocklistdir,
    )


def test_extract_major_versions():
    mjr_vs = parsing.extract_major_versions(["v0.2.0", "v1.1.0", "v2.0.0", "v2.2.0", "v2.12.0"])
    assert mjr_vs == [0, 1, 2, 2, 2]


def test_get_version_number(monkeypatch):
    def mock_listdir(*args):
        return ["foo", "bar"]
    monkeypatch.setattr(
        parsing.os,
        "listdir",
        mock_listdir,
    )

    

    def mock_extract_vrsts(*args):
        return ["v0.2.0", "v1.1.0", "v2.0.0", "v2.2.0", "v2.12.0"]
    monkeypatch.setattr(
        parsing,
        "extract_vrsts",
        mock_extract_vrsts,
    )

    assert parsing.get_version_number("foo/bar") == "v2.12.0"


@pytest.mark.integtest
def test_get_version_from_install():
    if os.path.exists("../pdbtmp"):
        shutil.rmtree("../pdbtmp")
    os.chdir("..")
    os.mkdir("pdbtmp")
    os.chdir("pdbtmp")
    print(os.getcwd())
    os.system("git clone https://github.com/pandas-dev/pandas.git")
    os.chdir("pandas")
    os.system("git checkout v2.0.2")
    os.chdir("..")
    assert parsing.get_version_number(os.path.join(os.getcwd(), "pandas")) == "v2.0.0"
    shutil.rmtree("pandas")