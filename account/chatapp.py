# from asyncio.windows_events import NULL
from ast import And
from venv import create
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from PIL import Image
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User,Group,Permission
from django.urls import reverse
from django.contrib.auth.hashers import make_password

def ChatApp(request):
    return render(request , 'admin/chatapp/chatapp.html')