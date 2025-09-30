from django.urls import path
from . import views
from django.views.generic import *

urlpatterns = [
        # Pages basiques
    path("home/", views.HomeView.as_view(),name="home"),
    path("home/<param>", views.HomeView.as_view(),name="home"),
    path("about/", views.AboutView.as_view()),
    path("contact/", views.ContactView,name="contact"),
    path('login/', views.ConnectView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.DisconnectView.as_view(), name='logout'),
    path('email-sent/', views.EmailSentView, name='email-sent'),
        # Produit
    path("produits/",views.ProduitListView.as_view(),name="lst_prdts"),
    path("produit/<pk>/" ,views.ProduitDetailView.as_view(), name="dtl_prdt"),
    path("produit/",views.ProduitCreateView.as_view(), name="crt-prdt"),
    path("produit/<pk>/update/",views.ProduitUpdateView.as_view(), name="prdt-chng"),
    path("produit/<pk>/delete/",views.ProduitDeleteView.as_view(), name="dlt-prdt"),
        # Categorie
    path("categories/", views.CategorieListView.as_view(), name="lst_ctgrs"),
    path("categorie/<pk>/", views.CategorieDetailView.as_view(), name="dtl_ctgr"),
    path("categorie/",views.CategorieCreateView.as_view(), name="crt-ctgr"),
    path("categorie/<pk>/update/",views.CategorieUpdateView.as_view(), name="ctgr-chng"),
    path("categorie/<pk>/delete/",views.CategorieDeleteView.as_view(), name="dlt-ctgr"),
        # Statut
    path("statuts/", views.StatutListView.as_view(), name="lst_sttts"),
    path("statut/<pk>/", views.StatutDetailView.as_view(), name="dtl_sttt"),
    path("statut/",views.StatutCreateView.as_view(), name="crt-sttt"),
    path("statut/<pk>/update/",views.StatutUpdateView.as_view(), name="sttt-chng"),
    path("statut/<pk>/delete/",views.StatutDeleteView.as_view(), name="dlt-sttt"),
        # Rayon
    path("rayons/", views.RayonListView.as_view(), name="lst_rs"),
    path("rayon/<pk>/", views.RayonDetailView.as_view(), name="dtl_r"),
    path("rayon/",views.RayonCreateView.as_view(), name="crt-r"),
    path("rayon/<pk>/update/",views.RayonUpdateView.as_view(), name="r-chng"),
    path("rayon/<pk>/delete/",views.RayonDeleteView.as_view(), name="dlt-r"),
]