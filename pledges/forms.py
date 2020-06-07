from django import forms
from .models import Pledge


class PledgeForm(forms.ModelForm):


    class Meta:
        fields = [
            'first_name', 'last_name',
            'email', 'description', 'image',
        ]
        model = Pledge
