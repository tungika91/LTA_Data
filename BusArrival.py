import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import numpy as np
import streamlit as st

st.title('Bus Arrival API - LTA')
# Global Variables
headers = { 
    'AccountKey' : 'LLS5w+z5TuiSZjQQz/1FMw==',
    'accept' : 'application/json'}
URL_TAXI_AVAIL = "http://datamall2.mytransport.sg/ltaodataservice/Taxi-Availability"
URL_BUS_ARRIAVL = "http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?BusStopCode="
BUS_STOP = '23021'
WALKING_MINUTES = 6

# Data extraction
busArrival = requests.get(URL_BUS_ARRIAVL + BUS_STOP, headers=headers)
bus_list = busArrival.json()['Services']
bus = bus_list[0]
bus_df = pd.DataFrame(bus).transpose()
bus_df = bus_df.drop(['ServiceNo', 'Operator'])
bus_df['ServiceNo'] = bus['ServiceNo']
bus_df['BusStop'] = BUS_STOP
bus_df['EstimatedArrival'] = pd.to_datetime(bus_df['EstimatedArrival'])
bus_df['ETA_min'] = (bus_df['EstimatedArrival'] - pd.Timestamp.now(timezone.utc)).dt.components['minutes']
bus_df = bus_df[['EstimatedArrival', 'ServiceNo', 'Type', 'Feature', 'ETA_min']]

# Label the ETA 
x = np.array(bus_df.index)
y = np.array(bus_df['ETA_min'])
text = np.array(bus_df['EstimatedArrival'].dt.strftime("%H:%M").values)

def addLabel(x,y,text):
    for i in range(len(x)):
        ax.text(x=x[i], y=(y[i]+0.5), s=text[i], ha = 'center', weight='bold')

# Visualization
fig, ax = plt.subplots(1,1, figsize=(6,4))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.bar(bus_df.index, bus_df['ETA_min'], width=0.4)
ax.set_ylabel('ETA (mins)')
ax.set_title(f"Estimated Time of Arrival - Bus {bus['ServiceNo']}", pad=10)
ax.set_axisbelow(True)
ax.yaxis.grid(True, color='#EEEEEE')
ax.xaxis.grid(False)
ax.axhline(y=WALKING_MINUTES, color='red',linestyle = ":")
addLabel(x,y,text)
