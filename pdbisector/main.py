# %%
# need to handle cython and numpy specially when building 1.x
# need to use different pip install command when v > 2.0.3
# need relatively recent pip for v > 2.0.3
# TODO: Should I use a mamba environment?
import logging
import sys
import os
import subprocess
import shutil

from pdbisector import bisect, dependencies, utils

logging.basicConfig(level=logging.INFO)

term_old = sys.argv[1]
old = sys.argv[2] # where script exits 0
term_new = sys.argv[3]
new = sys.argv[4]  # where script exits 1
script_path = sys.argv[5]
reclone = bool(int(sys.argv[6]))

install_path = os.path.join(os.getcwd(), '../pandas-bisect-install')

tmp_dir = os.path.join(os.getcwd(), "..", "tmp")
if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)

# %%-f
pd_exists = os.path.exists(install_path)
if pd_exists and reclone:
    shutil.rmtree(install_path)
    pd_exists = False
if not pd_exists:
    utils.say_and_do(f"git clone https://github.com/pandas-dev/pandas.git {install_path}")

utils.say_and_do(f"cd {install_path} && git checkout {new}")
utils.say_and_do(f"cd {install_path} && git log -n 1")

dependencies.install_pre_build_dependencies(install_path)
utils.say_and_do("pip install python-dateutil pytz scipy ninja meson-python")  
utils.say_and_do(f"cd {install_path} && python3 setup.py build_ext -j 1") 
install_cmd = dependencies.get_editable_install_command(install_path)
utils.say_and_do(f"cd {install_path} && python3 -c 'import pandas; print(pandas.__version__)'")
utils.say_and_do(f"cd {install_path} && git bisect start --term-old {term_old} --term-new {term_new}")
utils.say_and_do(f"cd {install_path} && git bisect {term_old} {old}")
utils.say_and_do(f"cd {install_path} && git bisect {term_new} {new}")

bisect.make_shell_script(install_path, py_path=script_path, tmp_dir=tmp_dir)

os.chdir(install_path)
output = subprocess.check_output(args=["git", "bisect",  "run",  "bash", f"{tmp_dir}/bisect_iteration.sh"])


# %%

os.chdir(tmp_dir)
print(f"{output=}")
# %%
with open('output.txt', 'w') as fd:
    fd.write(str(output))




