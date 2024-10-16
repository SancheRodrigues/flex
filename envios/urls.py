from envios.views import *
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', menu, name='menu'),
    path('dashboard', dashboard, name='dashboard'),
    path('auth/login/', login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('registrar', cad, name='cad'),
    path('mercado_livre', mercado_livre, name='mercado_livre'),
    path('shopee', shopee, name='shopee'),
    path('shopee/registrar_coleta/', registrar_coleta_shopee, name='registrar_coleta_shopee'),
    path('shopee/selected_delete/', bulk_delete_shopee, name='bulk_delete_shopee'),
    path('mercado_livre/selected_delete/', bulk_delete_mercado_livre, name='bulk_delete_mercado_livre'),
    path('mercado_livre/registrar_coleta/', registrar_coleta_mercado_livre, name='registrar_coleta_mercado_livre'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)