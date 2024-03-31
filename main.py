import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.patches import Circle, Rectangle, Arc

def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]
    if outer_lines:
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)
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
    draw_court(outer_lines=True)
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
        team_option = st.selectbox('Select a Team', options=all_data['TEAM_NAME'].unique())
        year_option = st.selectbox('Select a year', options=[str(i) for i in range(2004, 2024)])
        game_ids = all_data[(all_data['SEASON_1'] == int(year_option)) & (all_data['TEAM_NAME'] == team_option)]['GAME_ID'].unique()
        game_id_option = st.selectbox('Select a game', options=game_ids)
        btn = st.button("Create Heat Map for Team")
        if btn:
            plotTeamShotLocations(all_data, year_option, team_option, game_id_option)

if __name__ == "__main__":
    main()
