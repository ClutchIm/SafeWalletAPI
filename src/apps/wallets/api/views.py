from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.wallets.models import Wallet
from .serializers import WalletOperationSerializer, WalletSerializer


class WalletOperationView(APIView):
    """Wallet operation view."""
    @transaction.atomic
    def post(self, request, uuid):
        """
        POST Method that make operations with wallet
        depending on the type of operation.

        :param request: incoming request with operation_type and amount in body
        :param uuid: unique identifier of wallet
        :return: data for wallet or error
        """
        # lock another changes for this object
        wallet = get_object_or_404(
            Wallet.objects.select_for_update(),
            uuid=uuid
        )

        serializer = WalletOperationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if data['operation_type'] == 'DEPOSIT':
            wallet.balance += data['amount']
        elif data['operation_type'] == 'WITHDRAW':
            if wallet.balance < data['amount']:
                return Response(
                    {"detail": "Not enough balance."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            wallet.balance -= data['amount']

        wallet.save()
        return Response(
            {
                "detail": "Operation with wallet successful.",
                "uuid": wallet.uuid,
                "balance": wallet.balance
            },
            status=status.HTTP_200_OK
        )


class WalletsBalanceView(APIView):
    """Get wallet balance by uuid view."""
    def get(self, request, uuid):
        wallet = get_object_or_404(Wallet, uuid=uuid)

        serializer = WalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WalletsView(APIView):
    """
    It`s view just for easy testing of functionality.
    Can create and show list of wallets.
    """
    def post(self, request):
        serializer = WalletSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wallet = Wallet.objects.create(**serializer.validated_data)
        return Response(
            {
                "detail": "Wallet created successfully.",
                "uuid": wallet.uuid,
                "balance": wallet.balance
            },
            status=status.HTTP_201_CREATED
        )

    def get(self, request):
        wallets = Wallet.objects.all()
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
