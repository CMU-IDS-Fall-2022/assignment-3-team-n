#############################################################################
# This project is ///
# Course: Interactive Data Science(05839-A)
# Coded By: Jeffrey Na, Ninad Bandewar
# AndrewID: jjna, nbandewa
# Date: Oct 09, 2022
# Thanks to Prof. John Stamper, Prof. Adam Perer & TAs for there assistance
#############################################################################

#############################################################################
# Library Imports
#############################################################################
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from vega_datasets import data

#############################################################################
# Data Import
#############################################################################

st.set_page_config(layout = "wide")

@st.cache
def load_data():
    url = "https://raw.githubusercontent.com/CMU-IDS-Fall-2022/assignment-3-team-n/master/WC22_main.csv"
    return pd.read_csv(url)

df = load_data()

if st.checkbox("Show Raw Data"):
    st.write(df)

# MAIN CODE ######################################################

st.title("FIFA World Cup Qatar 2022")
st.text("Select your own team and get any data of the team in the FIFA WC 2022 here")

#############################################################################
# Map
#############################################################################

st.header("1. Explore the WC22 Map")
st.text("What country is included in the 32 teams on the group stage?")

mapData = alt.topo_feature(data.world_110m.url, "countries")

selection = alt.selection_single() 

map = (alt.Chart(mapData).mark_geoshape(stroke = "black", \
            strokeWidth = 0.5)
        .properties(width=1200, height=600)
        .add_selection(selection)
        .project("naturalEarth1")
        .encode
        (color = alt.Color("Group:N", scale = alt.Scale(\
            domain = ["A", "B", "C", "D", "E", "F", "G","H"],
            range = ["#e41a1c", "#377eb8", "#4daf4a",\
                 "#984ea3", "#ff7f00", "#ffff33", "#a65628", "#f781bf"])),
        tooltip = [alt.Tooltip("Team:N", title = "Country"),
            alt.Tooltip("Group:N", title = "Group"),
            alt.Tooltip("FIFA:N", title = "FIFA Ranking"),
            alt.Tooltip("Key Player:N", title = "Key Player")]) 
        .transform_lookup(lookup = "id",
        from_ = alt.LookupData(df, "uid", ["Team", "Key Player", "Group", "FIFA"])
        ))

map       

#############################################################################
# Team Selection
#############################################################################

st.header("2. Set your Team")
st.text("Select a Group and a Team")

# make the dropdown
cols = st.columns(2)

with cols[0]:
    groupinput = st.selectbox('Group', df['Group'].unique())
    
dfSubset = df.query("Group == @groupinput")

with cols[1]:
    teaminput = st.selectbox('Team', dfSubset['Team'].unique())

# Get the dropdown input
grouplist = []
grouplist.append(groupinput)
teamlist = []
teamlist.append(teaminput)

def get_input(df, grouplist, teamlist):
    labels = pd.Series([1] * len(df), index=df.index)
    if grouplist:
        labels &= df['Group'].isin(grouplist)
    if teamlist:
        labels &= df['Team'].isin(teamlist)
    return labels

slice_labels = get_input(df, grouplist, teamlist)
st.write("The sliced dataset contains {} elements".format(len(slice_labels)))
teaminput = df[slice_labels].Team.item()

st.write("Your team is **{Team}**".format(Team = teaminput))

#############################################################################
# Opponents
#############################################################################

st.header("3. Get to know the Opponents")
st.text("Check the Opponent teams and the match dates of WC22")

cols = st.columns(3)

team1 = df[slice_labels]['team1'].item()
team2 = df[slice_labels]['team2'].item()
team3 = df[slice_labels]['team3'].item()
FIFA1 = df[slice_labels]['FIFA1'].item()
FIFA2 = df[slice_labels]['FIFA2'].item()
FIFA3 = df[slice_labels]['FIFA3'].item()
date1 = df[slice_labels]['date1'].item()
date2 = df[slice_labels]['date2'].item()
date3 = df[slice_labels]['date3'].item()

with cols[0]:
    st.text("Team1")
    team_A = st.write("**{team}**".format(team = team1))
    FIFA_A = st.write("FIFA ranking: **{FIFA}**".format(FIFA = FIFA1))
    date_A = st.write("The match date is **{date}**".format(date = date1))
with cols[1]:
    st.text("Team2")
    team_B = st.write("**{team}**".format(team = team2))
    FIFA_B = st.write("FIFA ranking: **{FIFA}**".format(FIFA = FIFA2))
    date_B = st.write("The match date is **{date}**".format(date = date2))
