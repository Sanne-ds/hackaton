import streamlit as st
import plotly.express as px
import pandas as pd
import requests
import numpy as np

# Titel van de app
st.title('Luidste Vliegtuigfabrikanten (gemiddeld lasmax_dB)')

# Geef de gebruiker een dataloading indicator
with st.spinner('Gegevens ophalen...'):
    # Haal de data op van de API
    start_date = int(pd.to_datetime('2025-03-01').timestamp())
    end_date = int(pd.to_datetime('2025-03-7').timestamp())
    response = requests.get(f'https://sensornet.nl/dataserver3/event/collection/nina_events/stream?conditions%5B0%5D%5B%5D=time&conditions%5B0%5D%5B%5D=%3E%3D&conditions%5B0%5D%5B%5D={start_date}&conditions%5B1%5D%5B%5D=time&conditions%5B1%5D%5B%5D=%3C&conditions%5B1%5D%5B%5D={end_date}&conditions%5B2%5D%5B%5D=label&conditions%5B2%5D%5B%5D=in&conditions%5B2%5D%5B%5D=21&conditions%5B2%5D%5B%5D=32&conditions%5B2%5D%5B%5D=33&conditions%5B2%5D%5B%5D=34&args%5B%5D=aalsmeer&args%5B%5D=schiphol&fields%5B%5D=time&fields%5B%5D=location_short&fields%5B%5D=location_long&fields%5B%5D=duration&fields%5B%5D_
