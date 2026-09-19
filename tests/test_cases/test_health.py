def test_health(client):
    response = client.get("/")
    assert response.json() == {"status": "Welcome to My Grehthrapp By Vishal K. Pal"}


def test_health(client):
    response = client.get("/health")
    assert response.json() == {"status": "healthy"}
