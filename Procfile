<!-- # Procfile in the root of your project with this code inside
# The migrate command is to migrate the app models/ tables to the database hosted in heroku servers. -->
release: python3 manage.py migrate
<!-- # The project folder is named catcollector, that's why we used it here. 
# gunicorn will allow us to deploy to heroku 
# It will act as a middleman between our application and the internet. -->
web: gunicorn chrysalis.wsgi 
