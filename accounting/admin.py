from django.contrib import admin
from .models import DiscountRule, TaxRule

admin.site.register(DiscountRule)
admin.site.register(TaxRule)