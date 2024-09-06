from django.contrib import admin
from .models import YearlyDoseLog, YearlySideEffectLog

admin.site.register(YearlyDoseLog)
admin.site.register(YearlySideEffectLog)
