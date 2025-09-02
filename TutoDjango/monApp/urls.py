from django.urls import path
from . import views

urlpatterns = [
    path("home/<param>", views.home, name="home"),
    path("home/", views.homevide, name="home"),
    path("about/", views.about_us, name="about"),
    path("contact/", views.contact_us, name="contact"),
]