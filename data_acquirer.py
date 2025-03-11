import fastapi
import json
import responses
from fastapi.testclient import TestClient
from main import app






'''
Game class
contains single game information

'''   

class Game:
    def __init__(self):
        self.game_id = game_id
        self.game_team1 = game_team1
        self.game_team2 = game_team2
        self.game_date = game_date
        self.game_time = game_time
        self.game_region = game_location
        self.game_result = game_result
        self.game_tournament = game_tournament
        self.game_match = game_match
        self.team1_comp = []
        self.team2_comp = []
        self.team1_score = 0
        self.team2_score = 0
        self.timeline = {}
    
    def jsonify(self):
        return {'id': self.game_id, 'team1': self.game_team1, 'team2': self.game_team2, 'date': self.game_date, 'time': self.game_time, 'region': self.game_region, 'result': self.game_result, 'tournament': self.game_tournament, 'match': self.game_match, 'team1_comp': self.team1_comp, 'team2_comp': self.team2_comp, 'team1_score': self.team1_score, 'team2_score': self.team2_score, 'timeline': self.timeline}


'''
Match class
contains dictionary of games
'''

class Match:
    def __init__(self, id, title, status, prize, dates, location, img_url, tournament_name):
        self.match_id = id
        self.match_team1 = None
        self.match_team2 = None
        self.match_date = dates
        self.match_time = None
        self.match_location = location
        self.match_result = None
        self.match_tournament = tournament_name
        self.score_to_win = 2
        self.number_of_games = 2
        self.games = {}
        self.find_games()
        self.init_games()
    
    def jsonify(self):
        jsonified_games = {}
        for game in self.games:
            jsonified_games[game] = self.games[game].jsonify()
        return {'id': self.match_id, 'title': self.title, 'status': self.status, 'prize': self.prize, 'dates': self.dates, 'location': self.location, 'img_url': self.img_url, 'games': jsonified_games}

    def find_games(self):
        response = client.get('/match/{}'.format(self.match_id))
        #print(response.status_code)
        self.all_games = response.json()
    
    def init_games(self):
        print(self.all_games)

'''
Tournament class
contains list of upcoming and completed matches
'''

class Tournament:
    def __init__(self, id, title, status, prize, dates, location, img_url):
        self.id = id
        self.title = title
        self.status = status
        self.prize = prize
        self.dates = dates
        self.location = location
        self.img_url = img_url
        self.upcoming_matches = []
        self.completed_matches = []
        self.find_data()
        #self.init_matches()
    

    def find_data(self):
        print(self.id)
        response = client.get('/event/{}'.format(self.id))
        assert response.status_code == 200
        self.all_data = response.json()
        self.matches = self.all_data['matches']
        print(self.matches)
    
    def init_matches(self):
        #print('Upcoming Games:')
        print(self.all_data.keys())
        for match in self.all_data['upcoming']:
            #print('Match: {} \n date: {}\n\n'.format(match['id'], match['location']))
            self.upcoming_matches.append(Match(match['id'], match['title'], match['status'], match['prize'], match['dates'], match['location'], match['img'], self.title))
        for match in self.all_data['completed']:
            #print('Match: {} \n date: {}\n\n'.format(match['id'], match['location']))
            self.completed_matches.append(Match(match['id'], match['title'], match['status'], match['prize'], match['dates'], match['location'], match['img'], self.title))
    
    def __str__(self):
        return_string = 'id: {}\n title: {}\n status: {}\n prize: {}\n dates: {}\n location: {}\n img_url: {}\n'.format(self.id, self.title, self.status, self.prize, self.dates, self.location, self.img_url)
        return return_string
    
    def jsonify(self):
        jsonified_upcoming = []
        jsonified_completed = []
        for match in self.upcoming_matches:
            jsonified_upcoming.append(match.jsonify())
        for match in self.completed_matches:
            jsonified_completed.append(match.jsonify())
        return {'id': self.id, 'title': self.title, 'status': self.status, 'prize': self.prize, 'dates': self.dates, 'location': self.location, 'img_url': self.img_url, 'upcoming_matches': self.upcoming_matches, 'completed_matches': self.completed_matches}




def get_all_tournaments():
    response = client.get('/events')
    assert response.status_code == 200
    all_tournaments = response.json()
    upcoming_tournaments = all_tournaments['upcoming']
    completed_tournaments = all_tournaments['completed']
    upcoming_tournaments_formatted = []
    completed_tournaments_formatted = []
    counter = 0
    for tournament in upcoming_tournaments:
        counter = counter + 1
        upcoming_tournaments_formatted.append(Tournament(tournament['id'], tournament['title'], tournament['status'], tournament['prize'], tournament['dates'], tournament['location'], tournament['img']))
        if counter > max_iterations:
            break
    counter = 0
    for tournament in completed_tournaments:
        counter = counter + 1
        completed_tournaments_formatted.append(Tournament(tournament['id'], tournament['title'], tournament['status'], tournament['prize'], tournament['dates'], tournament['location'], tournament['img']))
        if counter > max_iterations:
            break
    return upcoming_tournaments_formatted, completed_tournaments_formatted







if __name__ == '__main__':

    global max_iterations
    max_iterations = 2
    client = TestClient(app)
    upcoming_tournaments, completed_tournaments = get_all_tournaments()
    #print(upcoming_tournaments[0])
    #print('Upcoming Tournaments 1:{} \n\n\n\n\n\n\n\n\n completed tournament 1: {}'.format(upcoming_tournaments[0], completed_tournaments[0]))
    #print('Upcoming Tournaments 1:{} \n\n\n\n\n\n\n\n\n completed tournament 1: {}'.format(upcoming_tournaments[0].keys(), completed_tournaments[0].keys()))
    
    #print(json.dumps(upcoming_tournaments[0].jsonify(), indent=4)) #TO JSON DUMP FOR JSON FOLDER LATER