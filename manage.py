# -*- coding: utf-8 -*-
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from slackbot import app, db
from slackbot.Locking import Locking

from pprint import pprint
import os, re

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def create():
    "Create database"

    db.create_all()
    db.session.commit()

@manager.command
def drop():
    "Drop database"

    db.drop_all()
    db.session.commit()


if __name__ == "__main__":
    manager.run()