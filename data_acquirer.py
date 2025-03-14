import fastapi
import json
import responses
from datetime import datetime,  timedelta
from fastapi.testclient import TestClient
from main import app






'''
Game class
contains single game information

'''   

class Game:
    def __init__(self, teams, score, note, event, data, head2head):
        self.teams = teams
        self.score = score
        self.note = note
        self.event = event
        self.data = data
        self.head2head = head2head
    
    def jsonify(self):
        return {'teams': self.teams, 'score': self.score, 'note': self.note, 'event': self.event, 'data': self.data, 'head2head': self.head2head}d

'''
Match class
contains dictionary of games
'''

class Match:
    def __init__(self, id, time, teams, status, eta, round, stage, date):
        self.match_id = id
        self.time = time
        self.teams = teams
        self.status = status
        self.eta = eta
        self.round = round
        self.stage = stage
        self.date = date
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
        #print('match_id in find_games -- {}'.format(self.match_id))
        try:
            #print('trying to get games for match: {}'.format(self.match_id))
            response = client.get('/match/{}'.format(self.match_id))
            #print(response.status_code)
            self.all_games = response.json()
        except Exception as e:
            print('Error getting games for match: {}'.format(self.match_id))
            print("error: {}\n\n".format(e))
    
    def init_games(self):
        print('IN init_games in Match class {}'.format(self.all_games.keys()))

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
        self.all_matches = []
        try:
            self.find_data()
        except Exception as e:
            print('Error finding data for tournament in Tournament.find_data --: {}'.format(self.title))
            print("error: {}\n\n".format(e))
        try:
            self.init_dates()
        except:
            print('Error making dates for tournament in Tournament.init_dates--: {}'.format(self.title))
            print("error: {}\n\n".format(e))
        self.init_matches()
    

    def find_data(self):

        response = client.get('/event/{}'.format(self.id))
        assert response.status_code == 200
        self.all_data = response.json()
        self.raw_matches = self.all_data['matches']

    def init_dates(self):
        #print(self.dates)
        current_year = datetime.now().year
        self.date_split = self.dates.split('—')
        self.start_date = self.date_split[0] + ' ' + str(current_year)
        self.end_date = self.date_split[1]
        
        if self.end_date.isdigit():
            #print(self.start_date.split(' ')[0])
            self.end_date = self.start_date.split(' ')[0] + ' ' + self.end_date
            #print(self.end_date)
        self.end_date = self.end_date + ' ' + str(current_year)

        self.start_date = datetime.strptime(self.start_date, '%b %d %Y')
        self.end_date = datetime.strptime(self.end_date, '%b %d %Y')
        #print('Start Date: {} \n End Date: {}'.format(self.start_date, self.end_date))
       

        #for match in self.matches:


    
    def init_matches(self):
        #print('Upcoming Games:')
        #print('second match in tournament in init_matches {}'.format(self.matches[2]))
        print(self.title)
        for match_day in self.raw_matches:
            match_date = datetime.strptime(match_day['date'], '%a, %B %d, %Y')
            #print('init_matches -- match date: {}'.format(match_date))
            #sanity check
            if (match_date > self.end_date) or (match_date < self.start_date):
                raise Exception('Match date is not within tournament date range')
            
            #continue on
            #print(len(match_day['matches']))
            for match in match_day['matches']:
                print('match_id in init_matches -- {}'.format(match['id']))
                self.all_matches.append(Match(match['id'], match['time'], match['teams'], match['status'], match['eta'], match['round'], match['stage'], match_date))
                #print('Match: {} \n date: {}\n\n'.format(match.keys(), match_date))
                


        '''

        try:
            for match in self.matches['upcoming']:
                #print('Match: {} \n date: {}\n\n'.format(match['id'], match['location']))
                self.upcoming_matches.append(Match(match['id'], match['title'], match['status'], match['prize'], match['dates'], match['location'], match['img'], self.title))
        except Exception as e:
            print('Error initializing matches for tournament: {}'.format(self.title))
            print("error: {}\n\n".format(e))
        try:
            for match in self.matches['completed']:
                #print('Match: {} \n date: {}\n\n'.format(match['id'], match['location']))
                self.completed_matches.append(Match(match['id'], match['title'], match['status'], match['prize'], match['dates'], match['location'], match['img'], self.title))
        except Exception as e:
            print('Error initializing matches for tournament: {}'.format(self.title))
            print("error: {}\n\n".format(e))
        '''
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

    for tournament in upcoming_tournaments:
        upcoming_tournaments_formatted.append(Tournament(tournament['id'], tournament['title'], tournament['status'], tournament['prize'], tournament['dates'], tournament['location'], tournament['img']))

    for tournament in completed_tournaments:

        completed_tournaments_formatted.append(Tournament(tournament['id'], tournament['title'], tournament['status'], tournament['prize'], tournament['dates'], tournament['location'], tournament['img']))

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
        tournament = Tournament(event['id'], event['title'], event['status'], event['prize'], event['dates'], event['location'], event['img'])
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