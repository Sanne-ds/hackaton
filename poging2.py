import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Titel van de Streamlit app
st.title("Luidste Vliegtuigfabrikanten Analyse")

# Laad de dataset
data = pd.read_csv('data_klein.csv')

# Voeg een nieuwe kolom 'manufacturer' toe met de eerste woordgroep uit 'type'
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

# Bereken de minimale en maximale waarde per fabrikant
min_max_per_manufacturer = filtered_data.groupby('manufacturer')['lasmax_dB'].agg(['min', 'max']).reset_index()

# Voeg de minimale en maximale waarden toe aan de top_manufacturers dataframe
top_manufacturers = top_manufacturers.merge(min_max_per_manufacturer[['manufacturer', 'min', 'max']], on='manufacturer')

# Maak een lege figuur aan voor de grafiek
fig = go.Figure()

# Voeg een enkele staaf toe die begint bij de minimum waarde en eindigt bij de maximum waarde
for i, row in top_manufacturers.iterrows():
    fig.add_trace(go.Scatter(
        x=[row['min'], row['max']],  # x-waarden van de staaf (min naar max)
        y=[row['manufacturer'], row['manufacturer']],  # y-waarden zijn constant (voor elke fabrikant)
        mode='lines',  # Lijnmodus om een staaf te maken
        line=dict(color='lightblue', width=6),  # Lichtblauwe lijn voor de staaf
        name=row['manufacturer']
    ))

    # Voeg een markering toe voor de gemiddelde waarde
    fig.add_trace(go.Scatter(
        x=[row['lasmax_dB']],  # x-positie van de markering
        y=[row['manufacturer']],  # y-positie van de markering
        mode='markers',  # Markeringen (punt)
        marker=dict(color='blue', size=10, symbol='circle'),  # Markering in blauw
        name=f"Gemiddeld: {row['manufacturer']}",
    ))

# Pas de layout aan voor betere zichtbaarheid van labels en de x-as
fig.update_layout(
    yaxis={'tickmode': 'array'},  # Zorg ervoor dat alle fabrikanten zichtbaar zijn
    margin={"l": 200, "r": 20, "t": 50, "b": 100},  # Vergroot de marge om ruimte te maken voor labels
    width=1000,  # Pas de breedte aan om de grafiek compacter te maken
    height=600,  # Pas de hoogte aan om de grafiek compacter te maken
    xaxis_title='Geluidniveaus (dB)',  # Toevoegen van titel aan de x-as
    yaxis_title='Fabrikant',  # Toevoegen van titel aan de y-as
)

# Draai de y-as labels zodat ze beter leesbaar zijn
fig.update_layout(
    yaxis_tickangle=-45,  # Draai de y-as labels met -45 graden voor betere leesbaarheid
    font=dict(size=12)  # Verklein het lettertype van de labels om ze beter leesbaar te maken
)

# Toon de grafiek in de Streamlit interface
st.plotly_chart(fig)
