import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# NFL-DATA-PY
# pbp = nfl.import_pbp_data([2023])

# # Get pbp when it is a pass or rush
# pbp_rp = pbp[(pbp['pass'] == 1) | (pbp['rush'] == 1)]
# pbp_rp = pbp_rp.dropna(subset=['epa', 'posteam', 'defteam'])

# # Passing EPA
# # Select from passes, group by possesion team, mean EPA, reset index so its a dataframe, rename to pass EPA
# pass_epa = pbp_rp[(pbp['pass'] == 1)].groupby('posteam')['epa'].mean().reset_index().rename(columns = {'epa' : 'pass_epa'})

# # Rushing EPA
# rush_epa = pbp_rp[(pbp['rush'] == 1)].groupby('posteam')['epa'].mean().reset_index().rename(columns = {'epa' : 'rush_epa'})

# # Combine datasets
# epa = pd.merge(pass_epa, rush_epa, on='posteam')
# print(epa)

# ESPN API
# url = 'https://sports.core.api.espn.com/v3/sports/football/nfl/athletes?limit=18000'
# jsonData = requests.get(url).json()

# players = pd.DataFrame(jsonData['items'])
# # players = players[['id', 'fullName']]
# tb = players[(players['fullName'] == "Tom Brady")]
# print(tb)

# SLEEPER API
# https://docs.sleeper.com/

def get_player_projection(player_stats, scoring_settings):
    projection = 0
    # get stats from projections
    for stats in player_stats:
        # for each stat
        for stat in stats:
            # if key from player stats is an actual stat
            if stat in scoring_settings:
                # multiply the scoring setting number with the player's projected number for that stat
                stat_projection = scoring_settings[stat] * stats[stat]
                # add to projected total for player
                projection += stat_projection
    return projection


def get_user_id_from_display_name(users, display_name):
    return users[display_name]['user_id']


def get_display_name_from_user_id(users, user_id):
    return users[user_id]['display_name']


# read JSON from file
with open('json/league.json') as file:
    league_data = json.load(file)
with open('json/players.json') as file:
    players_data = json.load(file)
# for each week
projections_data = []
for week in range(1, 19):
    with open(f'json/projections/projections_week_{week}.json') as file:
        projections_data.append(json.load(file))
with open('json/rosters.json') as file:
    rosters_data = json.load(file)
with open('json/users.json') as file:
    users_data = json.load(file)

# create dataframes
projections_df = pd.DataFrame(projections_data[2])
users_df = pd.DataFrame(users_data)


data = []

# create dict of user IDs and names
userDict = {}
for user in users_data:
    userDict[user['user_id']] = user['display_name']

# print roster owner name and thier players
for roster in rosters_data:
    for player_id in roster['starters']: # CHANGE FROM 'starters' TO 'players' TO INCLUDE PLAYERS ON TEAMS THAT ARE NOT STARTING
        owner_id = roster['owner_id']
        owner_name = userDict[roster['owner_id']]
        position = players_data[f'{player_id}']['position']
        projected_points = get_player_projection(projections_df[(projections_df['player_id'] == player_id)]['stats'], league_data['scoring_settings'])
        if player_id.isnumeric():
            player_name = players_data[f'{player_id}']['full_name']
            data.append([player_id, player_name, owner_id, owner_name, position, projected_points])
        else:
            player_name = player_id
            data.append([player_id, player_name, owner_id, owner_name, position, projected_points])


Player_df = pd.DataFrame(data, columns=['Player ID', 'Player Name', "Owner ID", "Owner Name", "Position", "Projected Points"])
print(Player_df.to_string())

# data = {}
# for user in userDict:
#     roster = Player_df[(Player_df['Position'] == 'WR')]
#     roster = roster[(Player_df['Owner ID'] == user)]
#     roster = roster.sort_values('Projected Points', ascending=False)
#     data[userDict[user]] = list(roster['Projected Points'])


# for owner in data:
#     plt.plot(data[owner], label=f"{owner}")
# plt.legend()
# plt.show()
qb_sums = np.zeros(10)
rb_sums = np.zeros(10)
wr_sums = np.zeros(10)
te_sums = np.zeros(10)
k_sums = np.zeros(10)
def_sums = np.zeros(10)
for i, user in enumerate(userDict):
    roster = Player_df[(Player_df['Owner ID'] == user) & (Player_df['Position'] == 'QB')]
    qb_sum = roster['Projected Points'].sum()
    qb_sums[i] = qb_sum
    
    roster = Player_df[(Player_df['Owner ID'] == user) & (Player_df['Position'] == 'RB')]
    rb_sum = roster['Projected Points'].sum()
    rb_sums[i] = rb_sum
    
    roster = Player_df[(Player_df['Owner ID'] == user) & (Player_df['Position'] == 'WR')]
    wr_sum = roster['Projected Points'].sum()
    wr_sums[i] = wr_sum
    
    roster = Player_df[(Player_df['Owner ID'] == user) & (Player_df['Position'] == 'TE')]
    te_sum = roster['Projected Points'].sum()
    te_sums[i] = te_sum
    
    roster = Player_df[(Player_df['Owner ID'] == user) & (Player_df['Position'] == 'K')]
    k_sum = roster['Projected Points'].sum()
    k_sums[i] = k_sum
    
    roster = Player_df[(Player_df['Owner ID'] == user) & (Player_df['Position'] == 'DEF')]
    def_sum = roster['Projected Points'].sum()
    def_sums[i] = def_sum

x = list(userDict.values())
plt.bar(x, def_sums, color='brown')
plt.bar(x, k_sums, bottom=def_sums, color='purple')
plt.bar(x, te_sums, bottom=def_sums+k_sums, color='orange')
plt.bar(x, wr_sums, bottom=def_sums+k_sums+te_sums, color='blue')
plt.bar(x, rb_sums, bottom=def_sums+k_sums+te_sums+wr_sums, color='green')
plt.bar(x, qb_sums, bottom=def_sums+k_sums+te_sums+wr_sums+rb_sums, color='red')

plt.xlabel("Teams")
plt.xticks(fontsize=6, rotation=45)
plt.ylabel("Projected Score")
plt.legend()
plt.show()