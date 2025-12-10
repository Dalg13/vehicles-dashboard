import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Dashboard de Vehículos", layout="wide")

st.title("Panel de Control - Anuncios de Vehículos Usados")
st.markdown("Explora un conjunto de anuncios con filtros interactivos y gráficos.")

@st.cache_data
def load_data(path: str = "vehicles_us.csv") -> pd.DataFrame:
    """Carga el CSV y realiza limpiezas básicas."""
    df = pd.read_csv(path)
    # Normalizar nombres de columnas sencillos si hace falta
    df.columns = [c.strip() for c in df.columns]
    return df

# Cargar datos
try:
    df = load_data()
except FileNotFoundError:
    st.error("No se encontró el archivo vehicles_us.csv. Asegúrate de colocarlo en la carpeta del entorno.")
    st.stop()
# Sidebar - filtros
st.sidebar.header("Filtros")

# Filtro por marca (brand) si existe
if "brand" in df.columns:
    brands = sorted(df["brand"].dropna().unique())
    brand_sel = st.sidebar.selectbox("Marca", options=["Todas"] + brands)
else:
    brand_sel = "Todas"

# Rango de año si existe
if "year" in df.columns:
    min_year = int(df["year"].min())
    max_year = int(df["year"].max())
    year_range = st.sidebar.slider("Rango de año", min_year, max_year, (min_year, max_year))
else:
    year_range = None

# Checkbox para elegir los gráficos
st.sidebar.header("Visualizaciones")
show_hist = st.sidebar.checkbox("Histograma de odómetro")
show_scatter = st.sidebar.checkbox("Diagrama de dispersión: precio vs odómetro")
show_table = st.sidebar.checkbox("Mostrar tabla de datos")

# Aplicar filtros
df_filtered = df.copy()
if brand_sel != "Todas" and "brand" in df.columns:
    df_filtered = df_filtered[df_filtered["brand"] == brand_sel]
if year_range and "year" in df.columns:
    df_filtered = df_filtered[(df_filtered["year"] >= year_range[0]) & (df_filtered["year"] <= year_range[1])]
# Main layout
st.subheader("Resumen de datos")
col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Total anuncios", len(df_filtered))
    if "price" in df_filtered.columns:
        try:
            st.metric("Precio medio", int(df_filtered["price"].dropna().mean()))
        except Exception:
            st.metric("Precio medio", "N/A")

with col2:
    st.write("Últimas filas del dataset filtrado")
    st.dataframe(df_filtered.head())

# Mostrar tabla si se seleccionó
if show_table:
    st.subheader("Tabla de datos filtrada")
    st.dataframe(df_filtered)

# Histograma
if show_hist:
    if "odometer" in df_filtered.columns:
        st.subheader("Histograma - odómetro")
        fig = go.Figure(data=[go.Histogram(x=df_filtered["odometer"].dropna())])
        fig.update_layout(xaxis_title="Odómetro", yaxis_title="Conteo")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("La columna 'odometer' no existe en el dataset.")
# Scatter
if show_scatter:
    if set(["odometer", "price"]).issubset(df_filtered.columns):
        st.subheader("Precio vs Kilometraje")
        fig2 = px.scatter(df_filtered, x="odometer", y="price", hover_data=df_filtered.columns)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Las columnas 'odometer' y/o 'price' no están presentes en el dataset.")

st.markdown("---")
st.write("Hecho con ❤️ — Puedes personalizar y añadir más visualizaciones.")
