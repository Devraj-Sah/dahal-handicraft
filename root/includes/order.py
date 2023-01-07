from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from ..models import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from .decorators import customized_user_passes_test,is_admin_role

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def CustomerOrder(request, pk=None, pdc=None):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    slug1 = "Order"
    all_data = Order.objects.filter(pdc=None).order_by('-updated_at')   
    if pk and pdc:
         Order.objects.filter(id=pk).update(pdc=pdc)  
    data = {'slug1':slug1,'create':False, 'all_data':all_data,'action':True}
    client_msg = ContactUs.objects.filter(read_unread=True)
    data['client_msg']=client_msg
    return render(request,'admin/customer_orders/order.html',data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def Orders(request, pk=None, pdc=None):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    slug1 = "Order"
    all_data = Order.objects.filter(pdc=None).order_by('-updated_at')   
    if pk and pdc:
         Order.objects.filter(id=pk).update(pdc=pdc)  
    data = {'slug1':slug1,'create':False, 'all_data':all_data,'action':True}
    client_msg = ContactUs.objects.filter(read_unread=True)
    data['client_msg']=client_msg
    return render(request,'admin/order/order.html',data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def Pending(request, pk=None, pdc=None):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    slug1 = "Pending Orders"
    all_data = Order.objects.filter(pdc="p").order_by('-updated_at')   
    if pk and pdc:
         Order.objects.filter(id=pk).update(pdc=pdc)  
    data = {'slug1':slug1,'create':False, 'all_data':all_data,'action':True}
    client_msg = ContactUs.objects.filter(read_unread=True)
    data['client_msg']=client_msg
    return render(request,'admin/order/order.html',data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def Delivered(request):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    slug1 = "Delivered Orders"
    all_data = Order.objects.filter(pdc="d").order_by('-updated_at')   
    data = {'slug1':slug1,'create':False, 'all_data':all_data,'action':False}
    client_msg = ContactUs.objects.filter(read_unread=True)
    data['client_msg']=client_msg
    return render(request,'admin/order/order.html',data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def CanclelledOrders(request):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('index_ecom')
    slug1 = "Canclelled Orders"
    all_data = Order.objects.filter(pdc="c").order_by('-updated_at')   
    data = {'slug1':slug1,'create':False, 'all_data':all_data,'action':False}
    client_msg = ContactUs.objects.filter(read_unread=True)
    data['client_msg']=client_msg
    return render(request,'admin/order/order.html',data)
