---------------------------------------------------
Common Libraries / Functions reused by Star2Billing
---------------------------------------------------

This repository is full of little goodies, some are recompiled from other sources, it contains the following script and packages,

1. Model : intermediate_model_base_class

2. FilterPersistMiddleware

3. Common functions :

    * ``pass_gen`` - Unique password generator 
    * ``comp_month_range`` - Prepare month range list to compare with selected month
    * ``comp_day_range`` - Prepare day range list to compare with selected day
    * ``date_range`` - Get date list between two dates
    * ``validate_days`` - Validate no of days in given month and year
    * ``get_news`` - Get news from news url
    * ``only_one`` - decorator for distributed task locking in celery

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

    5. build_test_suite_from : Returns a single or group of unittest test suite


