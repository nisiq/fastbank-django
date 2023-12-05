from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register('accounts', views.AccountViewSet)
router.register(r'historico_cartao', views.HistoricoCartaoViewSet, basename='historico_cartao')
router.register(r'historico-saldo', views.HistoricoSaldoViewSet, basename='historico-saldo')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls))
]