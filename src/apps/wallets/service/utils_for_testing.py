from apps.wallets.models import Wallet


def create_wallet(balance: int | None = None) -> Wallet:
    kwargs = {}
    if balance is not None:
        kwargs['balance'] = balance
    return Wallet.objects.create(**kwargs)
