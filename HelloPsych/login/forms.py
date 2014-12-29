from __future__ import unicode_literals
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import warnings
from django.template import loader
from django.utils.text import capfirst
from django.contrib.auth import authenticate, get_user_model
from django.utils.datastructures import SortedDict
from django.utils.encoding import force_bytes
from django.utils.html import format_html, format_html_join
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe

class RegistrationForm(forms.Form):
    '''The Registration for any user of this app'''
    fname = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs={'required':True,'placeholder':'First Name','max_length':30,'class':'Fields'}), label=_("First Name"))
    lname = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs={'required':True,'placeholder':'Last Name','max_length':30,'class':'Fields'}), label=_("Last Name"))
    email = forms.EmailField(widget=forms.TextInput(attrs={'required':True,'placeholder':'Email','max_length':30,'class':'Fields'}), label=_("Email address"))
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs={'required':True,'placeholder':'Username','max_length':30,'class':'Fields'}), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'required':True,'placeholder':'Password','render_value':False,'class':'Fields'}), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'required':True,'placeholder':'Re-enter Password','render_value':False,'class':'Fields'}), label=_("Repeat Password"))
    acc_type = forms.ChoiceField(label=_("Register as:"), widget=forms.Select(),choices=([('0','Patient'),('1','Doctor'),]))
    
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
    
    
    def clean_email(self):
        try:
            num = User.objects.filter(email=self.cleaned_data['email']).count()
            if num  > 0:
                raise forms.ValidationError(_("The email already exists. Please try another one."))
            else:
                return self.cleaned_data['email']
        except User.DoesNotExist:
            return self.cleaned_data['email']   

    def clean(self):
        pass1 = self.cleaned_data.get('password1')
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if len(pass1) < 8:
                raise forms.ValidationError(_("Your Password must have a minimum length of 8 characters."))
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data

class EditProfileForm(forms.Form):
    '''Form to edit the profile of the patient'''
    first_name = forms.CharField(label=_("First Name"))
    last_name = forms.CharField(label=_("Last Name"))   
    age = forms.IntegerField(widget=forms.TextInput(attrs={'class':'Fields', 'required':True}))
    sex = forms.ChoiceField(widget=forms.Select(), choices=([('M', 'Male'), ('F', 'Female'),]), required=True)
    concern = forms.ChoiceField(widget=forms.Select(),
        choices = ([
        ('addiction','addiction'),
        ('depression','Depression'),
        ('fear','Fear/Phobias'),
        ('relationship','Relationship'),
        ('life','Major Life Event'),
        ('halu','Hallucinations/Delusions'),
        ('edu','Education/Career'),
        ('anon','Others'),])
    )       
    marital_status = forms.ChoiceField(widget=forms.Select(),
        choices = ([
        ('S','Single'),
        ('M','Married'),
        ('D','Divorced'),])
    )
    
class ProfileForm(forms.Form):
    '''The profile registration form for a patient'''
    age = forms.IntegerField(widget=forms.TextInput(attrs={'class':'Fields','required':True}))
    sex = forms.ChoiceField(widget=forms.Select(), choices=([('M','Male'), ('F','Female'),]), required=True)
    concern = forms.ChoiceField(widget=forms.Select(),
        choices = ([
        ('addiction','addiction'),
        ('depression','Depression'),
        ('fear','Fear/Phobias'),
        ('relationship','Relationship'),
        ('life','Major Life Event'),
        ('halu','Hallucinations/Delusions'),
        ('edu','Education/Career'),
        ('anon','Others'),])
    )       
    marital_status = forms.ChoiceField(widget=forms.Select(), 
        choices = ([
        ('S','Single'),
        ('M','Married'),
        ('D','Divorced'),])
    )

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

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

    def check_for_test_cookie(self):
        warnings.warn("check_for_test_cookie is deprecated; ensure your login "
                "view is CSRF-protected.", DeprecationWarning)

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


        
