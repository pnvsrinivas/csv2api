# csv2api
Serves back your CSV data as an RESTAPI

# How to run

## Create virtualenv
python -m venv env

## Activate your virtual environment
env\Scripts\activate.bat

## Install required packages
pip install -r requirements.txt

## Run/Start the server
python manage.py runserver

# Documentation
[http://csv2api.pythonanywhere.com/api/docs/](http://csv2api.pythonanywhere.com/api/docs/)

# Live demo
## Upload data
[Upload](http://csv2api.pythonanywhere.com/api/upload/)

## Retrieve data
[Retrieve](http://csv2api.pythonanywhere.com/api/data/<uuid>/?format=json)