from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("displayCategory", views.displayCategory, name="displayCategory")
    
]
