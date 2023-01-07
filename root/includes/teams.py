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
def Teams(request, pk=None):
    slug1 = "Blogs"
    create_link_name = reverse("Teams")
    action = "TeamsStore"
    all_data = Team.objects.all()
    get_data = None
    if pk:
        get_data = Team.objects.get(id=pk)  
    data = {'slug1':slug1,'create':True,'create_link_name':create_link_name, 'p_list':all_data,'t':get_data, 'action':action}
    client_msg = ContactUs.objects.filter(read_unread=True)
    data['client_msg']=client_msg
    return render(request,'admin/teams/teams.html',data)

@login_required(login_url=settings.LOGIN_URL)
def TeamsStore(request,edit_id=None):
    if request.POST:       
        #return HttpResponse()
        count = int(request.POST['count'])
        for i in range(count):
            i=i+1
            teamid = request.POST.get('teamid'+str(i),False)
            if(teamid == ""):
                teamid = None            
            data2 = {
                'name' : request.POST.get('fname'+str(i),False),
                'post' : request.POST.get('fpost'+str(i),False),
                'short_description' :  request.POST.get('fshort_description'+str(i),False),
                'long_contents' :  request.POST.get('flong_contents'+str(i),False),
            }      
            for j in request.FILES:
                if "fimage"+str(i) == j :
                    data2['profile_picture']= request.FILES["fimage"+str(i)]
                    
            if(data2['name'] != "" and data2['post'] != "" ):
                Team.objects.update_or_create(id=teamid, defaults=data2)
                return redirect(Teams)


        messages.error(request,"Name and Post Can Not be empty !")
        return redirect(Teams)

        ###########################
        #messages.DEBUG: 'alert-info',
        # messages.info: 'alert-info',
        # messages.success: 'alert-success',
        # messages.warning: 'alert-warning',
        # messages.error: 'alert-danger',

@login_required(login_url=settings.LOGIN_URL)
def TeamsDelete(request, pk):
    udata = Team.objects.get(id=pk)
    udata.delete()
    messages.error(request, "Requested Member has been Removed. ")
    return redirect(Teams)

