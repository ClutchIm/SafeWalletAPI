from django.urls import path
from apps.wallets.api import WalletOperationView, WalletsView

urlpatterns = [
    path("<uuid:uuid>/operation/", WalletOperationView.as_view()),
    path("", WalletsView.as_view()),
]