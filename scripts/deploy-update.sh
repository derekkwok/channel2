#!/bin/sh
# This script deploys the latetst version of the channel2.

# Package the application and scp to the server.
rm -f /tmp/channel2.tar
git archive -o /tmp/channel2.tar HEAD
scp /tmp/channel2.tar channel2-root:/tmp/channel2.tar

# Setup and update a Python virtual environment.
echo "
# Extract channel2 server code.
rm -fr /var/www/channel2/server
mkdir -p /var/www/channel2/server
tar xvf /tmp/channel2.tar -C /var/www/channel2/server

# Install requirements.
/var/www/channel2/venv/bin/pip install -r /var/www/channel2/server/requirements.txt

# Restart Caddy.
service caddy stop
service caddy start
" | ssh channel2-root 'bash -s'
