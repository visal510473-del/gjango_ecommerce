from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class CustomRegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9 ]+$',
                message='Enter a valid username. This value may contain only letters, numbers, and spaces.',
                code='invalid_username'
            )
        ],
        help_text='Required. Letters, numbers and spaces only.'
    )

    code = forms.CharField(
        label='Code',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Enter a 4-digit numeric code.',
        validators=[
            RegexValidator(
                regex=r'^\d{4}$',
                message='Code must be exactly 4 digits.',
                code='invalid_code'
            )
        ]
    )

    code_confirmation = forms.CharField(
        label='Code confirmation',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Enter the same 4-digit code again.'
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with that username already exists.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        code_confirmation = cleaned_data.get('code_confirmation')

        if code and code_confirmation and code != code_confirmation:
            raise forms.ValidationError('The two code fields didn\'t match.')

        return cleaned_data

    def save(self, commit=True):
        user = User(username=self.cleaned_data['username'])
        user.set_password(self.cleaned_data['code'])
        if commit:
            user.save()
        return user
