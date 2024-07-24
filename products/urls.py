from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/categories/', views.category_list_api_view),
    path('api/v1/categories/<int:id>/', views.category_detail_api_view),

    path('api/v1/product/', views.products_list_api_view),
    # path('api/v1/product/<int:id>/', views.products_detail_api_view),

    path('api/v1/products/reviews/', views.rev_product_list_api_view),

    path('api/v1/review/', views.review_list_api_view),
    path('api/v1/review/<int:id>/', views.review_detail_api_view),
]