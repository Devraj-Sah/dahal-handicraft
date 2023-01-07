from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from root.models import *
from website.includes.Action import *

# Create your views here.
def index(request):        
        # return render(request, 'index.html')
        menus = Navigation.objects.filter(parent_page_id=0).order_by('position')
        blog = Blog.objects.filter(status=1).order_by('-updated_at')[:3]
        sliders = HomeNavigation.objects.filter(page_type='sale')
        contact_section = HomeNavigation.objects.filter(page_type='contact').all().first()
        clients = HomeNavigation.objects.filter(page_type='blog')
        customers = HomeNavigation.objects.filter(page_type='normal').order_by('-updated_at')[:3]
        # return HttpResponse(contact_section.caption)
        # top3 = Navigation.objects.filter(page_type='sale')
        clientsobj = HomeNavigation.objects.filter(name='clients').all().first()
        clientschild = []
        if clientsobj:
                clientschild = clientsobj.childs.all()
        pemplateobj = HomeNavigation.objects.filter(name='pemplate').all().first()
        pemplatechild = []
        if pemplateobj:
                pemplatechild = pemplateobj.childs.all()
        ftn = request.GET.get('ftn')
        if ftn:
                product = Products.objects.filter(ftn=ftn)  
        else:
                all_product = Products.objects.all().order_by('-created_at')
        
        most_ordered = Products.objects.all().order_by('-most_ordered')[:6]

        product = Paginator(all_product, 6)
        page_number = request.GET.get('page')
        product = product.get_page(page_number) 

        global_data = GlobalSettings.objects.first()
        data = {'page':"index",'global_data':global_data,'customers':customers,'clients':clients,'most_ordered':most_ordered,'contact_section':contact_section,'menus':menus,'blog':blog,'product':product,'sliders':sliders,'clientschild':clientschild,'pemplatechild':pemplatechild}
        try:
            c_id = request.COOKIES['c_id']
            cartvalue = Wishlist.objects.filter(temp_id=c_id,ishere=False)
            cartvalue = len(cartvalue)
            data['cartvalue'] = cartvalue
            return render(request, 'index.html',data)
        except:       
            rand_num = random.randint(100000,1000000)
            data['c_id'] = rand_num
            a = render(request, 'index.html',data)
            a.set_cookie(key="c_id", value=rand_num,max_age=100000000)
            return a
def Category(request, menu):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    page_detail = Navigation.objects.filter(name=menu) ##to display contants
    if Navigation.objects.filter(name=menu).first():
        page_type = Navigation.objects.filter(name=menu).first().page_type
    else:
        page_type = None
    # return HttpResponse(page_type)
    return CategoryAction(request,page_type,page_detail,c_id)   

def SubCategory(request, menu , submenu ):
    if menu=='admin':
        return redirect('/') #if user(client) input admin as menu then redirect to home
    else:
        if Navigation.objects.filter(name=submenu).first()==None: #if user input rough url then redirect to home
            return redirect('/')
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    page_detail = Navigation.objects.filter(name=submenu)
    if Navigation.objects.filter(name=submenu).first():
        page_type = Navigation.objects.filter(name=submenu).first().page_type
    else:
        page_type = None
    page_type = Navigation.objects.filter(name=submenu).first().page_type
    return SubcategoryAction(request,page_type,page_detail,c_id,submenu)   
    # return SubcategoryAction(request,page_type,menu,submenu)

def ProductDetail(request,id):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    menus = Navigation.objects.filter(parent_page_id=0).order_by('position')
    product = Products.objects.get(id=id) 
    global_data = GlobalSettings.objects.first()
    data = {'product':product,'global_data':global_data,'menus':menus,'c_id':c_id}
    return render(request, 'main/product-details.html',data)

def BlogDetail(request,id):
    menus = Navigation.objects.filter(parent_page_id=0).order_by('position')
    blog = Blog.objects.get(id=id) 
    global_data = GlobalSettings.objects.first()
    data = {'blog_detail':blog,'global_data':global_data,'menus':menus}
    return render(request, 'main/normal.html',data)

def WishList(request, p_id=None ,c_id=None):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    if p_id and c_id :
        if request.POST:
            data = {
                'size' : request.POST['size'],
                'quantity' : request.POST['number'],
                'color' : request.POST['color'], 
                'product_id' : p_id,
                'temp_id' : c_id
            }
            addingwishes = Wishlist.objects.update_or_create(temp_id=c_id,product_id=p_id,ishere=True,defaults=data)
            return redirect('WishList')
        else:
            data = {
                'product_id' : p_id,
                'temp_id' : c_id,
                'quantity' : 1,
            }
            addingwishes = Wishlist.objects.update_or_create(temp_id=c_id,product_id=p_id,ishere=True,defaults=data)
            return redirect('WishList')
    menus = Navigation.objects.filter(parent_page_id=0).order_by('position')
    wishlist = Wishlist.objects.filter(temp_id=c_id,ishere=True)
    global_data = GlobalSettings.objects.first()
    data = {'menus':menus,'global_data':global_data ,'wishlist':wishlist,'c_id':c_id}
    wishvalue = Wishlist.objects.filter(temp_id=c_id,ishere=True)
    cartvalue = Wishlist.objects.filter(temp_id=c_id,ishere=False)
    data['wishvalue'] = len(wishvalue)
    data['cartvalue'] = len(cartvalue)
    return render(request, 'main/wish-list.html', data)

