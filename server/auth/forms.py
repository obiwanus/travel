from django import forms
from django.core.validators import RegexValidator

from auth.models import User, UserProfile


alphanum = RegexValidator(r'^[0-9A-Za-z\-\s]*$', "Sorry, only the characters A-Z and hyphens are allowed")


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput, strip=False)


class AddUserForm(forms.Form):
    first_name = forms.CharField(max_length=100, validators=[alphanum])
    last_name = forms.CharField(max_length=100, validators=[alphanum])
    email = forms.EmailField(max_length=255)
    role = forms.CharField(max_length=15, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email):
            raise forms.ValidationError("User with this email already exists")
        return email

    def clean_role(self):
        role = self.cleaned_data['role']

        if not self.user.is_authenticated or self.user.profile.role == UserProfile.USER:
            # Anyone can create a normal user account
            role = UserProfile.USER

        if not role:
            role = UserProfile.USER

        if role not in (UserProfile.USER, UserProfile.USER_MANAGER, UserProfile.ADMIN):
            raise forms.ValidationError("Incorrect role specified")

        if self.user.profile.role != UserProfile.ADMIN and role == UserProfile.ADMIN:
            raise forms.ValidationError("Insufficient permissions to set this role")

        return role
