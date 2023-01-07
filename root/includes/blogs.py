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
def Blogs(request):
    slug1 = "Blogs"
    create_link_name = reverse("BlogsCreate")
    all_data = Blog.objects.all()
    data = {'slug1':slug1,'create':True,'create_link_name':create_link_name, 'p_list':all_data}
    client_msg = ContactUs.objects.filter(read_unread=True)
    data['client_msg']=client_msg
    return render(request,'admin/blogs/blogs.html',data)

@login_required(login_url=settings.LOGIN_URL)
def BlogsCreate(request, pk=None):
    create_link_name = reverse("BlogsCreate")
    if pk==None:
        slug1 = "Blogs-Create" 
    else:
        slug1 = "Blogs-Update" 
    action = "BlogsStore"
    #Fetching the data of particular ID
    get_data = None
    if pk:
        # action = "ProductUpdate"
        get_data = Blog.objects.get(id=pk)  
    data = {'slug1':slug1,'create':True,'create_link_name':create_link_name,'id_data':get_data, 'action':action}
    client_msg = ContactUs.objects.filter(read_unread=True)
    data['client_msg']=client_msg
    return render(request, 'admin/blogs/blogs-form.html',data)

@login_required(login_url=settings.LOGIN_URL)
def BlogsStore(request,pk=None):
    if request.POST:       
        title = request.POST['title']
        main_title = request.POST['main_title']
        discription = request.POST['discription']
        author = str(request.user)
        images = {} #dictionary of image
        for im in request.FILES:
            if im == "banner_image":
                images['banner_image'] = request.FILES['banner_image']
            if im == "icon_image":
                images['icon_image'] = request.FILES['icon_image']
        
           
        if not title:
            messages.error(request, "Without title not possible to create a blog ! ")
            return redirect(request.POST['next'])

        if not discription:
            messages.error(request, "You are adding blogs without contants !!!")
            return redirect(request.POST['next'])
     
        data={
            'title' :title,
            'status' : request.POST.get('status',False),
            'discription' :discription,
            'author': author,
            'main_title':main_title,
        }
        data = {**data,**images}   #merging two dictionary       
         
        if not images == None:
            for i in images:
                try:
                    im = Image.open(images[i])
                except:
                    messages.error(request, "Only images allowed "+str(images[i])+" is not an image in "+str(i))
                    return redirect(request.POST['next'])
       
        
        # Creating Object of Model Class
        # Inserting Data into Table
        addingproduct = Blog.objects.update_or_create(id=pk, defaults=data)#update_or_create method is used to creat data if id not exist. if id is exist then it update on particular id column

        #After Insert open product
        return redirect(Blogs)

@login_required(login_url=settings.LOGIN_URL)
def BlogsDelete(request, pk):
    udata = Blog.objects.get(id=pk)
    udata.delete()
    return redirect(Blogs)

