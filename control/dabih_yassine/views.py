from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# home page
def index(request):
    if not request.user.is_authenticated: #tester la session
        return redirect('login')
    total_operation = Operation.objects.all().count()
    context = {'total_operation': total_operation}
    total_client = Client.objects.all().count()
    context2 = {'total_client': total_client}
    total_retrait = Operation.objects.filter(type='retrait').count()
    context3 = {'total_retrait': total_retrait}
    total_versement = Operation.objects.filter(type='versement').count()
    context4 = {'total_versement': total_versement}
    return render(request,'index.html',{'context':context,'context2':context2,'context3':context3,'context4':context4})


# login en utilisant authentification de django
def login_page(request):
    logout(request)  # fermer la session
    if request.method == 'POST':
        us=request.POST.get('user')
        ps=request.POST.get('pass')
        user=authenticate(request,username=us , password=ps)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"login or password incorrect !!")
    return render(request, 'login.html')



##*******************************************************    client    *******************************************************

def clients_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    clients = Client.objects.all()
    p = Paginator(clients, 10)
    page_number = request.GET.get('page',1)
    print("nombre de page -> {}".format(p.num_pages)) ## nbre pages
    try:
        page_obj = p.get_page(page_number)  ##affiche la liste dans une page
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(1)
    context = {'items' : page_obj}
    ##instancier Formulaire qui va creer les elements html
    clientForm = ClientForm()
    context2 = {'items_forms': clientForm}
    return render(request, "client.html",{'context':context,'context2':context2 })



