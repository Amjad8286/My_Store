from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('seller', views.seller, name='seller'),
    path("prodview/<int:pid>", views.productsView, name="ProductView"),
    path("checkout", views.checkout, name="Checkout"),
    path("sing_up", views.handlesingup, name='handlesingup'),
    path("handlelogin", views.handlelogin, name='handlelogin'),
    path("logout", views.handlelogout, name="handlelogout"),
    path("like/<int:pid>", views.like_post, name='like'),
    path("liked", views.like_home, name='liked'),
    path("search", views.search, name="Search"),
    path("review/<int:pid>", views.review, name="review"),
]