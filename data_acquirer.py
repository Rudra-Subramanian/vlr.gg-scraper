import fastapi
import json
import responses
from datetime import datetime,  timedelta
from fastapi.testclient import TestClient
from main import app
from data_objects.Game import Game
from data_objects.Match import Match
from data_objects.Tournament import Tournament


def get_all_tournaments():
    response = client.get('/events')
    assert response.status_code == 200
    all_tournaments = response.json()
    upcoming_tournaments = all_tournaments['upcoming']
    completed_tournaments = all_tournaments['completed']
    upcoming_tournaments_formatted = []
    completed_tournaments_formatted = []

    for tournament in upcoming_tournaments:
        upcoming_tournaments_formatted.append(Tournament(tournament['id'], tournament['title'], tournament['status'], tournament['prize'], tournament['dates'], tournament['location'], tournament['img'], client))

    for tournament in completed_tournaments:

        completed_tournaments_formatted.append(Tournament(tournament['id'], tournament['title'], tournament['status'], tournament['prize'], tournament['dates'], tournament['location'], tournament['img'], client))

    return upcoming_tournaments_formatted, completed_tournaments_formatted


def get_correct_events():
    #Getting game changers tournaments first

    game_changers_response = client.get('/events/game-changers')
    if game_changers_response.status_code == 200:
        game_changers_response = game_changers_response.json()
        game_changers_upcoming_tournaments = game_changers_response['upcoming']
        game_changers_finished_tournaments = game_changers_response['completed']
    else:
        game_changers_upcoming_tournaments = []
        game_changers_finished_tournaments = []
        #ERROR GETTING GAME CHANGERS PAGE
        print("error getting Game changers Page")
    
    #Now getting the Valorant Challengers Leauge tournament
    vcl_response = client.get('/events/vcl-2025')

    if vcl_response.status_code == 200:
        vcl_response = vcl_response.json()
        vcl_upcoming_tournaments = vcl_response['upcoming']
        vcl_finished_tournaments = vcl_response['completed']
    else:
        vcl_upcoming_tournaments = []
        vcl_finished_tournaments = []
        #ERROR GETTING VCL PAGE
        print("error getting VCL Page")


    #Returning dictionary of data

    return {'game_changers': {'upcoming': game_changers_upcoming_tournaments, 'completed': game_changers_finished_tournaments}, 'vcl': {'upcoming': vcl_upcoming_tournaments, 'completed': vcl_finished_tournaments}}
    

def make_tournament_with_event(event):
    try:
        tournament = Tournament(event['id'], event['title'], event['status'], event['prize'], event['dates'], event['location'], event['img'], client)
        return tournament
    except:
        print("error making tournament with event name: {}".format(event['title']))
        return None






if __name__ == '__main__':

    client = TestClient(app)
    event_list = get_correct_events()
    game_changers = event_list['game_changers']
    vcl = event_list['vcl']
    game_changers_upcoming_match_list = []
    game_changers_completed_match_list = []
    vcl_upcoming_match_list = []
    vcl_completed_match_list = []
    print('length of game_changers upcoming = {}'.format(len(game_changers['upcoming'])))
    for event in game_changers['upcoming']:
        #print(event['title'])
        tournament = make_tournament_with_event(event)
        if tournament != None:
            game_changers_upcoming_match_list.append(tournament)    
    print(game_changers_upcoming_match_list[0])

    #print(upcoming_tournaments[0])
    #print('Upcoming Tournaments 1:{} \n\n\n\n\n\n\n\n\n completed tournament 1: {}'.format(upcoming_tournaments[0], completed_tournaments[0]))
    #print('Upcoming Tournaments 1:{} \n\n\n\n\n\n\n\n\n completed tournament 1: {}'.format(upcoming_tournaments[0].keys(), completed_tournaments[0].keys()))
    
    #print(json.dumps(upcoming_tournaments[0].jsonify(), indent=4)) #TO JSON DUMP FOR JSON FOLDER LATER