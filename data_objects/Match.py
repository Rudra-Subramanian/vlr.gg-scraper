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
        self.round = round
        self.stage = stage
        self.number_of_games = 2
        self.client = client
        self.score = None
        self.games = None
        self.winner = None
        self.loser = None
        self.team_1 = None
        self.team_2 = None
        self.maps = {}
        self.overall_player_stats = {}


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
            self.all_game_data = response.json()
        except Exception as e:
            print('Error getting games for match: {}'.format(self.match_id))
            print("error: {}\n\n".format(e))
    
    def init_games(self):
        print('IN init_games in Match class {}'.format(self.all_game_data.keys()))

        #TODO get correct data to fill match from all_games dictionary then create individual games from all_games['data']
        #TODO Then create player object that fills player info grom all_games['data']['members']
        #self.games = Game(self.all_games['teams'], self.all_games['score'], self.all_games['note'], self.all_games['event'], self.all_games['data'], self.all_games['head2head'], self.match_id)
        #finding winner and loser and score
        self.score = self.all_game_data['score']
        self.team_1 = self.all_game_data['teams'][0]['name']
        self.team_2 = self.all_game_data['teams'][1]['name']
        if self.score.split(':')[0] > self.score.split(':')[1]:
            self.winner = self.team_1
            self.loser = self.team_2
        elif self.score.split(':')[0] < self.score.split(':')[1]:
            self.winner = self.team_2
            self.loser = self.team_1
        else:
            self.winner = None
            self.loser = None
            print("No winner or loser")
        
        #Finding number of games
        self.number_of_games = len(self.all_game_data['data']) - 1

        #getting maps
        for game in self.all_game_data['data']:
            if game['map'] == 'All Maps':
                for member in game['members']:
                    name = member.get('name', None)
                    if name:
                        self.overall_player_stats[name] = member
                


                                                                                                                                                                                        
'''
Tournament class
contains list of upcoming and completed matches
'''
