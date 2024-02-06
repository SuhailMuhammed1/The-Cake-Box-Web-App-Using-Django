from django.urls import path
from cake_app import views



urlpatterns = [
    path('', views.index),
    path('about/', views.about),
    path('contact/', views.contact),
    path('gallery/', views.gallery),
    path('shop/', views.shop),
    path('order/', views.order),
    path('cart/', views.cart),
    path('checkout/', views.checkout),




#################################### ADMIN ##################################################    

    path('admin_page/', views.admin_page),
    path('admin_login/', views.admin_login),
    path('admin_logout/', views.admin_logout),
    path('add_category/', views.add_category),
    path('add_product/', views.add_product),
    path('delete_category/', views.delete_category),
    path('view_category/', views.view_category),
    path('view_product/', views.view_product),
    path('delete_product/', views.delete_product),
    path('update_product/', views.update_product),
    path('update_view_product/', views.update_view_product),
    path('view_order/', views.view_order),
    path('view_bill/', views.view_bill),






    
#################################### FRONT ##################################################    
    
    path('touch/', views.touch),
    path('productlist/', views.productlist),
    path('billing/', views.billing),
    path('view/', views.view),
    path('view1/', views.view1),
    path('view2/', views.view2),
    path('view3/', views.view3),
    path('view4/', views.view4),
    path('single_order/', views.single_order),
    # path('view_customer_order/', views.view_customer_order),
   


]


# handler404 = views.custom_404_view