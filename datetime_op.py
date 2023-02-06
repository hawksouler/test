# !/usr/bin/env python3
# -*- coding:utf-8 -*-

import datetime


def get_next_month(date_t: datetime.date) -> datetime.date:
    """
    :param date_t: datetime.date or datetime.datetime -> 2020-04-12
    :return: Class object for date_t(date_t.__class__), the first day of the month
    Usage:
        >>> next_month = get_next_month(datetime.date(2020, 4, 12))
            datetime.date(2020, 5, 1)
        >>> next_month = get_next_month(datetime.datetime(2020, 4, 12))
            datetime.datetime(2020, 5, 1)
        >>>
    """
    if not isinstance(date_t, (datetime.date, datetime.datetime)):
        raise Exception('Input format error')

    _month = date_t.month + 1
    _year = date_t.year
    if _month == 13:
        _month = 1
        _year += 1
    return getattr(date_t, '__class__')(month=_month, year=_year, day=1)


def get_last_month(date_t: datetime.date) -> datetime.date:
    """
    :param date_t: datetime.date or datetime.datetime -> 2020-04-12
    :return: Class object for date_t(date_t.__class__), the first day of the month
    Usage:
        >>> last_month = get_last_month(datetime.date(2020, 4, 12))
            datetime.date(2020, 3, 1)
        >>> last_month = get_last_month(datetime.datetime(2020, 4, 12))
            datetime.datetime(2020, 3, 1)
        >>>
    """
    if not isinstance(date_t, (datetime.date, datetime.datetime)):
        raise Exception('Input format error')
    _month = date_t.month - 1
    _year = date_t.year
    if _month == 0:
        _month = 12
        _year -= 1
    return getattr(date_t, '__class__')(month=_month, year=_year, day=1)


if __name__ == '__main__':
    dt = get_last_month(datetime.date.today())
    print(str(dt))