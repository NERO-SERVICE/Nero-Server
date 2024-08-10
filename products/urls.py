from django.urls import path
from .views import CreateProductView, RetrieveProductView, UpdateProductView, DeleteProductView, ListProductsView

app_name = "products"

urlpatterns = [
    path('', ListProductsView.as_view(), name='list_products'),
    path('create/', CreateProductView.as_view(), name='create_product'),
    path('<int:id>/', RetrieveProductView.as_view(), name='get_product'),
    path('<int:id>/update/', UpdateProductView.as_view(), name='update_product'),
    path('<int:id>/delete/', DeleteProductView.as_view(), name='delete_product'),
]
