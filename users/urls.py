from django.urls import path
from . import views

urlpatterns = [
    path('registraion/', views.register_api_view),
    path('authorization/', views.authorization_api_view),
    path('confirm/', views.confirm_api_view)
]