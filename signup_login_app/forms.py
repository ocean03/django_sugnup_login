from random import choice

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms

UserModel = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('image', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            user = UserModel.objects.get(email=email)
            raise forms.ValidationError("This email address already exists. Did you forget your password?")
        except UserModel.DoesNotExist:
            return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        letters = self.cleaned_data['email'] + self.cleaned_data['first_name'] + self.cleaned_data['last_name']
        user.username = ''.join([choice(letters) for i in range(30)])
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.is_active = False
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    email = forms.CharField(label='Email')

    class Meta:
        fields = ('email', 'password')
