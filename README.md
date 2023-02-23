# PrizeWheelProject

## BE
### 1-create python venv:
python -m venv ./venv 

###2-Activate python venv:
.\venv\Scripts\activate

###2-Add requierments file and istall them using pip:
pip install -r requirements.txt

###4-start crating the django project:
django-admin startproject app .

5- django-admin startapp core
6- django-admin startapp user

### create a mysql DB free from https://railway.app/ then go to seeting.py in app and add you connection credentials 

8- python manage.py makemigrations
9- python manage.py migrate
10- python manage.py createsuperuser (email: 'stev@example.com', pass: 'test_pass123')
11- python manage.py runserver