from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

"""
Configuração de URLs do projeto, mapeando endpoints para as respectivas views.

Endpoints:
- / -> Página inicial (index.html)
- carregamento/ -> Mediador entre páginas
- listar/ -> Lista categorias
- indicacoes/ -> Lista indicações realizadas
- indicar_usuario/<int:categoria_id>/ -> Indica um usuário em uma categoria específica
- exportar/ -> Exporta votos para um arquivo Excel
- api/token/ -> Obtém token JWT
- api/token/refresh/ -> Atualiza token JWT
- login/ -> Página de login
- votos/ -> Página de votos
- resetar-votos/ -> Reseta os votos
- delete/ -> Página de exclusão

"""

urlpatterns = [
    path('', views.index, name='index'),
    path('carregamento/', views.carregamento, name='carregamento'),
    path('listar/', views.listar_categorias, name='listar_categorias'),
    path('indicacoes/', views.listar_indicacoes_realizadas, name='listar_indicacoes_realizadas'),
    path('indicar_usuario/<int:categoria_id>/', views.indicar_usuario, name='indicar_usuario'),
    path('exportar/', views.exportar_votos_para_excel, name='exportar_excel'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.login_page, name='login'),
    path('votos/', views.votos_page, name='votos_page'),
    path('resetar-votos/', views.resetar_votos, name='resetar_votos'),
    path('delete/', views.delete_page, name='delete'),
]