#
# Switch2bill-common
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2011-2013 Star2Billing S.L.
#
# The Initial Developer of the Original Code is
# Arezqui Belaid <info@star2billing.com>
#

from django.utils.translation import gettext as _
from django.conf import settings
from inspect import stack
from datetime import datetime
from datetime import timedelta
from random import choice
import calendar
import string
import urllib


def get_unique_code(length):
    """Get unique code"""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ''.join([choice(chars) for i in range(length)])


def pass_gen(char_length, digit_length):
    """Unique password generator"""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digit = "1234567890"
    pass_str_char = ''.join([choice(chars) for i in range(char_length)])
    pass_str_digit = ''.join([choice(digit) for i in range(digit_length)])
    return pass_str_char + pass_str_digit


def current_view(request):
    #from inspect import getmodule
    #name = getmodule(stack()[1][0]).__name__
    return stack()[1][3]


def striplist(l):
    """Take a list of string objects and return the same list
    stripped of extra whitespace.

    >>> l = [1, 2, 3]

    >>> striplist(l)
    [1, 2, 3]
    """
    return([x.strip() for x in l])


#related to date manipulation
def relative_days(from_day, from_year):
    """get relative days from day & year (with leap year check)

    >>> relative_days(30, 2012)
    2
    """
    if from_day == 30:
        relative_days = 2
        return relative_days
    elif from_day == 31:
        relative_days = 1
        return relative_days
    else:
        if calendar.isleap(from_year) == 'false':
            relative_days = 2
        else:
            relative_days = 1
        return relative_days


def unique_list(inlist):
    """Prepare unique list

    >>> inlist = [1, 1, 2, 4, 5, 5, 6]

    >>> unique_list(inlist)
    [1, 2, 4, 5, 6]
    """
    # order preserving
    uniques = []
    for item in inlist:
        if item not in uniques:
            uniques.append(item)
    return uniques


def get_unique_id():
    """get unique id"""
    length = 8
    chars = "abcdefghijklmnopqrstuvwxyz1234567890"
    return ''.join([choice(chars) for i in range(length)])


def dictSort(d):
    """returns a dictionary sorted by keys

    >>> d = {"a": "1", "b": "3", "c": "2"}

    >>> dictSort(d)
    {'a': '1', 'c': '2', 'b': '3'}
    """
    our_list = d.items()
    our_list.sort()
    k = {}
    for item in our_list:
        k[item[0]] = item[1]
    return k


def comp_month_range():
    """Prepare month range list to compare with selected month

    >>> comp_month_range()
    ((12, '- 12 months'), (11, '- 11 months'), (10, '- 10 months'), (9, '- 9 months'), (8, '- 8 months'), (7, '- 7 months'), (6, '- 6 months'), (5, '- 5 months'), (4, '- 4 months'), (3, '- 3 months'), (2, '- 2 months'), (1, '- 1 month'))
    """
    word_months = _("months")
    word_month = _("month")
    COMP_MONTH_LIST = (
        (12, '- 12 ' + word_months),
        (11, '- 11 ' + word_months),
        (10, '- 10 ' + word_months),
        (9, '- 9 ' + word_months),
        (8, '- 8 ' + word_months),
        (7, '- 7 ' + word_months),
        (6, '- 6 ' + word_months),
        (5, '- 5 ' + word_months),
        (4, '- 4 ' + word_months),
        (3, '- 3 ' + word_months),
        (2, '- 2 ' + word_months),
        (1, '- 1 ' + word_month),
    )
    return COMP_MONTH_LIST


def comp_day_range(number_of_days=5):
    """Prepare day range list to compare with selected day

    >>> comp_day_range(5)
    [(1, '- 1 day'), (2, '- 2 days'), (3, '- 3 days'), (4, '- 4 days'), (5, '- 5 days')]
    """
    word_days = _("days")
    word_day = _("day")
    DAYS = range(2, number_of_days + 1)
    days = map(lambda x: (x, "- %d " % x + word_days), DAYS)
    COMP_DAY_LIST = [(1, '- 1 ' + word_day)]
    return COMP_DAY_LIST + days


def date_range(start, end):
    """get date list between two dates

    >>> start = datetime(2012, 8, 12, 0, 0, 0, 0)

    >>> end = datetime(2012, 8, 15 , 23, 59, 59)

    >>> date_range(start, end)
    [datetime.datetime(2012, 8, 12, 0, 0), datetime.datetime(2012, 8, 13, 0, 0), datetime.datetime(2012, 8, 14, 0, 0), datetime.datetime(2012, 8, 15, 0, 0)]
    """
    r = (end + timedelta(days=1) - start).days
    return [start + timedelta(days=i) for i in range(r)]


