import fastapi
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app


def test_health():
    response = testing_client.get("/")
    assert response.status_code == 200
    print(response.json())


def test_matches():
    response_schedule = testing_client.get('/matches/schedule')
    response_finished = testing_client.get('/matches/results')
    assert response_schedule.status_code == 200
    assert response_finished.status_code == 200
    print(response_schedule.json())
    print(response_finished.json())

def test_tournaments():
    response = testing_client.get('/events')
    assert response.status_code == 200
    print(response.json()['completed'][1])

def get_tournament_by_id(id):
    response = testing_client.get('/event/2310')
    return response.json()

def get_required_tournaments():
    vcl_response = testing_client.get('/vcl-2025')
    game_changers_response = testing_client.get('events/game-changers')
    print(vcl_response.status_code)
    print(game_changers_response.status_code)
    return vcl_response.json(), game_changers_response.json()
testing_client = TestClient(app)
x, y = get_required_tournaments()
print(y.keys())






