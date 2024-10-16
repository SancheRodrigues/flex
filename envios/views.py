from django.shortcuts import render, redirect
from django.contrib.auth import login as login_django
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from envios.models import * 
from django.contrib import messages
from envios.forms import *
from django.utils import timezone

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = authenticate(username=username, password=senha)

        if user:
            login_django(request, user)
            return redirect('menu')  
        else:
            messages.error(request, "Email ou senha inválidos")
            return redirect('login')  


@login_required(login_url="/auth/login/")
def cad(request):
    return render(request, 'cad.html')

@login_required(login_url="/auth/login/")
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url="/auth/login/")
def menu(request):
    return render(request, 'menu.html')

@login_required(login_url="/auth/login/")
def shopee(request):
    shopee = Shopee.objects.all().order_by('-data')
    shopee = [(item, timezone.localtime(item.data)) for item in shopee]  # Convertendo a data
    return render(request, 'shopee.html', {'shopees': shopee})

@login_required(login_url="/auth/login/")
def mercado_livre(request):
    mercado_livre = MercadoLivre.objects.all().order_by('-data')
    mercado_livre = [(item, timezone.localtime(item.data)) for item in mercado_livre]  # Convertendo a data
    return render(request, 'mercado_livre.html', {'mercado_livre': mercado_livre})

@login_required(login_url="/auth/login/")
def bulk_delete_shopee(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('items')
        if selected_items:
            Shopee.objects.filter(id__in=selected_items).delete()
            messages.success(request, f'{len(selected_items)} produtos foram excluídos.')
        else:
            messages.warning(request, 'Nenhum produto foi selecionado.')

    return redirect('shopee')

@login_required(login_url="/auth/login/")
def bulk_delete_mercado_livre(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('items')
        if selected_items:
            MercadoLivre.objects.filter(id__in=selected_items).delete()
            messages.success(request, f'{len(selected_items)} produtos foram excluídos.')
        else:
            messages.warning(request, 'Nenhum produto foi selecionado.')

    return redirect('mercado_livre')

@login_required(login_url="/auth/login/")
def registrar_coleta_shopee(request):
    if request.method == "POST":
        form = ShopeeForm(request.POST)
        if form.is_valid():

            if form.is_valid():  
                try:  
                    form.save()  
                    return redirect('shopee')  
                except Exception as e:  
                    print("Ocorreu um erro ao salvar o formulário:", e)
                    print(form.errors)
                    pass  
    else:
        form = ShopeeForm()  
    return render(request,'registrar_coleta_shopee.html',{'form':form})  

@login_required(login_url="/auth/login/")
def registrar_coleta_mercado_livre(request):
    if request.method == "POST":
        form = MercadoLivreForm(request.POST)
        if form.is_valid():

            if form.is_valid():  
                try:  
                    form.save()  
                    return redirect('shopee')  
                except Exception as e:  
                    print("Ocorreu um erro ao salvar o formulário:", e)
                    print(form.errors)
                    pass  
    else:
        form = MercadoLivreForm()  
    return render(request,'registrar_coleta_mercado_livre.html',{'form':form})  

