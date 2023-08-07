from pdbisector import dependencies

def test_get_editable_install_command(monkeypatch):
    def mock_get_version_number(install_path):
        return install_path
    
    monkeypatch.setattr(
        dependencies.parsing,
        "get_version_number",
        mock_get_version_number,
    )

    assert dependencies.get_editable_install_command("v1.0.0") == "pip install -e . --no-build-isolation --no-use-pep517"
    assert dependencies.get_editable_install_command("v2.0.3") == "python -m pip install -ve . --no-build-isolation --config-settings editable-verbose=true"