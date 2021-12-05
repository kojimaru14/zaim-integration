#!/bin/bash

export_env_dir() {
  env_dir=$1
  acceptlist_regex=${2:-''}
  denylist_regex=${3:-'^(PATH|GIT_DIR|CPATH|CPPATH|LD_PRELOAD|LIBRARY_PATH)$'}
  if [ -d "$env_dir" ]; then
    for e in $(ls $env_dir); do
      echo "$e" | grep -E "$acceptlist_regex" | grep -qvE "$denylist_regex" &&
      export "$e=$(cat $env_dir/$e)"
      :
    done
  fi
}

export DJANGO_SETTINGS_MODULE=config.settings.prod

# Google credentials are saved in env variable, so export it to a file.
if [ -f /code/service_account.json ]; then
  echo ${GOOGLE_CREDENTIALS} > /code/service_account.json
fi

echo $DYNO
printenv
echo $SOURCE_VERSION
export_env_dir
echo $SOURCE_VERSION
printenv

# https://help.heroku.com/YNG7SACF/how-do-i-define-a-start-command-for-an-app-using-docker-images
if [[ $DYNO == "web"* ]]; then
  if [[ -z ${SOURCE_VERSION+x}  ]]; then # Run migration only on release phase (Ref: https://stackoverflow.com/questions/59537030/release-phase-with-container-registry-on-heroku-runs-container#answer-59537345)
    set -e
    python manage.py migrate
  fi
  gunicorn config.wsgi --log-file -
  echo "Zaim web process started"
elif [[ $DYNO == "worker"* ]]; then
  celery -A config.celery worker --loglevel=INFO
  echo "Zaim worker process started"
fi
