from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as login_django
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from envios.models import * 
from django.contrib import messages
from envios.forms import *
from django.utils import timezone
from django.utils.timezone import now, localtime
from datetime import datetime, timedelta
from rolepermissions.checkers import has_role
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, Group
from rolepermissions.roles import assign_role
from django.contrib.auth.hashers import make_password

def has_any_role_decorator(*roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not any(has_role(request.user, role) for role in roles):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

@login_required(login_url="/auth/login/")
@has_any_role_decorator('admin')
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return HttpResponse("As senhas não coincidem")

        if User.objects.filter(username=username).exists():
            return HttpResponse("Nome de usuário já existe")

        hashed_password = make_password(password)  # Hash da senha
        user = User.objects.create(username=username, password=hashed_password)
        
        role = request.POST.get('role')  
        if role == 'admin':
            assign_role(user, 'admin')
        elif role == 'viewer':
            assign_role(user, 'viewer')
        elif role == 'expedition':
            assign_role(user, 'expedition')


        # Salvando o usuário antes de adicionar aos grupos
        user.save()

        # Adicionando o usuário aos grupos
        if role == 'admin':
            admin_group = Group.objects.get(name='admin')
            user.groups.add(admin_group)
        elif role == 'viewer':
            viewer_group = Group.objects.get(name='viewer')
            user.groups.add(viewer_group)
        elif role == 'expedition':
            viewer_group = Group.objects.get(name='expedition')
            user.groups.add(viewer_group)
  
        return redirect('/usuario/')

    return render(request, 'register.html')

@login_required(login_url="/auth/login/")
@has_any_role_decorator('admin')
def edit_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse("Usuário não encontrado.")
    
    if user.is_superuser:
        return HttpResponse("Esse usuário é um desenvolvedor, não é possível editar!")
    

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if password != confirm_password:
            return HttpResponse("As senhas não coincidem")

        user.username = username

        if password:
            user.set_password(password)

        user.save()

        user.groups.clear()  
        if role == 'admin':
            user.groups.add(Group.objects.get(name='admin'))
        elif role == 'viewer':
            user.groups.add(Group.objects.get(name='viewer'))
        elif role == 'expedition':
            user.groups.add(Group.objects.get(name='expedition'))
        
        if user.groups.filter(name="admin").exists():
            return redirect("/auth/login/")
        else:
            return redirect('/usuario/')

    return render(request, 'edit_usuarios.html', {'user': user})

@login_required(login_url="/auth/login/")
@has_any_role_decorator('admin')
def destroy_user(request, user_id):
  
    user = get_object_or_404(User, id=user_id)

    if user.is_superuser:
        return HttpResponse("Você não pode excluir ou editar um desenvolvedor.")
    else:
        user.delete()
    
    if user.has_perm('admin') and request.user.has_perm('admin'): 
        return HttpResponse("Você não pode excluir um administrador.")
    else:

        user.delete()

    return redirect('/usuario/')  

@has_any_role_decorator('admin')
def usuario(request):
    usuarios = User.objects.all()
    return render(request, "usuarios.html", {'usuarios': usuarios})

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

@has_any_role_decorator('admin', 'viewer', 'expedition')
@login_required(login_url="/auth/login/")
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url="/auth/login/")
def menu(request):
    return render(request, 'menu.html')

@has_any_role_decorator('admin', 'viewer', 'expedition')
@login_required(login_url="/auth/login/")
def shopee(request):

    today = now().date()

    start_date_str = request.GET.get('start_date', today.strftime('%Y-%m-%d'))
    end_date_str = request.GET.get('end_date', today.strftime('%Y-%m-%d'))

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1) 

    shopees = Shopee.objects.filter(data__range=[start_date, end_date])

    print(shopees.count())

    return render(request, 'shopee.html', {
        'shopees': shopees,
        'start_date': start_date_str,
        'end_date': end_date_str,
    })


@has_any_role_decorator('admin', 'viewer', 'expedition')
@login_required(login_url="/auth/login/")
def mercado_livre(request):

    today = now().date()

    start_date_str = request.GET.get('start_date', today.strftime('%Y-%m-%d'))
    end_date_str = request.GET.get('end_date', today.strftime('%Y-%m-%d'))

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1) 

    mercado_livre = MercadoLivre.objects.filter(data__range=[start_date, end_date])

    return render(request, 'mercado_livre.html', {
        'mercado_livre': mercado_livre,
        'start_date': start_date_str,
        'end_date': end_date_str,
    })


@has_any_role_decorator('admin', 'expedition')
@login_required(login_url="/auth/login/")
def bulk_delete_shopee(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('items')
        print(selected_items)
        if selected_items:
            Shopee.objects.filter(id__in=selected_items).delete()
            messages.success(request, f'{len(selected_items)} produtos foram excluídos.')
        else:
            messages.warning(request, 'Nenhum produto foi selecionado.')
            print(request)
            print("Nenhum produto selecionado")
            print(selected_items)

    return redirect('shopee')

#@has_any_role_decorator('admin', 'expedition')
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
    
@has_any_role_decorator('admin', 'expedition')
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

@has_any_role_decorator('admin', 'expedition')
@login_required(login_url="/auth/login/")
def registrar_coleta_mercado_livre(request):
    if request.method == "POST":
        form = MercadoLivreForm(request.POST)
        if form.is_valid():

            if form.is_valid():  
                try:  
                    form.save()  
                    return redirect('mercado_livre')  
                except Exception as e:  
                    print("Ocorreu um erro ao salvar o formulário:", e)
                    print(form.errors)
                    pass  
    else:
        form = MercadoLivreForm()  
    return render(request,'registrar_coleta_mercado_livre.html',{'form':form})  

@login_required(login_url="/auth/login/")
def edit_shopee(request, id):
    shopee = Shopee.objects.get(id=id)
    
    if request.method == "POST":
        form = ShopeeForm(request.POST, instance=shopee)
        if form.is_valid():
            form.save()
            return redirect('shopee')
    else:
        form = ShopeeForm(instance=shopee)
    
    return render(request, 'edit_shopee.html', {'form': form, 'shopee': shopee})

@login_required(login_url="/auth/login/")
def edit_mercado_livre(request, id):
    mercado_livre = MercadoLivre.objects.get(id=id)
    
    if request.method == "POST":
        form = MercadoLivreForm(request.POST, instance=mercado_livre)
        if form.is_valid():
            form.save()
            return redirect('mercado_livre')
    else:
        form = MercadoLivreForm(instance=mercado_livre)
    
    return render(request, 'edit_mercado_livre.html', {'form': form, 'mercado_livre': mercado_livre})