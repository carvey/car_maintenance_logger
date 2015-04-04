from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from logger.models import Entry, Car


# class LoginForm(forms.Form):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    #override of the default clean method, as this form should not raise form errors if a username is not unique
    # def clean(self):
    #     self._validate_unique = False
    #     return self.cleaned_data

    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #
    #     if username and password:
    #         self.user_cache = authenticate(username=username,
    #                                        password=password)
    #         if self.user_cache is None:
    #             raise forms.ValidationError(
    #                 self.error_messages['invalid_login'],
    #                 code='invalid_login',
    #                 params={'username': self.username_field.verbose_name},
    #             )
    #         elif not self.user_cache.is_active:
    #             raise forms.ValidationError(
    #                 self.error_messages['inactive'],
    #                 code='inactive',
    #             )
    #     return self.cleaned_data

class LoginForm(AuthenticationForm):
     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
     password = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

     def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }


class AddCarForm(forms.Form):
    label = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Car Name/Label'}))
    date_purchased = forms.CharField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}))
    initial_cost = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Initial Cost'}))
    initial_mileage = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Initial Mileage'}))


class AddEntryForm(forms.Form):
    date = forms.CharField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}))
    mileage = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Mileage at time of service'}))
    service_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Type'}))
    service_location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Location'}))
    contact_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Last'}))
    contact_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '555-555-5555'}))
    cost_of_parts = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '20'}))
    cost_of_service = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '20'}))
    comments = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comments'}))


class EditEntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        exclude = ['user']


class EditCarForm(forms.ModelForm):

    class Meta:
        model = Car
        exclude = ['user']