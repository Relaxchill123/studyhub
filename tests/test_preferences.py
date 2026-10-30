import pytest

@pytest.mark.parametrize(
    ("planner_version", "expected_status"),
    [("1", 200), ("A" * 65, 422)],
)

def test_contract_title(test_service, planner_version, expected_status):
    response_without_header = test_service.get("preferences")

    assert response_without_header.status_code == 200
    assert response_without_header.json()['view'] == 'compact'
    assert response_without_header.json()['client_version'] == None
    assert response_without_header.headers['X-Planner-Version'] == '1'

    response_with_correct_header = test_service.get(
            "preferences",
            headers={"X-Client-Version": ''},
        )

    assert response_with_correct_header.status_code == 200
    assert response_with_correct_header.json()['client_version'] == ''
    assert response_with_correct_header.json()['view'] == 'compact'
    assert response_with_correct_header.headers['X-Planner-Version'] == '1'

    response = test_service.get(
        "preferences",
        headers={"X-Client-Version": planner_version},
    )
    
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.headers['X-Planner-Version'] == '1'
        assert response.json()['view'] == 'compact'
        assert response.headers['X-Planner-Version'] == '1'

    if expected_status == 422:
        print(response.json()["detail"])
        assert response.json()["detail"][0]["loc"][0] == 'header'