with cols[2]:
    st.text("Team3")
    team_C = st.write("**{team}**".format(team = team3))
    FIFA_C = st.write("FIFA ranking: **{FIFA}**".format(FIFA = FIFA3))
    date_C = st.write("The match date is **{date}**".format(date = date3))

#############################################################################
# Compare
#############################################################################   

st.header("4. Analyze the 2 Teams")
st.text("Preview the Winning Rate based on the Historical Record")

yourinput = teaminput
oppinput = st.radio('Select the Opponent here', [team1, team2, team3])
colorspec = ['lightgrey','grey','darkblue']

#display the two dataset
col1, col2 = st.columns(2)

if oppinput == team1:
    with col1:
        FIFA0 = df[slice_labels]['FIFA'].item()
        games0 = df[slice_labels]['games1a'].item()
        wins0 = df[slice_labels]['wins1a'].item()
        loses0 = df[slice_labels]['loses1a'].item()
        draws0 = df[slice_labels]['draws1a'].item()
        rate0 = df[slice_labels]['rate1a'].item()
        st.header("{team}".format(team = yourinput))
        FIFA = st.write("FIFA Ranking: **{FIFA}**".format(FIFA = FIFA0))
        games = st.write("Games: **{games}**".format(games = games0))
        wins = st.write("Wins: **{wins}**".format(wins = wins0))
        loses = st.write("Loses: **{loses}**".format(loses = loses0))
        draws = st.write("Draws: **{draws}**".format(draws = draws0))
        rate = st.write("Winning rate: **{rate}**".format(rate = rate0))
        ser = pd.Series([wins0, loses0, draws0], index=['W', 'L', 'D'])
        ser = pd.DataFrame({"record": ['Win','Lose','Draw'], "value": [wins0,loses0,draws0]})
        c = alt.Chart(ser).mark_arc().encode(
            theta=alt.Theta(field="value", type="quantitative"),
            color=alt.Color('record', scale=alt.Scale(range=colorspec)),
            tooltip=['record', 'value'],
            ).properties(width=300)
        st.altair_chart(c)
    with col2:
        FIFA1 = df[slice_labels]['FIFA1'].item()
        games1 = df[slice_labels]['games1b'].item()
        wins1 = df[slice_labels]['wins1b'].item()
        loses1 = df[slice_labels]['loses1b'].item()
        draws1 = df[slice_labels]['draws1b'].item()
        rate1 = df[slice_labels]['rate1b'].item()
        st.header("{team}".format(team = oppinput))
        FIFA = st.write("FIFA ranking: **{FIFA}**".format(FIFA = FIFA1))
        games = st.write("Games: **{games}**".format(games = games1))
        wins = st.write("Wins: **{wins}**".format(wins = wins1))
        loses = st.write("Loses: **{loses}**".format(loses = loses1))
        draws = st.write("Draws: **{draws}**".format(draws = draws1))
        rate = st.write("Winning rate: **{rate}**".format(rate = rate1))
        ser = pd.Series([wins0, loses0, draws0], index=['W', 'L', 'D'])
        ser = pd.DataFrame({"record": ['Win','Lose','Draw'], "value": [wins1,loses1,draws1]})
        c = alt.Chart(ser).mark_arc().encode(
            theta=alt.Theta(field="value", type="quantitative"),
            color=alt.Color('record', scale=alt.Scale(range=colorspec)),
            tooltip=['record', 'value'],
            ).properties(width=300)
        st.altair_chart(c)
            
