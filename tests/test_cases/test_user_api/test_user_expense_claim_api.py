import json
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent / "expected_responses/user/expense_claim"

def read_json(filename):
    with open(BASE_PATH / filename, "r") as f:
        return json.load(f)

# -------------------------------------------------test user api ---------------------------------------------------
def test_user_get_my_expense_using_id(client, user_A1):
    response = client.get(
        "/user/my/expense-claims/5",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    expected = read_json("get_user1_expenseid_5.json")
    assert response.status_code == 200
    assert response.json() == expected
    

def test_user_get_others_expense_using_id(client, user_A1):
    response = client.get(
        "/user/my/expense-claims/1",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 403
    assert response.json() == {'detail': 'Not authorized'}


def test_user_get_my_expense_using_id_expense_not_exist(client, user_A1):
    response = client.get(
        "/user/my/expense-claims/16",
        headers={"Authorization": f"Bearer {user_A1}"},
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Expense claim not found'}




