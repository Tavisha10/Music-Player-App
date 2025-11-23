#!/bin/bash
set -o errexit

pip install --upgrade pip setuptools
pip install -r requirements.txt
python manage.py migrate
python manage.py add_songs
python manage.py collectstatic --noinput