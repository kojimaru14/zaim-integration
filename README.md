# Docker commands

Commands for running django server on Docker
```
# In order to initiate django server on docker, run the following command
docker-compose up

# In order to rebuild the docker image and run django server, use this:
docker-compose down && docker-compose up --build
```

Creating a superuser on django
```
python manage.py createsuperuser --settings config.settings.dev
docker-compose exec celery python manage.py createsuperuser --settings config.settings.dev
```

Commands for running tests
```
# Without docker
python manage.py test app --settings config.settings.dev

# Running test on Docker
docker build -t lyugaloki/zaim-celery -f Dockerfile.celery .
docker run -it --env ZAIM_USER="login@address.com" --env ZAIM_PASSWORD="password" --env DJANGO_SETTINGS_MODULE=config.settings.prod lyugaloki/zaim-celery python manage.py test app

docker-compose exec celery python manage.py test app --settings config.settings.dev
docker-compose run app python manage.py test app --settings config.settings.dev
docker-compose run celery python manage.py test app --settings config.settings.dev
```

For debugging by connecting to docker image via shell
```
docker-compose up

docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED       STATUS              PORTS                    NAMES
8427b63018f9   zaim_celery   "python manage.py ce…"   5 days ago    Up About a minute                            zaim_celery_1
1636555ef322   zaim_app      "sh -c 'python manag…"   5 days ago    Up About a minute   0.0.0.0:8000->8000/tcp   zaim_app_1
5b17ed4a3cdf   postgres      "docker-entrypoint.s…"   3 weeks ago   Up About a minute   0.0.0.0:5432->5432/tcp   zaim_db_1
085567d5f379   redis:6.2     "docker-entrypoint.s…"   5 weeks ago   Up About a minute   0.0.0.0:6379->6379/tcp   zaim_redis_1

docker run -it --entrypoint=/bin/bash $IMAGE -i 
docker run -it --entrypoint=/bin/bash zaim_app

```

Heroku commands
```
heroku ps:exec --dyno=worker.1 -a zaim
```