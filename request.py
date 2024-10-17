import json
import requests

# constants
LEAGUE_ID = 1132375629523062784
SEASON = 2024

# League
# Sleeper API call
league_url = f'https://api.sleeper.app/v1/league/{LEAGUE_ID}'
# convert to JSON
league_data = requests.get(league_url).json()
# write JSON to file
with open('json/league.json', 'w') as file:
    json.dump(league_data, file)

# Matchups
for week in range(1, 19):
    matchups_url = f'https://api.sleeper.app/v1/league/{LEAGUE_ID}/matchups/{week}'
    matchups_data = requests.get(matchups_url).json()
    with open(f'json/matchups/matchups_week_{week}.json', 'w') as file:
        json.dump(matchups_data, file)

# Players
players_url = f'https://api.sleeper.app/v1/players/nfl'
players_data = requests.get(players_url).json()
with open('json/players.json', 'w') as file:
    json.dump(players_data, file)

# Projections for each week in the season
for week in range(1, 19):
    projections_url = f"https://api.sleeper.app/projections/nfl/{SEASON}/{week}?season_type=regular&position[]=DB&position[]=DEF&position[]=DL&position[]=FLEX&position[]=IDP_FLEX&position[]=K&position[]=LB&position[]=QB&position[]=RB&position[]=REC_FLEX&position[]=SUPER_FLEX&position[]=TE&position[]=WR&position[]=WRRB_FLEX&order_by=ppr"
    projections_data = requests.get(projections_url).json()
    with open(f'json/projections/projections_week_{week}.json', 'w') as file:
        json.dump(projections_data, file)

# Stats for each week in the season
for week in range(1, 19):
    stats_url = f"https://api.sleeper.app/stats/nfl/{SEASON}/{week}?season_type=regular&position[]=DB&position[]=DEF&position[]=DL&position[]=FLEX&position[]=IDP_FLEX&position[]=K&position[]=LB&position[]=QB&position[]=RB&position[]=REC_FLEX&position[]=SUPER_FLEX&position[]=TE&position[]=WR&position[]=WRRB_FLEX&order_by=ppr"
    stats_data = requests.get(stats_url).json()
    with open(f'json/stats/stats_week_{week}.json', 'w') as file:
        json.dump(stats_data, file)

# Rosters
rosters_url = f'https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters'
rosters_data = requests.get(rosters_url).json()
with open('json/rosters.json', 'w') as file:
    json.dump(rosters_data, file)

# Users
users_url = f'https://api.sleeper.app/v1/league/{LEAGUE_ID}/users'
users_data = requests.get(users_url).json()
with open('json/users.json', 'w') as file:
    json.dump(users_data, file)