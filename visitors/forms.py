from datetime import timedelta

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone

from visitors.models import User, Booking


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields =['username',
                 'first_name',
                 'last_name',
                 'email',
                 'password1',
                 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class bookingForm(forms.Form):
    check_in = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': timezone.now().strftime('%Y-%m-%d'),
                'max': (timezone.now() + timedelta(days=365)).strftime('%Y-%m-%d')
            }))
    check_out = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                'max': (timezone.now() + timedelta(days=395)).strftime('%Y-%m-%d')
            }))
    persons = forms.IntegerField(max_value=10, initial=2)



    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            print('User:', user.current_booking_persons)
            self.fields['persons'] = forms.IntegerField(max_value=10, initial=user.current_booking_persons)



    def clean_check_out(self):
        check_in = self.cleaned_data.get('check_in')
        check_out = self.cleaned_data.get('check_out')

        if check_out <= check_in:
            raise forms.ValidationError("Check out date should be later than check-in")
        if check_out - check_in > timedelta(days=30):
            raise forms.ValidationError("Sorry, the maximum time of stay is 30 days")
        return check_out


class BookingUpdateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['tel', 'comments']

        widgets = {
            'comments': forms.Textarea(attrs={'rows': 6, 'cols': 26}),
        }
