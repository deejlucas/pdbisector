import os
import pytest
import shutil

from pdbisector import parsing

test_vs = ["v0.2.0", "v1.1.0", "v2.0.0", "v2.2.0", "v2.12.0", "v2.12.2", "v2.12.13"]

def mock_extract_major_versions(vrsts):
        return [0, 1, 2, 2, 2, 2, 2]


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

    assert(parsing.get_max_major(test_vs) == 2)


def test_get_minor(monkeypatch):
    monkeypatch.setattr(
        parsing,
        "extract_major_versions",
        mock_extract_major_versions
    )
    assert(parsing.get_max_minor(test_vs, 2) == 12)


def test_extract_major_versions():
    mjr_vs = parsing.extract_major_versions(test_vs)
    assert mjr_vs == [0, 1, 2, 2, 2, 2, 2]


def test_get_max_patch(monkeypatch):
    monkeypatch.setattr(
        parsing,
        "extract_major_versions",
        mock_extract_major_versions
    )
    max_patch = parsing.get_max_patch(
        test_vs,
        max_major=2,
        max_minor=12,
        )
    assert(max_patch == 13)



def test_get_version_numbers(monkeypatch):
    def mocklistdir():
        return 
    monkeypatch.setattr(
        parsing.os,
        "listdir",
        mocklistdir,
    )




def test_get_version_number(monkeypatch):
    def mock_listdir(*args):
        return ["foo", "bar"]
    monkeypatch.setattr(
        parsing.os,
        "listdir",
        mock_listdir,
    )

    def mock_extract_vrsts(*args):
        return test_vs
    monkeypatch.setattr(
        parsing,
        "extract_vrsts",
        mock_extract_vrsts,
    )

    def mock_get_max_major(vrsts):
        return 2
    def mock_get_max_minor(vrsts, max_major):
        return 12
    def mock_get_max_patch(vrsts, max_major, max_minor):
        return 13
    
    mocks = {
        "get_max_major": mock_get_max_major, 
        "get_max_minor": mock_get_max_minor, 
        "get_max_patch": mock_get_max_patch,
    }
    for k, v in mocks.items():
        monkeypatch.setattr(parsing, k, v)

    assert parsing.get_version_number("foo/bar") == "v2.12.13"


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
    assert parsing.get_version_number(os.path.join(os.getcwd(), "pandas")) == "v2.0.2"
    shutil.rmtree("pandas")