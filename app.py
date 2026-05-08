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
# Carregamento dos dados
# ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/bees.csv")

    # Normalização de colunas
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Converter ano (intervalos viram ano inicial)
    df["year"] = df["year"].astype(str).str[:4].astype(int)

    return df

df = load_data()

# ─────────────────────────────────────────────────────────────
# Cabeçalho
# ─────────────────────────────────────────────────────────────
st.title("🐝 Colapso de Colônias de Abelhas no Brasil")
st.caption(
    "Análise de perdas de colmeias e abelhas associadas ao uso de pesticidas "
    "e atividades antrópicas · Dados de TCC e Pós‑graduação"
)
st.divider()

# ─────────────────────────────────────────────────────────────
# Métricas principais
# ─────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

col1.metric("Casos registrados", len(df))
col2.metric("Colmeias perdidas", int(df["hives_lost"].sum()))
col3.metric("Abelhas perdidas", f"{int(df['bees_lost'].sum()):,}".replace(",", "."))
col4.metric("Estados afetados", df["state"].nunique())

st.divider()

# ─────────────────────────────────────────────────────────────
# Abas
# ─────────────────────────────────────────────────────────────
tab_map, tab_analysis, tab_data = st.tabs(
    ["🗺️ Mapa dos Casos", "📊 Análises", "📋 Dados Brutos"]
)

# =============================================================
# ABA 1 — MAPA
# =============================================================
with tab_map:
    st.subheader("Localização dos eventos de perda de colmeias")

    col_filt, col_info = st.columns([1, 3])

    with col_filt:
        state_filter = st.multiselect(
            "Filtrar por estado",
            options=sorted(df["state"].unique()),
            default=sorted(df["state"].unique())
        )

        pesticide_filter = st.multiselect(
            "Filtrar por pesticida",
            options=sorted(df["pesticide"].unique()),
            default=sorted(df["pesticide"].unique())
        )

    df_f = df[
        (df["state"].isin(state_filter)) &
        (df["pesticide"].isin(pesticide_filter))
    ]

    with col_info:
        st.info(
            f"**{len(df_f)}** casos exibidos · "
            f"**{int(df_f['hives_lost'].sum())}** colmeias perdidas"
        )

    m = folium.Map(location=[-23, -46], zoom_start=5, tiles="CartoDB positron")

    for _, r in df_f.iterrows():
        popup = f"""
        <b>Produtor:</b> {r['producer']}<br>
        <b>Estado:</b> {r['state']}<br>
        <b>Região:</b> {r['region']}<br>
        <b>Colmeias perdidas:</b> {r['hives_lost']}<br>
        <b>Abelhas perdidas:</b> {r['bees_lost']:,}<br>
        <b>Causa:</b> {r['cause']}<br>
        <b>Pesticida:</b> {r['pesticide']}<br>
        <b>Ano:</b> {r['year']}
        """.replace(",", ".")

        folium.CircleMarker(
            [r["latitude"], r["longitude"]],
            radius=6 + r["hives_lost"] ** 0.5,
            fill=True,
            fill_opacity=0.7,
            color="#c0392b",
            popup=popup,
        ).add_to(m)

    st_folium(m, height=520)

# =============================================================
# ABA 2 — ANÁLISES
# =============================================================
with tab_analysis:
    st.subheader("Perdas de colmeias por pesticida")

    fig_pest = px.bar(
        df.groupby("pesticide")["hives_lost"].sum().reset_index(),
        x="pesticide",
        y="hives_lost",
        labels={
            "pesticide": "Pesticida",
            "hives_lost": "Colmeias perdidas",
        },
    )
    st.plotly_chart(fig_pest, use_container_width=True)

    st.divider()
    st.subheader("Evolução temporal das perdas")

    fig_time = px.line(
        df.groupby("year")[["hives_lost", "bees_lost"]].sum().reset_index(),
        x="year",
        y="hives_lost",
        markers=True,
        labels={
            "year": "Ano",
            "hives_lost": "Colmeias perdidas",
        },
    )
    st.plotly_chart(fig_time, use_container_width=True)

# =============================================================
# ABA 3 — DADOS
# =============================================================
with tab_data:
    st.subheader("Base de dados completa")

    st.download_button(
        "⬇️ Baixar CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="bee_colony_collapse_brazil.csv",
        mime="text/csv",
    )

    st.dataframe(df, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# Rodapé
# ─────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Projeto acadêmico — Colapso de Colônias de Abelhas no Brasil · "
    "Baseado em dados de TCC (Fatec Jundiaí) e Pós‑Graduação (Unitau)"
)