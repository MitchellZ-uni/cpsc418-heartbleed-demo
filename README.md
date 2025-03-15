# CPSC418 Heartbleed Demo
An implementation of the vulnerable TLS 1.0 server, and a Heartbleed attack on that server. Also features some mitigation strategies that can be used.
This project is to exploit the buffer overread vulnerability found in OpenSSL `1.0.1` through `1.0.1f` (inclusive) using [Heartbleed attack](https://heartbleed.com/).

We will Python `3.4.10` combining with OpenSSL `1.0.1f` to create a HTTPS web server in Docker, and exploit the vulnerability.

## Build Server via Docker
1. Ensure [Docker](https://www.docker.com/) is installed
    - ``docker --version`` To verify the installation
2. ``git clone ...`` to copy the GitHub repository
3. ``openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.crt -days 365 -nodes`` to generate a self-signed 2048-bit RSA certificate
    - ``-nodes``: No DES, no passphrase to protect the private key
4. ``docker compose up --build`` to build and run both server and client on the same network

## View TLS 1.0 Website using FireFox
1. Ensure FireFox accepts TLS 1.0 connection
    - Go go ``about:config``
    - Set ``security.tls.version.min`` to ``1``
2. Go to ``https://localhost:8000/`` and accept the self-signed certificate
    - Click ``Advanced...`` and ``Accept and Risk and Continue``

## Check TLS 1
When the client is running, execute ``openssl s_client -connect server:8000 -tls1`` in client container to verify the TLS status of the server