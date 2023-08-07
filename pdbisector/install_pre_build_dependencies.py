import sys

from . import dependencies

dependencies.install_pre_build_dependencies(sys.argv[1])