from login.forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from login.models import *
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
import random, datetime, sha
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.cache import cache_control, never_cache
from django.contrib.auth.views import password_reset, password_reset_confirm
from django import forms
from django.forms.util import flatatt
from django.template import loader
from django.utils.datastructures import SortedDict
from django.utils.encoding import force_bytes
from django.utils.html import format_html, format_html_join
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_protect
def register(request):
    """
    Function to register the user as a doctor or patient and send a corresponding confirmation email
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['fname'],
            last_name=form.cleaned_data['lname'],
            )
            new_user.is_active=False
            new_user.save()         
            acc_type=form.cleaned_data['acc_type']
            if acc_type=='1':
                t=1
            else:
                t=0

            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt+new_user.username).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            new_profile = UserProfile(user=new_user, activation_key=activation_key, key_expires=key_expires,acc_type=t, verified = 0)
            new_profile.save()
    
            subject = 'Thank You for signing up!'
            message ="Hello, %s,! Thanks for signing up at MeetAShrink.!\n\nTo activate your account, click this link within 48 hours:\n\n%s/accounts/login/confirm/%s" %  ( new_profile.user.username, \
            settings.HOSTNAME, new_profile.activation_key )
            send_mail(subject,message, settings.EMAIL_HOST_USER ,[new_user.email])
            return render_to_response('registration/register_success.html', {'created': True},RequestContext(request,{'usrname':new_user.username,'acc':new_profile.acc_type}))
    else:       
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form })
    return render_to_response('registration/register.html',variables)

def confirm(request, activation_key):
    """
    Function to handle the email confirmation functionality
    """
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
    if user_profile.user.is_active:
        return render_to_response('patient')    
    else:   
        #if user_profile.key_expires <  timezone.now():
        #return render_to_response('registration/confirm.html', {'expired': True})
        user_account = user_profile.user
        user_account.is_active = True
        user_account.save()
    
    return render_to_response('registration/confirm.html', {'success': True},RequestContext(request,{'user':user_profile.user,'usrname':user_profile.user.username,'acc':user_profile.acc_type, 'verified':user_profile.verified}))


def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='registration/reset_confirm.html', uidb64=uidb64, token=token,post_reset_redirect=reverse('login:login'))

def reset(request):
    return password_reset(request, template_name='registration/reset.html',
        email_template_name='registration/reset_email.html',
        subject_template_name='registration/reset_subject.txt')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required 
def register_profile(request):
    """
    Function to register the patient profile details
    """
    if request.method == 'POST':
        fm = ProfileForm(request.POST,request.FILES)
        if fm.is_valid():
            u=User.objects.get(id=request.user.id)
            profile = patient.objects.create(
            user=request.user,          
            username=request.user.username,
            first_name=u.first_name,
            last_name=u.last_name,
            sex=fm.cleaned_data['sex'],
            marital_status=fm.cleaned_data['marital_status'],
            concern=fm.cleaned_data['concern'], 
            age=fm.cleaned_data['age'],         
            )
            profile.save()
            update=profileupdate.objects.create(
            user=request.user
            )
            update.save()
            return HttpResponseRedirect(reverse('patient:index'))
    else:  
        if not request.session.get('sex',None):
            request.session['sex']='M'

        if not request.session.get('marital',None):
            request.session['marital']='S'

        if not request.session.get('age',None):
            request.session['age']=18

        if not request.session.get('cond',None):
            request.session['cond']='Addiction'

        fm = ProfileForm(initial={'sex': request.session['sex'],'marital_status':request.session['marital'],'age':request.session['age'],'concern':request.session['cond'],})

    variables = RequestContext(request, {'form': fm,'flag':request.user.is_authenticated()})
    return render_to_response('registration/profile.html',variables,)

@login_required 
def edit_profile(request):
    """
    Function to edit the patient profile details
    """
    if request.method == 'POST':
        ins=patient.objects.get(user=request.user)
        fm = EditProfileForm(request.POST,request.FILES)
        if fm.is_valid():
            ins.sex=fm.cleaned_data['sex']
            ins.marital_status=fm.cleaned_data['marital_status']
            ins.concern=fm.cleaned_data['concern']
            ins.age=fm.cleaned_data['age']
            ins.first_name=fm.cleaned_data['first_name']
            ins.last_name=fm.cleaned_data['last_name']
            ins.save()
            return HttpResponseRedirect(reverse('patient:index'))
    else:
        ins=patient.objects.get(user=request.user)
        fm = EditProfileForm(initial={'first_name':ins.first_name,'last_name':ins.last_name,'sex': ins.sex,'marital_status':ins.marital_status,'concern':ins.concern,'age':ins.age,})
        
    variables = RequestContext(request, {'form': fm,'flag':request.user.is_authenticated(),'usrname':ins.username})
    return render_to_response('registration/editprofile.html',variables,)

@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_page(request):
    """
    Function that calls the in-built logout function
    """
    logout(request)
    return HttpResponseRedirect(reverse('patient:patient'))#/welcome')

def display(request):
    return render_to_response('registration/log.html')

def not_verified(request):
    """
    Function to display the verified/not_verified pages for the doctor's account
    """
    user_profile = UserProfile.objects.get(user=request.user)
    logout(request)
    if user_profile.verified:
        return render_to_response('registration/verified.html')
    else:
        return render_to_response('registration/not_verified.html')


@csrf_protect
@never_cache
def login(request, template_name='registration/login.html', authentication_form=AuthenticationForm, current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:    
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            user_profile = None
        try:    
            patient_profile = patient.objects.get(user=user)
        except patient.DoesNotExist:
            patient_profile = None
        try:
            doctor_profile = doctor.objects.get(user=user)  
        except doctor.DoesNotExist:
            doctor_profile = None   
            
        if form.is_valid():
            auth_login(request, form.get_user())
            if user_profile.acc_type == 1:
                if doctor_profile is None:
                    return HttpResponseRedirect(reverse('docview:create'))
                else:
                    if user_profile.verified:
                        return HttpResponseRedirect(reverse('docview:dashboard',args=(str(request.user.username),)))
                    else:
                        return HttpResponseRedirect(reverse('login:not_verified'))
            elif user_profile.acc_type == 0:
                if patient_profile is None:
                    return HttpResponseRedirect(reverse('login:profile'))
                else:
                    return HttpResponseRedirect(reverse('patient:index'))
    else:
        form = authentication_form(request)
 
    variables = RequestContext(request, {'form': form,'flag':request.user.is_authenticated()})
    return render_to_response('registration/log.html',variables)


