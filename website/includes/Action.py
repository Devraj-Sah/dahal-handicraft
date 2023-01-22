from ast import Return
from django.http import HttpResponse
from django.urls import reverse
from root.models import *
from django.shortcuts import render
from django.shortcuts import redirect
import random
from django.core.paginator import Paginator

def CategoryAction(request,page_type,page_detail,c_id=None):
    menus = Navigation.objects.filter(parent_page_id=0).order_by('position')
    page_types = PageType.objects.all()
    # nav = Navigation.objects.filter(id=page_detail.first().id)
    # product = nav.product.all()
    #page_detail.first().name
    all_product = Products.objects.filter(status=1)  
    # team = Team.objects.all()
    blog = Blog.objects.filter(status=1).order_by('-updated_at')[:6]
    global_data = GlobalSettings.objects.first()
    # wishvalue = Wishlist.objects.filter(temp_id=c_id,ishere=True)
    cartvalue = Wishlist.objects.filter(temp_id=c_id,ishere=False)
    # wishvalue = len(wishvalue)
    cartvalue = len(cartvalue)

    product = None
    about = None
    for i in page_types:      
        if page_type==i.page_name :   
            if page_type == 'normal':
                # return HttpResponse("normal")
                about = Navigation.objects.filter(page_type='normal').all().first()
                # return HttpResponse(about.name)
            # if page_type == 'product':
            #     return HttpResponse("product")
            if page_type == 'sale':
                product = Paginator(all_product, 16)
                page_number = request.GET.get('page')
                product = product.get_page(page_number)
            # if page_type == 'blog':
            #     return HttpResponse("blog")
            # if page_type == 'contact':
            #     return HttpResponse("contact")

            data = {'menus':menus,'global_data':global_data,'all_product':all_product,'product':product,'about':about,
                    'team':'team','page_detail':page_detail,'blog':blog, 'c_id':c_id, 'wishvalue':'wishvalue', 'cartvalue':cartvalue
                }
            return render(request,'main/'+page_type+'.html',data)

      
    return redirect('website.index')
            # return reverse("SubNavigationCreate", args=[id])


def SubcategoryAction(request,page_type,page_detail,c_id=None,submenu=None):
    menus = Navigation.objects.filter(parent_page_id=0).order_by('position')
    breadcom = menus.first().caption
    page_types = PageType.objects.all()
    # nav = Navigation.objects.filter(id=page_detail.first().id)
    # product = nav.product.all()
    #page_detail.first().name
    # team = Team.objects.all()
    # blog = Blog.objects.filter(status=1)
    global_data = GlobalSettings.objects.first()

    # wishvalue = Wishlist.objects.filter(temp_id=c_id,ishere=True)
    cartvalue = Wishlist.objects.filter(temp_id=c_id,ishere=False)
    # wishvalue = len(wishvalue)
    cartvalue = len(cartvalue)

    product = None

    for i in page_types:      
        if page_type==i.page_name :  
            # if page_type == 'normal':
            #     return HttpResponse("normal")
            # if page_type == 'product':
            #     return HttpResponse("product")
            if page_type == 'sale':
                nav_id = Navigation.objects.filter(name = submenu).get()
                all_product = Products.objects.filter(category_id = nav_id.id, status=1 )  
                # return HttpResponse(print (all_product))
                if all_product != None:
                    product = Paginator(all_product, 9)
                    page_number = request.GET.get('page')
                    product = product.get_page(page_number)
            # if page_type == 'blog':
            #     return HttpResponse("blog")
            # if page_type == 'contact':
            #     return HttpResponse("contact")

            data = {'menus':menus,'global_data':global_data,'all_product':all_product,'product':product,
                    'team':'team','page_detail':page_detail,'blog':'blog', 'c_id':c_id, 'wishvalue':'wishvalue', 'cartvalue':cartvalue
                } 
            return render(request,'main/'+page_type+'.html',data)