#!/bin/bash

# Add the content of JSON file (decrypted by openssl command on .travis.yml) to an env variable on Heroku
ls -al
cat service-account.json
openssl aes-256-cbc -K $encrypted_9f3b5599b056_key -iv $encrypted_9f3b5599b056_iv -in service-account.json.enc -out service-account.json -d
cp service-account.json service-account-temp.json
ls -al
cat service-account-temp.json
heroku config:set GOOGLE_CREDENTIALS="$(< service-account-temp.json)" --app $HEROKU_APP_NAME

# Building image for web
docker build -t registry.heroku.com/$HEROKU_APP_NAME/web -f ./Dockerfile.web .;
# Push a built image: https://devcenter.heroku.com/articles/container-registry-and-runtime#pushing-an-existing-image
docker push registry.heroku.com/$HEROKU_APP_NAME/web;
# Releasing an image: https://devcenter.heroku.com/articles/container-registry-and-runtime#releasing-an-image
heroku container:release web --app $HEROKU_APP_NAME

# Building image for worker
docker build -t registry.heroku.com/$HEROKU_APP_NAME/worker -f ./Dockerfile.celery .;
# Push a built image: https://devcenter.heroku.com/articles/container-registry-and-runtime#pushing-an-existing-image
docker push registry.heroku.com/$HEROKU_APP_NAME/worker;
# Releasing an image: https://devcenter.heroku.com/articles/container-registry-and-runtime#releasing-an-image
heroku container:release worker --app $HEROKU_APP_NAME