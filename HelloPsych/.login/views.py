from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("logi/")
    else:
        form = UserCreationForm()
    return render(request, "login/register.html", {
        'form': form,
    })
# Create your views here.
