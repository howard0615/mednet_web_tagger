"""
WSGI config for mednet_sum_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append("C:/...path.../mednet_server")

sys.path.append("C:/...path.../mednet_server/mednet_sum_site")

# path = 'C:\Users\howard\Desktop\mednet_server'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mednet_sum_site.settings')

application = get_wsgi_application()
