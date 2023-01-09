# from asyncio.windows_events import NULL
from logging import NullHandler
from struct import pack
from unicodedata import category
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from PIL import Image
from ..models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect

@login_required(login_url=settings.LOGIN_URL)
def EmailCreate(request):
    create_link_name = reverse("GlobalCreate")
    slug1 = "global-create" 
    action = "EmailStore"
    get_data = GlobalSettings.objects.first()
    data = {'slug1':slug1,'create':False,'create_link_name':create_link_name,'id_data':get_data, 'action':action}
    client_msg = ContactUs.objects.filter(read_unread=True)
    data['client_msg']=client_msg
    return render(request, 'admin/configure_email/configure-email-form.html',data)

@login_required(login_url=settings.LOGIN_URL)
def EmailStore(request,pk=None):
    if request.POST:
        configure_email = request.POST['email']      
         
        if not configure_email:
            messages.error(request, "Email is mendatory")
            return redirect(request.POST['next'])
        addingproduct = GlobalSettings.objects.update(id=pk, configure_email=configure_email)#update_or_create method is used to creat data if id not exist. if id is exist then it update on particular id column

        #After Insert open product
        return redirect(EmailCreate)



