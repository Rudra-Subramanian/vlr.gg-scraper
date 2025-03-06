import fastapi
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app


def test_health():
    response = testing_client.get("/")
    assert response.status_code == 200
    assert response.json() == 'OK'


def test_matches():
    response_schedule = testing_client.get('/matches/schedule')
    response_finished = testing_client.get('/matches/results')
    assert response_schedule.status_code == 200
    assert response_finished.status_code == 200
    print(response_schedule)
    print(response_finished)

def test_tournaments():
    response = testing_client.get('/events')
    assert response.status_code == 200
    print(response)



testing_client = TestClient(app)
test_health()
test_matches()
test_tournaments()





