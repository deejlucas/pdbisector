import sys

from pdbisector import dependencies, parsing

def main(install_path):
    dependencies.install_pre_build_dependencies(install_path)
    version = parsing.get_version_number(install_path)
    with open("version.txt", "wt") as fh:
        fh.write(version)

if __name__ == "__main__":
    install_path = sys.argv[1]
    main(install_path)
