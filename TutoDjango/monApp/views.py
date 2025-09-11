from django.shortcuts import render

from django.http import HttpResponse

from monApp.models import Produit, Categorie, Statut, Rayon

# def home(request, param=None):
#     # if param is None:
#     #     return HttpResponse("<h1>Hello toi </h1>")
#     # else:
#     #     return HttpResponse("<h1>Hello " + param + " </h1>")
#     if request.GET and request.GET['name']:
#         string = request.GET['name']
#         return HttpResponse("<h1>Hello %s </h1>" % string)
#     else:
#         return HttpResponse("<h1>Hello toi </h1>")
    
def accueil(request,param=None):
    if request.GET and request.GET['name']:
        string = request.GET['name']
        return render(request, 'monApp/home.html',{'param': string})
    return render(request, 'monApp/home.html',{'param': param})
    
def about_us(request):
    return render(request, 'monApp/about.html')

def contact_us(request):
    return render(request, 'monApp/contact.html')

def liste_produits(request):
    prdts = Produit.objects.all()
    return render(request, 'monApp/list_produits.html',{'prdts': prdts})

def liste_cat(request):
    ctgrs = Categorie.objects.all()
    return render(request, 'monApp/list_categories.html',{'ctgrs': ctgrs})

def liste_sta(request):
    sttts = Statut.objects.all()
    return render(request, 'monApp/list_statut.html',{'sttts': sttts})

def liste_rayon(request):
    rs = Rayon.objects.all()
    return render(request, 'monApp/list_rayons.html',{'rs': rs})