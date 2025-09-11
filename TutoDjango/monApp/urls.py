from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.accueil, name="home"),
    path("home/<param>",views.accueil ,name='accueil'),
    path("about/", views.about_us, name="about"),
    path("contact/", views.contact_us, name="contact"),
    path("produit/", views.liste_produits, name="produit"),
    path("categorie/", views.liste_cat, name="categorie"),
    path("statut/", views.liste_sta, name="statut"),
    path("rayon", views.liste_rayon, name="rayon"),
]