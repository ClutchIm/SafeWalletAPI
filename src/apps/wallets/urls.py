from django.urls import path
from apps.wallets.api import (WalletOperationView,
                              WalletsBalanceView,
                              WalletsView)

urlpatterns = [
    path("<uuid:uuid>/operation/", WalletOperationView.as_view()),
    path("<uuid:uuid>/", WalletsBalanceView.as_view()),
    path("", WalletsView.as_view()),
]
