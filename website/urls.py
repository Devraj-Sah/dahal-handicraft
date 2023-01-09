from django.urls import path

from . import views
from .includes import Action,search

urlpatterns = [  
    path('', views.index, name='website.index'),
    # path('contact-us/', views.Contactus, name='Contactus'),

    path('product-details/<int:id>', views.ProductDetail, name='ProductDetail'),
    path('blog-details/<int:id>', views.BlogDetail, name='BlogDetail'),
    # # ishere field 1 =>wishlist |||| 0 => cart ||| 2=> order
    # path('wish-list/', views.WishList, name='WishList'),
    # path('wish-list/<int:p_id>/<int:c_id>', views.WishList, name='WishList'),
    path('wish-delete/<int:p_id>/<int:pk>/<str:next>', views.WishListDelete, name='WishListDelete'),
    path('cart/', views.Cart, name='Cart'),
    path('cart/<int:p_id>/<int:c_id>', views.Cart, name='Cart'),
    path('checkout/', views.CheckOut, name='CheckOut'),
    # # path('checkout/<int:id>', views.CheckOut, name='CheckOut'), #not importent before userlogin

    # #user account
    # path('profile', user_account.index, name="UserProfile"),
    # path('logout', user_account.Logout, name="Logout"),
    # path('profile/<int:order_id>', user_account.index, name="UserProfile"),
    # path('setting', user_account.setting, name="UserSetting"),
    # path('change-password', user_account.ChangePassword, name="ChangePassword"),
    # path('view-order/<int:p_id>', user_account.ViewOrder, name="ViewOrder"),

    path('search',search.ProductSearch,name="ProductSearch"),

    # path('login', user_auth.Login, name='user_login'),
    # path('register', user_auth.SignUp, name='user_register'),
    # path('register/<int:id>', user_auth.SignUp, name='user_register'),
    # path('logout',user_auth.Logout,name='user_logout'),
    
    path('<str:menu>', views.Category, name='Category'),#127.0.0.1:8000/dhanusha here is only one slug.slug name is dhanusha . which is menu
    path('<str:menu>/<str:submenu>', views.SubCategory, name='SubCategory'),#127.0.0.1:8000/dhanusha/janakpur . here is two slug . main slug(menu) is dhanusha. and second slug(submenu) is janakpur.

]