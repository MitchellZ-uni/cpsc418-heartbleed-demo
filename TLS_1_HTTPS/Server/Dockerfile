# Use an official Debian Jessie base image
FROM debian:jessie

# Set environment variables
ENV PYTHON_VERSION=3.4.10
ENV OPENSSL_VERSION=1.0.1f

# Update repository sources to point to the Debian Archive
RUN sed -i '/jessie-updates/d' /etc/apt/sources.list && \
    sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i 's|security.debian.org/debian-security|archive.debian.org/debian-security|g' /etc/apt/sources.list && \
    echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until

# Update repositories and install dependencies
RUN apt-get update && apt-get install -y --allow-unauthenticated \
    wget \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Download OpenSSL 1.0.1f locally and copy it to docker 
# since OpenSSL moved it to GitHub, which would cause errors while downloading it
COPY openssl-1.0.1f.tar.gz /

# Install OpenSSL 1.0.1f
RUN tar -xvzf openssl-${OPENSSL_VERSION}.tar.gz && \
    cd openssl-${OPENSSL_VERSION} && \
    ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib && \
    make && \
    make install_sw && \
    cd .. && rm -rf openssl-${OPENSSL_VERSION}*

# Set OpenSSL 1.0.1f as default
ENV LD_LIBRARY_PATH="/usr/local/ssl/lib"
ENV PATH="/usr/local/ssl/bin:$PATH"
ENV OPENSSL_DIR="/usr/local/ssl"

# Download and install Python 3.4.10 from source
RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar xvf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --with-openssl=/usr/local/ssl && \
    make && \
    make install && \
    cd .. && rm -rf Python-${PYTHON_VERSION}*

# Verify Python can import OpenSSL successfully
RUN python3.4 -c "import ssl; print(ssl.OPENSSL_VERSION)"

# Set working directory
WORKDIR /app

# Copy server files
COPY httpsServer.py server.crt server.key /app/

# Expose the server port
EXPOSE 8000

# Default command to execute the server
CMD ["python3.4", "httpsServer.py"]