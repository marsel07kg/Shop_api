from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/categories/', views.CategoryListAPIView.as_view()),
    path('api/v1/categories/<int:id>/', views.CategoryDetailAPIView.as_view()),

    path('', views.ProductDetailAPIView.as_view()),
    path('api/v1/product/<int:id>/', views.ProductListAPIView.as_view()),

    path('api/v1/review/', views.ReviewListAPIView.as_view()),
    path('api/v1/review/<int:id>/', views.ReviewDetailAPIView.as_view()),
]