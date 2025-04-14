# CPSC418 Heartbleed Demo
An implementation of the vulnerable TLS 1.0 server, and a Heartbleed attack on that server. Also features some mitigation strategies that can be used.
This project is to exploit the buffer overread vulnerability found in OpenSSL `1.0.1` through `1.0.1f` (inclusive) using [Heartbleed attack](https://heartbleed.com/).

We will Python `3.4.10` combining with OpenSSL `1.0.1f` to create a HTTPS web server in Docker, and exploit the vulnerability.

## Build Server via Docker
1. Ensure [Docker](https://www.docker.com/) and [OpenSSL](https://openssl.org/) are installed
    - ``docker --version`` to verify the installation of Docker
    - ``openssl version`` to verify the installation of OpenSSL
2. ``git clone https://github.com/MitchellZ-uni/cpsc418-heartbleed-demo.git`` to copy the GitHub repository
3. ``cd cpsc418-heartbleed-demo`` to change the directory
4. ``openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.crt -days 365 -nodes`` to generate a self-signed 2048-bit RSA certificate
    - ``-nodes``: No DES, no passphrase to protect the private key
5. Run the Docker Desktop application
6. ``docker compose up --build`` to build and run both server and client on the same network

## View TLS 1.0 Website using FireFox
1. Ensure FireFox accepts TLS 1.0 connection
    - Type ``about:config`` in the URL bar
    - Set ``security.tls.version.min`` to ``1``
2. Go to ``https://localhost:8000/`` and accept the self-signed certificate
    - Click ``Advanced...`` and ``Accept and Risk and Continue``

## (Optional) Verify TLS 1.0 Server
When the server is running, execute ``openssl s_client -connect server:8000 -tls1`` in the **client container** terminal


## Heartbleed Attack
In order to execute the Heartbleed attack from the client container, please follow the steps:
1. Make sure the compose container is running
    - Refer to the section above **Build Server via Docker**
2. Go to the Docker Desktop application, and find the container ``client-1`` under the compose container ``tls_1_https``
3. Click on the three dots on the right, choose ``>_ Open in terminal``
4. Run ``python3.4 client.py`` in that terminal
    - Note: Since the exploitation only gets the message in the server's buffer, you may need to send requests from the client/browser to the server before running the Heartbleed attack

## Close the Virtual Machine
- From the command line where you run **Build Server via Docker**
    - ``ctrl + c`` for Windows or Linux, or ``control + c`` for MacOS
- From Docker Desktop
    - Click the square button on the right of the compose container ``tls_1_https``
