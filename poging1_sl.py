import plotly.express as px
import pandas as pd
import requests
import numpy as np

start_date = int(pd.to_datetime('2025-03-01').timestamp())
end_date = int(pd.to_datetime('2025-03-7').timestamp())
response = requests.get(f'https://sensornet.nl/dataserver3/event/collection/nina_events/stream?conditions%5B0%5D%5B%5D=time&conditions%5B0%5D%5B%5D=%3E%3D&conditions%5B0%5D%5B%5D={start_date}&conditions%5B1%5D%5B%5D=time&conditions%5B1%5D%5B%5D=%3C&conditions%5B1%5D%5B%5D={end_date}&conditions%5B2%5D%5B%5D=label&conditions%5B2%5D%5B%5D=in&conditions%5B2%5D%5B2%5D%5B%5D=21&conditions%5B2%5D%5B2%5D%5B%5D=32&conditions%5B2%5D%5B2%5D%5B%5D=33&conditions%5B2%5D%5B2%5D%5B%5D=34&args%5B%5D=aalsmeer&args%5B%5D=schiphol&fields%5B%5D=time&fields%5B%5D=location_short&fields%5B%5D=location_long&fields%5B%5D=duration&fields%5B%5D=SEL&fields%5B%5D=SELd&fields%5B%5D=SELe&fields%5B%5D=SELn&fields%5B%5D=SELden&fields%5B%5D=SEL_dB&fields%5B%5D=lasmax_dB&fields%5B%5D=callsign&fields%5B%5D=type&fields%5B%5D=altitude&fields%5B%5D=distance&fields%5B%5D=winddirection&fields%5B%5D=windspeed&fields%5B%5D=label&fields%5B%5D=hex_s&fields%5B%5D=registration&fields%5B%5D=icao_type&fields%5B%5D=serial&fields%5B%5D=operator&fields%5B%5D=tags')
colnames = pd.DataFrame(response.json()['metadata'])
data = pd.DataFrame(response.json()['rows'])
data.columns = colnames.headers
data['time'] = pd.to_datetime(data['time'], unit = 's')
print(data['time'].min(),data['time'].max())
print(data.shape)
data.head()
data = data.dropna(subset=['type'])
data.head()

# Neem alleen de eerste woordgroep (eerste woord) van de type-kolom
data['manufacturer'] = data['type'].str.split().str[0]

# Tel het aantal waarnemingen per fabrikant
manufacturer_counts = data['manufacturer'].value_counts()

# Filter alleen de fabrikanten die meer dan 5 keer zijn waargenomen
valid_manufacturers = manufacturer_counts[manufacturer_counts > 5].index

# Filter de dataset op de fabrikanten die meer dan 5 keer zijn waargenomen
filtered_data = data[data['manufacturer'].isin(valid_manufacturers)]

# Bereken het gemiddelde geluidsniveau per fabrikant
avg_sound_per_manufacturer = filtered_data.groupby('manufacturer')['lasmax_dB'].mean().sort_values(ascending=False).reset_index()

# Voeg het aantal waarnemingen per fabrikant toe aan de dataset
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
    yaxis={'tickmode': 'array'},  # Zorg ervoor dat alle fabrikanten zichtbaar zijn
    margin={"l": 200, "r": 20, "t": 50, "b": 100},  # Vergroot de marge om ruimte te maken voor labels
    width=1000,  # Pas de breedte aan om de grafiek compacter te maken
    height=600,  # Pas de hoogte aan om de grafiek compacter te maken
    xaxis_title='Gemiddelde lasmax_dB (dB)',  # Toevoegen van titel aan de x-as
    yaxis_title='Fabrikant',  # Toevoegen van titel aan de y-as
)

# Draai de y-as labels zodat ze beter leesbaar zijn
fig.update_layout(
    yaxis_tickangle=-45,  # Draai de y-as labels met -45 graden voor betere leesbaarheid
    font=dict(size=12)  # Verklein het lettertype van de labels om ze beter leesbaar te maken
)

# Toon de grafiek
fig.show()
