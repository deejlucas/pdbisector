from setuptools import setup, find_packages

setup(
    name='pdbisector',  # Name of your package
    version='0.0.1',  # Version number
    packages=find_packages(),  # List of module paths
    description='to ease regression testing of pandas',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Dan Lucas',  # Author name
    author_email='dan.lucas.21347@gmail.com',  # Author email
    # TODO: Link to the repository or package website
    install_requires=[  # List of dependencies
    ],
    classifiers=[  # Optional metadata about your package
        'Programming Language :: Python :: 3.10',
    ],
)