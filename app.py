
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

st.header("Dashboard de Anuncios de Vehículos")

# Leer datos
car_data = pd.read_csv("vehicles_us.csv")

# Botón para histograma
hist_button = st.button("Construir histograma")

if hist_button:
    st.write("Histograma del odómetro")
    fig = go.Figure(data=[go.Histogram(x=car_data['odometer'])])
    st.plotly_chart(fig, use_container_width=True)

# Botón para diagrama de dispersión
scatter_button = st.button("Construir diagrama de dispersión")

if scatter_button:
    st.write("Relación entre precio y odómetro")
    fig2 = px.scatter(car_data, x="odometer", y="price")
    st.plotly_chart(fig2, use_container_width=True)
