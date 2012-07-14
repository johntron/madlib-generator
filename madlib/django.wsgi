import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'madlib.settings'
sys.path.append( '/www/johntron.com/madlib' )
import django.core.handlers.wsgi


application = django.core.handlers.wsgi.WSGIHandler()