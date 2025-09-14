#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r staboost/requirements.txt

# Collect static files
python staboost/manage.py collectstatic --no-input

# Apply database migrations
python staboost/manage.py migrate
