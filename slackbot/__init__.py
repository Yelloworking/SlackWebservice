# -*- coding: utf-8 -*-


from flask import Flask, make_response, request, g, render_template
from flask.ext.sqlalchemy import SQLAlchemy

from Calendar import Calendar
from config import Config

from jinja2 import evalcontextfilter, Markup, escape

import time

app           = Flask(__name__, static_folder='static')
calendar      = Calendar()


app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['SECRET_KEY'] = 'slackhat!!!222'
app.config['DEBUG'] = Config.DEBUG
app.config['PREFERRED_URL_SCHEME'] = 'https' if Config.SSL is True else 'http'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@localhost/%s' % (Config.DB['user'], Config.DB['password'], Config.DB['db'])

db = SQLAlchemy(app)

@app.template_filter()
@evalcontextfilter
def frdate(eval_ctx, value):
    return value.strftime('%d/%m/%Y')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(exception):
    app.logger.exception(exception)
    return make_response("Some Internal error has taken place: "+str(exception), 500)

from slackbot.views import general

app.register_blueprint(general.general, url_prefix='/')
