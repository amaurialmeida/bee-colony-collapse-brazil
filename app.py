import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="🐝 Monitoramento de Abelhas no Brasil",
    page_icon="🐝",
    layout="wide",
)

# ── Carregamento de dados ───────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("data/bees.csv")

df = load_data()

# ── Cabeçalho ───────────────────────────────────────────────────────────────
st.title("🐝 Monitoramento de Abelhas no Brasil")
st.caption(
    "Apicultura e Meliponicultura · Dados de TCC / Pós‑graduação · "
    "Distribuição espacial e temporal de colmeias"
)
st.divider()

# ── Métricas resumo ─────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

col1.metric("Registros", len(df))
col2.metric("Espécies", df["especie"].nunique())
col3.metric("Total de colmeias", int(df["qtd_colmeias"].sum()))
col4.metric("Estados", df["estado"].nunique())

st.divider()

# ── Abas principais ─────────────────────────────────────────────────────────
tab_map, tab_trends, tab_data = st.tabs([
    "🗺️ Mapa de Colmeias",
    "📈 Tendências",
    "📋 Dados Brutos",
])

# ════════════════════════════════════════════════════════════════
# ABA 1 — MAPA
# ════════════════════════════════════════════════════════════════
with tab_map:
    st.subheader("Distribuição geográfica das colmeias")

    col_filter, col_info = st.columns([1, 3])

    with col_filter:
        tipo_filter = st.multiselect(
            "Tipo de abelha",
            options=df["tipo"].unique(),
            default=df["tipo"].unique(),
        )

        estado_filter = st.multiselect(
            "Estado",
            options=df["estado"].unique(),
            default=df["estado"].unique(),
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

    # Mapa
    m = folium.Map(
        location=[-14.235, -51.925],
        zoom_start=4,
        tiles="CartoDB positron",
    )

    for _, row in df_filtered.iterrows():
        color = "#f39c12" if row["tipo"] == "Africanizada" else "#2ecc71"
        popup_html = f"""
        <div style='font-family:sans-serif; width:220px'>
            <b>Espécie:</b> {row['especie']}<br>
            <b>Tipo:</b> {row['tipo']}<br>
            <b>Estado:</b> {row['estado']}<br>
            <b>Município:</b> {row['municipio']}<br>
            <b>Colmeias:</b> {row['qtd_colmeias']}<br>
            <b>Ano:</b> {row['ano']}
        </div>
        """
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=8,
            color="white",
            weight=2,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            popup=folium.Popup(popup_html, max_width=250),
        ).add_to(m)

    st_folium(m, width=1000, height=520)

    st.caption("🟢 Abelhas nativas · 🟡 Abelhas africanizadas")

# ════════════════════════════════════════════════════════════════
# ABA 2 — TENDÊNCIAS
# ════════════════════════════════════════════════════════════════
with tab_trends:
    st.subheader("Evolução do número de colmeias ao longo do tempo")

    fig_year = px.line(
        df.groupby(["ano", "tipo"])["qtd_colmeias"].sum().reset_index(),
        x="ano",
        y="qtd_colmeias",
        color="tipo",
        markers=True,
        labels={
            "ano": "Ano",
            "qtd_colmeias": "Quantidade de colmeias",
            "tipo": "Tipo",
        },
        title="Colmeias por tipo de abelha",
    )

    fig_year.update_layout(height=420, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_year, use_container_width=True)

    st.divider()

    st.subheader("Colmeias por estado")

    fig_state = px.bar(
        df.groupby(["estado", "tipo"])["qtd_colmeias"].sum().reset_index(),
        x="estado",
        y="qtd_colmeias",
        color="tipo",
        labels={
            "estado": "Estado",
            "qtd_colmeias": "Quantidade de colmeias",
            "tipo": "Tipo",
        },
    )

    fig_state.update_layout(height=420)
    st.plotly_chart(fig_state, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# ABA 3 — DADOS BRUTOS
# ════════════════════════════════════════════════════════════════
with tab_data:
    st.subheader("Base de dados completa")

    search = st.text_input("🔍 Buscar por espécie, município ou estado", "")

    df_show = df.copy()

    if search:
        df_show = df_show[
            df_show["especie"].str.contains(search, case=False) |
            df_show["municipio"].str.contains(search, case=False) |
            df_show["estado"].str.contains(search, case=False)
        ]

    st.download_button(
        "⬇️ Baixar CSV",
        data=df_show.to_csv(index=False).encode("utf-8"),
        file_name="abelhas_brasil.csv",
        mime="text/csv",
    )

    st.dataframe(df_show, use_container_width=True, hide_index=True)

# ── Rodapé ──────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Projeto desenvolvido para TCC / Pós‑graduação · "
    "Apicultura e Meliponicultura no Brasil · "
    "Visualização interativa com Streamlit"
)