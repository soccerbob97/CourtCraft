import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.patches import Circle, Rectangle, Arc

nba_teams = {
    'ATL': 'Atlanta Hawks',
    'BOS': 'Boston Celtics',
    'BKN': 'Brooklyn Nets',
    'CHA': 'Charlotte Hornets',
    'CHI': 'Chicago Bulls',
    'CLE': 'Cleveland Cavaliers',
    'DAL': 'Dallas Mavericks',
    'DEN': 'Denver Nuggets',
    'DET': 'Detroit Pistons',
    'GSW': 'Golden State Warriors',
    'HOU': 'Houston Rockets',
    'IND': 'Indiana Pacers',
    'LAC': 'Los Angeles Clippers',
    'LAL': 'Los Angeles Lakers',
    'MEM': 'Memphis Grizzlies',
    'MIA': 'Miami Heat',
    'MIL': 'Milwaukee Bucks',
    'MIN': 'Minnesota Timberwolves',
    'NJN': "New Jersey Nets",
    'NOH': "New Orleans Hornets",
    'NOP': 'New Orleans Pelicans',
    'NYK': 'New York Knicks',
    'OKC': 'Oklahoma City Thunder',
    'ORL': 'Orlando Magic',
    'PHI': 'Philadelphia 76ers',
    'PHX': 'Phoenix Suns',
    'POR': 'Portland Trail Blazers',
    'SAC': 'Sacramento Kings',
    'SAS': 'San Antonio Spurs',
    'SEA': 'Seattle Supersonics',
    'TOR': 'Toronto Raptors',
    'UTA': 'Utah Jazz',
    'WAS': 'Washington Wizards'
}

nba_teams_flipped = {
    'Atlanta Hawks': 'ATL',
    'Boston Celtics': 'BOS',
    'Brooklyn Nets': 'BKN',
    'Charlotte Hornets': 'CHA',
    'Chicago Bulls': 'CHI',
    'Cleveland Cavaliers': 'CLE',
    'Dallas Mavericks': 'DAL',
    'Denver Nuggets': 'DEN',
    'Detroit Pistons': 'DET',
    'Golden State Warriors': 'GSW',
    'Houston Rockets': 'HOU',
    'Indiana Pacers': 'IND',
    'Los Angeles Clippers': 'LAC',
    'Los Angeles Lakers': 'LAL',
    'Memphis Grizzlies': 'MEM',
    'Miami Heat': 'MIA',
    'Milwaukee Bucks': 'MIL',
    'Minnesota Timberwolves': 'MIN',
    'New Jersey Nets': 'NJN',
    'New Orleans Hornets': 'NOH',
    'New Orleans Pelicans': 'NOP',
    'New York Knicks': 'NYK',
    'Oklahoma City Thunder': 'OKC',
    'Orlando Magic': 'ORL',
    'Philadelphia 76ers': 'PHI',
    'Phoenix Suns': 'PHX',
    'Portland Trail Blazers': 'POR',
    'Sacramento Kings': 'SAC',
    'San Antonio Spurs': 'SAS',
    'Seattle Supersonics': 'SEA',
    'Toronto Raptors': 'TOR',
    'Utah Jazz': 'UTA',
    'Washington Wizards': 'WAS'
}


def draw_court(ax=None, color='black', lw=2, outer_lines_element=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()
    backboard_element = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)
    outer_box_element = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    inner_box_element = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)
    top_free_throw_element = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
    bottom_free_throw_element = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')
    restricted_element = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)
    center_outer_arc_element = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner_arc_element = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)
    corner_three_a_element = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b_element = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    three_arc_element = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)
    hoop_element = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)
    court_elements = [backboard_element, center_outer_arc_element, center_inner_arc_element,
                      top_free_throw_element, bottom_free_throw_element, restricted_element, corner_three_a_element, 
                      outer_box_element, inner_box_element, corner_three_b_element, three_arc_element, hoop_element]
    if outer_lines_element:
        outer_lines_element = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines_element)
    for element in court_elements:
        ax.add_patch(element)
    return ax

