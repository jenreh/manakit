#!/bin/bash
cd /reflexapp/
uv run alembic upgrade head
uv run reflex export --env prod --frontend-only --no-zip

# Create /srv directory
mkdir -p /srv

# Move files from the correct Reflex 0.8.7 export location
if [ -d ".web/build/client" ]; then
    echo "Moving static files from .web/build/client/ to /srv/"
    mv .web/build/client/* /srv/
else
    echo "Error: .web/build/client directory not found after reflex export"
    exit 1
fi

# Cleanup
rm -rf .web

# Start Caddy
caddy start

# Start backend
uv run reflex run --env prod --backend-only &
BACKEND_PID=$!

# Keep the container active
wait
