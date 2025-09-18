from django.shortcuts import render

from django.http import HttpResponse

from django.views.generic import *

from django.contrib.auth import *

from django.contrib.auth.views import LoginView

from django.contrib.auth.models import User

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
    
# def accueil(request,param=None):
#     if request.GET and request.GET['name']:
#         string = request.GET['name']
#         return render(request, 'monApp/home.html',{'param': string})
#     return render(request, 'monApp/home.html',{'param': param})
    
# def about_us(request):
#     return render(request, 'monApp/about.html')

# def contact_us(request):
#     return render(request, 'monApp/contact.html')

# def liste_produits(request):
#     prdts = Produit.objects.all()
#     return render(request, 'monApp/list_produits.html',{'prdts': prdts})

# def liste_cat(request):
#     ctgrs = Categorie.objects.all()
#     return render(request, 'monApp/list_categories.html',{'ctgrs': ctgrs})

# def liste_sta(request):
#     sttts = Statut.objects.all()
#     return render(request, 'monApp/list_statut.html',{'sttts': sttts})

# def liste_rayon(request):
#     rs = Rayon.objects.all()
#     return render(request, 'monApp/list_rayons.html',{'rs': rs})

class HomeView(TemplateView):
    template_name = "monApp/page_home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        param = self.kwargs.get('param')
        context['titreh1'] = f"Hello {param}" if param else "Hello DJANGO"
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name)
    
class AboutView(TemplateView):
    template_name = "monApp/page_home.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "About us..."
        return context
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)
    
class ContactView(TemplateView):
    template_name = "monApp/page_home.html"

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['titreh1'] = "Contact us..."
        return context
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)
    
class ProduitListView(ListView):
    model = Produit
    template_name = "monApp/list_produits.html"
    context_object_name = "prdts"

    def get_context_data(self, **kwargs):
        context = super(ProduitListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes produits"
        return context
    
    def get_queryset(self) :
        return Produit.objects.order_by("prixUnitaireProd")
    
class ProduitDetailView(DetailView):
    model = Produit
    template_name = "monApp/detail_produit.html"
    context_object_name = "prdt"

    def get_context_data(self, **kwargs):
        context = super(ProduitDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du produit"
        return context
    
class CategorieListView(ListView):
    model = Categorie
    template_name = "monApp/list_categories.html"
    context_object_name = "ctgrs"

    def get_context_data(self, **kwargs):
        context = super(CategorieListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes catégories"
        return context

class CategorieDetailView(DetailView):
    model = Categorie
    template_name = "monApp/detail_categorie.html"
    context_object_name = "ctgr"

    def get_context_data(self, **kwargs):
        context = super(CategorieDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail de la catégorie"
        return context
    
class StatutListView(ListView):
    model = Statut
    template_name = "monApp/list_statut.html"
    context_object_name = "sttts"

    def get_context_data(self, **kwargs):
        context = super(StatutListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes statuts"
        return context

class StatutDetailView(DetailView):
    model = Statut
    template_name = "monApp/detail_statut.html"
    context_object_name = "sttt"

    def get_context_data(self, **kwargs):
        context = super(StatutDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du statut"
        return context
    
class RayonListView(ListView):
    model = Rayon
    template_name = "monApp/list_rayons.html"
    context_object_name = "rs"

    def get_context_data(self, **kwargs):
        context = super(RayonListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes rayons"
        return context

class RayonDetailView(DetailView):
    model = Rayon
    template_name = "monApp/detail_rayon.html"
    context_object_name = "r"

    def get_context_data(self, **kwargs):
        context = super(RayonDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du rayon"
        return context
    
class ConnectView(LoginView):
    template_name = 'monApp/page_login.html'
    def post(self, request, **kwargs):
        lgn = request.POST.get('username', False)
        pswrd = request.POST.get('password', False)
        user = authenticate(username=lgn, password=pswrd)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'monApp/page_home.html', {'param': lgn, 'message': "You're connected"})
        else:
            return render(request, 'monApp/page_register.html')
        
class RegisterView(TemplateView):
    template_name = 'monApp/page_register.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        mail = request.POST.get('mail', False)
        password = request.POST.get('password', False)
        user = User.objects.create_user(username, mail, password)
        user.save()
        if user is not None and user.is_active:
            return render(request, 'monApp/page_login.html')
        else:
            return render(request, 'monApp/page_register.html')