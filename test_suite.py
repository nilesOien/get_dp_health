from fastapi import status
from fastapi.testclient import TestClient

# Import the app
from .get_dp_health import getDPhealthApp

# Get a test client (so the server doesn't have to be running to run unit tests).
client = TestClient(getDPhealthApp)


# Test if we get good HTTP status (status 200) when we ask for the JSON via GET
def test_getGoodStatusGet():
    response = client.get(
        "/get-dp-health-get?provider=NSO&source=GONG&instrument=Learmonth"
    )
    assert response.status_code == status.HTTP_200_OK


# Test if we get good HTTP status (status 200) when we ask for the JSON via POST
def test_getGoodStatusPost():
    response = client.post(
        "/get-dp-health-post",
        json={"provider": "NSO", "source": "GONG", "instrument": "Learmonth"},
    )
    assert response.status_code == status.HTTP_200_OK
