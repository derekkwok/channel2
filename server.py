import os
from wsgiref.simple_server import make_server

from django.core.wsgi import get_wsgi_application

os.environ['C2_MODE'] = 'prod'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channel2.settings')
application = get_wsgi_application()  # pylint: disable=invalid-name

with make_server('', 8081, application) as httpd:
    print('Serving Channel 2 on port 8081')
    httpd.serve_forever()
    httpd.handle_request()
