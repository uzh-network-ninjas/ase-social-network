
# !! variable must have the same name as the function in conftest.py
def test_read_helloworld(test_app):
    response = test_app.get("/helloworld")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}