import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests

# Tabbladen maken
tab1, tab2 = st.tabs(["Fabrikanten & Boeing Modellen", "Marijn's Visualisaties"])

# Tabblad 1: Jouw visualisaties
with tab1:
    st.title("Luidste Vliegtuigfabrikanten Analyse")

    # Laad de dataset
    data = pd.read_csv('data_klein.csv')

    # Voeg een nieuwe kolom 'manufacturer' toe met de eerste woordgroep uit 'type'
    data['manufacturer'] = data['type'].str.split().str[0]
    # Voeg een nieuwe kolom 'model' toe door het tweede woord uit de kolom 'type' te halen
    data['model'] = data['type'].str.split().str[1]

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
            x=[row['min'], row['max']],
            y=[row['manufacturer'], row['manufacturer']],
            mode='lines',
            line=dict(color='lightblue', width=6),
            name=row['manufacturer']
        ))

        # Voeg een markering toe voor de gemiddelde waarde
        fig.add_trace(go.Scatter(
            x=[row['lasmax_dB']],
            y=[row['manufacturer']],
            mode='markers',
            marker=dict(color='blue', size=10, symbol='circle'),
            name=f"Gemiddeld: {row['manufacturer']}",
            hoverinfo='text',
            hovertext=[f"Gemiddeld: {row['lasmax_dB']:.2f} dB<br>Waarnemingen: {row['count']}"],
            showlegend=False
        ))

    # Pas de layout aan
    fig.update_layout(
        yaxis={'tickmode': 'array'},
        margin={"l": 200, "r": 20, "t": 50, "b": 100},
        width=1000,
        height=600,
        xaxis_title='Geluidniveaus (dB)',
        yaxis_title='Fabrikant',
        showlegend=False,
        xaxis=dict(
            range=[top_manufacturers['min'].min() - 5, top_manufacturers['max'].max() + 5]
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
    )

    st.plotly_chart(fig)

    # Boeing modellen analyse
    st.title("Gemiddeld Geluidsniveau per Boeing Model")

    # Filter de rijen waar 'boeing' in de 'type' kolom staat
    boeing_data = data[data['type'].str.contains('Boeing', case=False, na=False)]

    # Groepeer het type door alleen het eerste deel van het model te behouden (zoals 'Boeing 777')
    boeing_data['model'] = boeing_data['type'].str.extract(r'(Boeing \d+)')

    # Groepeer nu op het nieuwe 'model' en bereken het gemiddelde geluidsniveau per model
    avg_sound_per_boeing_model = boeing_data.groupby('model')['lasmax_dB'].agg(['mean', 'min', 'max']).reset_index()

    # Hernoem kolommen voor duidelijkheid
    avg_sound_per_boeing_model.columns = ['model', 'lasmax_dB', 'min_lasmax_dB', 'max_lasmax_dB']

    # Sorteer op gemiddeld geluidsniveau
    avg_sound_per_boeing_model = avg_sound_per_boeing_model.sort_values(by='lasmax_dB', ascending=False)

    # Maak een lege figuur aan voor de grafiek
    fig = go.Figure()

    # Voeg een enkele staaf toe die begint bij de minimum waarde en eindigt bij de maximum waarde
    for i, row in avg_sound_per_boeing_model.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['min_lasmax_dB'], row['max_lasmax_dB']],
            y=[row['model'], row['model']],
            mode='lines',
            line=dict(color='lightblue', width=6),
            name=row['model']
        ))

        # Voeg een markering toe voor de gemiddelde waarde
        fig.add_trace(go.Scatter(
            x=[row['lasmax_dB']],
            y=[row['model']],
            mode='markers',
            marker=dict(color='blue', size=10, symbol='circle'),
            name=f"Gemiddeld: {row['model']}",
        ))

    # Pas de layout aan
    fig.update_layout(
        yaxis={'tickmode': 'array'},
        margin={"l": 200, "r": 20, "t": 50, "b": 100},
        width=1000,
        height=600,
        xaxis_title='Geluidniveaus (dB)',
        yaxis_title='Boeing Model',
        showlegend=False,
        xaxis=dict(
            range=[avg_sound_per_boeing_model['min_lasmax_dB'].min() - 5, avg_sound_per_boeing_model['max_lasmax_dB'].max() + 5]
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
    )

    st.plotly_chart(fig)

# Tabblad 2: Marijn's visualisaties
with tab2:
    st.title("Marijn's Visualisaties")

    # Voeg hier de code van Marijn toe
    @st.cache_data
    def fetch_data():
        url = 'https://sensornet.nl/dataserver3/event/collection/nina_events/stream?...'
        response = requests.get(url)
        response.raise_for_status()
        colnames = pd.DataFrame(response.json()['metadata'])
        data = pd.DataFrame(response.json()['rows'])
        data.columns = colnames.headers
        data['time'] = pd.to_datetime(data['time'], unit='s')
        return data

    # Mockdata voor 10 vliegtuigen
    def get_mock_data():
        data = pd.DataFrame({
            'time': pd.date_range(start="2025-01-01", periods=10, freq='D'),
            'vliegtuig_type': ['Boeing 737-800', 'Embraer ERJ 170-200 STD', 'Embraer ERJ 190-100 STD', 
                               'Boeing 737-700', 'Airbus A320 214', 'Boeing 777-300ER', 
                               'Boeing 737-900', 'Boeing 777-200', 'Airbus A319-111', 'Boeing 787-9'],
            'SEL_dB': [85, 90, 95, 100, 92, 88, 91, 96, 99, 93],
        })
        return data

    # Voeg hier de rest van Marijn's visualisaties toe
    # Bijvoorbeeld: Grafieken, berekeningen, enz.
    
