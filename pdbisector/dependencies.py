import os

from . import utils

has_versioneer = False

def select_single_version(rqt):
    rqt = rqt.split(",")[0]
    rqt = rqt.replace(">=", "==")
    return rqt

def install_pre_build_dependencies(install_path):
    """
    The appropriate versions of Cython, Numpy, and Versioneer must be in place
    before building, which must be done before the editable install, which is a
    requirement for installing some of the dev requirements.
    """
    with open(os.path.join((install_path, 'requirements-dev.txt'))) as fd:
        cython_rqt = None
        np_rqt = None
        for line in fd:
            if 'versioneer' in line:
                has_versioneer = True
                versioneer_rqt = line
            elif "cython" in line and "pytest" not in line:
                cython_rqt = select_single_version(line)
            elif "numpy" in line and "doc" not in line:
                np_rqt = select_single_version(line)
    print('has versioneer: ', has_versioneer)
    if has_versioneer:
        utils.say_and_do('pip install versioneer[toml]')
    else:
        utils.say_and_do('pip uninstall versioneer -y')
    utils.say_and_do(f"pip install {cython_rqt}")
    utils.say_and_do(f"pip install {np_rqt}")