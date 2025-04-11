from rest_framework import serializers
from decimal import Decimal

from apps.wallets.models import Wallet


class WalletOperationSerializer(serializers.Serializer):
    OPERATION_CHOICES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
    )

    operation_type = serializers.ChoiceField(choices=OPERATION_CHOICES)
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('0.01')
    )


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
