"""
"""

import os, sys

project = os.path.dirname(__file__)
workspace = os.path.dirname(project)
sys.path.append(workspace)
sys.path.append(project)

#prod system only
os.environ['DJANGO_SECRET_KEY']='3KmeFgGa1LYNFetu6iMFMB/bC18inZQz5GwgAYgasl4k5OwDZ2E='
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings.prod'
os.environ['AWS_ACCESS_KEY_ID'] = 'AKIAIS2U7NVNTQXL7AMQ'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
os.environ['AWS_BUCKET'] = 'd42cdn'
os.environ['DJANGO_DB_NAME']='d42'
os.environ['DJANGO_DB_USER']='d42user'
os.environ['DJANGO_DB_PASS']='device@42'
os.environ['DJANGO_DB_HOST']='localhost'
os.environ['DJANGO_DB_PORT']=''

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
