from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)  # Biblioteca de documentação da API

# Autenticação
from rest_framework_simplejwt.views import (
    TokenObtainPairView, #Pegar o par de tokens
    TokenRefreshView
)


urlpatterns = [
    path('api/v1/user', include('user.urls')), #Incluir todas as rotas de user.urls
    path('admin/', admin.site.urls),

    # Rotas de Autenticação
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    # Rotas de Documentação
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view('api-schema'), name='api-docs'),


]
