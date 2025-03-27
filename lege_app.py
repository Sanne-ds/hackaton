import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Titel van de Streamlit app
st.title("Streamlit App met Twee Tabbladen")

# Maak twee tabbladen
tab1, tab2 = st.tabs(["Tabblad 1", "Tabblad 2"])

# Inhoud voor Tabblad 1
with tab1:
 # Titel van de Streamlit app
st.title("Luidste Vliegtuigfabrikanten")

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
        x=[row['min'], row['max']],  # x-waarden van de staaf (min naar max)
        y=[row['manufacturer'], row['manufacturer']],  # y-waarden zijn constant (voor elke fabrikant)
        mode='lines',  # Lijnmodus om een staaf te maken
        line=dict(color='lightblue', width=6),  # Lichtblauwe lijn voor de staaf
        name=row['manufacturer']
    ))

    # Voeg een markering toe voor de gemiddelde waarde met het aantal waarnemingen als hover-informatie
    fig.add_trace(go.Scatter(
        x=[row['lasmax_dB']],  # x-positie van de markering
        y=[row['manufacturer']],  # y-positie van de markering
        mode='markers',  # Alleen markeringen (punten)
        marker=dict(color='blue', size=10, symbol='circle'),  # Markering in blauw
        name=f"Gemiddeld: {row['manufacturer']}",
        hoverinfo='text',  # Zet hover-informatie aan
        hovertext=[f"Gemiddeld: {row['lasmax_dB']:.2f} dB<br>Waarnemingen: {row['count']}"],  # Hover tekst met gemiddelde en aantal waarnemingen
        showlegend=False  # Verberg de legenda voor de markeringen
    ))

# Pas de layout aan voor betere zichtbaarheid van labels en de x-as
fig.update_layout(
    yaxis={'tickmode': 'array'},  # Zorg ervoor dat alle fabrikanten zichtbaar zijn
    margin={"l": 200, "r": 20, "t": 50, "b": 100},  # Vergroot de marge om ruimte te maken voor labels
    width=1000,  # Pas de breedte aan om de grafiek compacter te maken
    height=600,  # Pas de hoogte aan om de grafiek compacter te maken
    xaxis_title='Geluidniveaus (dB)',  # Toevoegen van titel aan de x-as
    yaxis_title='Fabrikant',  # Toevoegen van titel aan de y-as
    showlegend=False,  # Verwijder de legenda aan de rechterkant
    xaxis=dict(
        range=[top_manufacturers['min'].min() - 5, top_manufacturers['max'].max() + 5]  # Stel de x-as limieten in zodat alles zichtbaar is
    ),
    paper_bgcolor='white',  # Achtergrondkleur instellen als wit
    plot_bgcolor='white',  # Achtergrondkleur grafiek instellen als wit
)

# Draai de y-as labels zodat ze beter leesbaar zijn
fig.update_layout(
    yaxis_tickangle=-45,  # Draai de y-as labels met -45 graden voor betere leesbaarheid
    font=dict(size=12)  # Verklein het lettertype van de labels om ze beter leesbaar te maken
)

# Toon de grafiek in de Streamlit interface
st.plotly_chart(fig)


######################################################################################
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
        x=[row['min_lasmax_dB'], row['max_lasmax_dB']],  # x-waarden van de staaf (min naar max)
        y=[row['model'], row['model']],  # y-waarden zijn constant (voor elke fabrikant)
        mode='lines',  # Lijnmodus om een staaf te maken
        line=dict(color='lightblue', width=6),  # Lichtblauwe lijn voor de staaf
        name=row['model']
    ))

    # Voeg een markering toe voor de gemiddelde waarde
    fig.add_trace(go.Scatter(
        x=[row['lasmax_dB']],  # x-positie van de markering
        y=[row['model']],  # y-positie van de markering
        mode='markers',  # Markeringen (punt)
        marker=dict(color='blue', size=10, symbol='circle'),  # Markering in blauw
        name=f"Gemiddeld: {row['model']}",
    ))

# Pas de layout aan voor betere zichtbaarheid van labels en de x-as
fig.update_layout(
    yaxis={'tickmode': 'array'},  # Zorg ervoor dat alle Boeing-modellen zichtbaar zijn
    margin={"l": 200, "r": 20, "t": 50, "b": 100},  # Vergroot de marge om ruimte te maken voor labels
    width=1000,  # Pas de breedte aan om de grafiek compacter te maken
    height=600,  # Pas de hoogte aan om de grafiek compacter te maken
    xaxis_title='Geluidniveaus (dB)',  # Toevoegen van titel aan de x-as
    yaxis_title='Boeing Model',  # Toevoegen van titel aan de y-as
    showlegend=False,  # Verwijder de legenda aan de rechterkant
    xaxis=dict(
        range=[avg_sound_per_boeing_model['min_lasmax_dB'].min() - 5, avg_sound_per_boeing_model['max_lasmax_dB'].max() + 5]  # Stel de x-as limieten in zodat alles zichtbaar is
    ),
    paper_bgcolor='white',  # Achtergrondkleur instellen als wit
    plot_bgcolor='white',  # Achtergrondkleur grafiek instellen als wit
)

# Draai de y-as labels zodat ze beter leesbaar zijn
fig.update_layout(
    yaxis_tickangle=-45,  # Draai de y-as labels met -45 graden voor betere leesbaarheid
    font=dict(size=12)  # Verklein het lettertype van de labels om ze beter leesbaar te maken
)

# Toon de grafiek in de Streamlit interface
st.title("Gemiddeld Geluidsniveau per Boeing Model")
st.plotly_chart(fig)

# Inhoud voor Tabblad 2
with tab2:
    st.header("Tabblad 2")
    st.write("Dit is het tweede tabblad. Voeg hier je inhoud toe.")
