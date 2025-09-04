from django.shortcuts import render

from django.http import HttpResponse

from monApp.models import Produit, Categorie, Statut

def home(request, param):
    return HttpResponse("<h1>Hello " + param + " </h1>")

def homevide(request):
    return HttpResponse("<h1>Hello toi </h1>")

def about_us(request):
    return HttpResponse("<h1>About Us</h1>")

def contact_us(request):
    return HttpResponse("<h1>Contact Us</h1>")

def liste_produits(request):
    prdts = Produit.objects.all()
    strr = "<ul>"
    for prod in prdts:
        strr += f"<li> {prod.intituleProd} </li>"
    strr+="</ul>"
    return HttpResponse(strr)

def liste_cat(request):
    ctgr = Categorie.objects.all()
    strr = "<ul>"
    for cat in ctgr:
        strr += f"<li> {cat.nomProd} </li>"
    strr+="</ul>"
    return HttpResponse(strr)

def liste_sta(request):
    sttt = Statut.objects.all()
    strr = "<ul>"
    for sta in sttt:
        strr += f"<li> {sta.libelle} </li>"
    strr+="</ul>"
    return HttpResponse(strr)