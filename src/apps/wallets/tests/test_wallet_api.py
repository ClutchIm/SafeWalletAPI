import pytest
import uuid
from rest_framework.test import APIClient
from concurrent.futures import ThreadPoolExecutor, as_completed

from apps.wallets.service import create_wallet


@pytest.mark.django_db(transaction=True)
def test_concurrent_withdrawals_should_not_exceed_balance():
    client = APIClient()

    wallet = create_wallet(balance=90)

    url = f"/api/v1/wallets/{wallet.uuid}/operation/"
    data = {
        "operation_type": "WITHDRAW",
        "amount": 10
    }

    # 10 requests in parallel to withdraw 10 currencies
    def send_withdraw():
        return client.post(url, data=data, format="json")

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(send_withdraw) for _ in range(10)]
        for future in as_completed(futures):
            results.append(future.result())

    # Check that only 10 requests were successful (HTTP 200 or 201)
    success_count = sum(1 for r in results if r.status_code == 200)
    assert success_count == 9

    wallet.refresh_from_db()
    assert wallet.balance >= 0
    assert wallet.balance == 90 - 10 * success_count


@pytest.mark.django_db(transaction=True)
def test_concurrent_deposits_should_not_exceed_balance():
    client = APIClient()
    wallet = create_wallet()
    url = f"/api/v1/wallets/{wallet.uuid}/operation/"
    data = {
        "operation_type": "DEPOSIT",
        "amount": 10
    }

    def send_deposit():
        return client.post(url, data=data, format="json")

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(send_deposit) for _ in range(10)]
        for future in as_completed(futures):
            results.append(future.result())

    # Check that only 10 requests were successful (HTTP 200 or 201)
    success_count = sum(1 for r in results if r.status_code == 200)
    assert success_count <= 10

    wallet.refresh_from_db()
    assert wallet.balance == 10 * success_count


@pytest.mark.django_db
def test_get_wallet_by_uuid_successful():
    client = APIClient()
    wallet = create_wallet()
    url = f"/api/v1/wallets/{wallet.uuid}/"

    response = client.get(url)

    assert response.status_code == 200
    assert response.data['uuid'] == str(wallet.uuid)


@pytest.mark.django_db
def test_get_wallet_by_uuid_failed():
    client = APIClient()
    url = f"/api/v1/wallets/{uuid.uuid4()}/"

    response = client.get(url)

    assert response.status_code == 404