def getDataframeForYear(year):
    file_path = f'data/NBA_{year}_Shots.csv'
    df = pd.read_csv(file_path)
    return df

@st.cache_data
def getAllData():
    file_names = []
    for i in range(4, 24):
        if i < 10:
            year = "0" + str(i)
        else:
            year = str(i)
        file_names.append(f'data/NBA_20{year}_Shots.csv')
    
    df = pd.concat(map(pd.read_csv, file_names), ignore_index=True) 
    print("number of rows ", df.shape[0])
    return df
    
def plotPlayerShotLocations(df, player_name):
    player_df = df[df["PLAYER_NAME"] == player_name].copy()
    player_df.loc[:,"LOC_X"] = player_df.loc[:,"LOC_X"] * 10 
    player_df.loc[:,"LOC_Y"] = player_df.loc[:,"LOC_Y"] * 10 - 45
    plotLocations(player_df)

def plotTeamShotLocations(df, year, team_name, game_id):
    team_df = df[(df["TEAM_NAME"] == team_name) & (df["SEASON_1"] == int(year)) & (df["GAME_ID"] == int(game_id))].copy()
    team_df.loc[:, "LOC_X"] = team_df.loc[:, "LOC_X"] * 10 
    team_df.loc[:, "LOC_Y"] = team_df.loc[:, "LOC_Y"] * 10 - 45
    plotLocations(team_df)

def plotLocations(df):  
    sns.set_style("white")
    sns.set_color_codes()
    fig = plt.figure(figsize=(12,11))
    plt.scatter(df.LOC_X, df.LOC_Y)
    draw_court(outer_lines_element=True)
    plt.xlim(-250,250)
    plt.ylim(422.5, -15)
    st.pyplot(fig)

def main():
    st.title('NBA HeatMaps')
    all_data = getAllData()
    unique_players = all_data['PLAYER_NAME'].unique()
    option = st.selectbox('Select Player or Team', options=['Player', 'Team'])

    if option == 'Player':
        player_option = st.selectbox('Select a Player', options=unique_players)
        years = [str(i) for i in range(2004, 2024)]
        years.insert(0, "All years")
        year_option = st.selectbox('Select a year', options=years)
        btn = st.button("Create Heat Map for Player")
        if btn:
            if year_option == "All years":
                plotPlayerShotLocations(all_data, player_option)
            else:
                df = getDataframeForYear(year_option)
                plotPlayerShotLocations(df, player_option)
    elif option == 'Team':
        team_option = st.selectbox('Select a Team', options=list(nba_teams.values()))
        year_option = st.selectbox('Select a year', options=[str(i) for i in range(2004, 2024)])
        
        filtered_data = all_data[(all_data['SEASON_1'] == int(year_option)) & ((all_data['HOME_TEAM'].isin(nba_teams.keys())) | (all_data['AWAY_TEAM'].isin(nba_teams.keys())))]

        opposing_teams = pd.concat([pd.Series(filtered_data['HOME_TEAM'].map(nba_teams)), pd.Series((filtered_data['AWAY_TEAM'].map(nba_teams)))], ignore_index=True).unique()
        selected_opposing_team = st.selectbox('Select Opposing Team', options=opposing_teams)
        
        game_dates = filtered_data[((filtered_data['HOME_TEAM'].map(nba_teams) == selected_opposing_team) | (filtered_data['AWAY_TEAM'].map(nba_teams) == selected_opposing_team))]['GAME_DATE'].unique()
        selected_game_date = st.selectbox('Select Game Date', options=game_dates)
        
        selected_game_ids = filtered_data[((filtered_data['HOME_TEAM'].map(nba_teams) == team_option) | (filtered_data['AWAY_TEAM'].map(nba_teams) == team_option)) & (filtered_data['GAME_DATE'] == selected_game_date)]['GAME_ID'].unique()
        
        btn = st.button("Create Heat Map for Team")
        if btn:
            for game_id in selected_game_ids:
                plotTeamShotLocations(all_data, year_option, team_option, game_id)

if __name__ == "__main__":
    main()
