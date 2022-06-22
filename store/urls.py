from django.urls import path
from .views import ListProductData

urlpatterns = [
    path('list/product/data/', ListProductData.as_view())
]
