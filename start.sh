#!/bin/bash

export DJANGO_SETTINGS_MODULE=config.settings.prod

# Google credentials are saved in env variable, so export it to a file.
if [ -f /code/service_account.json ]; then
  echo ${GOOGLE_CREDENTIALS} > /code/service_account.json
fi

echo $DYNO

# https://help.heroku.com/YNG7SACF/how-do-i-define-a-start-command-for-an-app-using-docker-images
if [[ $DYNO == "web"* ]]; then
  if [[ "$DYNO" =~ ^release.* ]]; then # Run migration only on release phase (Ref: https://stackoverflow.com/questions/59537030/release-phase-with-container-registry-on-heroku-runs-container#answer-59537345)
    set -e
    python manage.py migrate
  fi
  gunicorn config.wsgi --log-file -
  echo "Zaim web process started"
elif  [[ $DYNO == "worker"* ]]; then
  celery -A config.celery worker --loglevel=INFO
  echo "Zaim worker process started"
fi