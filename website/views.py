from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from root.models import *
from website.includes.Action import *

#Mail
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


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
        data = {'page':"index",'global_data':global_data,'page_number':page_number,'customers':customers,'clients':clients,'most_ordered':most_ordered,'contact_section':contact_section,'menus':menus,'blog':blog,'product':product,'sliders':sliders,'clientschild':clientschild,'pemplatechild':pemplatechild}
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
    related_product = Products.objects.filter(category_id=product.category_id).order_by('-updated_at')
    # print(product.category_id)
    global_data = GlobalSettings.objects.first()
    data = {'product':product,'global_data':global_data,'menus':menus,'c_id':c_id,'related_product':related_product}
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


def read_template(filename):
    with open(filename, 'r') as template_file:
        template_file_content = template_file.read()
    return template_file_content

 # ishere field [ 1(TRUE) =>wishlist) ], [ 0(false) => cart)]  , 2=> order
# @login_required(login_url=settings.CLIENT_LOGIN_URL)
def CheckOut(request):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    if Wishlist.objects.filter(temp_id=c_id,ishere=False):
        if request.POST: 
            #mail

            MY_ADDRESS = 'fenfit@fenfitnepal.com'
            PASSWORD = 'fenfit@devraj'

            user_info = {
                'name'    : request.POST['name'],
                'phone'   : request.POST['phone'],
                'email'   : request.POST['email'],
                'shpping_address' : request.POST['address'],
                'billing_address' : request.POST['baddress'],
                'current_address' : request.POST['caddress'],
            }

            get_data = GlobalSettings.objects.only('configure_email').first()        
            emails = get_data.configure_email

           # html = html.replace('{{names}}',names)

            try:
                s = smtplib.SMTP(host='mail.fenfitnepal.com', port=587)
                s.starttls()
                s.login(MY_ADDRESS, PASSWORD)
            except:
                messages.info(request,"Connecting To Mail Server Failed !!!")
                return redirect('CheckOut')
            

            for i in Wishlist.objects.filter(temp_id=c_id,ishere=False) :
                total = 0
                html = read_template(os.path.join(BASE_DIR ,'website/templates/main/messages.html'))
                msg = MIMEMultipart()       # create a message
                msg['From']=MY_ADDRESS
                msg['To']=emails
                msg['Subject']="Order Details"

                # This example assumes the image is in the current directory
                fp = open(os.path.join(BASE_DIR ,'website/static/assets/images/logo.png'), 'rb')
                msgImage = MIMEImage(fp.read())
                fp.close()
                
                html = html.replace("{{Name}}",str(user_info['name']))
                html = html.replace("{{Email}}",str(user_info['email']))
                html = html.replace("{{Phone_Number}}",str(user_info['phone']))
                html = html.replace("{{Shipping_Address}}",str(user_info['shpping_address']))
                html = html.replace("{{Billing_Address}}",str(user_info['billing_address']))
                html = html.replace("{{Current_Address}}",str(user_info['current_address']))



                # Define the image's ID as referenced above
                msgImage.add_header('Content-ID', '<image0>')
                msg.attach(msgImage)
                shipping_data = {                   
                    'product_id' : i.product_id,
                    'product_quantity' : i.quantity,
                    'product_color' : i.color,
                    'product_size' : i.size
                }
                html = html.replace("{{shipping_data['product_quantity']}}",str(shipping_data['product_quantity']))
                html = html.replace("{{shipping_data['product_color']}}",str(shipping_data['product_color']))
                html = html.replace("{{shipping_data['product_size']}}",str(shipping_data['product_size']))

                j = Products.objects.filter(id=shipping_data['product_id']).first()
                product_data = {
                    'product_name' : j.name,
                    'product_price' : j.price,
                    'product_image' : j.image1,
                    'most_ordered' : j.most_ordered,
                }
                if(product_data['most_ordered'] != None):
                    temp_mostordered = int(product_data['most_ordered']) + 1
                else :
                    temp_mostordered = 1
                Products.objects.filter(id=shipping_data['product_id']).update(most_ordered=temp_mostordered)


                html = html.replace("{{product_data['product_name']}}",str(product_data['product_name']))
                html = html.replace("{{product_data['product_price']}}",str(product_data['product_price']))
                fp = open(os.path.join(BASE_DIR ,"media/"+str(product_data['product_image'])), 'rb')
                msgImage = MIMEImage(fp.read())
                fp.close()       
                msgImage.add_header('Content-ID', '<image1>')
                msg.attach(msgImage)  

                total =   int(shipping_data['product_quantity']) * int(product_data['product_price'])  
                html = html.replace("{{total}}",str(total))
                msg.attach(MIMEText(html, 'html'))
                s.send_message(msg)
                del msg
            # Terminate the SMTP session and close the connection
            s.quit()
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

def Custom(request):
    try:
        c_id = request.COOKIES['c_id']
    except:
        return redirect('website.index')
    
    if request.POST: 

        MY_ADDRESS = 'fenfit@fenfitnepal.com'
        PASSWORD = 'fenfit@devraj'
        user_info = {
            'name'    : request.POST['name'],
            'phone'   : request.POST['phone'],
            'email'   : request.POST['email'],
            'shpping_address' : request.POST['address'],
            'billing_address' : request.POST['baddress'],
            'current_address' : request.POST['caddress'],
            'product_name'    : request.POST['product_name'],
            'size'   : request.POST['size'],
            'color'   : request.POST['color'],
            'quantity'   : request.POST['number'],
        }
        get_data = GlobalSettings.objects.only('configure_email').first()        
        emails = get_data.configure_email

        # html = html.replace('{{names}}',names)
        try:
            s = smtplib.SMTP(host='mail.fenfitnepal.com', port=587)
            s.starttls()
            s.login(MY_ADDRESS, PASSWORD)
        except:
            messages.info(request,"Connecting To Mail Server Failed !!!")
            return redirect('website.index') 

        html = read_template(os.path.join(BASE_DIR ,'website/templates/main/custom-messages.html'))
        msg = MIMEMultipart()       # create a message
        msg['From']=MY_ADDRESS
        msg['To']=emails
        msg['Subject']="Order Details"

        # This example assumes the image is in the current directory
        fp = open(os.path.join(BASE_DIR ,'website/static/assets/images/logo.png'), 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        
        html = html.replace("{{product_name}}",str(user_info['product_name']))
        html = html.replace("{{size}}",str(user_info['size']))
        html = html.replace("{{color}}",str(user_info['color'])) 
        html = html.replace("{{quantity}}",str(user_info['quantity'])) 
        html = html.replace("{{Name}}",str(user_info['name']))
        html = html.replace("{{Email}}",str(user_info['email']))
        html = html.replace("{{Phone_Number}}",str(user_info['phone']))
        html = html.replace("{{Shipping_Address}}",str(user_info['shpping_address']))
        html = html.replace("{{Billing_Address}}",str(user_info['billing_address']))
        html = html.replace("{{Current_Address}}",str(user_info['current_address']))



        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<image0>')
        msg.attach(msgImage)     
       
        msg.attach(MIMEText(html, 'html'))
        s.send_message(msg)
        del msg
        # Terminate the SMTP session and close the connection
        s.quit()

        messages.info(request,"Successfully Orderd ! We will contact you very Soon. ")
        return redirect('website.index')            

    else:
        messages.error(request,"Please Try Again !!!")
        return redirect('website.index')


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


      
   