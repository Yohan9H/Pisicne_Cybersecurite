FROM ubuntu:22.04

RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y \
    libc6:i386 \
    libncurses5:i386 \
    libstdc++6:i386 \
    gdb \
    python3 \
    python3-pip \
    python3-venv \
    python3-distutils \
    python3-setuptools \
    python3-wheel \
    git \
    ca-certificates \
    build-essential \
    cmake \
    file \
    wget \
    less \
    vim \
    && rm -rf /var/lib/apt/lists/*

COPY level1 /level1
COPY level2 /level2
RUN chmod +x /level1 /level2

RUN git clone --depth=1 https://github.com/pwndbg/pwndbg /opt/pwndbg && \
    cd /opt/pwndbg && \
    python3 -m pip install --upgrade pip setuptools wheel && \
    if [ -f requirements.txt ]; then python3 -m pip install -r requirements.txt || true; fi && \
    /opt/pwndbg/setup.sh

CMD ["/bin/bash"]