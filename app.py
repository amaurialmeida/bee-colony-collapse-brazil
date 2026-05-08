import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

# ─────────────────────────────────────────────────────────────
# Configuração da página
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🐝 Colapso de Colônias de Abelhas no Brasil",
    page_icon="🐝",
    layout="wide",
)

# ─────────────────────────────────────────────────────────────
# Carregamento e tratamento dos dados
# ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/bees.csv")

    # Normaliza nomes das colunas
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Converter coluna year (intervalos ou anos únicos → ano inicial)
    df["year"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
        .astype(int)
    )

    return df

df = load_data()

# ─────────────────────────────────────────────────────────────
# Cabeçalho
# ─────────────────────────────────────────────────────────────
st.title("🐝 Colapso de Colônias de Abelhas no Brasil")
st.caption(
    "Perdas de colmeias e abelhas associadas ao uso de pesticidas "
    "e atividades antrópicas · Dados de TCC e Pós‑Graduação"
)
st.divider()

# ─────────────────────────────────────────────────────────────
# Métricas principais
# ─────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

col1.metric("Casos registrados", len(df))
col2.metric("Colmeias perdidas", int(df["hives_lost"].sum()))
col3.metric(
    "Abelhas perdidas",
    f"{int(df['bees_lost'].sum()):,}".replace(",", ".")
)
col4.metric("Estados afetados", df["state"].nunique())

st.divider()

# ─────────────────────────────────────────────────────────────
# Abas principais
# ─────────────────────────────────────────────────────────────
tab_map, tab_analysis, tab_data = st.tabs(
    ["🗺️ Mapa dos Casos", "📊 Análises", "📋 Dados Brutos"]
)

# ============================================================
# ABA 1 — MAPA
# ============================================================
with tab_map:
    st.subheader("Localização dos eventos de perda de colmeias")

    col_filter, col_info = st.columns([1, 3])

    with col_filter:
        state_filter = st.multiselect(
            "Filtrar por estado",
            options=sorted(df["state"].unique()),
            default=sorted(df["state"].unique()),
        )

        pesticide_filter = st.multiselect(
            "Filtrar por pesticida",
            options=sorted(df["pesticide"].unique()),
            default=sorted(df["pesticide"].unique()),
        )

    df_filtered = df[
        (df["state"].isin(state_filter)) &
        (df["pesticide"].isin(pesticide_filter))
    ]

    with col_info:
        st.info(
            f"**{len(df_filtered)}** casos exibidos · "
            f"**{int(df_filtered['hives_lost'].sum())}** colmeias perdidas"
        )

    m = folium.Map(
        location=[-23.0, -46.0],
        zoom_start=5,
        tiles="CartoDB positron",
    )

    for _, row in df_filtered.iterrows():
        popup_html = f"""
        <div style="font-family:sans-serif; width:240px">
            <b>Produtor:</b> {row['producer']}<br>
            <b>Estado:</b> {row['state']}<br>
            <b>Região:</b> {row['region']}<br>
            <b>Cidade:</b> {row['city']}<br>
            <b>Colmeias perdidas:</b> {row['hives_lost']}<br>
            <b>Abelhas perdidas:</b> {int(row['bees_lost']):,}<br>
            <b>Causa:</b> {row['cause']}<br>
            <b>Pesticida:</b> {row['pesticide']}<br>
            <b>Ano:</b> {row['year']}
        </div>
        """.replace(",", ".")

        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=5 + (row["hives_lost"] ** 0.5),
            color="#922B21",
            fill=True,
            fill_color="#C0392B",
            fill_opacity=0.75,
            popup=popup_html,
        ).add_to(m)

    st_folium(m, width=1100, height=520)

# ============================================================
# ABA 2 — ANÁLISES
# ============================================================
with tab_analysis:
    st.subheader("Perdas de colmeias por tipo de pesticida")

    df_pesticide = (
        df.groupby("pesticide")["hives_lost"]
        .sum()