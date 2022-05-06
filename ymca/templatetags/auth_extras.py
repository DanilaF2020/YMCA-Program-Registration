from django import template
from django.contrib.auth.models import Group 
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

# display messages
from django.contrib import messages

##from .models import User
from django.contrib.auth.models import User

register = template.Library()

@register.filter(name='has_group')
def has_group(users, group_name): 
    user = User.objects.all().get(id=users)
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False