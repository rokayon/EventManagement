from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Permission,Group
from django import forms
import re
from events.forms import StyleFromMixin
from django.contrib.auth.forms import AuthenticationForm
class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','password','password2','email']
    def __init__(self, *args, **kwargs):
        super(UserCreationForm,self).__init__(*args, **kwargs)
        
        for fieldname in ['username','password','password2']:
            
          self.fields[fieldname].help_text =None

class CustomRegistrationForm(StyleFromMixin,forms.ModelForm):
    password =forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password','confirm_password')
    def clean(self): #none field Error
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password= cleaned_data.get('confirm_password')
        
        if password!= confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data 
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError('Email already exists')
        return email
    def clean_password(self): 
         password = self.cleaned_data.get('password')
         errors=[]  
         if len(password) < 8:
            errors.append('Password must be at least 8 character long')

         if not re.search(r'[A-Z]', password):
            errors.append(
                'Password must include at least one uppercase letter.')

         if not re.search(r'[a-z]', password):
            errors.append(
                 'Password must include at least one lowercase letter.')

         if not re.search(r'[0-9]', password):
            errors.append('Password must include at least one number.')

         if not re.search(r'[@#$%^&+=]', password):
            errors.append(
                'Password must include at least one special character.')
         if errors:
            raise forms.ValidationError(errors)
         return password


class LoginForm( StyleFromMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AssignRoleForm(StyleFromMixin,forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label='Select a role'
    )

class CreateGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permissions'
    )
    
    class Meta:
        model = Group
        fields = ['name', 'permissions']