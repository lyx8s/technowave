from django.urls import include, path

urlpatterns = [
    path('', include('users.urls')),
    path('', include('products.urls')),
    path('', include('configurators.urls')),
    path('', include('orders.urls'))
]
