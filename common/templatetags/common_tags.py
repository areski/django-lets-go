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
from django import template
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.utils.datastructures import SortedDict
import copy

register = template.Library()


@register.filter(name='mul')
def mul(value, arg):
    """Multiplication

    >>> mul(2, 2)
    4
    """
    return value * arg
mul.is_safe = True


@register.filter(name='div')
def div(value, arg):
    """Division

    >>> div(4, 2)
    2
    """
    if arg is None:
        return 0
    elif arg is 0:
        return 0
    else:
        return value / arg


@register.filter(name='subtract')
def subtract(value, arg):
    """Subtraction

    >>> subtract(4, 2)
    2
    """
    return value - arg


@register.filter(name='percent')
def percent(value):
    """Percentage with % sign

    >>> percent(1)
    '100.0 %'
    """
    return str(round(value * 100, 2)) + " %"


@register.filter(name='profit_in_percentage')
def profit_in_percentage(value, arg):
    """Profit Percentage with % sign

    >>> profit_in_percentage(2, 1)
    '100.0 %'
    """
    val = value - arg
    return str(round(val * 100, 2)) + " %"


@register.filter(name='cal_width')
def cal_width(value, max):
    """Get width

    >>> cal_width(70, 100)
    140.0
    """
    if not value or not max:
        return "None"
    width = (value / float(max)) * 200
    return width


@register.filter(name='time_in_min')
def time_in_min(value, arg):
    """Convert value in min or second format

    >>> time_in_min(130, 'min')
    '02:10 min'

    >>> time_in_min(130, 'sec')
    '130 sec'
    """
    try:
        value = int(value)
    except:
        value = 0
    if value != 0:
        if arg == 'min':
            min = int(value / 60)
            sec = int(value % 60)
            return "%02d" % min + ":" + "%02d" % sec + " min"
        else:
            min = int(value / 60)
            min = (min * 60)
            sec = int(value % 60)
            total_sec = min + sec
            return str(total_sec) + " sec"
    else:
        return str("00:00 min")


@register.filter(name='conv_min')
def conv_min(value):
    """Convert value in min:sec format

    >>> conv_min(130)
    '02:10'
    """
    try:
        value = int(value)
    except:
        value = 0

    if value != 0:
        min = int(value / 60)
        sec = int(value % 60)
        return "%02d" % min + ":" + "%02d" % sec
    else:
        return "00:00"


@register.filter(name='month_name')
def month_name(value, arg):
    """Get month name from 1-12 int no

    >>> month_name(2, 1)
    'Feb 1'
    """
    month_dict = {1: "Jan", 2: "Feb", 3: "Mar",
                  4: "Apr", 5: "May", 6: "Jun",
                  7: "Jul", 8: "Aug", 9: "Sep",
                  10: "Oct", 11: "Nov", 12: "Dec"}
    no = int(value)
    m_name = month_dict[no]
    return str(m_name) + " " + str(arg)


@register.filter(name='to_json')
def to_json(value):
    return mark_safe(simplejson.dumps(value))


@register.inclusion_tag('sort_link_frag.html', takes_context=True)
def sort_link(context, link_text, sort_field, visible_name=None):
    """Usage: {% sort_link "link text" "field_name" %}
       Usage: {% sort_link "link text" "field_name" "Visible name" %}
    """
    is_sorted = False
    sort_order = None
    orig_sort_field = sort_field
    if context.get('current_sort_field') == sort_field:
        sort_field = '-%s' % sort_field
        visible_name = '-%s' % (visible_name or orig_sort_field)
        is_sorted = True
        sort_order = 'down'
    elif context.get('current_sort_field') == '-' + sort_field:
        visible_name = '%s' % (visible_name or orig_sort_field)
        is_sorted = True
        sort_order = 'up'

    if visible_name:
        if 'request' in context:
            request = context['request']
            request.session[visible_name] = sort_field

    if 'getsortvars' in context:
        extra_vars = context['getsortvars']
    else:
        if 'request' in context:
            request = context['request']
            getvars = request.GET.copy()
            if 'sort_by' in getvars:
                del getvars['sort_by']
            if len(getvars.keys()) > 0:
                context['getsortvars'] = "&%s" % getvars.urlencode()
            else:
                context['getsortvars'] = ''
            extra_vars = context['getsortvars']

        else:
            extra_vars = ''

    return {'link_text': link_text, 'sort_field': sort_field,
            'extra_vars': extra_vars, 'sort_order': sort_order,
            'is_sorted': is_sorted, 'visible_name': visible_name
            }


def get_fieldset(parser, token):
    """Usage: {% get_fieldset field1,field2 as list_field from xyz_form %}
              {% for list_field in xyz_form %}
              {% endfor %}
    """
    try:
        name, fields, as_, variable_name, from_, form = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('bad arguments for %r' %
                token.split_contents()[0])

    return FieldSetNode(fields.split(','), variable_name, form)

get_fieldset = register.tag(get_fieldset)


class FieldSetNode(template.Node):
    def __init__(self, fields, variable_name, form_variable):
        self.fields = fields
        self.variable_name = variable_name
        self.form_variable = form_variable

    def render(self, context):

        form = template.Variable(self.form_variable).resolve(context)
        new_form = copy.copy(form)
        new_form.fields = SortedDict(
            [(key, value) for key, value in form.fields.items() if key in self.fields])

        context[self.variable_name] = new_form
        return u''


class ArgumentError(ValueError):
    """Missing or incompatible argument."""


def _regroup_table(seq, rows=None, columns=None):
    if not (rows or columns):
        raise ArgumentError("Missing one of rows or columns")

    if columns:
        rows = (len(seq) // columns) + 1
    table = [seq[i::rows] for i in range(rows)]

    # Pad out short rows
    n = len(table[0])
    return [row + [None for x in range(n - len(row))] for row in table]


@register.filter(name='groupby_rows')
def groupby_rows(seq, n):
    """Returns a list of n lists. Each sub-list is the same length.

    Short lists are padded with None. This is useful for creating HTML tables
    from a sequence.

    >>> groupby_rows(range(1, 11), 3)
    [[1, 4, 7, 10], [2, 5, 8, None], [3, 6, 9, None]]
    """
    return _regroup_table(seq, rows=int(n))


@register.filter(name='groupby_columns')
def groupby_columns(seq, n):
    """Returns a list of lists where each sub-list has n items.

    Short lists are padded with None. This is useful for creating HTML tables
    from a sequence.

    >>> groupby_columns(range(1, 11), 3)
    [[1, 5, 9], [2, 6, 10], [3, 7, None], [4, 8, None]]
    """
    return _regroup_table(seq, columns=int(n))


@register.filter(name='sort')
def listsort(value):
    """Sort list

    >>> value = {'a': 1, 'c': 3, 'd': 4, 'b': 2}

    >>> listsort(value)
    {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    """
    if isinstance(value, dict):
        new_dict = SortedDict()
        key_list = value.keys()
        key_list.sort()
        for key in key_list:
            new_dict[key] = value[key]
        return new_dict
    elif isinstance(value, list):
        new_list = list(value)
        new_list.sort()
        return new_list
    else:
        return value
    listsort.is_safe = True


@register.filter(name='convert_to_int')
def convert_to_int(val):
    """
    Return int value
    """
    try:
        return int(val)
    except:
        return val
