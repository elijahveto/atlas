from django import forms
from .models import Company, User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password


class LoginForm(forms.Form):
    # overwrite the default field values like so, same field name required ofc
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'your email'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'your password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                raise forms.ValidationError('username does not exist')
            else:
                return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if password and username:
            hashed_pw = User.objects.get(username=username).password
            if not check_password(password, hashed_pw):
                raise forms.ValidationError('wrong password')
            else:
                return password


class CompanyForm(forms.ModelForm):
    # overwrite the default field values like so, same field name required ofc
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'please enter your company name'}))

    class Meta:
        model = Company
        fields = ['name']

    # def clean_name(self):
    #     company = self.cleaned_data.get('name').lower()
    #     if company:
    #         try:
    #             Company.objects.get(name=company).id
    #             raise forms.ValidationError('this company is already registered.')
    #         except Company.DoesNotExist:
    #             return company


class UserForm(forms.ModelForm):
    #company = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={'placeholder': 'your company'}))
    first_name = forms.CharField(max_length=30, label='', widget=forms.TextInput(attrs={'placeholder': 'first name'}))
    last_name = forms.CharField(max_length=30, label='', widget=forms.TextInput(attrs={'placeholder': 'last name'}))
    email = forms.CharField(max_length=40, label='', widget=forms.TextInput(attrs={'placeholder': 'email'}))
    password1 = forms.CharField(label='',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'password'}),
        validators=[validate_password])
    password2 = forms.CharField(label='',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'please confirm password'}),
        strip=False)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('password mismatch')
        elif password1 and password2:
            return password2


    # def clean_company(self):
    #     company = self.cleaned_data.get('company').lower()
    #     if company:
    #         try:
    #             company = Company.objects.get(name=company)
    #         except Company.DoesNotExist:
    #             raise forms.ValidationError('this company is not registered yet.')
    #         else:
    #             return company

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError('please only include alphabet values in your name (sorry X Æ A-12).')
        else:
            return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError('please only include alphabet values in your name.')
        else:
            return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if not '@' in email:
            raise forms.ValidationError('invalid email.')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('this email is already registered. please log in instead.')
        else:
            return email
