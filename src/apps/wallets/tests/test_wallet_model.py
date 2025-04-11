import pytest
from django.core.exceptions import ValidationError

from apps.wallets.models import Wallet
from apps.wallets.service import create_wallet


@pytest.mark.django_db
def test_create_wallet():
    wallet = create_wallet()

    assert isinstance(wallet, Wallet)
    assert wallet.balance == 0


@pytest.mark.django_db
def test_create_wallet_with_balance():
    wallet = create_wallet(balance=1000)

    assert isinstance(wallet, Wallet)
    assert wallet.balance == 1000


@pytest.mark.django_db
def test_wallet_negative_balance_should_fail():
    wallet = Wallet(balance=-100)

    with pytest.raises(ValidationError):
        wallet.full_clean()
        wallet.save()
