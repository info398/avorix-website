#!/bin/bash
# Auto-Deploy Script for Avorix Website
# Runs every 5 minutes via cron. Pulls latest commits, rebuilds Docker, deploys.

set -euo pipefail

REPO_DIR="/docker/avorix-website"
LOCK_FILE="/tmp/avorix-deploy.lock"
LOG_FILE="/var/log/avorix-deploy.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Prevent parallel runs
if [ -f "$LOCK_FILE" ]; then
    log "Deploy already running (lock file exists). Skipping."
    exit 0
fi
touch "$LOCK_FILE"
trap "rm -f $LOCK_FILE" EXIT

cd "$REPO_DIR"

# Fetch latest changes
git fetch origin master --quiet

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/master)

if [ "$LOCAL" = "$REMOTE" ]; then
    exit 0
fi

log "New commits detected. Deploying $LOCAL -> $REMOTE"

# Pull changes
git pull origin master --quiet

# Build Docker image
log "Building Docker image..."
if ! docker compose build --no-cache 2>&1 | tee -a "$LOG_FILE"; then
    log "ERROR: Docker build failed. Aborting deploy."
    exit 1
fi

# Deploy (restart containers)
log "Deploying new version..."
docker compose up -d 2>&1 | tee -a "$LOG_FILE"

log "Deploy successful. Running commit: $(git rev-parse --short HEAD)"
