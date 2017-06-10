from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm
from django.utils.translation import ugettext_lazy as _

from .models import RdxUser


class RegisterUserForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    User creation form.
    """
    password = forms.CharField(
        label=_("Password"),
        max_length=10,
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': '10 char only'}),
    )

    class Meta:
        model = RdxUser
        fields = ("email", "username", "mobile", "password",)

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs = {'class': 'form-control',
                                             'placeholder': 'Email'}
        self.fields['username'].widget.attrs = {'class': 'form-control',
                                                'placeholder': 'Full name'}
        self.fields['mobile'].widget.attrs = {'class': 'form-control',
                                              'placeholder': 'Contact no.'}

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class RdxUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
    )

    class Meta:
        model = RdxUser
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class RdxUserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=10, widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect passsword")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(RdxUserLoginForm, self).clean(*args, **kwargs)
