FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    tcpdump \
    iproute2 \
    net-tools \
    binutils \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN pip install scapy pyinstaller

CMD ["tail", "-f", "/dev/null"]