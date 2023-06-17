from datetime import timedelta

from django import forms
from django.utils import timezone

class bookingForm(forms.Form):
    check_in = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': timezone.now().strftime('%Y-%m-%d'),
                'max': (timezone.now() + timedelta(days=365)).strftime('%Y-%m-%d')
            }))
    check_out = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    persons = forms.IntegerField(max_value=100)
    rooms = forms.IntegerField(max_value=10)

    def clean_check_out(self):
        check_in = self.cleaned_data.get('check_in')
        check_out = self.cleaned_data.get('check_out')

        if check_out <= check_in:
            raise forms.ValidationError("Check out date should be later than check-in")
        if check_out - check_in > timedelta(days=30):
            raise forms.ValidationError("Sorry, the maximum time of stay is 30 days")
        return check_out




