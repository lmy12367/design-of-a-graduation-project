import datetime
from flask import url_for

def add_datetime(app):
    app.add_template_global(datetime,'datetime')

def add_strf_datetime(app):
    def strf_datetime(value,strf="%Y-%m-%d %H:%M:%S"):
        return value.strftime(strf)
    app.add_template_filter(strf_datetime,"strf_datetime")


def add_blue_url_for(app,pm):
    app.add_template_global(pm.blue_url_for, "blue_url_for")

def get_change_language(app,pm,app_tools):
    _ = app_tools.BabelGetText
    def get_local():
        lanuage = app_tools.Session.get('lang', 'en') #app_tools.Request.accept_languages.best_match(app_tools.LANGUAGES.keys())
        change_language = _("英文") if lanuage == "zh" else _("中文")
        return change_language
    app.add_template_global(get_local,"get_change_language")

def add_template(app,pm,app_tools):
    add_datetime(app)
    add_strf_datetime(app)
    add_blue_url_for(app,pm)
    get_change_language(app,pm,app_tools)
