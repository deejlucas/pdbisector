import os

from pdbisector import utils

def make_shell_script(install_path, py_path, tmp_dir):
    mod_path = os.path.dirname(utils.__file__)
    shell_template = f"""
    #!/bin/bash

    # Get version from Python script
    python3 {mod_path}/get_version.py {install_path}
    VERSION=$(cat version.txt)
    python3 {mod_path}/iteration_install.py {install_path}

    if [[ "$VERSION" < "v1.0.5" ]]; then
        python setup.py build_ext --inplace --force -j 1
    else
        python3 setup.py build_ext -j 1 
    fi

    # Check version and decide the install command
    if [[ "$VERSION" < "v2.0.3" ]]; then
        pip install -e . --no-build-isolation --no-use-pep517
    else
        python -m pip install -ve . --no-build-isolation --config-settings editable-verbose=true
    fi

    python3 {py_path}
    """

    sh_path = os.path.join(tmp_dir, "bisect_iteration.sh")

    with open(sh_path, "w") as fh:
        fh.write(shell_template)

    utils.say_and_do(f"chmod +x {sh_path}")