def day_range():
    """Get no of days list

    >>> day_range()
    [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)]
    """
    DAYS = range(1, 32)
    days = map(lambda x: (x, x), DAYS)
    return days


def validate_days(year, month, day):
    """validate no of days in given month and year

    >>> validate_days(2012, 8, 31)
    31
    >>> validate_days(2012, 8, 32)
    31
    """
    total_days = calendar.monthrange(year, month)
    if day > total_days[1]:
        return total_days[1]
    else:
        return day


def month_year_range(enter_date):
    """Get month-year range list
       e.g.
            2012-03 => March-2012
            2012-04 => April-2012

    >>> enter_date = datetime(2012, 8, 1)
    >>> month_year_range(enter_date)
    [('2012-08', 'August-2012'), ('2012-07', 'July-2012'), ('2012-06', 'June-2012'), ('2012-05', 'May-2012'), ('2012-04', 'April-2012'), ('2012-03', 'March-2012'), ('2012-02', 'February-2012'), ('2012-01', 'January-2012'), ('2011-12', 'December-2011'), ('2011-11', 'November-2011'), ('2011-10', 'October-2011'), ('2011-09', 'September-2011'), ('2011-08', 'August-2011'), ('2011-07', 'July-2011'), ('2011-06', 'June-2011'), ('2011-05', 'May-2011'), ('2011-04', 'April-2011'), ('2011-03', 'March-2011'), ('2011-02', 'February-2011'), ('2011-01', 'January-2011')]
    """
    year_actual = enter_date.year
    YEARS = range(year_actual - 1, year_actual + 1)
    YEARS.reverse()
    m_list = []
    for n in YEARS:
        if year_actual == n:
            month_no = enter_date.month + 1
        else:
            month_no = 13
        months_list = range(1, month_no)
        months_list.reverse()
        for m in months_list:
            name = datetime(n, m, 1).strftime("%B")
            str_year = datetime(n, m, 1).strftime("%Y")
            str_month = datetime(n, m, 1).strftime("%m")
            sample_str = str_year + "-" + str_month
            sample_name_str = name + "-" + str_year
            m_list.append((sample_str, sample_name_str))
    return m_list


def nl2br(s):
    """Related to string operation

    >>> nl2br('abc\nxyz')
    'abc<br/>xyz'
    """
    return '<br/>'.join(s.split('\n'))


# get news from http://cdr-stats.org/news.php
def get_news(news_url):
    """To get news from news url & append into list"""
    news_final = []
    try:
        news_handler = urllib.urlopen(news_url)
        news = news_handler.read()
        news = nl2br(news)
        news = string.split(news, '<br/>')

        news_array = {}
        value = {}
        for newsweb in news:
            value = string.split(newsweb, '|')
            if len(value[0]) > 1:
                news_array[value[0]] = value[1]

        info = {}
        for k in news_array:
            info = k[0:int(k.find("http://") - 1)]
            info = string.split(k, ' - ')
            news_final.append((info[0], info[1], news_array[k]))

        news_handler.close()
    except IndexError:
        pass
    except IOError:
        pass

    return news_final


#variable check with request
def variable_value(request, field_name):
    """Check field in POST/GET request and return field value"""
    if request.method == 'GET':
        if field_name in request.GET:
            field_name = request.GET[field_name]
        else:
            field_name = ''

    if request.method == 'POST':
        if field_name in request.POST:
            field_name = request.POST[field_name]
        else:
            field_name = ''

    return field_name


#source_type/destination_type filed check with request
def source_desti_field_chk(base_field, base_field_type, field_name):
    """Prepare filters (kwargs{}) for django queryset
       where fields contain string are checked like
       exact | startswith | contains | endswith

    >>> source_desti_field_chk(21, '1', 'contact')
    {'contact__exact': 21}

    >>> source_desti_field_chk(21, '2', 'contact')
    {'contact__startswith': 21}

    >>> source_desti_field_chk(21, '3', 'contact')
    {'contact__contains': 21}

    >>> source_desti_field_chk(21, '4', 'contact')
    {'contact__endswith': 21}
    """
    kwargs = {}
    if base_field != '':
        if base_field_type == '1':
            kwargs[field_name + '__exact'] = base_field
        if base_field_type == '2':
            kwargs[field_name + '__startswith'] = base_field
        if base_field_type == '3':
            kwargs[field_name + '__contains'] = base_field
        if base_field_type == '4':
            kwargs[field_name + '__endswith'] = base_field
    return kwargs


