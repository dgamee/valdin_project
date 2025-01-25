from django.urls import path
from .views import (DashboardListView, 
                    CreateClientView, ClientsListView, ClientDetailView, ClientDeleteView, ClientUpdateView, 
                    ProductsListView,CreateProductView,ProductUpdateView, ProductDetailView,ProductDeleteView, 
                    AddToCartView, CartView,CartItemDeleteView,CheckoutView,
)



urlpatterns = [
    path('create-client/', CreateClientView.as_view(), name='create_client'),
    path("clients/", ClientsListView.as_view(), name="list_client"),
    path("client/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='delete_client'),
    path('client/<int:pk>/edit/', ClientUpdateView.as_view(), name='edit_client'),


    path("", DashboardListView.as_view(), name="dashboard"),

    path('product/create-product/', CreateProductView.as_view(), name='create_product'),
    path("products/", ProductsListView.as_view(), name="list_product"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path('product/<int:pk>/delete/',ProductDeleteView.as_view(), name='delete_product'),
    path('product/<int:pk>/edit/',ProductUpdateView.as_view(), name='edit_product'),

    path('product/<int:pk>/add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart', CartView.as_view(), name='view_cart'),
    path('cart/<int:pk>/delete/',CartItemDeleteView.as_view(), name='delete_cart_product'),
    path('checkout',CheckoutView.as_view(), name='checkout'),
    
]