def Cart(request, p_id=None ,c_id=None):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    if p_id and c_id :
        if request.POST:           
            data = {
                'size' : request.POST['size'],
                'quantity' :  request.POST['number'],
                'color' : request.POST['color'], 
                'product_id' : p_id,
                'temp_id' : c_id,
                'user_id' : request.user.id,
                'ishere' : False
            }
            addingwishes = Wishlist.objects.update_or_create(temp_id=c_id,product_id=p_id,ishere=False,defaults=data)
            return redirect('Cart')
        else:
            data = {
                'product_id' : p_id,
                'temp_id' : c_id,
                'ishere' : False
            }
            addingwishes = Wishlist.objects.update_or_create(temp_id=c_id,product_id=p_id,ishere=False,defaults=data)
            deleteifcolide = Wishlist.objects.filter(temp_id=c_id,product_id=p_id,ishere=True)
            deleteifcolide.delete()
            return redirect('Cart')
    menus = Navigation.objects.filter(parent_page_id=0).order_by('position')
    wishlist = Wishlist.objects.filter(temp_id=c_id,ishere=False)
    global_data = GlobalSettings.objects.first()
    data = {'menus':menus,'global_data':global_data, 'wishlist':wishlist,'c_id':c_id}
    wishvalue = Wishlist.objects.filter(temp_id=c_id,ishere=True)
    cartvalue = Wishlist.objects.filter(temp_id=c_id,ishere=False)
    data['wishvalue'] = len(wishvalue)
    data['cartvalue'] = len(cartvalue)
    return render(request, 'main/cart.html', data)

def WishListDelete(request, p_id, pk, next):
    udata = Wishlist.objects.filter(temp_id=pk,product_id=p_id)
    udata.delete()
    if next=="cart":
        return redirect('Cart')
    elif next=="wish":
        return redirect('WishList')
    else:
        return redirect('website.index')

 # ishere field [ 1(TRUE) =>wishlist) ], [ 0(false) => cart)]  , 2=> order
@login_required(login_url=settings.CLIENT_LOGIN_URL)
def CheckOut(request):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    if Wishlist.objects.filter(temp_id=c_id,ishere=False):
        if request.POST:        
            for i in Wishlist.objects.filter(temp_id=c_id,ishere=False) :
                shipping_data = {
                    'user_id' : request.user.id,
                    'name'    : request.POST['name'],
                    'phone'   : request.POST['phone'],
                    'email'   : request.POST['email'],
                    'shpping_address' : request.POST['address'],
                }
                ship =  Shipping.objects.create(**shipping_data)
                data = {
                    'user_detail' : request.POST['name'],
                    'phone' :  request.POST['phone'],
                    'shipping_address' : request.POST['address'], 
                    'user_id' : request.user.id, 
                    'product_id' : i.product_id,
                    'product_details' : i.quantity,
                    'get_shipping_address_id' : ship.id,
                }
             
                Order.objects.create(**data)
                # Order.objects.update_or_create(product_id=data['product_id'],user_id=c_id,defaults=data)
            messages.info(request,"Successfully Orderd ! We will contact you very Soon. ")
            Wishlist.objects.filter(temp_id=c_id,ishere=False).update(ishere=2)
            return redirect('Cart')            
        menus = Navigation.objects.filter(parent_page_id=0).order_by('position')
        global_data = GlobalSettings.objects.first()
        data = {'page':"index",'global_data':global_data,'menus':menus}  
        wishvalue = Wishlist.objects.filter(temp_id=c_id,ishere=True)
        cartvalue = Wishlist.objects.filter(temp_id=c_id,ishere=False)
        data['wishvalue'] = len(wishvalue)
        data['cartvalue'] = len(cartvalue)
        return render(request, 'main/checkout.html', data)

    else:
        messages.error(request,"Please add to Cart. Before Checkout")
        return redirect('Cart')

def Contactus(request):
    data = {
        'name' : request.POST['name'],
        'email' :  request.POST['email'],
        'subject' : request.POST['subject'], 
        'message' : request.POST['message'], 
    }
    ContactUs.objects.create(**data)
    messages.error(request,"You Message has been Sent Successfully !")
    return redirect('/about-us')


def Login(request):
    return render(request, 'main/login.html')


def Signup(request):
    return render(request, 'main/register.html')


      
   