def mongodb_str_filter(base_field, base_field_type):
    """Prepare filters (kwargs{}) for django queryset for mongodb
       where fields contain strings are checked like
       exact | startswith | contains | endswith

    >>> mongodb_str_filter(21, '1')
    '21'
    >>> mongodb_str_filter(21, '2')
    {'$regex': '^21'}
    >>> mongodb_str_filter(21, '3')
    {'$regex': '.*21.*'}
    >>> mongodb_str_filter(21, '4')
    {'$regex': '21$'}
    """
    q = ''
    base_field = str(base_field)
    if base_field != '':
        if base_field_type == '1':  # Equals
            q = base_field
        if base_field_type == '2':  # Begins with
            q = {'$regex': str('^' + base_field)}
        if base_field_type == '3':  # Contains
            q = {'$regex': str('.*' + base_field + '.*')}
        if base_field_type == '4':  # Ends with
            q = {'$regex': str(base_field + '$')}
    return q


def mongodb_int_filter(base_field, base_field_type):
    """Prepare filters (kwargs{}) for django queryset
    where fields contain digits are checked like = | > | >= | < | <=

    >>> mongodb_int_filter(10, '1')
    10.0
    >>> mongodb_int_filter(10, '2')
    {'$gt': 10.0}
    >>> mongodb_int_filter(10, '3')
    {'$gte': 10.0}
    >>> mongodb_int_filter(10, '4')
    {'$lt': 10.0}
    """
    q = ''
    if base_field != '':
        if base_field_type == '1':  # =
            q = float(base_field)
        if base_field_type == '2':  # >
            q = {'$gt': float(base_field)}
        if base_field_type == '3':  # >=
            q = {'$gte': float(base_field)}
        if base_field_type == '4':  # <
            q = {'$lt': float(base_field)}
        if base_field_type == '5':  # <=
            q = {'$lte': float(base_field)}
    return q


def reverseString(s):
    """reverse string

    >>> reverseString('abc')
    'cba'
    """
    return s[::-1]


def int_convert_to_minute(value):
    """Convert value into min & sec

    >>> int_convert_to_minute(123)
    '02:03'
    """
    min = int(int(value) / 60)
    sec = int(int(value) % 60)
    return "%02d" % min + ":" + "%02d" % sec


def isint(str):
    """ Is the given string an integer

    >>> isint(str('1234'))
    1
    >>> isint(str('11a'))
    0
    """
    ok = 1
    if not str:
        return 0
    try:
        int(str)
    except ValueError:
        ok = 0
    except TypeError:
        ok = 0
    return ok


def ceil_strdate(str_date, start):
    """convert a string date to either a start or end day date"""
    if start == 'start':
        return datetime(int(str_date[0:4]), int(str_date[5:7]),
            int(str_date[8:10]), 0, 0, 0, 0)
    else:
        return datetime(int(str_date[0:4]), int(str_date[5:7]),
            int(str_date[8:10]), 23, 59, 59, 999999)


def get_pagination_vars(request, col_field_list, default_sort_field):
    """Return data for django pagination with sort order"""
    # Define no of records per page
    PAGE_SIZE = settings.PAGE_SIZE
    try:
        PAGE_NUMBER = int(request.GET['page'])
    except:
        PAGE_NUMBER = 1

    # page index
    if PAGE_NUMBER > 1:
        start_page = (PAGE_NUMBER - 1) * int(PAGE_SIZE)
        end_page = start_page + int(PAGE_SIZE)
    else:
        start_page = int(0)
        end_page = int(PAGE_SIZE)

    # default column order
    col_name_with_order = {}
    for field_name in col_field_list:
        col_name_with_order[field_name] = '-' + field_name

    sort_field = variable_value(request, 'sort_by')
    if not sort_field:
        sort_field = default_sort_field  # default sort field
        sort_order = '-' + sort_field  # desc
    else:
        if "-" in sort_field:
            sort_order = sort_field
            col_name_with_order[sort_field[1:]] = sort_field[1:]
        else:
            sort_order = sort_field
            col_name_with_order[sort_field] = '-' + sort_field

    data = {
        'PAGE_SIZE': PAGE_SIZE,
        'PAGE_NUMBER': PAGE_NUMBER,
        'start_page': start_page,
        'end_page': end_page,
        'col_name_with_order': col_name_with_order,
        'sort_order': sort_order,
    }
    return data


def percentage(value, total_sum):
    """calculate a percentage"""
    if total_sum == 0:
        return 0
    else:
        return round(100 * float(value) / float(total_sum))
