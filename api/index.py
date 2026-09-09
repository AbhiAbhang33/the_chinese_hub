import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "chinese_hub_shop.settings"  
)

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
