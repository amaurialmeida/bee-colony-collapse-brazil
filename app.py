import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

# ─────────────────────────────────────────────────────────────────────────────
# Configuração da página
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🐝 Monitoramento de Abelhas no Brasil",
    page_icon="🐝",
    layout="wide",
)

# ─────────────────────────────────────────────────────────────────────────────
# Carregamento e padronização dos dados (ANTI‑KEYERROR)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/bees.csv")

    # Normalização básica dos nomes das colunas
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
        .str.replace(" ", "_")
    )

    # Mapeamento automático de colunas possíveis → padrão do app
    column_map = {}

    def map_col(possibles, target):
        for c in possibles:
            if c in df.columns:
                column_map[c] = target
                return

    map_col(["especie", "species", "especie_abelha", "nome_especie"], "especie")
    map_col(["tipo", "tipo_abelha", "categoria"], "tipo")
    map_col(["estado", "uf"], "estado")
    map_col(["municipio", "cidade"], "municipio")
    map_col(["latitude", "lat"], "latitude")
    map_col(["longitude", "lon", "lng"], "longitude")
    map_col(["qtd_colmeias", "quantidade_colmeias", "colmeias"], "qtd_colmeias")
    map_col(["ano", "year"], "ano")

    df = df.rename(columns=column_map)

    return df

df = load_data()

# ─────────────────────────────────────────────────────────────────────────────
# Cabeçalho
# ─────────────────────────────────────────────────────────────────────────────
st.title("🐝 Monitoramento de Abelhas no Brasil")
st.caption(
    "Apicultura e Meliponicultura · Dados de TCC / Pós‑graduação · "
    "Distribuição espacial e temporal de colmeias"
)
st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# Métricas
# ─────────────────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

col1.metric("Registros", len(df))
col2.metric("Espécies", df["especie"].nunique())
col3.metric("Total de colmeias", int(df["qtd_colmeias"].sum()))
col4.metric("Estados", df["estado"].nunique())

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# Abas
# ─────────────────────────────────────────────────────────────────────────────
tab_map, tab_trends, tab_data = st.tabs(
    ["🗺️ Mapa de Colmeias", "📈 Tendências", "📋 Dados Brutos"]
)

# ════════════════════════════════════════════════════════════════
# ABA 1 — MAPA
# ════════════════════════════════════════════════════════════════
with tab_map:
    st.subheader("Distribuição geográfica das colmeias")

    col_filter, col_info = st.columns([1, 3])

    with col_filter:
        tipo_filter = st.multiselect(
            "Tipo de abelha",
            options=sorted(df["tipo"].unique()),
            default=sorted(df["tipo"].unique()),
        )

        estado_filter = st.multiselect(
            "Estado",
            options=sorted(df["estado"].unique()),
            default=sorted(df["estado"].unique()),
        )

        ano_filter = st.multiselect(
            "Ano",
            options=sorted(df["ano"].unique()),
            default=sorted(df["ano"].unique()),
        )

    df_filtered = df[
        (df["tipo"].isin(tipo_filter)) &
        (df["estado"].isin(estado_filter)) &
        (df["ano"].isin(ano_filter))
    ]

    with col_info:
        st.info(
            f"**{len(df_filtered)}** registros exibidos · "
            f"**{df_filtered['qtd_colmeias'].sum()}** colmeias"
        )

    m = folium.Map(
        location=[-14.2, -51.9],
        zoom_start=4,
        tiles="CartoDB positron",
    )

    for _, row in df_filtered.iterrows():
        color = "#f39c12" if "afri" in str(row["tipo"]).lower() else "#2ecc71"
        popup = f"""
        <b>Espécie:</b> {row['especie']}<br>
        <b>Tipo:</b> {row['tipo']}<br>
        <b>Estado:</b> {row['estado']}<br>
        <b>Município:</b> {row['municipio']}<br>
        <b>Colmeias:</b> {row['qtd_colmeias']}<br>
        <b>Ano:</b> {row['ano']}
        """
        folium.CircleMarker(
            [row["latitude"], row["longitude"]],
            radius=7,
            color="white",
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            popup=popup,
        ).add_to(m)

    st_folium(m, width=1100, height=520)

# ════════════════════════════════════════════════════════════════
# ABA 2 — TENDÊNCIAS
# ════════════════════════════════════════════════════════════════
with tab_trends:
    st.subheader("Evolução temporal do número de colmeias")

    df_year = (
        df.groupby(["ano", "tipo"])["qtd_colmeias"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        df_year,
        x="ano",
        y="qtd_colmeias",
        color="tipo",
        markers=True,
        labels={
            "ano": "Ano",
            "qtd_colmeias": "Quantidade de colmeias",
            "tipo": "Tipo",
        },
    )

    st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# ABA 3 — DADOS BRUTOS
# ════════════════════════════════════════════════════════════════
with tab_data:
    st.subheader("Base de dados completa")

    search = st.text_input("🔍 Buscar por espécie, estado ou município")

    df_show = df.copy()
    if search:
        df_show = df_show[
            df_show["especie"].str.contains(search, case=False) |
            df_show["estado"].str.contains(search, case=False) |
            df_show["municipio"].str.contains(search, case=False)
        ]

    st.download_button(
        "⬇️ Baixar CSV",
        data=df_show.to_csv(index=False).encode("utf-8"),
        file_name="abelhas_brasil.csv",
        mime="text/csv",
    )
    st.dataframe(df_show, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# Rodapé
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Projeto acadêmico — Apicultura e Meliponicultura no Brasil · "
    "Dashboard interativo desenvolvido em Streamlit"
)