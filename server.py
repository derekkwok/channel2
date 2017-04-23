import os
os.environ['C2_MODE'] = 'prod'

from wsgiref.simple_server import make_server
from channel2.wsgi import application

with make_server('', 8000, application) as httpd:
    print('Serving Channel 2 on port 8000')
    httpd.serve_forever()
    httpd.handle_request()
