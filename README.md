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
## Upload csv file
[Upload](http://csv2api.pythonanywhere.com/api/file/upload/)


## Retrieve data
[Retrieve](http://csv2api.pythonanywhere.com/api/file/<uuid>/?format=json&page=1&size=5&sort_by=age,balance)

### page
Default page index is 1
`&page=1`

### size
Default page size is 10
`&size=5`

#### Retrieve all rows
`&size=all`

### sort_by
`&sort_by=column1`

#### Multiple sort support
`&sort_by=column1,column2`