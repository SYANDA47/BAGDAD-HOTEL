web: gunicorn Bar_project.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn Bar_project.wsgi
