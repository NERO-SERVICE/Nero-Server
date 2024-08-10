from django.urls import path
from .views import CreateProductView, RetrieveProductView, UpdateProductView, DeleteProductView, ListProductsView

app_name = "products"

urlpatterns = [
    path('', ListProductsView.as_view(), name='list_products'),
    path('create/', CreateProductView.as_view(), name='create_product'),
    path('<int:docId>/', RetrieveProductView.as_view(), name='get_product'),
    path('<int:docId>/update/', UpdateProductView.as_view(), name='update_product'),
    path('<int:docId>/delete/', DeleteProductView.as_view(), name='delete_product'),
]
