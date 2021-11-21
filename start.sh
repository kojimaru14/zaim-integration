# start.sh
# https://help.heroku.com/YNG7SACF/how-do-i-define-a-start-command-for-an-app-using-docker-images
if [[ $DYNO == "web"* ]]; then
  python manage.py runserver --settings=config.settings.prod
elif  [[ $DYNO == "worker"* ]]; then
  celery -A config.celery worker --loglevel=INFO
fi