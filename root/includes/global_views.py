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
def GlobalCreate(request, pk=None):
    create_link_name = reverse("GlobalCreate")
    if pk==None:
        slug1 = "global-create" 
    else:
        slug1 = "global-update" 
    action = "GlobalStore"
    #Fetching the data of particular ID
    if pk:
        get_data = GlobalSettings.objects.get(id=pk)  
    else: 
        get_data = GlobalSettings.objects.first()
    data = {'slug1':slug1,'create':False,'create_link_name':create_link_name,'id_data':get_data, 'action':action}
    client_msg = ContactUs.objects.filter(read_unread=True)
    data['client_msg']=client_msg
    return render(request, 'admin/global_settings/global-form.html',data)

@login_required(login_url=settings.LOGIN_URL)
def GlobalStore(request,pk=None):
    if request.POST:
        # Data come from HTML to View
        #print(request.FILES['image1'])
        #return HttpResponse(request.POST.items())
        site_name = request.POST['site_name']
        site_name_nepali = request.POST['site_name_nepali']
        site_email = request.POST['site_email']
        site_contact = request.POST['site_contact']
        site_contact_nepali = request.POST['site_contact_nepali']
        site_address = request.POST['site_address']
        site_address_nepali = request.POST['site_address_nepali']
        fb_link = request.POST['fb_link']
        twitter_link = request.POST['twitter_link']
        linkedin_link = request.POST['linkedin_link']
        other_link = request.POST['other_link']
        page_title = request.POST['page_title']
        page_keyword = request.POST['page_keyword']
        page_discription = request.POST['page_discription']

        if not site_contact_nepali:
            site_contact_nepali = 0

        images = {} #dictionary of image
        for i in request.FILES:#adding filled image in dictionary.if image is empty then not add to dictionary
            if(i==i):
                images[i] = request.FILES[i]
        
        data={
            'site_name' : site_name,
            'site_name_nepali' : site_name_nepali,
            'site_email' : site_email,
            'site_contact' :site_contact,
            'site_contact_nepali' :site_contact_nepali,
            'site_address' : site_address,
            'site_address_nepali' : site_address_nepali,
            'fb_link' : fb_link,
            'tiktok_link' : request.POST['tiktok_link'],
            'twitter_link' : twitter_link,
            'linkedin_link' : linkedin_link,
            'other_link' : other_link,
            'page_title' : page_title,
            'page_keyword' : page_keyword,
            'page_discription' : page_discription,

        }
        data = {**data,**images}   #merging two dictionary       
         
        if not site_name:
            messages.error(request, "Site_name is mendatory")
            return redirect(request.POST['next'])

        # if not site_name.isalnum(): 
        #     messages.error(request, site_name+" = site name should only contain letters and numbers")
        #     return redirect(request.POST['next'])
        else:
            global_setting = GlobalSettings.objects.filter(site_name=site_name)
            if global_setting and pk==None:
                messages.error(request, "Sitename Already exist")
                return redirect(request.POST['next'])
        if not images == None:
            for i in images:
                try:
                    im = Image.open(images[i])
                except:
                    messages.error(request, "Only images allowed "+str(images[i])+" is not an image in "+str(i))
                    return redirect(request.POST['next'])
        if not site_email:
            messages.error(request, "Site email is mendatory")
            return redirect(request.POST['next'])
        if not site_address:
            messages.error(request, "Site address is mendatory")
            return redirect(request.POST['next'])
        if not page_title:
            messages.error(request, "Page Title is mendatory")
            return redirect(request.POST['next'])
        if not site_contact:
            messages.error(request, "Site Contact Number is mendatory")
            return redirect(request.POST['next'])

        # Creating Object of Model Class
        # Inserting Data into Table
        addingproduct = GlobalSettings.objects.update_or_create(id=pk, defaults=data)#update_or_create method is used to creat data if id not exist. if id is exist then it update on particular id column

        #After Insert open product
        return redirect(GlobalCreate)



