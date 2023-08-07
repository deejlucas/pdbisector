# %%
# need to handle cython and numpy specially when building 1.x
# need to use different pip install command when v > 2.0.3
# need relatively recent pip for v > 2.0.3
# TODO: Should I use a mamba environment?

import sys
import os
import subprocess
import logging
import shutil

from . import dependencies, parsing, utils

term_old = sys.argv[1]
old = sys.argv[2] # where script exits 0
term_new = sys.argv[3]
new = sys.argv[4]  # where script exits 1
test_path = sys.argv[5]
install_path = '../pandas-bisect-install'

# %%

if os.path.exists(install_path):
    shutil.rmtree(install_path)
_ = utils.say_and_do(f"git clone https://github.com/pandas-dev/pandas.git {install_path}")

# %%

# if version <=2.0.3, use 
# pip install -e . --no-build-isolation --no-use-pep517
BISECT = f"""
python3 install_pre_build_dependencies.py {install_path}
python3 setup.py build_ext -j 1
python -m pip install -ve . --no-build-isolation --config-settings editable-verbose=true
python3 t.py
"""

with open('pandas-dev/bisect.sh', 'w') as fd:
    fd.write(BISECT)
    
SETUP_BISECT = f"""
git bisect start
git bisect good {old}
git bisect bad {new}
"""

with open('pandas-dev/setup_bisect.sh', 'w') as fd:
    fd.write(SETUP_BISECT)
    
CHECKOUT_BAD = f"""
git checkout {new}
"""

with open('pandas-dev/checkout_bad.sh', 'w') as fd:
    fd.write(CHECKOUT_BAD)

CHECKOUT_GOOD = f"""
git checkout {old}
"""

with open('pandas-dev/checkout_good.sh', 'w') as fd:
    fd.write(CHECKOUT_GOOD)

# %%
CHECKOUT_BAD

# %%
utils.say_and_do("cd pandas-dev && bash checkout_bad.sh")

# %%
utils.say_and_do("cd pandas-dev && git log -n 1")

# %%
def select_single_version(rqt):
    rqt = rqt.split(",")[0]
    rqt = rqt.replace(">=", "==")
    return rqt


with open('pandas-dev/requirements-dev.txt') as fd:
    cython_rqt = None
    np_rqt = None
    for line in fd:
        if "cython" in line and "pytest" not in line:
            cython_rqt = select_single_version(line)
        elif "numpy" in line and "doc" not in line:
            np_rqt = select_single_version(line)
        if np_rqt is not None and cython_rqt is not None:
            break
utils.say_and_do(f"pip install {cython_rqt}")
utils.say_and_do(f"pip install {np_rqt}")
utils.say_and_do("pip install python-dateutil pytz scipy ninja meson-python")

# %%
_ = utils.say_and_do("cd pandas-dev && python3 setup.py build_ext -j 1")

# %%
_


# %%
utils.say_and_do("cd pandas-dev && pip install -ve . --no-build-isolation --config-settings editable-verbose=true")

# %%
utils.say_and_do("cd pandas-dev && python3 -c 'import pandas; print(pandas.__version__)'")

# %%
utils.say_and_do("cd pandas-dev && bash bisect.sh")

# %%
utils.say_and_do("cd pandas-dev && bash checkout_good.sh")

# %%
utils.say_and_do("cd pandas-dev && bash bisect.sh")

# %%
utils.say_and_do("cd pandas-dev && bash setup_bisect.sh")

# %%
os.chdir("pandas-dev")
output = subprocess.check_output(args=["git", "bisect",  "run",  "bash", "bisect.sh"])
os.chdir("..")
print(f"{output=}")

# # %%
# for line in output:
#     if 'is the first bad commit' in line:
#         print(line)
#         commit = line.split()[0]

# %%
# utils.say_and_do(f'git log --format=%B -n 1 {commit}')

# %%
with open('output.txt', 'w') as fd:
    fd.write(str(output))

# %%
print(output)

# # %%
# GOOD

# # %%
# BAD

# %%



