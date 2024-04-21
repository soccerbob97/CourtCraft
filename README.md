# Description 

This is CourtCraft, a data analysis tool that allows users to see NBA shot charts for players and teams. We used python, specifically streamlit, mathplotlib, seaborn, to create engaging visuals to help users understand confusing NBA statistics better. The package consists of main.py file and the data folder which you will soon download. The code is all in the main.py file, and the necessary csv files are in the data folder.

# Installation

First, run this command in the CourtCraft folder to get the data folder.

git clone https://github.com/soccerbob97/CourtCraft.git

In the data folder, we will see zip files containing the csv files that has the NBA shot information for a specific year. Go to the folder on your computer and open each zip file.

After this, the installation part is done.

# Execution 

In the CourtCraft directory, execute the following command: 

streamlit run main.py

This will open a tab that contains our project in your browser. It will take a few seconds to get the data loaded, but after that, the data will be cached. If you do not open all the zip files, you will get an error message and the specific file you are missing will be printed in the console. 

When the application is loaded, you can see the shot chart for a specific player in a specific year or all years. You can also see the shot information in three different charts: Simple Shot chart, KDE chart (Heat map), and Hex chart.

Additionally, you can see the shot chart for a team against a specific team given a date. 

Each of these parameters are text boxes so you can click and scroll down to the selection you want. If you want to type, you have to delete the entire text in the textbox and then type. 