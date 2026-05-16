import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Síndrome do Colapso das Colônias · Brasil",
    page_icon="🐝",
    layout="wide"
)

# ============================================================
# ESTILOS VISUAIS — TEMA CIÊNCIA + NATUREZA PREMIUM
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&family=DM+Mono&display=swap');

:root {
    --honey: #F5A623;
    --honey-dark: #C47D0E;
    --forest: #1A3A2A;
    --forest-mid: #2D5A3D;
    --forest-light: #3D7A52;
    --cream: #FDF8F0;
    --warm-gray: #8C7B6B;
    --danger: #C0392B;
    --danger-soft: #F8D7DA;
    --black: #0D1117;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream);
    color: var(--black);
}

/* HERO */
.hero-wrap {
    background: linear-gradient(135deg, var(--forest) 0%, var(--forest-mid) 60%, #1E4D30 100%);
    border-radius: 20px;
    padding: 3rem 2.5rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: "🐝";
    font-size: 180px;
    position: absolute;
    right: -20px;
    top: -20px;
    opacity: 0.06;
}
.hero-tag {
    background: var(--honey);
    color: var(--forest);
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: bold;
    letter-spacing: 2px;
    padding: 4px 12px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 1rem;
    text-transform: uppercase;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 900;
    color: #fff;
    line-height: 1.15;
    margin-bottom: 0.8rem;
}
.hero-subtitle {
    font-size: 1rem;
    color: rgba(255,255,255,0.75);
    max-width: 600px;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}
.hero-badges {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}
.badge {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    color: rgba(255,255,255,0.85);
    font-size: 0.72rem;
    font-family: 'DM Mono', monospace;
    padding: 5px 12px;
    border-radius: 20px;
    letter-spacing: 0.5px;
}
.badge-honey {
    background: rgba(245,166,35,0.2);
    border-color: var(--honey);
    color: var(--honey);
}

/* MÉTRICAS */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}
.metric-box {
    background: white;
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    border-top: 4px solid var(--honey);
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    text-align: center;
}
.metric-box.danger { border-top-color: var(--danger); }
.metric-box.forest { border-top-color: var(--forest-light); }
.metric-val {
    font-family: 'Playfair Display', serif;
    font-size: 2.1rem;
    font-weight: 900;
    color: var(--forest);
    line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-label {
    font-size: 0.75rem;
    color: var(--warm-gray);
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* SEÇÕES */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: var(--honey-dark);
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 0.3rem;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--forest);
    margin-bottom: 1.2rem;
    line-height: 1.2;
}

/* CARDS */
.info-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    border-left: 4px solid var(--forest-light);
    margin-bottom: 1rem;
}
.info-card.honey { border-left-color: var(--honey); }
.info-card.danger { border-left-color: var(--danger); }

/* OCULTAÇÃO DAS CAUSAS — ESTILO REDAÇÃO CIENTÍFICA */
.causa-hidden {
    font-family: 'DM Mono', monospace;
    background: var(--forest);
    color: var(--forest);
    border-radius: 4px;
    padding: 1px 4px;
    cursor: help;
    user-select: none;
    font-size: 0.85em;
    position: relative;
    letter-spacing: 1px;
    transition: all 0.2s;
}
.causa-hidden:hover {
    background: var(--honey);
    color: white;
}

/* TIMELINE */
.timeline-item {
    display: flex;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid #f0ebe2;
}
.timeline-year {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--honey);
    min-width: 50px;
}
.timeline-content { flex: 1; }
.timeline-title {
    font-weight: 500;
    color: var(--forest);
    margin-bottom: 0.2rem;
}
.timeline-desc { font-size: 0.85rem; color: var(--warm-gray); }

