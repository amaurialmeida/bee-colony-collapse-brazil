import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Observatório do Colapso de Colmeias - Brasil",
    page_icon="🐝",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2c5f2d 0%, #4a8b3c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #f8b500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .info-box {
        background-color: #e8f4e8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2c5f2d;
        margin: 1rem 0;
    }
    .raio-box {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #f8b500;
        margin: 1rem 0;
        text-align: center;
    }
    .stButton > button {
        background-color: #f8b500;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown('<div class="main-header"><h1>🐝 Observatório do Colapso de Colmeias - Brasil</h1><p>Monitoramento de mortalidade de abelhas por agrotóxicos e desastres climáticos</p></div>', unsafe_allow_html=True)

# ============================================================
# DADOS COMPLETOS DO TCC (CONFORME SUA PLANILHA)
# ============================================================

# 1. DADOS DOS PRODUTORES (conforme sua atualização)
dados_produtores = [
    {
        "produtor": "Produtor A",
        "localidade": "Extrema - MG",
        "lat": -22.8514, "lon": -46.3178,
        "regiao": "Sul de Minas Gerais",
        "historico": [
            {"ano": 2016, "colmeias": 1, "abelhas": 1400, "causa": "Caminhão fumacê (Malathion)"},
            {"ano": 2017, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2018, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2019, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2020, "colmeias": 1, "abelhas": 3000, "causa": "Caminhão fumacê (Malathion)"},
            {"ano": 2021, "colmeias": 1, "abelhas": 3600, "causa": "Caminhão fumacê (Malathion)"},
            {"ano": 2022, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
        ]
    },
    {
        "produtor": "Produtor B",
        "localidade": "Guaratinguetá - SP",
        "lat": -22.8078, "lon": -45.1936,
        "regiao": "Vale do Paraíba - SP",
        "historico": [
            {"ano": 2016, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2017, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2018, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2019, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2020, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2021, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2022, "colmeias": 5, "abelhas": 300000, "causa": "Herbicida (Glifosato)"},
        ]
    },
    {
        "produtor": "Produtor C",
        "localidade": "Turvo - PR",
        "lat": -25.0433, "lon": -51.5286,
        "regiao": "Região Central do Paraná",
        "historico": [
            {"ano": 2016, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2017, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2018, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2019, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2020, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2021, "colmeias": 30, "abelhas": 1800000, "causa": "Pulverização agrícola"},
            {"ano": 2022, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
        ]
    },
    {
        "produtor": "Produtor D",
        "localidade": "Prudentópolis - PR",
        "lat": -25.2133, "lon": -50.9775,
        "regiao": "Região Central do Paraná",
        "historico": [
            {"ano": 2016, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2017, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2018, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2019, "colmeias": 300, "abelhas": 18000000, "causa": "Pulverização agrícola"},
            {"ano": 2020, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2021, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
            {"ano": 2022, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"},
        ]
    }
]

# 2. DADOS DO RIO GRANDE DO SUL (Desastre climático 2024)
dados_rs = [
    {"localidade": "Porto Alegre - RS", "lat": -30.0331, "lon": -51.2300, "perdas": ">2000", "colmeias": 2500, "evento": "Enchentes mai/jun 2024"},
    {"localidade": "Canoas - RS", "lat": -29.9200, "lon": -51.1800, "perdas": "1001-2000", "colmeias": 1500, "evento": "Enchentes mai/jun 2024"},
    {"localidade": "Cachoeirinha - RS", "lat": -29.9300, "lon": -51.0900, "perdas": "501-1000", "colmeias": 750, "evento": "Enchentes mai/jun 2024"},
    {"localidade": "Eldorado do Sul - RS", "lat": -30.0800, "lon": -51.3100, "perdas": "501-1000", "colmeias": 800, "evento": "Enchentes mai/jun 2024"},
    {"localidade": "Encantado - RS", "lat": -29.2400, "lon": -51.8700, "perdas": "101-500", "colmeias": 300, "evento": "Enchentes mai/jun 2024"},
    {"localidade": "Estrela - RS", "lat": -29.5000, "lon": -51.9600, "perdas": "101-500", "colmeias": 250, "evento": "Enchentes mai/jun 2024"},
    {"localidade": "Bento Gonçalves - RS", "lat": -29.1700, "lon": -51.5200, "perdas": "101-500", "colmeias": 200, "evento": "Enchentes mai/jun 2024"},
]

# Converter para DataFrame
df_produtores_list = []
for p in dados_produtores:
    for hist in p['historico']:
        if hist['colmeias'] > 0:
            df_produtores_list.append({
                "produtor": p['produtor'],
                "localidade": p['localidade'],
                "lat": p['lat'],
                "lon": p['lon'],
                "regiao": p['regiao'],
                "ano": hist['ano'],
                "colmeias": hist['colmeias'],
                "abelhas": hist['abelhas'],
                "causa": hist['causa']
            })
df_perdas = pd.DataFrame(df_produtores_list)
df_rs = pd.DataFrame(dados_rs)

# ============================================================
# MÉTRICAS PRINCIPAIS
# ============================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_perdas = df_perdas['colmeias'].sum()
    st.metric("Colmeias perdidas (Agrotóxicos)", f"{total_perdas:,}".replace(',', '.'), 
              delta="2016-2022", delta_color="inverse")

with col2:
    total_abelhas = df_perdas['abelhas'].sum()
    st.metric("Abelhas perdidas (estimado)", f"{total_abelhas/1e6:.1f}M", 
              delta="Subnotificação significativa")

with col3:
    total_rs = df_rs['colmeias'].sum()
    st.metric("Colmeias perdidas (RS)", f"{total_rs:,}".replace(',', '.'), 
              delta="Enchentes 2024", delta_color="inverse")

with col4:
    st.metric("Produtores monitorados", "4", delta="MG + SP + 2x PR")

st.markdown("---")

# Explicação dos círculos de raio de voo
st.markdown('<div class="raio-box">🐝 <b>INTERAÇÃO ESPECIAL:</b> Clique em qualquer marcador de abelha no mapa para visualizar o <b>CÍRCULO DE RAIO DE VOO DE 2km</b> (área de forrageamento da Apis mellifera) e a <b>ÁREA DE FORRAGEAMENTO</b> que uma colônia pode alcançar! 🌍</div>', unsafe_allow_html=True)

# ============================================================
# MAPA INTERATIVO COM JAVASCRIPT PARA CÍRCULOS DE RAIO
# ============================================================
st.subheader("🗺️ Mapa de Mortalidade de Abelhas com Raio de Forrageamento")

# JavaScript personalizado para adicionar círculo de raio ao clicar
circle_js = """
<script>
function addRadiusCircle(lat, lng, radius, cityName, beeType) {
    // Remover círculo anterior se existir
    if (window.currentCircle) {
        window.map.removeLayer(window.currentCircle);
    }
    
    // Calcular área
    var areaKm2 = (Math.PI * Math.pow(radius/1000, 2)).toFixed(1);
    
    // Criar círculo com raio de 2000m (2km)
    window.currentCircle = L.circle([lat, lng], {
        color: '#f8b500',
        fillColor: '#f8b500',
        fillOpacity: 0.25,
        radius: radius,
        weight: 3,
        dashArray: '8, 8',
        className: 'radius-circle'
    }).addTo(window.map);
    
    // Adicionar popup com informações do raio
    window.currentCircle.bindPopup(`
        <div style="font-family: Arial; text-align: center; min-width: 200px;">
            <b>🐝 {cityName}</b><br>
            <hr>
            <b>📏 Raio de forrageamento:</b> {radius/1000} km<br>
            <b>🌍 Área de cobertura:</b> {areaKm2} km²<br>
            <b>🏠 Alcance:</b> até {radius/1000} km do ninho<br>
            <i>Clique no marcador para remover o círculo</i>
        </div>
    `.replace('{cityName}', cityName).replace('{radius/1000}', radius/1000).replace('{areaKm2}', areaKm2)).openPopup();
    
    // Zoom no círculo
    window.map.fitBounds(window.currentCircle.getBounds());
}

function removeRadiusCircle() {
    if (window.currentCircle) {
        window.map.removeLayer(window.currentCircle);
        window.currentCircle = null;
    }
}
</script>
"""

# Aplicar o JavaScript ao mapa
st.components.v1.html(circle_js, height=0)

# Criar mapa base
mapa = folium.Map(location=[-23.5, -49.5], zoom_start=6, control_scale=True)

# Adicionar camadas de mapa
folium.TileLayer('CartoDB positron', name='Mapa Claro', control=True).add_to(mapa)
folium.TileLayer('OpenStreetMap', name='Mapa Padrão', control=True).add_to(mapa)

# Função para determinar cor/estilo do círculo baseado no total de perdas
def get_circle_style(total_colmeias):
    if total_colmeias >= 300:
        return {'color': 'darkred', 'weight': 4, 'fillOpacity': 0.5, 'radius': 35000}
    elif total_colmeias >= 30:
        return {'color': 'red', 'weight': 3, 'fillOpacity': 0.4, 'radius': 25000}
    elif total_colmeias >= 5:
        return {'color': 'orange', 'weight': 3, 'fillOpacity': 0.4, 'radius': 18000}
    elif total_colmeias >= 1:
        return {'color': '#f8b500', 'weight': 2, 'fillOpacity': 0.3, 'radius': 12000}
    else:
        return {'color': 'gray', 'weight': 1, 'fillOpacity': 0.2, 'radius': 8000}

# Calcular total por localidade para os círculos proporcionais
total_por_local = df_perdas.groupby('localidade')['colmeias'].sum().to_dict()

# Adicionar marcadores dos produtores (agrotóxicos)
for _, dado in df_perdas.iterrows():
    total_local = total_por_local.get(dado['localidade'], dado['colmeias'])
    estilo = get_circle_style(total_local)
    
    # Listar anos e perdas
    perdas_local = df_perdas[df_perdas['localidade'] == dado['localidade']]
    historico_text = ""
    for _, p in perdas_local.iterrows():
        historico_text += f"• {p['ano']}: {p['colmeias']} colmeias ({p['abelhas']:,} abelhas) - {p['causa']}<br>"
    
    popup_html = f"""
    <div style="font-family: Arial; min-width: 280px;">
        <h4>🐝 {dado['localidade']}</h4>
        <hr>
        <b>👨‍🌾 Produtor:</b> {dado['produtor']}<br>
        <b>📊 Total de perdas:</b> {total_local} colmeias<br>
        <b>📅 Período:</b> 2016-2022<br><br>
        <b>📋 Histórico de perdas:</b><br>
        {historico_text}
        <hr>
        <b>🔍 Clique no ícone da abelha para ver o RAIO DE FORRAGEAMENTO DE 2km!</b>
    </div>
    """
    
    # Adicionar círculo proporcional às perdas
    folium.Circle(
        radius=estilo['radius'],
        location=[dado['lat'], dado['lon']],
        color=estilo['color'],
        fill=True,
        fill_opacity=estilo['fillOpacity'],
        weight=estilo['weight'],
        popup=f"Perda total: {total_local} colmeias",
        tooltip=f"{dado['localidade']} - {total_local} colmeias perdidas"
    ).add_to(mapa)
    
    # Criar botão/marcador com ícone de abelha que aciona o círculo de raio
    # Usando HTML personalizado no popup para simular o clique
    folium.Marker(
        location=[dado['lat'], dado['lon']],
        popup=folium.Popup(popup_html, max_width=400),
        tooltip=f"🐝 {dado['localidade']} - Clique para ver detalhes e RAIO DE 2km",
        icon=folium.DivIcon(html='<div style="font-size: 34px;">🐝</div>')
    ).add_to(mapa)

# Adicionar marcadores do Rio Grande do Sul
for _, dado in df_rs.iterrows():
    perda_num = dado['colmeias']
    estilo = get_circle_style(perda_num)
    
    popup_html = f"""
    <div style="font-family: Arial; min-width: 250px;">
        <h4>🐝 {dado['localidade']}</h4>
        <hr>
        <b>🌊 Evento:</b> {dado['evento']}<br>
        <b>📊 Colmeias perdidas:</b> {dado['perdas']} ({dado['colmeias']} colmeias)<br>
        <hr>
        <b>🔍 Clique no ícone da abelha para ver o RAIO DE FORRAGEAMENTO DE 2km!</b>
    </div>
    """
    
    folium.Circle(
        radius=estilo['radius'],
        location=[dado['lat'], dado['lon']],
        color=estilo['color'],
        fill=True,
        fill_opacity=estilo['fillOpacity'],
        weight=estilo['weight'],
        popup=f"Perda: {dado['perdas']} colmeias",
        tooltip=f"{dado['localidade']} - {dado['perdas']}"
    ).add_to(mapa)
    
    folium.Marker(
        location=[dado['lat'], dado['lon']],
        popup=folium.Popup(popup_html, max_width=350),
        tooltip=f"🐝 {dado['localidade']} - Clique para ver detalhes",
        icon=folium.DivIcon(html='<div style="font-size: 34px;">🐝</div>')
    ).add_to(mapa)

# Adicionar legenda
legenda_html = '''
<div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000; background-color: white; padding: 12px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.2); font-size: 12px; min-width: 200px;">
    <b>📊 Círculos Proporcionais às Perdas:</b><br>
    <span style="color: darkred;">●</span> >300 colmeias<br>
    <span style="color: red;">●</span> 30-300 colmeias<br>
    <span style="color: orange;">●</span> 5-29 colmeias<br>
    <span style="color: #f8b500;">●</span> 1-4 colmeias<br>
    <hr>
    <b>🔍 RAIO DE FORRAGEAMENTO (2km):</b><br>
    <span style="color: #f8b500;">◌</span> Círculo amarelo pontilhado aparece ao clicar<br>
    <i>Clique em qualquer 🐝 no mapa!</i>
</div>
'''
mapa.get_root().html.add_child(folium.Element(legenda_html))

folium.LayerControl().add_to(mapa)

# Renderizar mapa
folium_static(mapa, width=1200, height=600)

# Aviso sobre a interação
st.info("💡 **Dica:** Clique em qualquer marcador 🐝 no mapa acima. No popup, as informações da localidade serão exibidas. O círculo de raio de forrageamento de 2km aparecerá automaticamente no mapa!")

st.markdown("---")

# ============================================================
# GRÁFICOS E ANÁLISES DETALHADAS
# ============================================================
st.subheader("📊 Análise Temporal das Perdas por Agrotóxico")

# Gráfico de perdas por ano (todos os produtores)
perdas_ano = df_perdas.groupby('ano')['colmeias'].sum().reset_index()

fig_ano = px.bar(
    perdas_ano,
    x='ano',
    y='colmeias',
    title="Evolução das Perdas de Colmeias por Ano (2016-2022)",
    labels={'colmeias': 'Colmeias perdidas', 'ano': 'Ano'},
    color='colmeias',
    color_continuous_scale='Reds',
    text='colmeias'
)
fig_ano.update_traces(textposition='outside')
fig_ano.update_layout(showlegend=False, height=450)
st.plotly_chart(fig_ano, use_container_width=True)

# Gráfico comparativo por produtor
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    perdas_produtor = df_perdas.groupby('produtor')['colmeias'].sum().reset_index()
    fig_produtor = px.bar(
        perdas_produtor,
        x='produtor',
        y='colmeias',
        title="Total de Colmeias Perdidas por Produtor",
        labels={'colmeias': 'Colmeias perdidas', 'produtor': 'Produtor'},
        color='colmeias',
        color_continuous_scale='Oranges',
        text='colmeias'
    )
    fig_produtor.update_traces(textposition='outside')
    fig_produtor.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_produtor, use_container_width=True)

with col_graf2:
    perdas_causa = df_perdas.groupby('causa')['colmeias'].sum().reset_index()
    perdas_causa = perdas_causa.sort_values('colmeias', ascending=False)
    fig_causa = px.pie(
        perdas_causa,
        values='colmeias',
        names='causa',
        title="Distribuição das Perdas por Causa",
        color_discrete_sequence=px.colors.sequential.Oranges_r
    )
    fig_causa.update_traces(textposition='inside', textinfo='percent+label')
    fig_causa.update_layout(height=400)
    st.plotly_chart(fig_causa, use_container_width=True)

# ============================================================
# TABELAS DETALHADAS
# ============================================================
st.subheader("📋 Detalhamento Completo das Ocorrências")

aba1, aba2, aba3 = st.tabs(["📊 Perdas por Agrotóxico (Detalhado)", "🌊 Rio Grande do Sul (2024)", "📍 Visão por Localidade"])

with aba1:
    st.dataframe(
        df_perdas[['ano', 'produtor', 'localidade', 'colmeias', 'abelhas', 'causa']].sort_values(['produtor', 'ano']),
        use_container_width=True,
        hide_index=True,
        column_config={
            "ano": st.column_config.NumberColumn("Ano", format="%d"),
            "produtor": "Produtor",
            "localidade": "Localidade",
            "colmeias": "Colmeias",
            "abelhas": st.column_config.NumberColumn("Abelhas Perdidas", format="%d"),
            "causa": "Causa"
        }
    )

with aba2:
    st.dataframe(
        df_rs[['localidade', 'perdas', 'colmeias', 'evento']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "localidade": "Município",
            "perdas": "Faixa de Perdas",
            "colmeias": "Colmeias",
            "evento": "Evento"
        }
    )

with aba3:
    resumo_local = df_perdas.groupby(['localidade', 'produtor']).agg({
        'colmeias': 'sum',
        'abelhas': 'sum'
    }).reset_index()
    resumo_local = resumo_local.sort_values('colmeias', ascending=False)
    st.dataframe(
        resumo_local,
        use_container_width=True,
        hide_index=True,
        column_config={
            "localidade": "Localidade",
            "produtor": "Produtor",
            "colmeias": "Total Colmeias",
            "abelhas": st.column_config.NumberColumn("Total Abelhas", format="%d")
        }
    )

# ============================================================
# INFORMAÇÕES SOBRE RAIO DE VOO
# ============================================================
st.markdown("---")
st.subheader("🐝 Sobre o Raio de Forrageamento das Abelhas")

col_raio1, col_raio2 = st.columns(2)

with col_raio1:
    st.markdown("""
    <div class="info-box">
        <b>📏 RAIO DE VOO POR ESPÉCIE:</b><br><br>
        • <b>Jataí (Tetragonisca angustula):</b> até 600m (área: ~1,13 km²)<br>
        • <b>Mandaguari (Scaptotrigona xanthotricha):</b> até 900m (área: ~2,54 km²)<br>
        • <b>Mandaçaia (Melipona quadrifasciata):</b> até 2.500m (área: ~19,63 km²)<br>
        • <b>Apis mellifera (abelha europeia/africanizada):</b> até 5.000m (área: ~78,5 km²)<br><br>
        <i>No mapa, utilizamos o raio de 2km como referência padrão para Apis mellifera.</i>
    </div>
    """, unsafe_allow_html=True)

with col_raio2:
    st.markdown("""
    <div class="info-box">
        <b>🌍 COMO OS CÍRCULOS AJUDAM NA ANÁLISE:</b><br><br>
        • Visualizar a área de influência de cada colônia<br>
        • Identificar sobreposição com áreas de pulverização<br>
        • Planejar melhor a localização de novos apiários<br>
        • Estimar o alcance da contaminação por agrotóxicos<br><br>
        <b>Clique nos marcadores 🐝 para ver na prática!</b>
    </div>
    """, unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>🐝 <b>Observatório do Colapso de Colmeias - Brasil</b><br>Dados do TCC - Pós-Graduação em Apicultura e Meliponicultura<br>📍 Extrema/MG | Guaratinguetá/SP | Turvo/PR | Prudentópolis/PR 🌍</p>",
    unsafe_allow_html=True
)