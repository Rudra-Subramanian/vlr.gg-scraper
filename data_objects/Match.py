from data_objects.Game import Game
import fastapi
import json
import responses
from datetime import datetime,  timedelta
from fastapi.testclient import TestClient
'''
Match class
contains dictionary of games
'''

class Match:
    def __init__(self, id, time, teams, status, eta, round, stage, date, client):
        self.match_id = id
        self.time = time
        self.teams = teams
        self.status = status
        self.eta = eta
        self.round = round
        self.stage = stage
        self.date = date
        self.number_of_games = 2
        self.games = None
        self.client = client


        self.find_games()
        
        #print("TEAMS ARE - \n{}\n as {}\n".format(self.teams, type(self.teams)))
        try:
            self.init_games()
        except Exception as e:
            print('Error initializing games for match in Match -- {}'.format(self.match_id))
            print("error: {}\n\n".format(e))
    
    def jsonify(self):
        jsonified_games = {}
        for game in self.games:
            jsonified_games[game] = self.games[game].jsonify()
        return {'id': self.match_id, 'title': self.title, 'status': self.status, 'prize': self.prize, 'dates': self.dates, 'location': self.location, 'img_url': self.img_url, 'games': jsonified_games}

    def find_games(self):
        #print('match_id in find_games -- {}'.format(self.match_id))
        try:
            #print('trying to get games for match: {}'.format(self.match_id))
            response = self.client.get('/match/{}'.format(self.match_id))
            #print(response.status_code)
            self.all_games = response.json()
        except Exception as e:
            print('Error getting games for match: {}'.format(self.match_id))
            print("error: {}\n\n".format(e))
    
    def init_games(self):
        print('IN init_games in Match class {}'.format(self.all_games.keys()))
        #TODO get correct data to fill match from all_games dictionary then create individual games from all_games['data']
        #TODO Then create player object that fills player info grom all_games['data']['members']
        #self.games = Game(self.all_games['teams'], self.all_games['score'], self.all_games['note'], self.all_games['event'], self.all_games['data'], self.all_games['head2head'], self.match_id)

'''
Tournament class
contains list of upcoming and completed matches
'''
