from django.urls import path, include

urlpatterns = [
    path('wallets/', include('apps.wallets.urls')),
]