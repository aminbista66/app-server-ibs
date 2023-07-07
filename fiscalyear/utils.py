import nepali_datetime
import re

from django.core.exceptions import ValidationError

def fiscal_year_generator():
    # calculates the current year fiscial year
    todays_date = nepali_datetime.date.today()
    current_year = todays_date.year
    current_month = todays_date.month
    if current_month >= 4:
        first = current_year
        second = current_year + 1
    else:
        second = current_year
        first = current_year - 1

    fiscal_year_choice = str(first) + "-" + str(second)
    return fiscal_year_choice


def validate_fiscal_year(input):
    pattern = re.compile(r"\d\d\d\d-\d\d\d\d")
    if not pattern.match(input):
        raise ValidationError("Invalid fiscal year")
    years = input.split("-")
    diff = int(years[1]) - int(years[0])
    if diff != 1:
        raise ValidationError("Invalid fiscal year")