##ajouter client depuis formulaire
def client_forms_add(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            context = {'data':form.cleaned_data}
            print("nom  -> {}".format(form.cleaned_data["nom"]))
            print("prenom  -> {}".format(form.cleaned_data["prenom"]))
            Client(nom=form.cleaned_data["nom"],prenom=form.cleaned_data["prenom"]).save()
            return redirect('client')



#recherche client par son nom
def client_search(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # on récupere les données du model
    if request.method == 'POST':
        if request.POST.get("nom") != '':
            print(f"valeur nom -----> : {request.POST.get('nom')}")
            clients = Client.objects.filter(nom__icontains=request.POST.get("nom")).all()
            p = Paginator(clients, 10)
            page_number = request.GET.get('page')
            try:
                page_obj = p.get_page(page_number)
            except PageNotAnInteger:
                page_obj = p.page(1)
            except EmptyPage:
                page_obj = p.page(p.num_pages)
            context = {'items': page_obj}
            clientForm = ClientForm()
            context2 = {'items_forms': clientForm}
            return render(request, "client.html", {'context':context,'context2':context2})
        else:
            return redirect('client')
    else:
        return redirect('client')



# pour afficher les détail d'un client
def client_details(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    client=Client.objects.get(code=id)
    context = {'client': client}
    return render(request, 'client_details.html', context)




# supprimer client
def client_delete(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    print("herrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrre")

    try:
        client = Client.objects.get(code=id)
        print(f"client ->       {client}")
    except Client.DoesNotExist:
        return redirect('client')
    client.delete()
    return redirect('client')


# pour afficher les détail d'un client dans le nom contient un mot clé
def client_details_via_nom(request,mot):
    if not request.user.is_authenticated:
        return redirect('login')
    client=Client.objects.filter(nom__icontains=mot)
    context = {'client': client}
    return render(request, 'client_details_via_nom.html', context)



##*******************************************************    Compte    *******************************************************


def comptes_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    comptes = Compte.objects.all()
    p = Paginator(comptes, 10)
    page_number = request.GET.get('page',1)
    print("nombre de page -> {}".format(p.num_pages)) ## nbre pages
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
         page_obj = p.page(1)
    context = {'items': page_obj}
    ##instancier Formulaire qui va creer les elements html
    compteForm = CompteForm()
    context2 = {'items_forms': compteForm}
    return render(request, "compte.html", {'context': context, 'context2': context2})


#recherche des comptes d'un client par son nom
def compte_search(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # on récupere les données du model
    if request.POST.get("nom") != '':
        comptes = Compte.objects.filter(client__nom__icontains=request.POST.get("nom"))
        p = Paginator(comptes, 10)
        page_number = request.GET.get('page', 1)
        print("nombre de page -> {}".format(p.num_pages))  ## nbre pages
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
        context = {'items': page_obj}
        compteForm = CompteForm()
        context2 = {'items_forms': compteForm}
        return render(request, "compte.html",  {'context':context,'context2':context2})
    else:
        return redirect('compte')



##ajouter compte depuis formulaire
def compte_forms_add(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        form = CompteForm(request.POST)
        if form.is_valid():
            context = {'data':form.cleaned_data}
            print("numero  -> {}".format(form.cleaned_data["numero"]))
            print("dateCreation  -> {}".format(form.cleaned_data["dateCreation"]))
            print("solde  -> {}".format(form.cleaned_data["solde"]))
            print("client  -> {}".format(form.cleaned_data["client"]))
            Compte(numero=form.cleaned_data["numero"], dateCreation=form.cleaned_data["dateCreation"], solde=form.cleaned_data["solde"], client=form.cleaned_data["client"]).save()
            return redirect('compte')



# supprimer compte
def compte_delete(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        compte = Compte.objects.get(id=id)
    except Client.DoesNotExist:
        return redirect('compte')
    compte.delete()
    return redirect('compte')




##*******************************************************    Operation    *******************************************************



def operations_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    operations = Operation.objects.all()
    p = Paginator(operations, 10)
    page_number = request.GET.get('page',1)
    print("nombre de page -> {}".format(p.num_pages)) ## nbre pages
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(1)
    context = {'items': page_obj}
    ##instancier Formulaire qui va creer les elements html
    operationForm = OperationForm()
    context2 = {'items_forms': operationForm}
    return render(request, "operation.html", {'context': context, 'context2': context2})




#recherche des operations effectué par un client via son nom

def operation_search(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # on récupere les données du model
    if request.POST.get("nom") != '':
        operations = Operation.objects.filter(compte__client__nom__icontains=request.POST.get("nom"))
        p = Paginator(operations, 10)
        page_number = request.GET.get('page', 1)
        print("here         nombre de page -> {}".format(p.num_pages))  ## nbre pages
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
        context = {'items': page_obj}
        print(f"context-------------------------> {context}")
        operationForm = OperationForm()
        context2 = {'items_forms': operationForm}
        return render(request, "operation.html",  {'context':context,'context2':context2})
    else:
        return redirect('operation')



##ajouter compte depuis formulaire
def operation_forms_add(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        form = OperationForm(request.POST)
        if form.is_valid():
            context = {'data':form.cleaned_data}
            print("dateOperation  -> {}".format(form.cleaned_data["dateOperation"]))
            print("montant  -> {}".format(form.cleaned_data["montant"]))
            print("type  -> {}".format(form.cleaned_data["type"]))
            print("compte  -> {}".format(form.cleaned_data["compte"]))
            Operation(dateOperation=form.cleaned_data["dateOperation"], montant=form.cleaned_data["montant"], type=form.cleaned_data["type"], compte=form.cleaned_data["compte"]).save()
            return redirect('operation')



# supprimer operation
def operation_delete(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        operation = Operation.objects.get(numeroOperation=id)
    except Client.DoesNotExist:
        return redirect('operation')
    operation.delete()
    return redirect('operation')




def operation_client(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    operation = Operation.objects.filter(compte__client__code=id)
    context = {'operations':operation}
    return render(request , 'operation_client.html',context)



def recherche_form(request):
    if not request.user.is_authenticated:
        return redirect('login')
    form = RechercheForm()
    context2 = {'items_forms': form}
    return render(request,'recherche_form.html',{'context2':context2})


##recherche des operations entre 2 dates
def recherche_forms(request):
    if not request.user.is_authenticated:
        return redirect('login')
    print("haniiiiiiiiiii")
    if request.method == "POST":
        form = RechercheForm(request.POST)
        if form.is_valid():
            print("haniiiiiiiiiii2")
            context = {'data':form.cleaned_data}
            print("datedebut  -> {}".format(form.cleaned_data["date_debut"]))
            print("datefin  -> {}".format(form.cleaned_data["date_fin"]))
            operations = Operation.objects.filter(dateOperation__gte=form.cleaned_data["date_debut"]).filter(dateOperation__lte=form.cleaned_data["date_fin"])
            p = Paginator(operations, 10)
            page_number = request.GET.get('page', 1)
            print("nombre de page -> {}".format(p.num_pages))  ## nbre pages
            try:
                page_obj = p.get_page(page_number)  ##affiche la liste dans une page
            except PageNotAnInteger:
                page_obj = p.page(1)
            except EmptyPage:
                page_obj = p.page(1)
            context = {'items': page_obj}
            form = RechercheForm()
            context2 = {'items_forms': form}
            return render(request, "recherche_form.html", {'context': context, 'context2': context2 })