def test_saved_client_cookie(test_service):
    first_responce_after_put = test_service.put(
        "/preferences", 
        json = {'view': 'detailed'}
    )

    assert first_responce_after_put.status_code == 200
    assert first_responce_after_put.json()['view'] == 'detailed'

    second_responce = test_service.get("/preferences")

    assert second_responce.status_code == 200
    assert second_responce.json()['view'] == 'detailed'

    bad_responce = test_service.put(
        "/preferences", 
        json = {'view': ''}
    )

    assert bad_responce.status_code == 422
    assert bad_responce.json()["detail"][0]["loc"][1] == 'view'