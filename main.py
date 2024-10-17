import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class League:
    def __init__(self):
        with open('json/league.json') as file:
            data = json.load(file)
        self.data = data

class Matchup:
    def __init__(self, week):
        with open(f'json/matchups/matchups_week_{week}.json') as file:
            data = json.load(file)
        self.df = pd.DataFrame(data)

class Player:
    def __init__(self):
        with open('json/players.json') as file:
            data = json.load(file)
        self.df = pd.DataFrame(data).transpose()
    
    def get_player_id_from_full_name(self, full_name):
        return self.df[(self.df['full_name'] == full_name)]['player_id'].item()

    def get_full_name_from_player_id(self, player_id):
        return self.df[(self.df['player_id'] == player_id)]['full_name'].item()


class Roster:
    def __init__(self):
        with open('json/rosters.json') as file:
            data = json.load(file)
        self.df = pd.DataFrame(data)

class User:
    def __init__(self):
        with open('json/users.json') as file:
            data = json.load(file)
        self.df = pd.DataFrame(data)

    def get_user_id_from_display_name(self, display_name):
        return self.df[(self.df['display_name'] == display_name)]['user_id'].item()

    def get_display_name_from_user_id(self, user_id):
        return self.df[(self.df['user_id'] == user_id)]['display_name'].item()
    
class WeeklyProjections:
    def __init__(self, week):
        with open(f'json/projections/projections_week_{week}.json') as file:
            data = json.load(file)
        self.df = pd.DataFrame(data)

    def get_player_projected_points(self, player_id, scoring_settings):
        projection = 0
        # get player projections
        player_projection = self.df[(self.df['player_id'] == player_id)]['stats']
        # get stats from projections
        for stats in player_projection:
            # for each stat
            for stat in stats:
                # if key from player stats is an actual stat
                if stat in scoring_settings:
                    # multiply the scoring setting number with the player's projected number for that stat
                    stat_projection = scoring_settings[stat] * stats[stat]
                    # add to projected total for player
                    projection += stat_projection
        return projection

class WeeklyStatistics:
    def __init__(self, week):
        with open(f'json/stats/stats_week_{week}.json') as file:
            data = json.load(file)
        self.df = pd.DataFrame(data)
    
    def get_player_scored_points(self, player_id, scoring_settings):
        scored = 0
        # get player stats
        if not self.df.empty and (self.df['player_id'] == player_id).any():
            player_stats = self.df[(self.df['player_id'] == player_id)]['stats']
            # get stats
            for stats in player_stats:
                # for each stat
                for stat in stats:
                    # if key from player stats is an actual stat
                    if stat in scoring_settings:
                        # multiply the scoring setting number with the player's stat
                        stat_scored = scoring_settings[stat] * stats[stat]
                        # add to projected total for player
                        scored += stat_scored
            return scored
        else:
            print(f'Error: Player {player_id} has not played this week.')


#================


# SLEEPER API: https://docs.sleeper.com/

league = League()
players = Player()
rosters = Roster()
users = User()

proj_week_7 = WeeklyProjections(7)
stats_week_6 = WeeklyStatistics(6)
matchups_week_1 = Matchup(1)

#df = pd.merge(matchups_week_1.df[['roster_id', 'starters', 'matchup_id']], rosters.df[['roster_id', 'owner_id']], on='roster_id', how='inner').rename(columns={'owner_id': 'user_id'})
#print(pd.merge(df, users.df[['user_id', 'display_name']], on='user_id', how='inner'))

print(proj_week_7.get_player_projected_points(players.get_player_id_from_full_name('Chuba Hubbard'), league.data['scoring_settings']))
print(stats_week_6.get_player_scored_points(players.get_player_id_from_full_name('Chuba Hubbard'), league.data['scoring_settings']))