if oppinput == team2:
    with col1:
        FIFA0 = df[slice_labels]['FIFA'].item()
        games0 = df[slice_labels]['games2a'].item()
        wins0 = df[slice_labels]['wins2a'].item()
        loses0 = df[slice_labels]['loses2a'].item()
        draws0 = df[slice_labels]['draws2a'].item()
        rate0 = df[slice_labels]['rate2a'].item()
        st.header("{team}".format(team = yourinput))
        FIFA = st.write("FIFA ranking: **{FIFA}**".format(FIFA = FIFA0))
        games = st.write("Games: **{games}**".format(games = games0))
        wins = st.write("Wins: **{wins}**".format(wins = wins0))
        loses = st.write("Loses: **{loses}**".format(loses = loses0))
        draws = st.write("Draws: **{draws}**".format(draws = draws0))
        rate = st.write("Winning rate: **{rate}**".format(rate = rate0))
        ser = pd.Series([wins0, loses0, draws0], index=['W', 'L', 'D'])
        ser = pd.DataFrame({"record": ['Win','Lose','Draw'], "value": [wins0,loses0,draws0]})
        c = alt.Chart(ser).mark_arc().encode(
            theta=alt.Theta(field="value", type="quantitative"),
            color=alt.Color('record', scale=alt.Scale(range=colorspec)),
            tooltip=['record', 'value'],
            ).properties(width=300)
        st.altair_chart(c)
    with col2:
        FIFA1 = df[slice_labels]['FIFA2'].item()
        games1 = df[slice_labels]['games2b'].item()
        wins1 = df[slice_labels]['wins2b'].item()
        loses1 = df[slice_labels]['loses2b'].item()
        draws1 = df[slice_labels]['draws2b'].item()
        rate1 = df[slice_labels]['rate2b'].item()
        st.header("{team}".format(team = oppinput))
        FIFA = st.write("FIFA ranking: **{FIFA}**".format(FIFA = FIFA1))
        games = st.write("Games: **{games}**".format(games = games1))
        wins = st.write("Wins: **{wins}**".format(wins = wins1))
        loses = st.write("Loses: **{loses}**".format(loses = loses1))
        draws = st.write("Draws: **{draws}**".format(draws = draws1))
        rate = st.write("Winning rate: **{rate}**".format(rate = rate1))
        ser = pd.Series([wins0, loses0, draws0], index=['W', 'L', 'D'])
        ser = pd.DataFrame({"record": ['Win','Lose','Draw'], "value": [wins1,loses1,draws1]})
        c = alt.Chart(ser).mark_arc().encode(
            theta=alt.Theta(field="value", type="quantitative"),
            color=alt.Color('record', scale=alt.Scale(range=colorspec)),
            tooltip=['record', 'value'],
            ).properties(width=300)
        st.altair_chart(c)
        
if oppinput == team3:
    with col1:
        FIFA0 = df[slice_labels]['FIFA'].item()
        games0 = df[slice_labels]['games3a'].item()
        wins0 = df[slice_labels]['wins3a'].item()
        loses0 = df[slice_labels]['loses3a'].item()
        draws0 = df[slice_labels]['draws3a'].item()
        rate0 = df[slice_labels]['rate3a'].item()
        st.header("{team}".format(team = yourinput))
        FIFA = st.write("FIFA ranking: **{FIFA}**".format(FIFA = FIFA0))
        games = st.write("Games: **{games}**".format(games = games0))
        wins = st.write("Wins: **{wins}**".format(wins = wins0))
        loses = st.write("Loses: **{loses}**".format(loses = loses0))
        draws = st.write("Draws: **{draws}**".format(draws = draws0))
        rate = st.write("Winning rate: **{rate}**".format(rate = rate0))
        ser = pd.Series([wins0, loses0, draws0], index=['W', 'L', 'D'])
        ser = pd.DataFrame({"record": ['Win','Lose','Draw'], "value": [wins0,loses0,draws0]})
        c = alt.Chart(ser).mark_arc().encode(
            theta=alt.Theta(field="value", type="quantitative"),
            color=alt.Color('record', scale=alt.Scale(range=colorspec)),
            tooltip=['record', 'value'],
            ).properties(width=300)
        st.altair_chart(c)
    with col2:
        FIFA1 = df[slice_labels]['FIFA3'].item()
        games1 = df[slice_labels]['games3b'].item()
        wins1 = df[slice_labels]['wins3b'].item()
        loses1 = df[slice_labels]['loses3b'].item()
        draws1 = df[slice_labels]['draws3b'].item()
        rate1 = df[slice_labels]['rate3b'].item()
        st.header("{team}".format(team = oppinput))
        FIFA = st.write("FIFA ranking: **{FIFA}**".format(FIFA = FIFA1))
        games = st.write("Games: **{games}**".format(games = games1))
        wins = st.write("Wins: **{wins}**".format(wins = wins1))
        loses = st.write("Loses: **{loses}**".format(loses = loses1))
        draws = st.write("Draws: **{draws}**".format(draws = draws1))
        rate = st.write("Winning rate: **{rate}**".format(rate = rate1))
        ser = pd.Series([wins0, loses0, draws0], index=['W', 'L', 'D'])
        ser = pd.DataFrame({"record": ['Win','Lose','Draw'], "value": [wins1,loses1,draws1]})
        c = alt.Chart(ser).mark_arc().encode(
            theta=alt.Theta(field="value", type="quantitative"),
            color=alt.Color('record', scale=alt.Scale(range=colorspec)),
            tooltip=['record', 'value'],
            ).properties(width=300)
        st.altair_chart(c)

st.markdown("This project was created by Jeffrey Na and Ninad Bandewar for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
