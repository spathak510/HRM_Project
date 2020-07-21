from django import forms
from .models import *

class TimesheetForm(forms.ModelForm):

    class Meta:
        model = Activity_report
        fields = ('time_of_day_start', 'module')
