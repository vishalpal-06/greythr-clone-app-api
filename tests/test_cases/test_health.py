import pytest


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        (
            "/",
            {"status": "Welcome to Greyth-Hr Clone By Vishal K. Pal"},
        ),
        (
            "/health",
            {"status": "healthy"},
        ),
    ],
)
def test_health(client, url, expected):
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == expected
