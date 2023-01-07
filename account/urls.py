from django.urls import path
from . import user_authentication_authorization,chatapp,mailapp

urlpatterns = [
    path('login',user_authentication_authorization.Login,name='Login'),
    path('signup',user_authentication_authorization.SignUp,name='SignUp'),
    path('logout',user_authentication_authorization.Logout,name='Logout'),
    #****************Users************************************
    path('users-list', user_authentication_authorization.UserList, name='UserList'),
    path('user-type/<int:role_id>', user_authentication_authorization.AdvanceUserList, name='AdvanceUserList'),
    path('user-create',user_authentication_authorization.UserCreate,name="UserCreate"),
    path('user-create/<int:id>',user_authentication_authorization.UserCreate,name="UserCreate"),
    path('user-store',user_authentication_authorization.UserStore,name='UserStore'),
    path('user-store/<int:id>',user_authentication_authorization.UserStore,name='UserStore'),
    path('user-delete/<int:id>', user_authentication_authorization.UserDelete, name='UserDelete'),
     
     #********************************************************************

    path('role-list', user_authentication_authorization.RoleList, name='RoleList'),
    path('role-create', user_authentication_authorization.RoleCreate, name='RoleCreate'),
    path('role-edit/<int:id>', user_authentication_authorization.RoleCreate, name='RoleCreate'),
    path('role-delete/<int:id>', user_authentication_authorization.RoleDelete, name='RoleDelete'),
    path('role-store', user_authentication_authorization.RoleStore, name='RoleStore'),
    path('role-store/<int:id>', user_authentication_authorization.RoleStore, name='RoleStore'),

    path('group-list', user_authentication_authorization.GroupList, name='GroupList'),
    path('group-create/', user_authentication_authorization.GroupCreate, name='GroupCreate'),
    path('group-edit/<int:id>', user_authentication_authorization.GroupCreate, name='GroupCreate'),
    path('group-delete/<int:id>', user_authentication_authorization.GroupDelete, name='GroupDelete'),
    path('group-store', user_authentication_authorization.GroupStore, name='GroupStore'),
    path('group-store/<int:id>', user_authentication_authorization.GroupStore, name='GroupStore'),

    path('permission-list', user_authentication_authorization.PermissionList, name='PermissionList'),
    path('permission-delete/<int:id>', user_authentication_authorization.PermissionDelete, name='PermissionDelete'),
    path('permission-store', user_authentication_authorization.PermissionStore, name='PermissionStore'),
    path('user-logs', user_authentication_authorization.UserLogs, name='UserLogs'),

    #****************CHATAPP************************************
    path('chatapp', chatapp.ChatApp, name='ChatApp'),

    #****************MailBox************************************
    path('mail-app', mailapp.MailApp, name='MailApp'),
    path('mail-detail', mailapp.MailDetail, name='MailDetail'),
    path('mail-compose', mailapp.MailCompose, name='MailCompose'),

    #****************category************************************
    ]