import os
import sys
import traceback

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "chinese_hub_shop.settings"
)

from django.core.wsgi import get_wsgi_application

django_app = get_wsgi_application()


def app(environ, start_response):
    try:
        return django_app(environ, start_response)
    except Exception:
        print("\n========== DJANGO ERROR ==========")
        traceback.print_exc()
        print("========== END DJANGO ERROR ==========\n")
        raise