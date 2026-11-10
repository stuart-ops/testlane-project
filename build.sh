#!/bin/bash
# Build script for Testlane.ai Sovereign AI deployment
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Build complete."