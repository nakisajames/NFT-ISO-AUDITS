

activate_this = '/var/www/example.com/public_html/myenv/bin/activate_this.py'


# execfile(activate_this, dict(__file__=activate_this))


exec(open(activate_this).read(),dict(__file__=activate_this))




import os


import sys


import site




# Add the site-packages of the chosen virtualenv to work with


site.addsitedir('/var/www/example.com/public_html/myenv/lib/python3.7/site-packages')




# Add the app's directory to the PYTHONPATH


sys.path.append('/var/www/example.com/public_html/')


sys.path.append('/var/www/example.com/public_html/django_jailuapp')




os.environ['DJANGO_SETTINGS_MODULE'] = 'django_jailuapp.settings'


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_jailuapp.settings")
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_jailuapp.django_jailuapp.settings")




from django.core.wsgi import get_wsgi_application


application = get_wsgi_application()

