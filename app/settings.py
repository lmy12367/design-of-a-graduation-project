import os
from config import pm
from . import Apps

BASE_APP_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG = pm.get_config("default")
pm.set_basedir(BASE_APP_DIR,CONFIG)

CONFIG.DEBUG = True

INSTALLED_APPS = [
    Apps(name="school",url_prefix="/"),
    Apps(name="school", url_prefix="/school"),
]

TEMPLATE_FOLDER = "templates"
STATIC_FOLDER = "statics"

IS_LOGIN = True
LOGIN_VIEW = "app.user.user_login"
LOGIN_INDEX = "show_all_users"

IS_BABEL = True
BABEL_DEFAULT_LOCALE = "zh"
BABEL_DEFAULT_TIMEZONE = "UTC"
BABEL_TRANSLATION_DIRECTORIES = "babel/translations"

# config.pm.sql_url()
#(DATABASE, USERNAME="", PASSWORD="", PORT="", HOSTNAME="", sql=SQL_SQLITE)