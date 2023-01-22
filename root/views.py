# from asyncio.windows_events import NULL
import datetime
from itertools import product
from logging import NullHandler
from pickle import FALSE
from struct import pack
from unicodedata import category
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from PIL import Image

from account.models import CustomUser
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse

#For Data Import and export
import pandas as pd
from .includes.decorators import customized_user_passes_test,is_admin_role,is_admin_group
from .includes.serializers import ProductsSerializer
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from wsgiref.util import FileWrapper
from django.shortcuts import redirect
from django.core.paginator import Paginator


@login_required(login_url=settings.LOGIN_URL)
# @customized_user_passes_test(is_admin_role)
@customized_user_passes_test(is_admin_role)
def index(request, pk=None, pdc=None):
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)

    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    # return  HttpResp  onse(today_max)

    # try:
    #     c_id = request.COOKIES['c_id']
    # except:
    #     return redirect('website.index')
    slug1 = "Order"
    all_data = Order.objects.filter(pdc=None).order_by('-updated_at')
    pending = Order.objects.filter(pdc='p').order_by('-updated_at')
    delivered = Order.objects.filter(pdc='d').order_by('-updated_at')
    cancelled = Order.objects.filter(pdc='c').order_by('-updated_at')
    today_order = Order.objects.filter(created_at__range=(today_min, today_max)).count()
    today_income=0
    total_users = CustomUser.objects.all().count()
    for eachorder in Order.objects.filter(pdc='d',created_at__range=(today_min, today_max)):
        try:
            eachorder_quantity = eachorder.product_details
            eachorder_price = eachorder.product.price
            eachorder_discount = eachorder.product.discount
            price_after_discount = int(eachorder_price)-int(eachorder_discount)
            full_price_with_quantity = price_after_discount*int(eachorder_quantity)
            today_income = today_income + full_price_with_quantity
        except:
            pass

    total_income = 0
    for eachorder in Order.objects.filter(pdc='d'):
        try:
            eachorder_quantity = eachorder.product_details
            eachorder_price = eachorder.product.price
            eachorder_discount = eachorder.product.discount
            price_after_discount = int(eachorder_price)-int(eachorder_discount)
            full_price_with_quantity = price_after_discount*int(eachorder_quantity)
            total_income = total_income + full_price_with_quantity
        except:
            pass

    if pk and pdc:
         Order.objects.filter(id=pk).update(pdc=pdc)  

    data = {'total_users':total_users,'total_income':total_income,'today_income':today_income,'today_order':today_order,'slug1':slug1,'create':False, 'all_data':all_data,'action':True,'pending':pending,'delivered':delivered,'cancelled':cancelled}
    client_msg = ContactUs.objects.filter(read_unread=True)
    data['client_msg']=client_msg
    # data = {'total_users':"",
    #         'total_income':"",
    #         'today_income':"",
    #         'today_order':"",
    #         'slug1':"",
    #         'create':False, 
    #         'all_data':"",
    #         'action':True,'pending':"",'delivered':"",'cancelled':""}
    # data['client_msg']=""
    return render(request,'admin/home.html',data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def NavigationList(request,id=None):
    slug1 = "Navigation"
    create_link_name = reverse("NavigationCreate")
    all_data = Navigation.objects.filter(parent_page_id=0)
    open = None
    if id:
        open = "open"
        all_data = Navigation.objects.filter(parent_page_id=id)
        create_link_name = reverse("SubNavigationCreate", args=[id])
        
    data = {'slug1':slug1,'create':True,'create_link_name':create_link_name,'all_data':all_data,'open':open}
    client_msg = ContactUs.objects.filter(read_unread=True)
    data['client_msg']=client_msg
    return render(request, 'admin/navigation/navigation-list.html',data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def NavigationCreate(request,edit_id=None,parent_id=None):
    # return HttpResponse(parent_id)
    title = "Navigation-create" 
    action = "NavigationStore"
    page_type = PageType.objects.all()
    category = Navigation.objects.all()
    team = Team.objects.all()
    edit_id_data = None
    parent_data = None #importent to create main navigation
    getposition = None

    if edit_id:
        edit_id_data = Navigation.objects.get(id=edit_id) #it is used for edit form. 
        try:      
            parent_data = Navigation.objects.get(id=edit_id_data.parent.id) #this is used to create subcategory where parent_page_id is parent_page_id
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
        parent_data = Navigation.objects.get(id=parent_id)
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
    return render(request, 'admin/navigation/navigation-form.html',data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def NavigationStore(request,edit_id=None):
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
                category = Navigation.objects.filter(parent_page_id=data['parent_page_id'],position=data['position'])
                for i in category:
                    if i.id != edit_id:                        
                        count += 1                
                if (count >= 1) :
                    messages.info(request, "This position " + data['position'] + " already exist - 404 Conflict <input type='hidden' id='newposition' name='newposition' value='"+data['position']+"'>  <input type='hidden' name='force' value='force'> <button id='force' onsubmit='changeTextForce' type='submit' class='btn btn-success text-white' style='float: right; margin-top: -7px;'> <i class='fa fa-check'></i> Force Save</button> ")
                    return redirect(request.POST['next'])

 
        data = {**data,**images}   #merging two dictionary
        addingproduct = Navigation.objects.update_or_create(id=edit_id, defaults=data)#update_or_create method is used to creat data if id not exist. if id is exist then it update on particular id column
        messages.success(request, 'Navigation created sucessfully!!!.')
        return redirect("NavigationList",id = request.POST['parent_page_id']) #second way to redirect back
       
       

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def NavigationDelete(request,id):
    nav_obj = Navigation.objects.get(id=id)
    nav_obj.delete()
    messages.success(request, 'Navigation Deleted sucessfully!!!.')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def ProductList(request, pk=None, ftn=None):
    slug1 = "Product"
    create_link_name = reverse("ProductCreate")
    export_link_name = reverse("ExportProduct")
    if pk and ftn:
        Products.objects.filter(id=pk).update(ftn=ftn)

    all_data = Products.objects.all().order_by('-updated_at')
    product = Paginator(all_data, 10)
    page = request.GET.get('page')
    products = product.get_page(page)
    # return HttpResponse(product)
    
    data = {'slug1':slug1,'export':True,'create':True,'create_link_name':create_link_name,'export_link_name':export_link_name, 'p_list':products}
    client_msg = ContactUs.objects.filter(read_unread=True)
    data['client_msg']=client_msg
    return render(request,'admin/products/product-list.html',data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def ProductCreate(request, pk=None):
    create_link_name =  reverse("ProductCreate")
    if pk==None:
        slug1 = "product-create" 
    else:
        slug1 = "product-update" 
    action = "ProductStore"
    category = Navigation.objects.filter(page_type="Sale")
    #Fetching the data of particular ID
    get_data = None
    if pk:
        # action = "ProductUpdate"
        get_data = Products.objects.get(id=pk)  
    data = {'slug1':slug1,'import':True,'create':True,'create_link_name':create_link_name,'id_data':get_data, 'action':action,'category':category}
    client_msg = ContactUs.objects.filter(read_unread=True)
    data['client_msg']=client_msg
    return render(request, 'admin/products/product-form.html',data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def ProductStore(request,pk=None):
    if request.POST:
        # Data come from HTML to View
        #print(request.FILES['image1'])
        #return HttpResponse(request.POST.items())
        pname = request.POST['product_name']
        category = request.POST['category']
        price = request.POST['price']
        dtype = request.POST['discount_type']
        discount = request.POST['discount']
        status = request.POST['status']
        payment_type = request.POST['payment_type']
        vendor = request.POST['vendor']
        brand = request.POST['brand']
        title = request.POST['title']
        discription = request.POST['discription']
        long_contents = request.POST['long_contents']
        meta_title = request.POST['meta_title']
        keyword = request.POST['keyword']
        images = {} #dictionary of image
        for i in request.FILES:#adding filled image in dictionary.if image is empty then not add to dictionary
            if(i==i):
                images[i] = request.FILES[i]
        
        data = {
            'name' : pname,
            'category_id' : category,
            'price' : price,
            'discount_type' : dtype,
            'discount' : discount,
            'status' :status,
            'payment_type' : payment_type,
            'vendor' : vendor,
            'brand' : brand, 
            'color' : request.POST['color'], 
            'size' : request.POST['size'], 
            'title' : title,
            'discription' : discription,
            'long_contents' : long_contents,
            'meta_title' : meta_title,
            'keyword' : keyword,
            'most_ordered' : 0
        }
        data = {**data,**images}   #merging two dictionary       
        # return HttpResponse(data['size'])
        if not pname:
            messages.error(request, "Productname name should not be empty")
            return redirect(request.POST['next'])
        else:
            Product = Products.objects.filter(name=pname)
            if Product and pk==None:
                messages.error(request, "Product Already exist")
                return redirect(request.POST['next'])
        if not images == None:
            for i in images:
                try:
                    im = Image.open(images[i])
                except:
                    messages.error(request, "Only images allowed "+str(images[i])+" is not an image in "+str(i))
                    return redirect(request.POST['next'])
        if not category:
            messages.error(request, "Category is mendatory")
            return redirect(request.POST['next'])
        if not price:
            messages.error(request, "Price is mendatory")
            return redirect(request.POST['next'])
        # if not dtype:
        #     messages.error(request, "DiscountType is mendatory")
        #     return redirect(request.POST['next'])

        # Creating Object of Model Class
        # Inserting Data into Table
        addingproduct = Products.objects.update_or_create(id=pk, defaults=data)#update_or_create method is used to creat data if id not exist. if id is exist then it update on particular id column

        #After Insert open product
        messages.success(request, 'Product Inserted sucessfully!!!.')
        return redirect(ProductList)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def ProductDelete(request, pk):
    udata = Products.objects.get(id=pk)
    udata.delete()
    messages.success(request, 'product deleted sucessfully!!!.')
    return redirect(ProductList)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def AddProduct(request):
    if request.FILES:
        excel_upload_obj = ExcelFileUpload.objects.create(excel_file_upload=request.FILES['file'])
        df = pd.read_excel(f"{settings.MEDIA_ROOT}/{excel_upload_obj.excel_file_upload}")
        for i in df.values.tolist():
            data={
                'name' : i[0],
                'price' : i[1],
                'discount_type' : i[2]
            }            
            Products.objects.create(**data)
        messages.success(request, 'product Created sucessfully!!!.')
        return redirect(ProductList)        
    messages.success(request, 'Something Went Wrong')
    return redirect(ProductList) 

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def ClientMessage(request, id):
    slug1 = "Client Messages"
    ContactUs.objects.update(read_unread=False)
    client_msg = ContactUs.objects.filter(read_unread=True) #notification
    client_details = ContactUs.objects.filter(id=id).first()
    data = {'slug1':slug1,'create':False,'client_msg':client_msg,'client_details':client_details}
    return render(request, 'admin/clients_messages/client-msg-details.html',data)
    return HttpResponse('okay')

class ExportProduct(LoginRequiredMixin,APIView):

    def get(self,request):
        product_objs = Products.objects.all()
        serializer = ProductsSerializer(product_objs, many=True)
        df = pd.DataFrame(serializer.data)
        # tempname=uuid.uuid4()
        # df.to_excel(f"Ecommerce/static/excel/{tempname}.xlsx")
        # file_path = os.path.join(settings.STATIC_URL, 'excel/'+str(tempname)+'.xlsx')
        # return redirect(file_path)


        # inquiry_form = Products.objects.all()
        # data_list = []
        # for i in inquiry_form:
        #     data = i.__dict__
        #     data_list.append(data)
        # df = pd.DataFrame(df)
          
        total_data = df.iloc[:,]
        response = HttpResponse(content_type='csv')
        response['Content-Disposition'] = 'attachment; filename=products_form.csv'
        total_data.to_csv(path_or_buf=response)
        return response
       
