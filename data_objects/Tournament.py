from data_objects.Match import Match
import fastapi
import json
import responses
from datetime import datetime,  timedelta
from fastapi.testclient import TestClient


class Tournament:
    def __init__(self, id, title, status, prize, dates, location, img_url, client):
        self.id = id
        self.title = title
        self.status = status
        self.prize = prize
        self.dates = dates
        self.location = location
        self.img_url = img_url
        self.all_matches = []
        self.client = client
        
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

        response = self.client.get('/event/{}'.format(self.id))
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
                #print('match_id in init_matches -- {}'.format(match['id']))
                self.all_matches.append(Match(match['id'], match['time'], match['teams'], match['status'], match['eta'], match['round'], match['stage'], match_date, self.client))
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

