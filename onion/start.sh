#!/bin/bash

mkdir -p /run/sshd

echo "Starting SSH server on port 4242..."
/usr/sbin/sshd

echo "Starting Nginx web server on port 80..."
nginx

echo "Starting Tor..."
su -s /bin/bash -c "tor" debian-tor
