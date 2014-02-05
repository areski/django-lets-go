============================
Django/Python Common Helpers
============================


Switch2Bill-Common provide a set of helpers built by Star2Billing (http://www.star2billing.com)
which are used in a subset of their open source projects.


What can you find ?
-------------------

This repository is full of goodies, some are useful snippets recompiled.

It contains the following helper mainly related to Django :

1. Model : intermediate_model_base_class

2. FilterPersistMiddleware

3. Common functions :

    * ``get_unique_code`` - Generate unique code
    * ``pass_gen`` - Unique password generator
    * ``comp_month_range`` - Prepare month range list to compare with selected month
    * ``comp_day_range`` - Prepare day range list to compare with selected day
    * ``date_range`` - Get date list between two dates
    * ``validate_days`` - Validate no of days in given month and year
    * ``get_news`` - Get news from news url
    * ``only_one`` - Decorator for distributed task locking in celery
    * ``ceil_strdate`` - Convert a string date to either a start or end day date
    * ``percentage`` - Get percentage value
    * ``unset_session_var`` - Unset settion variable
    * ``getvar`` - Check field in POST/GET request and return field value. if there is value you can also save a session variable
    * ``word_capital`` -  Capitalizes the first character of each word

4. Common Template tags :

    * ``time_in_min`` - Convert value in min:sec or seconds format
    * ``conv_min`` - Convert value in min:sec format
    * ``month_name`` - Get month name from 1-12 int no
    * ``sort_link`` - Usage: {% sort_link "link text" "field_name" %} or {% sort_link "link text" "field_name" "Visible name" %}
    * ``get_fieldset``- Make group of fields for field-set
                        Usage: {% get_fieldset field1,field2 as list_field from xyz_form %}
    * ``groupby_rows`` - Returns a list of n lists. Each sub-list is the same length
    * ``groupby_rows`` - Returns a list of lists where each sub-list has n items.
    * ``listsort`` - Perform sorting on template list
    * ``convert_to_int`` - Convert value to interger
    * ``wordcap`` - Capitalizes the first character of each words.
    * ``percentage_tag`` - get percentage value.


5. build_test_suite_from : Returns a single or group of unittest test suite

6. LanguageField - Field to language list

7. AppLabelRenamer Class for django admin UI

8. export_as_csv_action - Admin custom action which returns an export csv


Installation
------------

1. Install using the sources ::

    pip install -r requirements.txt
    python setup.py install


2. Install with PIP ::

    python install switch2bill-common


License
-------

MPL V2.0 License
Copyright (C) 2011-2014 Star2Billing S.L.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.

The Initial Developer is Arezqui Belaid <info@star2billing.com>
