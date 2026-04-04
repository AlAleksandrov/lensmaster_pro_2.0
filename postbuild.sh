#!/bin/bash

source antenv/bin/activate

python manage.py collectstatic --noinput
python manage.py migrate
