from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name="home"),#Here name "home" is used in url links in pages
    path('register/', views.register, name="register"),
    path('contact/', views.contact, name="contact"),
    path('success/', views.success, name="success"),
    path('login/', views.login_view, name="login_view"),#avoid using login because Django has inbuilt login
    path('logout/', views.logout_view, name="logout_view"),#avoid using logout because Django has inbuilt login
    path('collections/', views.collections, name="collections"),
    path('collections/<str:name>', views.collections_view, name="collections_view"),
    path('collections/<str:cname>/<str:pname>', views.product_details, name="product_details"),
    path('update/', views.updateprofile, name='update_profile'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('add_to_cart/', views.add_to_cart, name="add_to_cart"),
    path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),
    path('cart',views.cart_page,name="cart"),

    
]