/* FONTES / BADGES */
.source-badges {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 0.8rem;
}
.source-badge {
    background: var(--forest);
    color: white;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    padding: 4px 10px;
    border-radius: 4px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* METODOLOGIA TABS */
.method-step {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem;
    background: white;
    border-radius: 12px;
    margin-bottom: 0.8rem;
    box-shadow: 0 1px 6px rgba(0,0,0,0.04);
}
.step-num {
    background: var(--honey);
    color: white;
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 700;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.step-content { flex: 1; }
.step-title { font-weight: 500; color: var(--forest); font-size: 0.95rem; }
.step-desc { font-size: 0.82rem; color: var(--warm-gray); margin-top: 0.2rem; }

/* DESTAQUES CAMPO */
.field-card {
    background: linear-gradient(135deg, var(--forest) 0%, var(--forest-mid) 100%);
    border-radius: 16px;
    padding: 1.8rem;
    color: white;
    position: relative;
    overflow: hidden;
}
.field-card::after {
    content: "📷";
    position: absolute;
    right: 1rem;
    top: 1rem;
    font-size: 2rem;
    opacity: 0.3;
}

/* DESCOBERTAS */
.discovery-box {
    background: linear-gradient(135deg, #FFF9F0 0%, #FFF3DC 100%);
    border: 2px solid var(--honey);
    border-radius: 16px;
    padding: 1.8rem;
    margin: 1rem 0;
}
.discovery-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--forest);
    margin-bottom: 1rem;
}

/* FOOTER */
.footer-wrap {
    background: var(--forest);
    border-radius: 20px;
    padding: 2rem;
    color: rgba(255,255,255,0.8);
    text-align: center;
    margin-top: 3rem;
}
.footer-title {
    font-family: 'Playfair Display', serif;
    color: var(--honey);
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
}

/* ALERTA SUBNOTIFICAÇÃO */
.alert-box {
    background: var(--danger-soft);
    border-left: 4px solid var(--danger);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    font-size: 0.9rem;
}

div[data-testid="stTabs"] { margin-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DADOS
# ============================================================
dados_produtores = [
    {
        "produtor": "Produtor A",
        "localidade": "Extrema - MG",
        "lat": -22.8514, "lon": -46.3178,
        "regiao": "Sul de Minas Gerais",
        "tipo": "Meliponicultor",
        "historico": [
            {"ano": 2016, "colmeias": 1, "abelhas": 1400, "causa": "Agente_urbano_vetorial"},
            {"ano": 2017, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2018, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2019, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2020, "colmeias": 1, "abelhas": 3000, "causa": "Agente_urbano_vetorial"},
            {"ano": 2021, "colmeias": 1, "abelhas": 3600, "causa": "Agente_urbano_vetorial"},
            {"ano": 2022, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
        ]
    },
    {
        "produtor": "Produtor B",
        "localidade": "Guaratinguetá - SP",
        "lat": -22.8078, "lon": -45.1936,
        "regiao": "Vale do Paraíba - SP",
        "tipo": "Apicultor",
        "historico": [
            {"ano": 2016, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2017, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2018, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2019, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2020, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2021, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2022, "colmeias": 5, "abelhas": 300000, "causa": "Composto_herbicida_sistêmico"},
        ]
    },
    {
        "produtor": "Produtor C",
        "localidade": "Turvo - PR",
        "lat": -25.0433, "lon": -51.5286,
        "regiao": "Região Central do Paraná",
        "tipo": "Apicultor",
        "historico": [
            {"ano": 2016, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2017, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2018, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2019, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2020, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2021, "colmeias": 30, "abelhas": 1800000, "causa": "Inseticida_monocultura"},
            {"ano": 2022, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
        ]
    },
    {
        "produtor": "Produtor D",
        "localidade": "Prudentópolis - PR",
        "lat": -25.2133, "lon": -50.9775,
        "regiao": "Região Central do Paraná",
        "tipo": "Apicultor",
        "historico": [
            {"ano": 2016, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2017, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2018, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2019, "colmeias": 300, "abelhas": 18000000, "causa": "Inseticida_monocultura"},
            {"ano": 2020, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2021, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2022, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
        ]
    }
]

dados_rs = [
    {"localidade": "Porto Alegre - RS", "lat": -30.0331, "lon": -51.2300, "colmeias": 2500, "evento": "Enchentes mai/jun 2024"},
    {"localidade": "Canoas - RS", "lat": -29.9200, "lon": -51.1800, "colmeias": 1500, "evento": "Enchentes mai/jun 2024"},
    {"localidade": "Cachoeirinha - RS", "lat": -29.9300, "lon": -51.0900, "colmeias": 750, "evento": "Enchentes mai/jun 2024"},
    {"localidade": "Eldorado do Sul - RS", "lat": -30.0800, "lon": -51.3100, "colmeias": 800, "evento": "Enchentes mai/jun 2024"},
    {"localidade": "Encantado - RS", "lat": -29.2400, "lon": -51.8700, "colmeias": 300, "evento": "Enchentes mai/jun 2024"},
    {"localidade": "Estrela - RS", "lat": -29.5000, "lon": -51.9600, "colmeias": 250, "evento": "Enchentes mai/jun 2024"},
    {"localidade": "Bento Gonçalves - RS", "lat": -29.1700, "lon": -51.5200, "colmeias": 200, "evento": "Enchentes mai/jun 2024"},
]

df_list = []
for p in dados_produtores:
    for h in p['historico']:
        if h['colmeias'] > 0:
            df_list.append({
                "produtor": p['produtor'],
                "localidade": p['localidade'],
                "lat": p['lat'], "lon": p['lon'],
                "regiao": p['regiao'],
                "tipo": p['tipo'],
                "ano": h['ano'],
                "colmeias": h['colmeias'],
                "abelhas": h['abelhas'],
                "causa": h['causa']
            })

df_perdas = pd.DataFrame(df_list)
df_rs = pd.DataFrame(dados_rs)

# ============================================================
# LEGENDA DAS CAUSAS (com ocultação criativa)
# ============================================================
causa_labels = {
    "Agente_urbano_vetorial": "Agente Urbano Vetorial [omitido por protocolo]",
    "Composto_herbicida_sistêmico": "Composto Herbicida Sistêmico [omitido por protocolo]",
    "Inseticida_monocultura": "Inseticida de Monocultura [omitido por protocolo]",
    "Sem perdas": "Sem perdas"
}

# ============================================================
# HERO
# ============================================================
st.markdown("""
<div class="hero-wrap">
    <div class="hero-tag">TCC · FATEC Jundiaí · Gestão Ambiental · 2022</div>
    <div class="hero-title">Síndrome do Colapso<br>das Colônias de Abelhas</div>
    <div class="hero-subtitle">
        Análise da mortalidade de abelhas por compostos químicos agrícolas e eventos climáticos 
        em 3 regiões brasileiras (2016–2022). Pesquisa com 338 colmeias e ~20 milhões de abelhas.
    </div>
    <div class="hero-badges">
        <span class="badge badge-honey">🐝 338 Colmeias</span>
        <span class="badge badge-honey">~20M Abelhas</span>
        <span class="badge">MG · SP · PR · RS</span>
        <span class="badge">2016 — 2022</span>
        <span class="badge">FATEC JUNDIAÍ · 3º ENADE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# AVISO DE PROTOCOLO (substituindo os ****)
# ============================================================
st.markdown("""
<div class="alert-box">
    <strong>📋 Nota de Protocolo Científico:</strong> Os nomes comerciais dos compostos químicos identificados 
    nesta pesquisa foram omitidos nesta publicação a pedido dos produtores entrevistados e por cautela legal, 
    substituídos por categorias técnicas genéricas. Os dados completos estão disponíveis no TCC original 
    depositado na FATEC Jundiaí (2022). Para fins acadêmicos, solicite acesso pelo formulário de contato.
</div>
""", unsafe_allow_html=True)

# ============================================================
# MÉTRICAS
# ============================================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""<div class="metric-box danger">
        <div class="metric-val">338</div>
        <div class="metric-label">Colmeias perdidas</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="metric-box danger">
        <div class="metric-val">~20M</div>
        <div class="metric-label">Abelhas perdidas (est.)</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="metric-box">
        <div class="metric-val">4</div>
        <div class="metric-label">Produtores monitorados</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""<div class="metric-box forest">
        <div class="metric-val">6.300+</div>
        <div class="metric-label">Colmeias RS (2024)</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# ABAS PRINCIPAIS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ Mapa & Análise",
    "🔬 Metodologia & Pipeline",
    "💡 O que Descobrimos",
    "📷 Em Campo",
    "📚 Fontes & Créditos"
])

# ============================================================
# ABA 1 — MAPA & ANÁLISE
# ============================================================
with tab1:

    st.markdown('<div class="section-label">VISUALIZAÇÃO GEOESPACIAL</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Distribuição das Perdas no Brasil</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card honey">
    🐝 <strong>Interação:</strong> Clique em qualquer marcador no mapa para ver os detalhes da localidade 
    e o raio de forrageamento de 2km da <em>Apis mellifera</em> — área que uma colônia pode alcançar em busca de alimento.
    </div>
    """, unsafe_allow_html=True)

    mapa = folium.Map(location=[-23.5, -50.5], zoom_start=6,
                      tiles='CartoDB positron')

    cores_causa = {
        "Agente_urbano_vetorial": "#E67E22",
        "Composto_herbicida_sistêmico": "#C0392B",
        "Inseticida_monocultura": "#8E44AD",
    }

    for p in dados_produtores:
        for h in p['historico']:
            if h['colmeias'] > 0:
                raio = max(8, min(45, h['colmeias'] / 8))
                cor = cores_causa.get(h['causa'], "#F5A623")
                popup_html = f"""
                <div style="font-family:sans-serif;min-width:200px;padding:8px">
                <h4 style="color:#1A3A2A;margin:0 0 6px">{p['produtor']}</h4>
                <p style="margin:2px 0;font-size:13px">📍 {p['localidade']}</p>
                <p style="margin:2px 0;font-size:13px">📅 Ano: <b>{h['ano']}</b></p>
                <p style="margin:2px 0;font-size:13px">🏠 Colmeias: <b>{h['colmeias']:,}</b></p>
                <p style="margin:2px 0;font-size:13px">🐝 Abelhas: <b>{h['abelhas']:,}</b></p>
                <p style="margin:2px 0;font-size:11px;color:#888">Causa: {causa_labels.get(h['causa'], h['causa'])}</p>
                <div style="background:#f5f5f5;padding:6px;border-radius:4px;margin-top:8px;font-size:11px">
                ◌ Raio de voo Apis mellifera: até 5km
                </div>
                </div>"""
                folium.CircleMarker(
                    location=[p['lat'], p['lon']],
                    radius=raio, color=cor, fill=True, fill_color=cor, fill_opacity=0.6,
                    popup=folium.Popup(popup_html, max_width=250),
                    tooltip=f"🐝 {p['produtor']} — {h['ano']}: {h['colmeias']} colmeias"
                ).add_to(mapa)
                folium.Circle(
                    location=[p['lat'], p['lon']],
                    radius=2000, color="#F5A623", fill=False,
                    weight=1, dash_array='5 5', opacity=0.4
                ).add_to(mapa)

    for r in dados_rs:
        raio_rs = max(8, min(50, r['colmeias'] / 60))
        folium.CircleMarker(
            location=[r['lat'], r['lon']],
            radius=raio_rs, color='#2980B9', fill=True, fill_color='#2980B9', fill_opacity=0.5,
            tooltip=f"🌊 {r['localidade']}: {r['colmeias']} colmeias",
            popup=folium.Popup(f"<b>{r['localidade']}</b><br>{r['colmeias']} colmeias<br><em>{r['evento']}</em>", max_width=200)
        ).add_to(mapa)

    legenda = """
    <div style="position:fixed;bottom:20px;right:20px;z-index:1000;background:white;padding:12px 16px;
    border-radius:10px;box-shadow:0 2px 12px rgba(0,0,0,0.15);font-family:sans-serif;font-size:12px;">
    <b>Tipo de Evento</b><br>
    <span style="color:#E67E22">●</span> Agente Urbano Vetorial<br>
    <span style="color:#C0392B">●</span> Composto Herbicida<br>
    <span style="color:#8E44AD">●</span> Inseticida Monocultura<br>
    <span style="color:#2980B9">●</span> Enchentes RS 2024<br>
    <span style="color:#F5A623">◌</span> Raio de voo (2km)
    </div>"""
    mapa.get_root().html.add_child(folium.Element(legenda))

    folium_static(mapa, width=1100, height=550)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">ANÁLISE TEMPORAL</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Evolução das Perdas por Ano</div>', unsafe_allow_html=True)

    perdas_ano = df_perdas.groupby('ano').agg({'colmeias': 'sum', 'abelhas': 'sum'}).reset_index()

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=perdas_ano['ano'], y=perdas_ano['colmeias'],
        marker=dict(
            color=perdas_ano['colmeias'],
            colorscale=[[0, '#FDF8F0'], [0.3, '#F5A623'], [0.7, '#C0392B'], [1, '#8E1515']],
            line=dict(width=0)
        ),
        text=perdas_ano['colmeias'],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Colmeias: %{y}<extra></extra>'
    ))
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans'), height=380,
        xaxis=dict(showgrid=False, tickfont=dict(size=13)),
        yaxis=dict(showgrid=True, gridcolor='#f0ebe2', title='Colmeias perdidas'),
        title=dict(text="Colmeias perdidas por ano (2016–2022)", font=dict(size=15, family='Playfair Display')),
        margin=dict(t=50, b=20)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        fig_prod = px.bar(
            df_perdas.groupby('produtor')['colmeias'].sum().reset_index(),
            x='produtor', y='colmeias',
            title="Total por Produtor",
            color='colmeias', color_continuous_scale='Oranges',
            text='colmeias'
        )
        fig_prod.update_traces(textposition='outside')
        fig_prod.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False, height=360, coloraxis_showscale=False,
            font=dict(family='DM Sans'),
            title=dict(font=dict(size=14, family='Playfair Display')),
            margin=dict(t=50, b=20)
        )
        st.plotly_chart(fig_prod, use_container_width=True)

    with col_b:
        causa_resumo = df_perdas.groupby('causa')['colmeias'].sum().reset_index()
        causa_resumo['causa_label'] = causa_resumo['causa'].map({
            "Agente_urbano_vetorial": "Agente Urbano Vetorial",
            "Composto_herbicida_sistêmico": "Composto Herbicida",
            "Inseticida_monocultura": "Inseticida Monocultura",
        })
        fig_pie = px.pie(
            causa_resumo, values='colmeias', names='causa_label',
            title="Distribuição por Categoria de Causa",
            color_discrete_sequence=['#F5A623', '#C0392B', '#8E44AD']
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False, height=360,
            font=dict(family='DM Sans'),
            title=dict(font=dict(size=14, family='Playfair Display')),
            margin=dict(t=50, b=20)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Timeline por produtor
    st.markdown('<div class="section-label">LINHA DO TEMPO POR PRODUTOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Histórico Detalhado das Ocorrências</div>', unsafe_allow_html=True)

    produtor_sel = st.selectbox("Selecione o produtor", [p['produtor'] for p in dados_produtores])
    p_data = next(p for p in dados_produtores if p['produtor'] == produtor_sel)

    st.markdown(f"""
    <div class="info-card">
    <strong>📍 {p_data['localidade']}</strong> — {p_data['regiao']}<br>
    <span style="font-size:0.85rem;color:#8C7B6B">Tipo: {p_data['tipo']}</span>
    </div>""", unsafe_allow_html=True)

    anos_p = [h['ano'] for h in p_data['historico']]
    colmeias_p = [h['colmeias'] for h in p_data['historico']]

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=anos_p, y=colmeias_p, mode='lines+markers',
        line=dict(color='#F5A623', width=3),
        marker=dict(size=10, color=['#C0392B' if c > 0 else '#3D7A52' for c in colmeias_p],
                    line=dict(width=2, color='white')),
        fill='tozeroy', fillcolor='rgba(245,166,35,0.1)',
        hovertemplate='<b>%{x}</b><br>Colmeias: %{y}<extra></extra>'
    ))
    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=300, font=dict(family='DM Sans'),
        xaxis=dict(showgrid=False, tickmode='array', tickvals=anos_p),
        yaxis=dict(showgrid=True, gridcolor='#f0ebe2', title='Colmeias'),
        title=dict(text=f"Perdas anuais — {produtor_sel}", font=dict(size=14, family='Playfair Display')),
        margin=dict(t=50, b=20)
    )
    st.plotly_chart(fig_line, use_container_width=True)


