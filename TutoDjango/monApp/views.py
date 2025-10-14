from itertools import count
from sqlite3 import IntegrityError
from django.shortcuts import render

from django.http import HttpResponse

from django.views.generic import *

from django.contrib.auth import *

from django.contrib.auth.views import LoginView

from django.contrib.auth.models import User

from django.core.mail import send_mail

from django.shortcuts import redirect, get_object_or_404

from django.forms import BaseModelForm

from django.urls import reverse_lazy

from django.db.models import Count, Prefetch

from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from django.contrib import messages

from monApp.models import Produit, Categorie, Statut, Rayon, Contenir

from monApp.forms import ContactUsForm, ProduitForm, CategorieForm, StatutForm, RayonForm, ContenirForm

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
    
def ContactView(request):
    titreh1 = "Contact us !"

    if request.method=='POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
            subject = f'Message from {form.cleaned_data.get("name") or "anonyme"} via MonProjet Contact Us form',
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['admin@monprojet.com'],
            )
            return redirect('email-sent')
    else:
        form = ContactUsForm()
    return render(request, "monApp/page_home.html",{'titreh1':titreh1, 'form':form})
    
class ProduitListView(ListView):
    model = Produit
    template_name = "monApp/list_produits.html"
    context_object_name = "prdts"

    def get_context_data(self, **kwargs):
        context = super(ProduitListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes produits"
        return context
    
    def get_queryset(self) :
        query = self.request.GET.get('search')
        if query:
            return Produit.objects.filter(intituleProd__icontains=query).select_related('categorie').select_related('statut')
        return Produit.objects.select_related('categorie').select_related('statut')
    
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

    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        query = self.request.GET.get('search')
        if query:
            return Categorie.objects.annotate(nb_produits=Count('produits')).filter(nomCat__icontains=query)
        return Categorie.objects.annotate(nb_produits=Count('produits'))
    
    def get_context_data(self, **kwargs):
        context = super(CategorieListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes catégories"
        return context

class CategorieDetailView(DetailView):
    model = Categorie
    template_name = "monApp/detail_categorie.html"
    context_object_name = "ctgr"

    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        return Categorie.objects.annotate(nb_produits=Count('produits'))
    
    def get_context_data(self, **kwargs):
        context = super(CategorieDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail de la catégorie"
        context['prdts'] = self.object.produits.all()
        return context
    
class StatutListView(ListView):
    model = Statut
    template_name = "monApp/list_statut.html"
    context_object_name = "sttts"

    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        query = self.request.GET.get('search')
        if query:
            return Statut.objects.annotate(nb_produits=Count('produitS')).filter(libelle__icontains=query)
        return Statut.objects.annotate(nb_produits=Count('produitS'))

    def get_context_data(self, **kwargs):
        context = super(StatutListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes statuts"
        return context

class StatutDetailView(DetailView):
    model = Statut
    template_name = "monApp/detail_statut.html"
    context_object_name = "sttt"

    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        return Statut.objects.annotate(nb_produits=Count('produitS'))

    def get_context_data(self, **kwargs):
        context = super(StatutDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du statut"
        context['prdts'] = self.object.produitS.all()
        return context
    
class RayonListView(ListView):
    model = Rayon
    template_name = "monApp/list_rayons.html"
    context_object_name = "rs"

    def get_queryset(self):
        
        query = self.request.GET.get('search')
        if query:
            return Rayon.objects.prefetch_related(Prefetch("contenirR", queryset=Contenir.objects.select_related("refProd"))).filter(nomRayon__icontains=query)
        return Rayon.objects.prefetch_related(Prefetch("contenirR", queryset=Contenir.objects.select_related("refProd")))


    def get_context_data(self, **kwargs):
        context = super(RayonListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes rayons"
        rs_dt = []
        for rayon in context['rs']:
            total = 0
            for contenir in rayon.contenirR.all():
                total += contenir.refProd.prixUnitaireProd * contenir.qte
            rs_dt.append({'rayon': rayon,'total_stock': total})
        context['rs_dt'] = rs_dt
        return context

class RayonDetailView(DetailView):
    model = Rayon
    template_name = "monApp/detail_rayon.html"
    context_object_name = "r"

    def get_context_data(self, **kwargs):
        context = super(RayonDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du rayon"

        prdts_dt = []
        total_rayon = 0
        total_nb_produit = 0

        for contenir in self.object.contenirR.all():
            total_produit = contenir.refProd.prixUnitaireProd * contenir.qte
            prdts_dt.append({   'produit': contenir.refProd,
                                'qte': contenir.qte,
                                'prix_unitaire': contenir.refProd.prixUnitaireProd,
                                'total_produit': total_produit} )
            total_rayon += total_produit
            total_nb_produit += contenir.qte

        context['prdts_dt'] = prdts_dt
        context['total_rayon'] = total_rayon
        context['total_nb_produit'] = total_nb_produit

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
        
class DisconnectView(TemplateView):
    template_name = 'monApp/page_logout.html'

    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)
    
def EmailSentView(request):
    return render(request, "monApp/email_sent.html")

@method_decorator(login_required(login_url='/monApp/login/'), name='dispatch')
class ProduitCreateView(CreateView):
    model = Produit
    form_class=ProduitForm
    template_name = "monApp/create_produit.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('dtl_prdt', prdt.refProd)
    
@method_decorator(login_required(login_url='/monApp/login/'), name='dispatch')
class ProduitUpdateView(UpdateView):
    model = Produit
    form_class=ProduitForm
    template_name = "monApp/update_produit.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('dtl_prdt', prdt.refProd)

@method_decorator(login_required(login_url='/monApp/login/'), name='dispatch')
class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = "monApp/delete_produit.html"
    success_url = reverse_lazy('lst_prdts')

@method_decorator(login_required(login_url='/monApp/login/'), name='dispatch')
class CategorieCreateView(CreateView):
    model = Categorie
    form_class=CategorieForm
    template_name = "monApp/create_categorie.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        ctgr = form.save()
        return redirect('dtl_ctgr', ctgr.idCat)

@method_decorator(login_required(login_url='/monApp/login/'), name='dispatch')
class CategorieUpdateView(UpdateView):
    model = Categorie
    form_class=CategorieForm
    template_name = "monApp/update_categorie.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        ctgr = form.save()
        return redirect('dtl_ctgr', ctgr.idCat)

@method_decorator(login_required(login_url='/monApp/login/'), name='dispatch')
class CategorieDeleteView(DeleteView):
    model = Categorie
    template_name = "monApp/delete_categorie.html"
    success_url = reverse_lazy('lst_ctgrs')

@method_decorator(login_required(login_url='/monApp/login/'), name='dispatch')
class StatutCreateView(CreateView):
    model = Statut
    form_class=StatutForm
    template_name = "monApp/create_statut.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        sttt = form.save()
        return redirect('dtl_sttt', sttt.idStatut)

@method_decorator(login_required(login_url='/monApp/login/'), name='dispatch')
class StatutUpdateView(UpdateView):
    model = Statut
    form_class=StatutForm
    template_name = "monApp/update_statut.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        sttt = form.save()
        return redirect('dtl_sttt', sttt.idStatut)

@method_decorator(login_required(login_url='/monApp/login/'), name='dispatch')    
class StatutDeleteView(DeleteView):
    model = Statut
    template_name = "monApp/delete_statut.html"
    success_url = reverse_lazy('lst_sttts')

@method_decorator(login_required(login_url='/monApp/login/'), name='dispatch')
class RayonCreateView(CreateView):
    model = Rayon
    form_class=RayonForm
    template_name = "monApp/create_rayon.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        r = form.save()
        return redirect('dtl_r', r.idRayon)

@method_decorator(login_required(login_url='/monApp/login/'), name='dispatch')
class RayonUpdateView(UpdateView):
    model = Rayon
    form_class=RayonForm
    template_name = "monApp/update_rayon.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        r = form.save()
        return redirect('dtl_r', r.idRayon)

@method_decorator(login_required(login_url='/monApp/login/'), name='dispatch')
class RayonDeleteView(DeleteView):
    model = Rayon
    template_name = "monApp/delete_rayon.html"
    success_url = reverse_lazy('lst_rs')


class ContenirCreateView(CreateView):
    model = Contenir
    form_class=ContenirForm
    template_name = "monApp/create_contenir.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        r = get_object_or_404(Rayon, pk=self.kwargs['pk'])
        ctnr = form.save(commit=False)
        ctnr.idRayon = r

        if Contenir.objects.filter(refProd=ctnr.refProd, idRayon=r).exists():
            messages.error(self.request, "Ce produit est déjà présent dans ce rayon.")
            return self.form_invalid(form)

        ctnr.save()
        return redirect('dtl_r', pk=r.pk)
    
class ContenirUpdateView(CreateView):
    model = Contenir
    form_class=ContenirForm
    template_name = "monApp/update_contenir.html"

    def get_initial(self):
        return {}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        r = get_object_or_404(Rayon, pk=self.kwargs['pk'])
        ctnr = form.save(commit=False)
        ctnr.idRayon = r
        refProd = form.cleaned_data['refProd']
        qte = form.cleaned_data['qte']

        existing = Contenir.objects.filter(refProd=refProd, idRayon=r).first()

        if existing:
            if qte == 0:
                existing.delete()
                messages.warning(self.request, f"🗑️ Produit {refProd} supprimé du rayon.")
            else:
                existing.qte = qte
                existing.save()
        else:
            if qte > 0:
                Contenir.objects.create(refProd=refProd, idRayon=r, qte=qte)

        return redirect('dtl_r', pk=r.pk)

class ContenirUpdateAddView(CreateView):
    model = Contenir
    form_class=ContenirForm
    template_name = "monApp/update_contenir_add.html"

    def get_initial(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        r = get_object_or_404(Rayon, pk=self.kwargs['pk'])
        ctnr = form.save(commit=False)
        ctnr.idRayon = r

        existing = Contenir.objects.filter(refProd=ctnr.refProd, idRayon=r).first()
        if existing:
            existing.qte += ctnr.qte
            existing.save()
        else:
            ctnr.save()
        return redirect('dtl_r', pk=r.pk)

