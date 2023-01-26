# from asyncio.windows_events import NULL
from ast import And
import email
from venv import create
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from PIL import Image
from .models import *
from account.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User,Group,Permission
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from .decorators import customized_user_passes_test,is_admin_role,is_superadmin_role
from django.contrib.auth.decorators import user_passes_test
from axes.models import AccessAttempt
def Login(request):
    data = {'login_attempt_left':settings.AXES_FAILURE_LIMIT}
    login_attempt_left = 20
    if request.POST:
        # return HttpResponse(request.POST)

        email = request.POST['email']
        password =  request.POST['password']
        user = authenticate(request=request,username=email, password=password)
        if user is not None:
            login(request,user,backend='django.contrib.auth.backends.ModelBackend') 
            return redirect('index')    
        else:
             try:
                user_login_attempt = AccessAttempt.objects.filter(username=email).first().failures_since_start
                login_attempt_left = settings.AXES_FAILURE_LIMIT-user_login_attempt
             except:
                login_attempt_left =  settings.AXES_FAILURE_LIMIT

             messages.error(request, "incorrect user or password")
             
            #  return render(request , 'admin/authentication/login.html')
    data = {
       'login_attempt_left':login_attempt_left
       }
    return render(request , 'admin/authentication/login.html',data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def UserList(request):
   slug1 = "Users"
   create_link_name = reverse("UserCreate")
   all_data = CustomUser.objects.all()
#    if request.user.role == CustomUser.STAFF:
#         all_data = CustomUser.objects.filter(role__gte = request.user.role) #gte greater than and lte less than
#    else:
#         all_data = CustomUser.objects.filter(role__gte = request.user.role).exclude(role=CustomUser.PRIVATE) #gte greater than and lte less than
    # oneuser = all_data.last()
    # return HttpResponse(oneuser.groups.all())
   data = {'slug1':slug1,'create':True,'create_link_name':create_link_name, 'users':all_data}
   return render(request , "admin/users/user-list.html",data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def AdvanceUserList(request,role_id=None):
    
    slug1 = "Users classified according to roles"
    create_link_name = reverse("UserCreate")    

    roles = CustomUser.ROLE_CHOICES
    try:
        users = CustomUser.objects.filter(role=role_id)
        if users.count()==0:
            users = CustomUser.objects.all()
    except:
        users = CustomUser.objects.all()

    data = {'slug1':slug1,'create':True,'create_link_name':create_link_name, 'users':users,'roles':roles}
    return render(request , "admin/users/user-type.html",data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def UserCreate(request,id=None):
    create_link_name = reverse("UserCreate")
    if id==None:
        slug1 = "User-create" 
    else:
        slug1 = "User-update" 
    action = "UserStore"
    groups = Group.objects.all()
    roles = CustomUser.ROLE_CHOICES
    #Fetching the data of particular ID
    get_data = None
    if id:
        # action = "ProductUpdate"
        get_data = CustomUser.objects.get(id=id)  
    data = {'slug1':slug1,'create':True,'create_link_name':create_link_name,'id_data':get_data, 'action':action,'groups':groups,'roles':roles}
    return render(request, "admin/users/user-form.html",data)
@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def UserStore(request,id=None):

    if CustomUser.objects.filter(email=request.POST['email']).exists():
        messages.info(request, "email_already_exists")
        return redirect(request.POST['next'])

    if request.POST['password1'] == request.POST['password2']:
        password = make_password(request.POST['password1'])
    else:
        messages.info(request, "Password not match. please confirm the password")
        return redirect(request.POST['next'])

    if request.POST:
        data = {
            'first_name' : request.POST['first_name'],
            'last_name' : request.POST['last_name'],
            'username' : request.POST['username'],
            'email' : request.POST['email'],
            'phone' : request.POST['phone'],
        }
        # return HttpResponse(data)
        if request.POST['password1']!='':
            data['password'] = password
        user,create = CustomUser.objects.update_or_create(id=id , defaults=data)
        try:
            user.image = request.FILES['profile_image']
        except:
            pass
        # return HttpResponse(request.POST['role'])
        if request.POST['role'] != '0':
            if user:
                if int(request.user.role) <= int(request.POST['role']):
                    role_id = request.POST['role']
                    # role_name = user.SetRoleToUserById(int(role_id))
                    # return HttpResponse(role_name)
                    user.role = role_id
                    user.save()
                    messages.success(request, 'Role is seted')
                else:
                    messages.info(request,'Sorry You can not set Upper Level Role')
        if request.POST['group'] != '0':
            if user:
                user.groups.clear()
                group = Group.objects.get(id = request.POST['group'])
                group.user_set.add(user)
                messages.success(request, 'Group Permission is set to '+ group.name)
            else:
                messages.INFO(request, 'Group not Seted!!!')
        
        # if str(user.role) == str(CustomUser.DISTRICT) and 'division_forest_email' in request.POST:
        #     division_forest_email = request.POST['division_forest_email']
        #     user.division_forest_email = division_forest_email
        #     user.save()
        request.session['user_id'] = user.id
        messages.info(request, 'User inserted Successfully !!!')
        return redirect(UserList)


@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def UserDelete(request,id):
    try:
        user = CustomUser.objects.get(id=id).delete()
        messages.success(request, 'User deleted sucessfully!!!.')
        return redirect(UserList)
    except:
        messages.info(request,"foreign key constraint fails CONSTRAINT error")
        return redirect(UserList)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def RoleList(request):
    slug1 = "Role"
    create_link_name = reverse("RoleCreate")   
    roles = CustomUser.ROLE_CHOICES
    data = {'slug1':slug1,'create':False,'create_link_name':create_link_name, 'roles':roles}
    return render(request , "admin/role/role-list.html",data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def RoleCreate(request,id=None):
    create_link_name = reverse("RoleCreate")
    if id==None:
        slug1 = "Role-create" 
    else:
        slug1 = "Role-update" 
    action = "RoleStore"
    category = Navigation.objects.filter(page_type="group")

    permissions_1_19 = Permission.objects.all()[1:19]
    permissions_20_39 = Permission.objects.all()[19:38]
    permissions_40_58 = Permission.objects.all()[38:57]
    #Fetching the data of particular ID
    get_data = None
    group_has_permission = None
    if id:
        # action = "ProductUpdate"
        get_data = Group.objects.get(id=id)  
        group_has_permission  = get_data.permissions.all()
       
    data = {'group_has_permission':group_has_permission,'slug1':slug1,'create':True,'create_link_name':create_link_name,'id_data':get_data, 'action':action,'category':category,'permissions_1_19':permissions_1_19,'permissions_20_39':permissions_20_39,'permissions_40_58':permissions_40_58}
    return render(request, "admin/role/role-form.html",data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def RoleStore(request,id=None):
    if request.POST['name']=="":
        messages.info(request, "Please Fill Group Name")
        return redirect(request.POST['next'])
    if request.POST:          
        data = {
            'name' : request.POST['name'],
        }
        permission = request.POST.getlist('permissions')
        groupobj,create = Group.objects.update_or_create(id=id , defaults = data )
        # groupobj , create = Group.objects.get_or_create(name=request.POST['name'])
       
        groupobj.permissions.set(permission)
        messages.success(request, 'User Inserted sucessfully!!!.')
        return redirect(RoleList)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def RoleDelete(request,id):
    groupobj = Group.objects.get(id=id)
    groupobj.delete()
    messages.success(request,'Group deleted Sucessful!!!')
    return redirect(RoleList)


@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def GroupList(request):
    slug1 = "Groups"
    create_link_name = reverse("GroupCreate")
   
    all_data = Group.objects.all()
    data = {'slug1':slug1,'create':True,'create_link_name':create_link_name, 'groups':all_data}
    return render(request , "admin/group/group-list.html",data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def GroupCreate(request,id=None):
    create_link_name = reverse("GroupCreate")
    if id==None:
        slug1 = "Group-create" 
    else:
        slug1 = "Group-update" 
    action = "GroupStore"


    permissions_1_19 = Permission.objects.all()[0:19]
    permissions_20_39 = Permission.objects.all()[19:38]
    permissions_40_58 = Permission.objects.all()[38:57]
    #Fetching the data of particular ID
    get_data = None
    group_has_permission = None
    if id:
        # action = "ProductUpdate"
        get_data = Group.objects.get(id=id)  
        group_has_permission  = get_data.permissions.all()
       
    data = {'group_has_permission':group_has_permission,'slug1':slug1,'create':True,'create_link_name':create_link_name,'id_data':get_data, 'action':action,'category':category,'permissions_1_19':permissions_1_19,'permissions_20_39':permissions_20_39,'permissions_40_58':permissions_40_58}
    return render(request, "admin/group/group-form.html",data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def GroupStore(request,id=None):
    if request.POST['name']=="":
        messages.info(request, "Please Fill Group Name")
        return redirect(request.POST['next'])

    if request.POST:          
        data = {
            'name' : request.POST['name'],
        }
        permission = request.POST.getlist('permissions')
        groupobj,create = Group.objects.update_or_create(id=id , defaults = data )
        # groupobj , create = Group.objects.get_or_create(name=request.POST['name'])
       
        groupobj.permissions.set(permission)
        messages.success(request, 'User Inserted sucessfully!!!.')
        return redirect(GroupList)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def GroupDelete(request,id):
    # groupobj = Group.objects.get(id=id)
    # groupobj.delete()
    messages.info(request,'Group cant  delete it is protected!!!')
    return redirect(GroupList)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def PermissionList(request):
    # https://docs.djangoproject.com/en/1.8/topics/auth/default/#permission-caching
    action = "PermissionStore"
    slug1 = "Permissions"
    create_link_name = reverse("PermissionList")
    all_data = Permission.objects.all()
    data = {'slug1':slug1,'create':False,'create_link_name':create_link_name,'permission_create':True, 'permissions':all_data,'action':action}
    return render(request , "admin/permissions/permission-list.html",data)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def PermissionStore(request):
    if request.POST:
       
        permission_data = {
            'name' : request.POST['name'],
            'codename' : request.POST['codename'],
            'content_type_id' : 1
        }
        if request.POST['id']:
            perm_id = request.POST['id']
            distobj,create = Permission.objects.update_or_create(id=perm_id,defaults=permission_data) #edit
        else:
            perm_id = 0
            distobj,create = Permission.objects.update_or_create(codename=request.POST['codename'],defaults=permission_data) #create new


    return redirect(PermissionList)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def PermissionDelete(request,id):
    Permission.objects.filter(id=id).delete()
   
    return redirect(PermissionList)

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def UserLogs(request):
    return HttpResponse("i am logs")

@login_required(login_url=settings.LOGIN_URL)
@customized_user_passes_test(is_admin_role)
def UserLogs(request):
    return HttpResponse("i am logs")


def SignUp(request):
    if request.POST:
        first_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        
        check_user_exist = CustomUser.objects.filter(email=email)
        if check_user_exist:
            messages.error(request,'This '+ email + ' is already Registered. Contact admin to get your Login Password')
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        user = CustomUser.objects.create_user(first_name, email, password)
        user.first_name = first_name        
        if user:
            user.role = user.USER
        try:
            user.image = request.FILES['profile_image']
        except:
            pass
        try:
            user.phone = request.POST['phone']
        except:
            pass
        if user:
            user.save()
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            #return HttpResponse("loged in")
        return redirect('index')
    data = {
       'block':'block',
    }
    return render(request , 'admin/authentication/register.html',data)
def Logout(request):
    logout(request)
    return redirect('index')


