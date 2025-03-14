# TLS 1.0 Message Exchange Server
This project is to exploit the buffer overread vulnerability found in OpenSSL `1.0.1` through `1.0.1f` (inclusive) using [Heartbleed attack](https://heartbleed.com/).

We will Python `3.4.10` combining with OpenSSL `1.0.1f` to create a HTTPS web server in Docker, and exploit the vulnerability.

## Build Server via Docker
1. Ensure [Docker](https://www.docker.com/) is installed
    - ``docker --version`` To verify the installation
2. ``git clone ...`` to copy the GitHub repository
3. ``docker compose up --build`` to build and run both server and client on the same network

## View TLS 1.0 Website using FireFox
1. Ensure FireFox accepts TLS 1.0 connection
    - Go go ``about:config``
    - Set ``security.tls.version.min`` to ``1``
2. Go to ``https://localhost:8000/`` and accept the self-signed certificate
    - Click ``Advanced...`` and ``Accept and Risk and Continue``

## Details
[ChatGPT](https://chatgpt.com/share/67ce6f9c-e854-8013-b970-29bfa634dfee)

## Check TLS 1 (client)
``openssl s_client -connect server:8000 -tls1``