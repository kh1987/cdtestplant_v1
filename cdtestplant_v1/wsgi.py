import os

from django.core.wsgi import get_wsgi_application

# 以后开发环境分离
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cdtestplant_v1.settings')

application = get_wsgi_application()
