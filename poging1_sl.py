import streamlit as st
import plotly.express as px
import pandas as pd
import requests
import numpy as np

# Titel van de app
st.title("Luidste Vliegtuigfabrikanten Analyse")

# Haal data op van de API
start_date = int(pd.to_datetime('2025-03-01').timestamp())
end_date = int(pd.to_datetime('2025-03-7').timestamp())
response = requests.get(f'https://sensornet.nl/dataserver3/event/collection/nina_events/stream?conditions%5B0%5D%5B%5D=time&conditions%5B0%5D%5B%5D=%3E%3D&conditions%5B0%5D%5B%5D={start_date}&conditions%5B1%5D%5B%5D=time&conditions%5B1%5D%5B%5D=%3C&conditions%5B1%5D%5B%5D={end_date}&conditions%5B2%5D%5B%5D=label&conditions%5B2%5D%5B%5D=in&conditions%5B2%5D%5B%5D=21&conditions%5B2%5D%5B%5D=32&conditions%5B2%5D%5B%5D=33&conditions%5B2%5D%5B%5D=34&args%5B%5D=aalsmeer&args%5B%5D=schiphol&fields%5B%5D=time&fields%5B%5D=location_short&fields%5B%5D=location_long&fields%5B%5D=duration&fields%5B%5D=SEL&fields%5B%5D=SELd&fields%5B%5D=SELe&fields%5B%5D=SELn&fields%5B%5D=SELden&fields%5B%5D=SEL_dB&fields%5B%5D=lasmax_dB&fields%5B%5D=callsign&fields%5B%5D=type&fields%5B%5D=altitude&fields%5B%5D=distance&fields%5B%5D=winddirection&fields%5B%5D=windspeed&fields%5B%5D=label&fields%5B%5D=hex_s&fields%5B%5D=registration&fields%5B%5D=icao_type&fields%5B%5D=serial&fields%5B%5D=operator&fields%5B%5D=tags')
colnames = pd.DataFrame(response.json()['metadata'])
data = pd.DataFrame(response.json()['rows'])
data.columns = colnames.headers
data['time'] = pd.to_datetime(data['time'], unit='s')

# Data inspectie
st.write(f"Minimale tijd: {data['time'].min()}")
st.write(f"Maximale tijd: {data['time'].max()}")
st.write(f"Aantal waarnemingen: {data.shape[0]}")

# Verwijder rijen zonder 'type'
data = data.dropna(subset=['type'])

# Maak een nieuwe kolom 'manufacturer' met alleen het eerste woord van 'type'
data['manufacturer'] = data['type'].str.split().str[0]

# Tel het aantal waarnemingen per fabrikant
manufacturer_counts = data['manufacturer'].value_counts()

# Filter fabrikanten die meer dan 5 keer zijn waargenomen
valid_manufacturers = manufacturer_counts[manufacturer_counts > 5].index
filtered_data = data[data['manufacturer'].isin(valid_manufacturers)]

# Bereken het gemiddelde geluidsniveau per fabrikant
avg_sound_per_manufacturer = filtered_data.groupby('manufacturer')['lasmax_dB'].mean().sort_values(ascending=False).reset_index()

# Voeg het aantal waarnemingen per fabrikant toe
avg_sound_per_manufacturer['count'] = avg_sound_per_manufacturer['manufacturer'].map(manufacturer_counts)

# Selecteer de top 20 luidste fabrikanten
top_manufacturers = avg_sound_per_manufacturer.head(20)

# Maak een interactieve barplot met Plotly
fig = px.bar(top_manufacturers, 
             x='lasmax_dB', 
             y='manufacturer', 
             hover_data={'manufacturer': True, 'count': True, 'lasmax_dB': True}, 
             labels={'lasmax_dB': 'Gemiddelde lasmax_dB (dB)', 'manufacturer': 'Fabrikant'},
             title="Top 20 Luidste Vliegtuigfabrikanten (gemiddeld lasmax_dB)",
             orientation='h')

# Pas de layout aan voor betere zichtbaarheid van labels
fig.update_layout(
    yaxis={'tickmode': 'array'},
    margin={"l": 200, "r": 20, "t": 50, "b": 100},
    width=1000,
    height=600,
    xaxis_title='Gemiddelde lasmax_dB (dB)',
    yaxis_title='Fabrikant',
)

# Draai de y-as labels zodat ze beter leesbaar zijn
fig.update_layout(
    yaxis_tickangle=-45,
    font=dict(size=12)
)

# Toon de grafiek in Streamlit
st.plotly_chart(fig)
