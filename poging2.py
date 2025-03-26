import streamlit as st
import plotly.express as px
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

# Bepaal de minimum en maximum waarde van lasmax_dB in de dataset
min_lasmax = top_manufacturers['lasmax_dB'].min()
max_lasmax = top_manufacturers['lasmax_dB'].max()

# Maak een interactieve barplot met Plotly
fig = px.bar(top_manufacturers, 
             x='lasmax_dB', 
             y='manufacturer', 
             hover_data={'manufacturer': True, 'count': True, 'lasmax_dB': True}, 
             labels={'lasmax_dB': 'Gemiddelde lasmax_dB (dB)', 'manufacturer': 'Fabrikant'},
             title="Top 20 Luidste Vliegtuigfabrikanten (gemiddeld lasmax_dB)",
             orientation='h')

# Pas de layout aan voor betere zichtbaarheid van labels en de x-as
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

# Stel de x-as in voor een beter verschil
fig.update_xaxes(range=[min_lasmax - 1, max_lasmax + 1], tickmode='array')  # Vergroot het bereik met 1 dB om de verschillen duidelijker te maken

# Voeg de minimum en maximum waarde toe aan de grafiek als tekst
fig.add_annotation(
    x=min_lasmax, y=0, xref="x", yref="paper", 
    text=f"Min: {min_lasmax:.2f} dB", showarrow=True, arrowhead=2
)

fig.add_annotation(
    x=max_lasmax, y=0, xref="x", yref="paper", 
    text=f"Max: {max_lasmax:.2f} dB", showarrow=True, arrowhead=2
)

# Toon de grafiek in de Streamlit interface
st.plotly_chart(fig)
