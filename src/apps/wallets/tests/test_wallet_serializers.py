from decimal import Decimal

from apps.wallets.api import WalletOperationSerializer


def test_wallet_operation_serializer_valid_deposit():
    data = {
        "operation_type": "DEPOSIT",
        "amount": 100
    }

    serializer = WalletOperationSerializer(data=data)

    assert serializer.is_valid()
    assert serializer.validated_data['operation_type'] == 'DEPOSIT'
    assert serializer.validated_data['amount'] == Decimal('100.00')


def test_wallet_operation_serializer_invalid_operation():
    data = {
        'operation_type': 'TRANSFER',  # not in choices
        'amount': '100.00'
    }
    serializer = WalletOperationSerializer(data=data)

    assert not serializer.is_valid()
    assert 'operation_type' in serializer.errors


def test_wallet_operation_serializer_negative_amount():
    data = {
        'operation_type': 'WITHDRAW',
        'amount': '-50.00'
    }
    serializer = WalletOperationSerializer(data=data)

    assert not serializer.is_valid()
    assert 'amount' in serializer.errors


def test_wallet_operation_serializer_empty_data():
    serializer = WalletOperationSerializer(data={})

    assert not serializer.is_valid()
    assert 'operation_type' in serializer.errors
    assert 'amount' in serializer.errors
