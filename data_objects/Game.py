import json
import responses
from datetime import datetime,  timedelta
'''
Game class
contains single game information


TODO change game to get the data from a match and make individual games
'''   

class Game:
    def __init__(self, teams, score, note, event, data, head2head, id):
        self.teams = teams
        self.score = score
        self.note = note
        self.event = event
        self.data = data
        self.head2head = head2head
        self.id = id
        self.save_to_file()
        
    
    def jsonify(self):
        return {'teams': self.teams, 'score': self.score, 
                'note': self.note, 'event': self.event, 
                'data': self.data, 'head2head': self.head2head, 
                'id': self.id}


    def save_to_file(self):
        file_name = 'LastGame'
        output_data = self.jsonify()
        with open(file_name, 'w') as file:
            json.dump(output_data, file, indent=4)

    def process_game_data(self):
        processed_data = {
            "team1": self.teams[0]['name'],
            "team2": self.teams[1]['name'],
            "maps": []
        }
        map_count = 0
        for map_data in self.data:
            map_info = {
                "map": map_data["map"],
                "teams": map_data["teams"],
                "members": map_data["members"],
                "rounds": map_data["rounds"]
            }
            if map_data['map'] != 'All Maps':
                map_count += 1
            processed_data["maps"].append(map_info)

        return processed_data