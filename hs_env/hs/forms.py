from django import forms

from .models import Wzz

class HanziForm(forms.ModelForm):
    class Meta:
        model = Wzz
        fields = ['character']
        labels = {'character':''}