from django import forms
from .models import DataPoint

class DataPointForm(forms.ModelForm):
    class Meta:
        model = DataPoint
        fields = ['x_value', 'y_value']