from flask.ext.sqlalchemy import SQLAlchemy
from slackbot import db
from datetime import *
from dateutil.relativedelta import relativedelta
from flask import session
from slackbot import calendar


QUICK_ADD_FORMAT_CLOSE = "Fermeture %s %s 7pm"
QUICK_ADD_FORNAT_OPEN  = "Ouverture %s %s 8am"

class Locking(db.Model):
    id       =           db.Column(db.Integer, primary_key=True)
    dayid    =           db.Column(db.String(6), index=True, nullable=False)
    date     =           db.Column(db.Date, nullable=False)

    kind     =           db.Column(db.Enum('open', 'close', name="kind"), nullable=False)

    slackuser =          db.Column(db.String(16), index=True, nullable=False)
    fullname  =          db.Column(db.Unicode(64), nullable=False)

    eventid   =          db.Column(db.String(32), index=True, nullable=True)


    def dump(self):
        return {
            "date": self.date.strftime("%d/%m/%Y"),
            "kind": self.kind,
            "slackuser": self.slackuser,
            "fullname": self.fullname
        }

    @staticmethod
    def genDayId(relativeDayFromNow=0):
        return (datetime.utcnow() + relativedelta(days=relativeDayFromNow)).strftime("%d%m%y")

    @staticmethod
    def getNextDay(relativeDayFromNow=0):
        return (datetime.utcnow() + relativedelta(days=relativeDayFromNow))

    @staticmethod
    def Create(dayid, slackuser, what, fullname):
        try:
            realdate = datetime.strptime(dayid, "%d%m%y")
        except:
            return False


        """
        Check for existing event
        """
        try:
            locking = Locking.query.filter_by(dayid=dayid, kind=what).one()
            if locking.eventid:
                calendar.delete(locking.eventid)
        except:
            locking = Locking(dayid=dayid)
            db.session.add(locking)


        locking.slackuser   = slackuser
        locking.kind        = what
        locking.fullname    = fullname
        locking.date        = realdate

        try:
            eventid = calendar.add((QUICK_ADD_FORMAT_CLOSE if what == "close" else QUICK_ADD_FORMAT_OPEN) % (fullname, realdate.strftime("%m/%d/%y")))
        except:
            db.session.rollback()
            return False

        locking.eventid = eventid

        db.session.commit()

        return locking