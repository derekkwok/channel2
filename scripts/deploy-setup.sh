#!/bin/sh
# This script setups the machine to serve channel2.

# Copy configuration files.
scp scripts/config/Caddyfile channel2-root:/etc/caddy/Caddyfile
scp scripts/config/caddy.service channel2-root:/lib/systemd/system/caddy.service

echo "
apt-get update && apt-get -y upgrade
apt-get install curl

# Install Caddy.
curl https://getcaddy.com | bash -s personal

# Once the installation is completed, we need to add the
# cap_net_bind_service capability to the Caddy binary. This capability will
# allow the Caddy executable to bind to a port less than 1024.
setcap 'cap_net_bind_service=+ep' /usr/local/bin/caddy

# Setup directories.
mkdir -p /etc/caddy
chown -R root:www-data /etc/caddy
mkdir -p /etc/ssl/caddy
chown -R www-data:root /etc/ssl/caddy
chmod 0770 /etc/ssl/caddy
touch /etc/caddy/Caddyfile
mkdir -p /var/www/channel2/media
chown www-data: /var/www/channel2/media
mkdir -p /var/www/channel2/db
chown www-data: /var/www/channel2/db

# Enable Caddy to start on boot.
systemctl enable caddy.service

# Restart Caddy.
service caddy stop
service caddy start

# Setup a python virtual environment.
python3.6 -m venv /var/www/channel2/venv
" | ssh channel2-root 'bash -s'