# ============================================================
# ABA 2 — METODOLOGIA & PIPELINE
# ============================================================
with tab2:

    st.markdown('<div class="section-label">PESQUISA CIENTÍFICA</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Pergunta & Metodologia</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="discovery-box">
    <div class="discovery-title">❓ Pergunta Científica Central</div>
    <p style="font-size:1.05rem;color:#2D5A3D;line-height:1.7">
    <em>"O uso de compostos químicos agrícolas e vetoriais nas regiões Sul de Minas Gerais, 
    Vale do Paraíba (SP) e Região Central do Paraná está correlacionado com a mortalidade 
    de colônias de abelhas entre 2016 e 2022?"</em>
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label" style="margin-top:1.5rem">PIPELINE DE DADOS</div>', unsafe_allow_html=True)

    steps = [
        ("1", "Coleta — Entrevistas de Campo",
         "Entrevistas com 9 apicultores/meliponicultores via WhatsApp, Instagram e e-mail. "
         "Retorno efetivo de 4 produtores (anonimato assegurado por protocolo). "
         "Identificados como Produtor A (MG), B (SP), C e D (PR)."),
        ("2", "Coleta — Revisão Bibliográfica",
         "Levantamento de literatura científica sobre CCD (Colony Collapse Disorder), "
         "compostos organofosforados, neonicotinoides e fungicidas. Bases: Google Acadêmico, "
         "IBAMA, EMBRAPA, APTA, artigos SCIELO."),
        ("3", "Processamento — Tabulação",
         "Dados das entrevistas tabulados em Microsoft Excel. Cruzamento com mapa regional "
         "do Vale do Paraíba (IBGE 2006) e dados de uso de agrotóxicos por município "
         "(Bombardini, 2017 — FFLCH/USP)."),
        ("4", "Processamento — Georreferenciamento",
         "Localidades associadas a coordenadas geográficas para mapeamento com Folium. "
         "Cálculo de raios de forrageamento por espécie (Jataí: 600m; Apis mellifera: 5km) "
         "conforme EMBRAPA (2021)."),
        ("5", "Análise — Abordagem Quali-Quantitativa",
         "Método hipotético-dedutivo. Análise descritiva das perdas por ano, produtor e causa. "
         "Cruzamento entre padrão de mortalidade e padrão de uso de compostos químicos "
         "identificado na literatura (RT25/RT40 — IBAMA 2012)."),
        ("6", "Visualização & Publicação",
         "Dashboard interativo desenvolvido em Python (Streamlit + Plotly + Folium). "
         "Mapeamento geoespacial com marcadores proporcionais às perdas. "
         "Publicado como projeto de portfólio ambiental."),
    ]

    for num, title, desc in steps:
        st.markdown(f"""
        <div class="method-step">
            <div class="step-num">{num}</div>
            <div class="step-content">
                <div class="step-title">{title}</div>
                <div class="step-desc">{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.markdown("""
        <div class="info-card">
        <strong>🐝 Espécies e Raios de Forrageamento</strong><br><br>
        <div style="font-size:0.88rem;line-height:2">
        • <b>Jataí</b> (Tetragonisca angustula): até 600m — 1,13 km²<br>
        • <b>Mandaguari</b> (Scaptotrigona xanthotricha): até 900m — 2,54 km²<br>
        • <b>Mandaçaia</b> (Melipona quadrifasciata): até 2.500m — 19,63 km²<br>
        • <b>Apis mellifera</b>: até 5.000m — 78,5 km²<br>
        </div>
        <div style="font-size:0.78rem;color:#8C7B6B;margin-top:0.5rem">Fonte: EMBRAPA, 2021</div>
        </div>""", unsafe_allow_html=True)

    with col_m2:
        st.markdown("""
        <div class="info-card honey">
        <strong>⚗️ Categorias de Compostos Identificados</strong><br><br>
        <div style="font-size:0.88rem;line-height:2">
        • <b>Agente Urbano Vetorial</b>: inseticida organofosforado utilizado no controle 
        de mosquitos vetores em centros urbanos. Aplicado por veículos municipais.<br>
        • <b>Composto Herbicida Sistêmico</b>: herbicida de largo espectro utilizado em 
        terrenos baldios e bordas de propriedades. Elimina fontes de néctar.<br>
        • <b>Inseticida de Monocultura</b>: defensivo agrícola utilizado em culturas de 
        soja e milho próximas a apiários. Contato direto via deriva de pulverização.<br>
        </div>
        <div style="font-size:0.78rem;color:#8C7B6B;margin-top:0.5rem">
        Nomes comerciais omitidos — ver nota de protocolo no topo da página
        </div>
        </div>""", unsafe_allow_html=True)


# ============================================================
# ABA 3 — O QUE DESCOBRIMOS
# ============================================================
with tab3:

    st.markdown('<div class="section-label">RESULTADOS DA PESQUISA</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">O que os Dados Revelaram</div>', unsafe_allow_html=True)

    descobertas = [
        ("🔴", "Pico de mortalidade em 2019",
         "O Produtor D (PR) perdeu 300 colmeias em um único ano — aproximadamente 18 milhões de abelhas. "
         "O evento foi associado à pulverização de inseticida em plantação de monocultura adjacente. "
         "Representa 88,9% de todas as perdas registradas no período 2016-2022."),
        ("🟠", "Subnotificação sistêmica identificada",
         "Dos 9 produtores contatados, apenas 4 responderam. O principal obstáculo foi o temor de represálias: "
         "62,5% das perdas nunca foram comunicadas a órgãos competentes (GEDAVE, Polícia Ambiental). "
         "Isso sugere que o problema real é significativamente maior que os dados disponíveis."),
        ("🟡", "Ambiente urbano como vetor de risco",
         "O Produtor A (MG) foi afetado 3 vezes em 7 anos pelo agente vetorial municipal de controle de mosquitos. "
         "50% dos apiários afetados estavam próximos de mata nativa — não de lavouras — "
         "indicando contaminação por deriva a distâncias superiores a 1km."),
        ("🟢", "Subregistro no sistema oficial",
         "Nenhum dado oficial nacional havia sido publicado sobre mortalidade de abelhas no Vale do Paraíba "
         "antes desta pesquisa. O levantamento pioneiro via formulário Google (Alves, 2022) confirmou "
         "mortalidade crescente entre 2015-2022 na região, sem registro acadêmico prévio."),
        ("🔵", "Enchentes do RS amplificam o cenário (2024)",
         "As enchentes de maio/junho de 2024 no Rio Grande do Sul devastaram mais de 6.300 colmeias, "
         "adicionando eventos climáticos extremos como novo vetor de risco para a apicultura brasileira — "
         "fenômeno não contemplado no TCC original, incorporado ao monitoramento deste observatório."),
    ]

    for emoji, titulo, texto in descobertas:
        st.markdown(f"""
        <div class="discovery-box" style="margin-bottom:0.8rem">
            <div style="display:flex;align-items:flex-start;gap:1rem">
                <span style="font-size:1.5rem">{emoji}</span>
                <div>
                    <div class="discovery-title" style="font-size:1.1rem">{titulo}</div>
                    <p style="color:#3D4D3A;line-height:1.65;font-size:0.93rem;margin:0">{texto}</p>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">CONCLUSÃO CIENTÍFICA</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card forest" style="border-left-color:#1A3A2A;background:linear-gradient(135deg,#F0F8F3,#E8F4EC)">
    <strong style="color:#1A3A2A;font-size:1rem">Confirmação da Hipótese</strong><br><br>
    <p style="color:#2D5A3D;line-height:1.7;font-size:0.93rem">
    O uso de compostos químicos agrícolas e vetoriais foi confirmado como principal causa da 
    mortalidade de colônias de abelhas nas regiões estudadas. Os dados corroboram a hipótese 
    de que o Brasil — maior consumidor mundial de agrotóxicos — enfrenta um processo de 
    Síndrome do Colapso das Colônias (CCD) regionalmente distribuído, agravado pela ausência 
    de sistemas oficiais de notificação e pelo temor de represálias que inibe o registro das perdas.
    </p>
    <p style="color:#3D7A52;font-size:0.82rem;margin-bottom:0">
    <em>Amauri Almeida — TCC Gestão Ambiental, FATEC Jundiaí, 2022</em>
    </p>
    </div>
    """, unsafe_allow_html=True)

    # Gráfico de impacto — abelhas perdidas por evento
    st.markdown("<br>", unsafe_allow_html=True)
    fig_impact = go.Figure()
    eventos = ["Inseticida\nMonocultura PR\n(2019)", "Composto\nHerbicida SP\n(2022)",
               "Inseticida\nMonocultura PR\n(2021)", "Agente\nVetorial MG\n(2016-21)"]
    valores = [18000000, 300000, 1800000, 8000]
    cores = ['#C0392B', '#8E44AD', '#C0392B', '#E67E22']

    fig_impact.add_trace(go.Bar(
        y=eventos, x=valores, orientation='h',
        marker=dict(color=cores, line=dict(width=0)),
        text=[f"{v/1e6:.1f}M" if v > 100000 else f"{v:,}" for v in valores],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Abelhas: %{x:,}<extra></extra>'
    ))
    fig_impact.update_layout(
        title=dict(text="Abelhas perdidas por evento (escala logarítmica)", font=dict(size=14, family='Playfair Display')),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=350, font=dict(family='DM Sans'),
        xaxis=dict(type='log', showgrid=True, gridcolor='#f0ebe2'),
        yaxis=dict(showgrid=False),
        margin=dict(t=50, b=20, r=80)
    )
    st.plotly_chart(fig_impact, use_container_width=True)


# ============================================================
# ABA 4 — EM CAMPO
# ============================================================
with tab4:

    st.markdown('<div class="section-label">PESQUISA APLICADA</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">A Pesquisa que Saiu da Tela</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="field-card">
    <strong style="font-size:1.1rem">📷 Adicione suas fotos de campo aqui</strong><br><br>
    <p style="opacity:0.85;line-height:1.6;font-size:0.92rem">
    Esta seção foi reservada para as fotos da pesquisa de campo realizada entre 2021 e 2022 
    com apicultores do Sul de Minas Gerais, Vale do Paraíba e Região Central do Paraná.
    Para adicionar as fotos, faça o upload para a pasta <code>assets/</code> do projeto 
    e edite a seção abaixo com os caminhos corretos.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Placeholder para fotos — instruções para o dev
    col_f1, col_f2, col_f3 = st.columns(3)

    fotos_info = [
        ("🏡", "Apiário em Extrema - MG", "Produtor A · Colmeias de Jataí\npróximas a área residencial", "assets/foto_produtor_a.jpg"),
        ("🌱", "Meliponário no Vale do Paraíba", "Produtor B · Colmeias Apis\nGuaratinguetá - SP", "assets/foto_produtor_b.jpg"),
        ("🌾", "Lavoura adjacente ao apiário", "Paraná Central · Área de\nmonocultura próxima", "assets/foto_monocultura.jpg"),
    ]

    for col, (emoji, titulo, desc, path) in zip([col_f1, col_f2, col_f3], fotos_info):
        with col:
            try:
                st.image(path, caption=titulo, use_container_width=True)
            except Exception:
                st.markdown(f"""
                <div style="background:#f0ebe2;border:2px dashed #C47D0E;border-radius:12px;
                padding:2rem;text-align:center;min-height:180px;display:flex;flex-direction:column;
                align-items:center;justify-content:center">
                <div style="font-size:2.5rem">{emoji}</div>
                <div style="font-weight:600;color:#1A3A2A;margin-top:0.5rem;font-size:0.9rem">{titulo}</div>
                <div style="font-size:0.75rem;color:#8C7B6B;margin-top:0.3rem;white-space:pre-line">{desc}</div>
                <div style="font-size:0.65rem;color:#C47D0E;margin-top:0.5rem;font-family:monospace">{path}</div>
                </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
    <strong>📌 Como adicionar as fotos ao projeto</strong><br>
    <ol style="font-size:0.88rem;color:#3D4D3A;line-height:2;margin-top:0.5rem">
    <li>Crie uma pasta <code>assets/</code> na raiz do projeto Streamlit</li>
    <li>Faça upload das fotos com os nomes exatos listados acima</li>
    <li>As imagens serão exibidas automaticamente nesta seção</li>
    <li>Para fotos adicionais, replique o padrão de código nesta aba</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

    # Contexto de campo
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">CONTEXTO DAS ENTREVISTAS</div>', unsafe_allow_html=True)

    timeline_items = [
        ("Abr 2022", "Entrevista Produtor A", "Sul de Minas Gerais · via WhatsApp e e-mail · Apiário próximo a área residencial afetado por agente vetorial municipal"),
        ("Abr 2022", "Entrevista Produtor B", "Vale do Paraíba, SP · via Instagram e e-mail · Apiário próximo a terrenos com herbicida sistêmico"),
        ("Mai 2022", "Entrevista Produtor C", "Região Central do Paraná · via Instagram e e-mail · Grande apiário próximo a monocultura"),
        ("Jun 2022", "Entrevista Produtor D", "Região Central do Paraná · via Instagram e e-mail · Maior perda individual: 300 colmeias em 2019"),
        ("Jun 2022", "Defesa do TCC", "FATEC Jundiaí, SP · Orientador: Prof. Me. Claudio da Cunha · Curso de Gestão Ambiental"),
    ]

    for data, titulo, desc in timeline_items:
        st.markdown(f"""
        <div class="timeline-item">
            <div class="timeline-year">{data}</div>
            <div class="timeline-content">
                <div class="timeline-title">{titulo}</div>
                <div class="timeline-desc">{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)


# ============================================================
# ABA 5 — FONTES & CRÉDITOS
# ============================================================
with tab5:

    st.markdown('<div class="section-label">REFERÊNCIAS CIENTÍFICAS</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Fontes & Base de Dados</div>', unsafe_allow_html=True)

    fontes = [
        ("IBAMA", "Instituto Brasileiro do Meio Ambiente e dos Recursos Naturais Renováveis",
         "Relatório técnico de pesticidas e efeitos nas abelhas (2012). Dados de uso de agrotóxicos no Brasil.",
         "#1A3A2A"),
        ("EMBRAPA", "Empresa Brasileira de Pesquisa Agropecuária",
         "Meliponicultura Urbana (2021). Dados de raio de forrageamento por espécie.",
         "#2D5A3D"),
        ("APTA", "Agência Paulista de Tecnologia dos Agronegócios",
         "Síndrome do Colapso das Colônias das abelhas pesquisada pela APTA (2015).",
         "#3D7A52"),
        ("FFLCH-USP", "Faculdade de Filosofia, Letras e Ciências Humanas – USP",
         "Bombardini, L.M. (2017) — Geografia do Uso de Agrotóxicos no Brasil e Conexões com a União Europeia.",
         "#4A8B5E"),
        ("IBGE", "Instituto Brasileiro de Geografia e Estatística",
         "Mapa regional do Vale do Paraíba (2006). Dados de uso do solo por município.",
         "#1A3A2A"),
        ("UNITAU", "Universidade de Taubaté — Pós-Graduação em Apicultura e Meliponicultura",
         "Alves, J.F.G. (2022) — Levantamento de Mortalidade de Abelhas por Agrotóxicos no Vale do Paraíba.",
         "#2D5A3D"),
        ("FATEC JUNDIAÍ", "Faculdade de Tecnologia de Jundiaí — Centro Paula Souza",
         "TCC: Almeida, A. (2022) — A Problemática da Síndrome das Colônias de Abelhas. Nota máxima ENADE.",
         "#C0392B"),
    ]

    for sigla, nome, descricao, cor in fontes:
        st.markdown(f"""
        <div class="info-card" style="border-left-color:{cor}">
        <div style="display:flex;align-items:flex-start;gap:1rem">
            <div style="background:{cor};color:white;font-family:'DM Mono',monospace;font-size:0.65rem;
            padding:4px 8px;border-radius:4px;white-space:nowrap;flex-shrink:0;margin-top:2px;
            letter-spacing:1px;font-weight:bold">{sigla}</div>
            <div>
                <div style="font-weight:500;font-size:0.9rem;color:#1A3A2A">{nome}</div>
                <div style="font-size:0.82rem;color:#8C7B6B;margin-top:0.2rem">{descricao}</div>
            </div>
        </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">TECNOLOGIAS UTILIZADAS</div>', unsafe_allow_html=True)

    techs = ["Python 3.11", "Streamlit", "Plotly", "Folium", "Pandas", "NumPy", "Google Forms"]
    badges_html = "".join([f'<span class="source-badge">{t}</span>' for t in techs])
    st.markdown(f'<div class="source-badges">{badges_html}</div>', unsafe_allow_html=True)

    # Sobre o pesquisador
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="footer-wrap">
        <div class="footer-title">🐝 Amauri Almeida</div>
        <p style="margin:0.5rem 0;font-size:0.9rem">
        Tecnólogo em Gestão Ambiental · FATEC Jundiaí (3º ENADE) <br>
        Pós-Graduação em IA, Machine Learning & Data Science · Pós-Graduação em Ciência de Dados & Big Data<br>
        Análise e Desenvolvimento de Sistemas · FACINT Maringá
        </p>
        <p style="margin:1rem 0 0.5rem;font-size:0.85rem;opacity:0.7">
        📍 Brasil · Chile · Argentina &nbsp;|&nbsp; 
        🌐 <a href="https://amaurialmeida.github.io/environmental-portfolio/" 
        style="color:#F5A623">Portfólio Ambiental</a> &nbsp;|&nbsp;
        🐙 <a href="https://github.com/amaurialmeida" style="color:#F5A623">GitHub</a>
        </p>
        <p style="font-size:0.75rem;opacity:0.5;margin:0">
        © 2026 · Observatório do Colapso de Colmeias · Pesquisa Acadêmica
        </p>
    </div>
    """, unsafe_allow_html=True)
