from django.urls import path
from . import views
from .includes import global_views,blogs,teams,home,order,tree,configure_email_views

urlpatterns = [
    path('', views.index, name='index'),

    #****************category************************************
    path('navigation-list', views.NavigationList, name='NavigationList'),
    path('navigation-list/<int:id>/list', views.NavigationList, name='NavigationList'),
    path('category-create',views.NavigationCreate,name="NavigationCreate"),
    path('category-create/<int:parent_id>', views.NavigationCreate, name='SubNavigationCreate'),#sub page
    path('category-edit/<int:edit_id>/', views.NavigationCreate, name='NavigationCreate'),
    path('category-store',views.NavigationStore,name="NavigationStore"),
    path('category-update/<int:edit_id>', views.NavigationStore, name='NavigationStore'),
    path('category-delete/<int:id>',views.NavigationDelete,name="NavigationDelete"),

    #****************Home Navigation************************************
    path('home-navigation-list', home.HomeNavigationList, name='HomeNavigationList'),
    path('home-navigation-list/<int:id>/list', home.HomeNavigationList, name='HomeNavigationList'),
    path('home-category-create',home.HomeNavigationCreate,name="HomeNavigationCreate"),
    path('home-category-create/<int:parent_id>', home.HomeNavigationCreate, name='HomeSubNavigationCreate'),#sub page
    path('home-category-edit/<int:edit_id>', home.HomeNavigationCreate, name='HomeNavigationCreate'),
    path('home-category-store',home.HomeNavigationStore,name="HomeNavigationStore"),
    path('home-category-update/<int:edit_id>', home.HomeNavigationStore, name='HomeNavigationStore'),
    path('home-category-delete/<int:id>',home.HomeNavigationDelete,name="HomeNavigationDelete"),

    #****************product**************************************
    path('product-list', views.ProductList, name='ProductList'),
    path('product-list/<int:pk>/<str:ftn>', views.ProductList, name='ProductList'), #For FTN
    path('product-create/<int:pk>', views.ProductCreate, name='ProductCreate'),
    path('product-create/', views.ProductCreate, name='ProductCreate'),
    path('product-store/', views.ProductStore, name='ProductStore'),
    path('product-store/<int:pk>', views.ProductStore, name='ProductStore'),
    path('product-delete/<int:pk>', views.ProductDelete, name='ProductDelete'),

    #****************Add Product**************************************
    path('add-excel',views.AddProduct , name='AddProduct' ),
    path('export-excel',views.ExportProduct.as_view()  , name='ExportProduct' ),

   #****************global-setting**************************************
    path('global-create/<int:pk>', global_views.GlobalCreate, name="GlobalCreate"),
    path('global-create', global_views.GlobalCreate, name='GlobalCreate'),
    path('global-store', global_views.GlobalStore, name='GlobalStore'),
    path('global-store/<int:pk>', global_views.GlobalStore, name='GlobalStore'),
    # path('/global-delete/<int:pk>', global_views.GlobalDelete, name='GlobalDelete'),

    #****************Email Configure**************************************
    # path('email-create/<int:pk>', configure_email_views.EmailCreate, name="EmailCreate"),
    path('email-create', configure_email_views.EmailCreate, name='EmailCreate'),
    path('email-store', configure_email_views.EmailStore, name='EmailStore'),
    path('email-store/<int:pk>', configure_email_views.EmailStore, name='EmailStore'),
    # path('/global-delete/<int:pk>', global_views.GlobalDelete, name='GlobalDelete'),

   #****************blogs**************************************
    path('blogs', blogs.Blogs, name='Blogs'),
    path('blogs-create/<int:pk>', blogs.BlogsCreate, name="BlogsCreate"),
    path('blogs-create', blogs.BlogsCreate, name='BlogsCreate'),
    path('blogs-store', blogs.BlogsStore, name='BlogsStore'),
    path('blogs-store/<int:pk>', blogs.BlogsStore, name='BlogsStore'),
    path('blogs-delete/<int:pk>', blogs.BlogsDelete, name='BlogsDelete'),

    #****************Teams**************************************
    path('teams', teams.Teams, name='Teams'),
    path('teams/<int:pk>', teams.Teams, name='Teams'),
    # path('/teams-create/<int:pk>/', teams.TeamsCreate, name="TeamsCreate"),
    # path('/teams-create/', teams.TeamsCreate, name='TeamsCreate'),
    path('teams-store', teams.TeamsStore, name='TeamsStore'),
    path('teams-store/<int:pk>', teams.TeamsStore, name='TeamsStore'),
    path('teams-delete/<int:pk>', teams.TeamsDelete, name='TeamsDelete'),

    #****************Orders**************************************
    path('customer-order', order.CustomerOrder, name='CustomerOrder'),
    #****************Orders**************************************
    path('order', order.Orders, name='Order'),
    path('order/<int:pk>/<str:pdc>', order.Orders, name='Order'),

    #**** Client messages*****#
    path('client-messages/<int:id>', views.ClientMessage, name='ClientMessage'),

    #****************Pending**************************************
    path('pending', order.Pending, name='Pending'),
    path('pending/<int:pk>/<str:pdc>', order.Pending, name='Pending'),

    #****************Delivered**************************************
    path('delivered', order.Delivered, name='Delivered'),
    path('delivered/<int:pk>/<str:pdc>', order.Delivered, name='Delivered'),
    
    #****************CanclelledOrders**************************************
    path('canclelled-orders', order.CanclelledOrders, name='CanclelledOrders'),
    path('canclelled-orders/<int:pk>/<str:pdc>', order.CanclelledOrders, name='CanclelledOrders'),

    path('ajax-tree', tree.TreeAjax, name='TreeAjax'),
    

]   