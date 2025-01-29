#!/bin/bash
# chmod +x prod_watcher.sh
# Usage: */5 * * * * /imaging-plaza/shacl-api/ci/prod_watcher.sh >> /imaging-plaza/shacl-api/ci/prod_watcher.log 2>&1

cd /imaging-plaza/shacl-api || exit

# Fetch the latest changes from the remote
git fetch origin main > /dev/null 2>&1

# Check if local is behind remote
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S'). Changes detected. Pulling..."
  git pull origin main
  
  # Stop and remove the old container
  docker stop shacl-api || true
  docker rm shacl-api || true
  
  # Rebuild and run the new container
  docker build -t shacl-api .
  docker run -d --name shacl-api -p 7200:15400 -p 8501:8501 shacl-api
else
  echo "$(date '+%Y-%m-%d %H:%M:%S'). No changes found."
fi
