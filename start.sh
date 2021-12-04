#!/bin/bash

export DJANGO_SETTINGS_MODULE=config.settings.prod

# Google credentials are saved in env variable, so export it to a file.
if [ -f /code/service_account.json ]; then
  echo ${GOOGLE_CREDENTIALS} > /code/service_account.json
fi

# https://help.heroku.com/YNG7SACF/how-do-i-define-a-start-command-for-an-app-using-docker-images
if [[ $DYNO == "web"* ]]; then
  gunicorn config.wsgi --log-file -
  echo "Zaim web process started"
elif  [[ $DYNO == "worker"* ]]; then
  celery -A config.celery worker --loglevel=INFO
  echo "Zaim worker process started"
fi