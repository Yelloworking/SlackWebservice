# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, session, redirect, url_for, \
     request, jsonify, abort, make_response

from slackbot import db, app, calendar
from slackbot.Locking import Locking
from slackbot.Utils import getMonthInFrench, getDayInFrench

from datetime import *

general = Blueprint('general', __name__)

@general.route('/')
def home():
    return 'up'


@general.route("locking/get/<what>/<dayid>", methods=('GET',))
def lockingGet(what, dayid):
    days = []
    realdate = datetime.strptime(dayid, "%d%m%y")

    obj = {
        "date": "%s %02d %s" % (getDayInFrench(realdate.weekday()+1), realdate.day, getMonthInFrench(realdate.month)),
        "who": [f.dump() for f in Locking.query.filter_by(dayid=dayid, kind=what).all()]
    }

    days.append(obj)

    return jsonify({"res":days})

@general.route("locking/getNext/<int:next>", methods=('GET',))
def lockingGetNext(next):
    days = []

    for i in range(next):
        dayid = Locking.genDayId(i)
        realdate = datetime.strptime(dayid, "%d%m%y")

        """
            Skip weekend
        """
        if realdate.weekday() in [5, 6]:
            continue

        obj = {
            "date": "%s %02d %s" % (getDayInFrench(realdate.weekday()+1), realdate.day, getMonthInFrench(realdate.month)),
            "who": [f.dump() for f in Locking.query.filter_by(dayid=dayid).all()]
        }

        days.append(obj)

    return jsonify({"res":days})


@general.route("locking/set/<what>/<dayid>", methods=('POST',))
def lockingSet(what, dayid):

    slackuser = request.form.get('slackuser', '000')
    fullname = request.form.get('fullname', '')

    ret = Locking.Create(dayid, slackuser, what, fullname)

    if not ret:
        return 'fail'

    return 'ok'


@general.route("locking/setNext/<what>/<int:dayIndex>", methods=('POST',))
def lockingSetForTheNextDays(what, dayIndex):

    slackuser = request.form.get('slackuser', '000')
    fullname = request.form.get('fullname', '')

    for i in range(200):
        date = Locking.getNextDay(i)
        dayid = date.strftime("%d%m%y")

        if date.weekday() != dayIndex:
            continue

        ret = Locking.Create(dayid, slackuser, what, fullname)
        
        if not ret:
            return 'fail'

    return 'ok'