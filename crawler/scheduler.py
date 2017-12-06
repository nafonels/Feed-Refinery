#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model import engine

__version__ = "$"

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


# from apscheduler.executors.pool import ProcessPoolExecutor

def tick():
    print("tick!")


def timer_1():
    print("1")


def timer_2():
    print("2")


def timer_3():
    print("3")


store = SQLAlchemyJobStore(engine = engine)
scheduler = BackgroundScheduler()
scheduler.add_jobstore(store)
