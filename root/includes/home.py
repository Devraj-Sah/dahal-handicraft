from logging import NullHandler
from struct import pack
from unicodedata import category
from urllib import response
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



@login_required(login_url=settings.LOGIN_URL)
def HomeNavigationList(request,id=None):
    slug1 = "Home Navigation"
    create_link_name = reverse("HomeNavigationCreate")
    all_data = HomeNavigation.objects.filter(parent_page_id=0)
    # for cat in all_data:
        # return HttpResponse(cat.product)
    open = None
    create=False
    if id:
        create=True
        open = "open"
        all_data = HomeNavigation.objects.filter(parent_page_id=id)
        create_link_name = reverse("HomeSubNavigationCreate", args=[id])
        #return HttpResponse(create_link_name)
        
    data = {'slug1':slug1,'create':create,'create_link_name':create_link_name,'all_data':all_data,'open':open}
    client_msg = ContactUs.objects.filter(read_unread=True)
    data['client_msg']=client_msg
    return render(request, 'admin/homenavigation/navigation-list.html',data)

@login_required(login_url=settings.LOGIN_URL)
def HomeNavigationCreate(request,edit_id=None,parent_id=None):
    title = "Home Navigation-create" 
    action = "HomeNavigationStore"
    page_type = PageType.objects.all()
    category = HomeNavigation.objects.all()
    team = Team.objects.all()
    edit_id_data = None
    parent_data = None #importent to create main navigation
    getposition = None

    if edit_id:
        edit_id_data = HomeNavigation.objects.get(id=edit_id) #it is used for edit form. 
        try:      
            parent_data = HomeNavigation.objects.get(id=edit_id_data.parent.id) #this is used to create subcategory where parent_page_id is parent_page_id
        except:
            None
            
        #auto position
    if edit_id == None and parent_id==None: # Means creating main navigation
        position = []
        for i in category.filter(parent_page_id = 0):
            position.append(i.position)
        if position:
            getposition = max(position) + 1

    if parent_id:
        parent_data = HomeNavigation.objects.get(id=parent_id)
        position = []
        #Means creating sub navigation
        for i in category.filter(parent_page_id = parent_id):
            position.append(i.position)
        if position:
            getposition = max(position) + 1
    
    
    data = {
        'slug1':title,
        'create':True,
        'id_data':edit_id_data, 
        'action':action,
        'page_type':page_type,
        'category':category,
        'parent_data':parent_data,
        'team':team,
        'position' : getposition
    }
    client_msg = ContactUs.objects.filter(read_unread=True)
    data['client_msg']=client_msg
    return render(request, 'admin/homenavigation/navigation-form.html',data)

@login_required(login_url=settings.LOGIN_URL)
def HomeNavigationStore(request,edit_id=None):
    if request.POST:
        images = {} #dictionary of image
        for im in request.FILES:
            if im == "image1":
                images['banner_image1'] = request.FILES['image1']
            if im == "image2":
                images['banner_image2'] = request.FILES['image2']
            if im == "image3":
                images['icon_image'] = request.FILES['image3']

        parent_page_id = request.POST['parent_page_id']
        if parent_page_id:
            if parent_page_id=="0":
                parent_id = '' #parent id is set to null if parent_page_id == 0 . if not set  to null then error
            else:
                parent_id = parent_page_id #parent_id is always equal to parent_page_id
            pass
        else:
            messages.error(request, "parent page id passing null , instead of 0. plz contact admin")
            return redirect(request.POST['next'])
        #return HttpResponse(request.POST['status'])
        data = {
            'name' : request.POST['name'],
            'parent_page_id' : request.POST['parent_page_id'],
            'caption' : request.POST['caption'],
            'status' : request.POST['status'],
            'page_type' : request.POST['page_type'],
            'title' : request.POST['title'],
            'short_description' : request.POST['short_description'],
            'long_contents' : request.POST['long_contents'],
            'meta_title' : request.POST['meta_title'],
            'keyword' : request.POST['keyword'],
            'position' : request.POST['position'],
            'parent_id' : parent_id,              
        }
        if edit_id != None:
            force = request.POST.get('force',False)
            if force != "force":
                count = 0
                category = HomeNavigation.objects.filter(parent_page_id=data['parent_page_id'],position=data['position'])
                for i in category:
                    if i.id != edit_id:                        
                        count += 1                
                if (count >= 1) :
                    messages.info(request, "This position " + data['position'] + " already exist - 404 Conflict <input type='hidden' id='newposition' name='newposition' value='"+data['position']+"'>  <input type='hidden' name='force' value='force'> <button id='force' onsubmit='changeTextForce' type='submit' class='btn btn-success text-white' style='float: right; margin-top: -7px;'> <i class='fa fa-check'></i> Force Save</button> ")
                    return redirect(request.POST['next'])

 
        data = {**data,**images}   #merging two dictionary
        addingproduct = HomeNavigation.objects.update_or_create(id=edit_id, defaults=data)#update_or_create method is used to creat data if id not exist. if id is exist then it update on particular id column
        messages.success(request, 'Navigation created sucessfully!!!.')
        return redirect("HomeNavigationList",id = request.POST['parent_page_id']) #second way to redirect back
       
       

@login_required(login_url=settings.LOGIN_URL)
def HomeNavigationDelete(request,id):
    nav_obj = HomeNavigation.objects.get(id=id)
    nav_obj.delete()
    messages.success(request, 'Navigation Deleted sucessfully!!!.')
    return redirect(request.META.get('HTTP_REFERER'))