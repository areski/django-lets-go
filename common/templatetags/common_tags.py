#
# Switch2bill-common
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2011-2012 Star2Billing S.L.
#
# The Initial Developer of the Original Code is
# Arezqui Belaid <info@star2billing.com>
#
from django import template
from django.template.defaultfilters import *
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django.utils.translation import gettext as _
from django.utils.datastructures import SortedDict
from datetime import datetime
import operator
import copy

register = template.Library()

@register.filter()
def time_in_min(value, arg):
    """Convert value in min or second format"""
    if int(value)!=0:
        if arg == 'min':
            min = int(value / 60)
            sec = int(value % 60)
            return "%02d" % min + ":" + "%02d" % sec + "min"
        else:
            min = int(value / 60)
            min = (min * 60)
            sec = int(value % 60)
            total_sec = min + sec
            return str(total_sec + " sec")
    else:
        return str("00:00 min")


@register.filter()
def conv_min(value):
    """Convert value in min:sec format"""
    if int(value)!=0:
        min = int(value / 60)
        sec = int(value % 60)
        return "%02d" % min + ":" + "%02d" % sec
    else:
        return "00:00"


@register.filter()
def month_name(value, arg):
    """Get month name from 1-12 int no"""
    month_dict = {1: "Jan", 2: "Feb", 3: "Mar",
                  4: "Apr", 5: "May", 6:"Jun",
                  7: "Jul", 8: "Aug", 9: "Sep",
                  10: "Oct", 11: "Nov", 12: "Dec"}
    no=int(value)
    m_name = month_dict[no]
    return str(m_name) + " " + str(arg)


@register.filter
def to_json(value):
    return mark_safe(simplejson.dumps(value))


@register.inclusion_tag('cdr/sort_link_frag.html', takes_context=True)
def sort_link(context, link_text, sort_field, visible_name=None):
    """Usage: {% sort_link "link text" "field_name" %}
       Usage: {% sort_link "link text" "field_name" "Visible name" %}
    """
    is_sorted = False
    sort_order = None
    orig_sort_field = sort_field
    if context.get('current_sort_field') == sort_field:
        sort_field = '-%s'%sort_field
        visible_name = '-%s'%(visible_name or orig_sort_field)
        is_sorted = True
        sort_order = 'down'
    elif context.get('current_sort_field') == '-'+sort_field:
        visible_name = '%s'%(visible_name or orig_sort_field)
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


    return {'link_text':link_text, 'sort_field':sort_field, 'extra_vars':extra_vars,
            'sort_order':sort_order, 'is_sorted':is_sorted, 'visible_name':visible_name
            }


def get_fieldset(parser, token):
    """Usage: {% get_fieldset field1,field2 as list_field from xyz_form %}
              {% for list_field in xyz_form %}
              {% endfor %}
    """
    try:
        name, fields, as_, variable_name, from_, form = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('bad arguments for %r'  % token.split_contents()[0])

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
        new_form.fields = SortedDict([(key, value) for key, value in form.fields.items() if key in self.fields])

        context[self.variable_name] = new_form

        return u''


def _regroup_table(seq, rows=None, columns=None):
    if not (rows or columns):
        raise ArgumentError("Missing one of rows or columns")

    if columns:
        rows = (len(seq) // columns) + 1
    table = [seq[i::rows] for i in range(rows)]

    # Pad out short rows
    n = len(table[0])
    return [row + [None for x in range(n - len(row))] for row in table]


@register.filter
def groupby_rows(seq, n):
    """Returns a list of n lists. Each sub-list is the same length.

    Short lists are padded with None. This is useful for creating HTML tables
    from a sequence.

    >>> groupby_rows(range(1, 11), 3)
    [[1, 4, 7, 10], [2, 5, 8, None], [3, 6, 9, None]]
    """
    return _regroup_table(seq, rows=int(n))


@register.filter
def groupby_columns(seq, n):
    """Returns a list of lists where each sub-list has n items.

    Short lists are padded with None. This is useful for creating HTML tables
    from a sequence.

    >>> groupby_columns(range(1, 11), 3)
    [[1, 5, 9], [2, 6, 10], [3, 7, None], [4, 8, None]]
    """
    return _regroup_table(seq, columns=int(n))


register.filter('conv_min', conv_min)
register.filter('time_in_min', time_in_min)
register.filter('month_name', month_name)
register.filter('to_json', to_json)
register.filter('groupby_rows', groupby_rows)
register.filter('groupby_columns', groupby_columns)