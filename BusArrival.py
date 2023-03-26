import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import numpy as np
import streamlit as st

st.title('Bus from SLB SWTC to Joo Koon MRT')
# Global Variables
headers = { 
    'AccountKey' : 'LLS5w+z5TuiSZjQQz/1FMw==',
    'accept' : 'application/json'}
URL_TAXI_AVAIL = "http://datamall2.mytransport.sg/ltaodataservice/Taxi-Availability"
URL_BUS_ARRIAVL = "http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?BusStopCode="
BUS_STOPS = ['23021', '23209']
WALKING_MINUTES = 6

def getBusArrival(busStop):
    # Data extraction
    busArrival = requests.get(URL_BUS_ARRIAVL + busStop, headers=headers)
    bus_list = busArrival.json()['Services']
    bus = bus_list[0]
    bus_df = pd.DataFrame(bus).transpose()
    bus_df = bus_df.drop(['ServiceNo', 'Operator'])
    bus_df['ServiceNo'] = bus['ServiceNo']
    bus_df['BusStop'] = busStop
    bus_df['EstimatedArrival'] = pd.to_datetime(bus_df['EstimatedArrival'])
    bus_df['ETA_min'] = (bus_df['EstimatedArrival'] - pd.Timestamp.now(timezone.utc)).dt.components['minutes']
    bus_df = bus_df[['EstimatedArrival', 'ServiceNo', 'Type', 'Feature', 'ETA_min']]
    return bus['ServiceNo'], bus_df

def addLabel(x,y,text):
    for i in range(len(x)):
        ax.text(x=x[i], y=(y[i]+0.5), s=text[i], ha = 'center', weight='bold')

fig, ax = plt.subplots(1,2, figsize=(12,4))
for i, busStop in enumerate(BUS_STOPS):
    busNo, bus_df = getBusArrival(busStop)
    # Label the ETA 
    x = np.array(bus_df.index)
    y = np.array(bus_df['ETA_min'])
    text = np.array(bus_df['EstimatedArrival'].dt.strftime("%H:%M").values)                     

    # Visualization
    ax[i].spines['top'].set_visible(False)
    ax[i].spines['right'].set_visible(False)
    ax[i].bar(bus_df.index, bus_df['ETA_min'], width=0.4)
    ax[i].set_ylabel('ETA (mins)')
    ax[i].set_title(f"Estimated Time of Arrival - Bus {busNo}", pad=10)
    ax[i].set_axisbelow(True)
    ax[i].yaxis.grid(True, color='#EEEEEE')
    ax[i].xaxis.grid(False)
    ax[i].axhline(y=WALKING_MINUTES, color='red',linestyle = ":")
    # addLabel(x,y,text)

st.pyplot(fig)
