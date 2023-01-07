#FamPay Backend Assignment

##Backend Setup

1. Create a python virtual environment

2. Activate the virtual environment

3. Install packages from requirements.txt

4. `cd server`

5. Create django superuser

`python manage.py createsuperuser`

6. Run migrations

`python manage.py makemigrations`

`python manage.py migrate`

7. Run server

`python manage.py runserver`

8. Log in to admin and add an initial api key in the 'Keyss' table. Leave other fields blank. without this, frontend wont work.

9. Run the background script to ingest data every 10 seconds (generally quota is exhausted after 100 requests, so after 1000 seconds, you will need to provide a new api key, or add a lot of api keys at the start itself)

`python manage.py ingest`

If api key is invalid it will print to the terminal

###API List

http://localhost:8000/api/Landingpage/list?page=1&size=20&filter=&orderBy=&orderDirection=

####params

filter -> 'day' or 'month' or 'year' or ''

orderBy -> 'date' or 'channel' or 'title' or ''

orderDirection -> 'asc' or 'desc'

http://localhost:8000/api/Landingpage/search?query=it

http://localhost:8000/api/Landingpage/change_request/?query=hindi | smartphone | it | fashion | female | male

####info

This API will change the query with which Youtube Api is being called for ingesting

####params

query -> | is used for logical OR and - is used for logical NOT

http://localhost:8000/api/Landingpage/add_keys/?keys=AIzaSyDf_lVpX-4YznsCt-qnm92GwD2wqCTcmCI

####params

query -> comma seperated api keys

##Frontend Setup

1. Install "Allow CORS: Access-Control-Allow-Origin" extension.

2. Host frontend/index.html with Live server VSCode extension.

###Features:

1. Pagination on get api

2. 3 Filters

3. Sorting by Date

4. Searching by title and description

5. Click the hamburger to add more api keys

6. Basic Responsiveness
