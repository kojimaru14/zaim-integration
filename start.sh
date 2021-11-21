#!/bin/bash

# https://help.heroku.com/YNG7SACF/how-do-i-define-a-start-command-for-an-app-using-docker-images
if [[ $DYNO == "web"* ]]; then
  python manage.py runserver --settings=config.settings.prod
  echo "Zaim web process started"
elif  [[ $DYNO == "worker"* ]]; then
  export DJANGO_SETTINGS_MODULE=config.settings.prod
  celery -A config.celery worker --loglevel=INFO
  echo "Zaim worker process started"
fi