#!/usr/bin/env python
# encoding: utf-8
import datetime

def get_today_time():
    """
    time_help
    :return: 
    """
    start_time = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    end_time = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

    return start_time, end_time