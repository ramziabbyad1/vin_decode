#!/usr/bin/env python3

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#pytestmark = pytest.mark.parametrize("test_vin", ["1XPWD40X1ED215307", "4V4NC9EJXEN171694"])

@pytest.fixture(scope="session")
def test_vin():
    return "4V4NC9EJXEN171694"

def test_lookup_vin_existing_cache(test_vin):
    response = client.get(f"/lookup?vin={test_vin}")
    response = client.get(f"/lookup?vin={test_vin}")
    assert response.status_code == 200
    assert response.json()["cached_result"] is True


def test_lookup_vin_new_cache(test_vin):
    response = client.get(f"/remove?vin={test_vin}")
    response = client.get(f"/lookup?vin={test_vin}")
    assert response.status_code == 200
    assert response.json()["cached_result"] is False


def test_lookup_vin_invalid_vin():
    response = client.get("/lookup?vin=INVALIDVIN123")
    assert response.status_code == 422


def test_remove_vin(test_vin):
    response = client.get(f"/remove?vin={test_vin}")
    assert response.status_code == 200
    assert response.json()["cache_delete_success"] is True


def test_export_cache():
    response = client.get("/export")
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__])

