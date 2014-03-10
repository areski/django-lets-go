
Django Helper, Utils and mix of Snippets
========================================

Django-Lets-go provide a lot of goodies, functions, useful snippets recompiled,
if you develop some Django projects you will certainly found something useful here.


Django-lets-go contains the following :
---------------------------------------

1. Model
~~~~~~~~

* intermediate_model_base_class


2. Middleware
~~~~~~~~~~~~~

* FilterPersistMiddleware


3. Functions
~~~~~~~~~~~~

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


4. Template tags
~~~~~~~~~~~~~~~~

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


5. Fields
~~~~~~~~~

* LanguageField - Field to language list


6. Test suite tools
~~~~~~~~~~~~~~~~~~~

* build_test_suite_from : Returns a single or group of unittest test suite


7. Admin Class Helper
~~~~~~~~~~~~~~~~~~~~~~

* AppLabelRenamer Class for django admin UI

* export_as_csv_action - Admin custom action which returns an export csv


Installation
------------

1. Install using the sources ::

    pip install -r requirements.txt
    python setup.py install


2. Install with PIP ::

    python install django-lets-go


Projects using Django-lets-go
-----------------------------

* CDR-Stats : http://www.cdr-stats.org
* Newfies-Dialer : http://www.newfies-dialer.org


Changelog
---------

Changelog summary : https://github.com/areski/django-lets-go/blob/master/CHANGELOG.rst


License
-------

Django-lets-go is licensed under `MIT`_

The Initial Developer is Arezqui Belaid <areski@gmail.com>

.. _`MIT`: https://github.com/areski/django-lets-go/blob/master/MIT-LICENSE.txt
