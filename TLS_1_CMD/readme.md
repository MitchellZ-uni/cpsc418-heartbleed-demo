# TLS 1.0 Message Exchange Server
This project is to exploit the buffer overread vulnerability found in OpenSSL `1.0.1` through `1.0.1f` (inclusive) using [Heartbleed attack](https://heartbleed.com/).

We will Python `3.4.10` combining with OpenSSL `1.0.1f` to create a message exchange server in Docker, and exploit the vulnerability.

## Build Server via Docker
1. Ensure [Docker](https://www.docker.com/) is installed
    - ``docker --version`` To verify the installation
2. ``git clone ...`` to copy the GitHub repository
3. ``docker compose up --build`` to build and run both server and client on the same network