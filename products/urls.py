from django.urls import path
from .views import CreateProductView, RetrieveProductView, UpdateProductView, DeleteProductView, ListProductsView

app_name="products"

urlpatterns = [
    path('products/', ListProductsView.as_view(), name='list_products'),
    path('products/create/', CreateProductView.as_view(), name='create_product'),
    path('products/<str:doc_id>/', RetrieveProductView.as_view(), name='get_product'),
    path('products/<str:doc_id>/update/', UpdateProductView.as_view(), name='update_product'),
    path('products/<str:doc_id>/delete/', DeleteProductView.as_view(), name='delete_product'),
]
