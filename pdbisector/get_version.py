import sys

from . import dependencies

def main(install_path):
    version = dependencies.install_pre_build_dependencies(install_path)
    print(version)

if __name__ == "__main__":
    install_path = sys.argv[1]
    main(install_path)
