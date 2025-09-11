FROM debian:bullseye

RUN apt-get update && apt-get install -y nginx tor openssh-server sudo && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user && \
    echo "user:123" | chpasswd && \
    adduser user sudo

COPY nginx.conf /etc/nginx/nginx.conf
COPY sshd_config /etc/ssh/sshd_config
COPY torrc /etc/tor/torrc

COPY index.html /var/www/html/index.html

RUN mkdir -p /var/lib/tor/hidden_service && \
    chown -R debian-tor:debian-tor /var/lib/tor/hidden_service && \
    chmod 700 /var/lib/tor/hidden_service

EXPOSE 80 4242

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
