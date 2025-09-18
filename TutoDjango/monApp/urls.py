from django.urls import path
from . import views
from django.views.generic import *

urlpatterns = [
    #path("home/", views.accueil, name="home"),
    #path("home/<param>",views.accueil ,name='accueil'),
    #path("about/", views.about_us, name="about"),
    #path("contact/", views.contact_us, name="contact"),
    #path("produit/", views.liste_produits, name="produit"),
    #path("categorie/", views.liste_cat, name="categorie"),
    #path("statut/", views.liste_sta, name="statut"),
    #path("rayon", views.liste_rayon, name="rayon"),
    path("home/", views.HomeView.as_view()),
    path("home/<param>", views.HomeView.as_view()),
    path("about/", views.AboutView.as_view()),
    path("contact/", views.ContactView.as_view()),
    path("produits/",views.ProduitListView.as_view(),name="lst_prdts"),
    path("produit/<pk>/" ,views.ProduitDetailView.as_view(), name="dtl_prdt"),
    path("categorie/", views.CategorieListView.as_view(), name="lst_ctgrs"),
    path("categorie/<pk>/", views.CategorieDetailView.as_view(), name="dtl_ctgr"),
    path("statut/", views.StatutListView.as_view(), name="lst_sttts"),
    path("statut/<pk>/", views.StatutDetailView.as_view(), name="dtl_sttt"),
    path("rayon", views.RayonListView.as_view(), name="lst_rs"),
    path("rayon/<pk>/", views.RayonDetailView.as_view(), name="dtl_r"),
]