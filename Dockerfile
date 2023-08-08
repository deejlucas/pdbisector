# We start from a base image with Python 3.7
FROM python:3.8-slim

# It's recommended to not run applications as root in Docker
RUN useradd -m dockerdan

# Set the working directory in the Docker image
WORKDIR /home/dockerdan

# Install build dependencies
RUN apt-get update && apt-get install -y git gcc python3-dev g++

# Install versioneer if needed
COPY pandas-dev/install_versioneer.py /home/dockerdan/

# Clone the pandas repository into the Docker image
RUN git clone https://github.com/pandas-dev/pandas.git pandas-dev

# Change the owner of the pandas directory to dan
RUN chown -R dockerdan:dockerdan /home/dockerdan/pandas-dev

# Switch to user dockerdan
USER dockerdan

# Change into the directory with the pandas source code
WORKDIR /home/dockerdan/pandas-dev

# Checkout latest 1.x.x
RUN git checkout v1.5.3

# Build and install pandas from source
RUN python /home/dockerdan/install_versioneer.py
RUN pip install cython==0.29.33 numpy pytz python-dateutil scipy
RUN python setup.py build_ext -j 1
RUN pip install -e . --no-build-isolation --no-use-pep517

# Set the default command for the image
CMD ["python"]
