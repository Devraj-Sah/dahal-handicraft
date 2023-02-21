from django.db import models
from django.conf import settings
from django.contrib.humanize.templatetags import humanize

# Create your models here.
class PageType(models.Model):
    page_name =  models.CharField(max_length=255)  
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return "{page_name:"+self.page_name+","+"status:"+str(self.status)+"}"

class Navigation(models.Model):
    # product = models.ForeignKey('Products',on_delete=models.CASCADE,null=True)
    parent = models.ForeignKey('self', related_name="childs",on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255)
    parent_page_id = models.IntegerField(default=0)
    caption = models.CharField(max_length=255 , null=True)
    status = models.BooleanField(default=True)
    page_type = models.CharField(max_length=255,null=False,default=False)
    title = models.CharField(max_length=500,null=True)
    short_description = models.CharField(max_length=3000, null=True)
    long_contents = models.TextField(max_length=255,null=True)
    meta_title = models.CharField(max_length=255,null=True)
    keyword = models.CharField(max_length=255,null=True)
    position = models.IntegerField()
    banner_image1 = models.ImageField(upload_to='navigation/banner1', null=True)
    banner_image2 = models.ImageField(upload_to='navigation/banner2', null=True)
    icon_image = models.ImageField(upload_to='navigation/icon', null=True)
    created_at = models.DateTimeField(auto_now=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    @property
    def getBannerImage1(self):
        if self.banner_image1 :
            return self.banner_image1.url
        return ''

class HomeNavigation(models.Model):
    # product = models.ForeignKey('Products',on_delete=models.CASCADE,null=True)
    parent = models.ForeignKey('self', related_name="childs",on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255)
    parent_page_id = models.IntegerField(default=0)
    caption = models.CharField(max_length=255 , null=True)
    status = models.BooleanField(default=True)
    page_type = models.CharField(max_length=255,null=False,default=False)
    title = models.CharField(max_length=500,null=True)
    short_description = models.CharField(max_length=3000, null=True)
    long_contents = models.TextField(max_length=255,null=True)
    meta_title = models.CharField(max_length=255,null=True)
    keyword = models.CharField(max_length=255,null=True)
    position = models.IntegerField()
    banner_image1 = models.ImageField(upload_to='home/banner1', null=True)
    banner_image2 = models.ImageField(upload_to='home/banner2', null=True)
    icon_image = models.ImageField(upload_to='home/icon', null=True)
    created_at = models.DateTimeField(auto_now=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    @property
    def getBannerImage1(self):
        if self.banner_image1 :
            return self.banner_image1.url
        return ''

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Navigation,related_name="product",on_delete=models.CASCADE,null=True)
    price = models.CharField(max_length=255)
    discount_type = models.CharField(max_length=255)
    discount = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    most_ordered = models.BigIntegerField(null=True)
    most_viewed = models.BigIntegerField(null=True)
    vendor = models.CharField(max_length=255,null=True)
    payment_type = models.CharField(max_length=255,default="COD")
    size =models.CharField(max_length=255,default="medium")
    color =models.CharField(max_length=255,default="white")
    title = models.CharField(max_length=2000,null=True)
    discription = models.TextField(max_length=5000,null=True)   #overview
    long_contents = models.TextField(max_length=5000,null=True) #more
    meta_title = models.CharField(max_length=300,null=True)
    keyword = models.CharField(max_length=2000,null=True)
    brand = models.CharField(max_length=2000,null=True)
    status = models.BooleanField(default=True)
    image1 = models.ImageField(upload_to='uploads/', null=True)
    image2 = models.ImageField(upload_to='uploads/', null=True)
    image3 = models.ImageField(upload_to='uploads/', null=True)
    image4 = models.ImageField(upload_to='uploads/', null=True)
    image5 = models.ImageField(upload_to='uploads/', null=True)
    created_at = models.DateTimeField(auto_now=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    ftn_choice = [("f","featured"),("t","trending"),("n","new_arrival")]
    ftn = models.CharField(max_length=50,choices=ftn_choice,default="n")

    def __str__(self):
        return "{name:"+self.name+","+"Prpduct_id"+str(self.id)+"}"

class ExcelFileUpload(models.Model):
    excel_file_upload = models.FileField(upload_to='excel')
    updated_at = models.DateTimeField(auto_now=True,null=True)

class Shipping(models.Model):
    user_id = models.CharField(max_length=200)
    name = models.CharField(max_length=205)
    phone = models.CharField(max_length=205)
    email = models.CharField(max_length=205)
    shpping_address = models.CharField(max_length=2055)

class Order(models.Model):
    # product_id = models.IntegerField(default=0)
    get_shipping_address = models.ForeignKey(Shipping,related_name="order",on_delete=models.DO_NOTHING,null=True)
    product = models.ForeignKey(Products,related_name="order",on_delete=models.DO_NOTHING,null=True)
    product_details = models.TextField(max_length=5000)
    user_id = models.IntegerField(null=False)
    user_detail = models.CharField(max_length=300)
    shipping_address = models.CharField(max_length=2055)
    created_at = models.DateTimeField(auto_now=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    phone = models.CharField(max_length=25,null=True)
    pdc = models.CharField(max_length=10,null=True) # p>pending , d=delivered , c=cancled
    def get_date(self):
        return humanize.naturaltime(self.updated_at)    

class GlobalSettings(models.Model):
    site_name = models.CharField(max_length=255)
    site_name_nepali = models.CharField(max_length=255,null=True)
    site_email = models.EmailField()
    configure_email = models.EmailField(null=True)
    site_contact = models.CharField(max_length=255,null=True)
    site_contact_nepali = models.BigIntegerField(null=True)
    site_address = models.CharField(max_length=255)
    site_address_nepali = models.CharField(max_length=255,null=True)
    fb_link = models.CharField(max_length=255,null=True)
    twitter_link = models.CharField(max_length=255,null=True)
    linkedin_link = models.CharField(max_length=255,null=True)
    tiktok_link = models.CharField(max_length=255,null=True) 
    other_link = models.CharField(max_length=255,null=True) #youtube
    page_title = models.CharField(max_length=255)
    page_keyword = models.CharField(max_length=200,null=True)
    page_discription = models.TextField(max_length=5000,null=True)
    image1 = models.ImageField(upload_to='global/fav_ico', null=True)
    image2 = models.ImageField(upload_to='global/logo', null=True)
    image3 = models.ImageField(upload_to='global/footer_logo', null=True)
    created_at = models.DateTimeField(auto_now=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return "{name:"+self.name+","+"global_setting"+str(self.id)+"}"

class Team(models.Model):
    name = models.CharField(max_length=255)
    post = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255, null=True)
    long_contents = models.TextField(max_length=255,null=True)
    profile_picture = models.ImageField(upload_to='founders/', null=True)

class Blog(models.Model):
    title = models.CharField(max_length=2000,null=True)
    created_at = models.DateTimeField(auto_now=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    main_title = models.TextField(max_length=5000,null=True)
    discription = models.TextField(max_length=5000,null=True)
    author = models.CharField(max_length=255,null=True)
    banner_image = models.ImageField(upload_to='blogs/banner', null=True)
    icon_image = models.ImageField(upload_to='blogs/icon', null=True)
    status = models.BooleanField(default=True)
    def get_date(self):
        return humanize.naturaltime(self.updated_at)

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING,null=True)
    product = models.ForeignKey('Products',on_delete=models.DO_NOTHING)
    ishere = models.SmallIntegerField(default=True)   # ishere field 1 =>wishlist |||| 0 => cart ||| 2=> order
    color = models.CharField(max_length=50, null=True)
    size = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField(null=True,default=1)
    temp_id = models.BigIntegerField(null=True)

class ContactUs(models.Model):
    name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    subject = models.CharField(max_length=100, null=True)
    message = models.TextField(null=True)
    read_unread = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def get_date(self):
        return humanize.naturaltime(self.updated_at)

