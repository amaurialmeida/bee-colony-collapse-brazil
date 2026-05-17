import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
 
st.set_page_config(
    page_title="Síndrome do Colapso das Colônias · Brasil",
    page_icon="🐝",
    layout="wide"
)
 
# ============================================================
# SISTEMA DE IDIOMAS
# ============================================================
if "lang" not in st.session_state:
    st.session_state.lang = "pt"
 
TRANSLATIONS = {
    "pt": {
        "page_title": "Síndrome do Colapso das Colônias · Brasil",
        "hero_tag": "TCC · FATEC Jundiaí · Gestão Ambiental · 2022",
        "hero_title": "Síndrome do Colapso\ndas Colônias de Abelhas",
        "hero_subtitle": "Análise da mortalidade de abelhas por compostos químicos agrícolas e eventos climáticos em 3 regiões brasileiras (2016–2022). Pesquisa com 338 colmeias e ~20 milhões de abelhas.",
        "badge1": "🐝 338 Colmeias", "badge2": "~20M Abelhas", "badge3": "MG · SP · PR · RS",
        "badge4": "2016 — 2022", "badge5": "FATEC JUNDIAÍ · 3º ENADE",
        "protocol_title": "📋 Nota de Protocolo Científico:",
        "protocol_text": "Os nomes comerciais dos compostos químicos identificados nesta pesquisa foram omitidos nesta publicação a pedido dos produtores entrevistados e por cautela legal, substituídos por categorias técnicas genéricas. Os dados completos estão disponíveis no TCC original depositado na FATEC Jundiaí (2022). Para fins acadêmicos, solicite acesso pelo formulário de contato.",
        "m1": "Colmeias perdidas", "m2": "Abelhas perdidas (est.)", "m3": "Produtores monitorados", "m4": "Colmeias RS (2024)",
        "tab1": "🗺️ Mapa & Análise", "tab2": "🔬 Metodologia & Pipeline",
        "tab3": "💡 O que Descobrimos", "tab4": "📷 Em Campo", "tab5": "📚 Fontes & Créditos",
        "map_label": "VISUALIZAÇÃO GEOESPACIAL", "map_title": "Distribuição das Perdas no Brasil",
        "map_hint": "🐝 <strong>Interação:</strong> Clique em qualquer marcador no mapa para ver os detalhes da localidade e o raio de forrageamento de 2km da <em>Apis mellifera</em>.",
        "temporal_label": "ANÁLISE TEMPORAL", "temporal_title": "Evolução das Perdas por Ano",
        "bar_title": "Colmeias perdidas por ano (2016–2022)", "bar_y": "Colmeias perdidas",
        "prod_title": "Total por Produtor", "pie_title": "Distribuição por Categoria de Causa",
        "timeline_label": "LINHA DO TEMPO POR PRODUTOR", "timeline_title": "Histórico Detalhado das Ocorrências",
        "select_producer": "Selecione o produtor",
        "method_label": "PESQUISA CIENTÍFICA", "method_title": "Pergunta & Metodologia",
        "sci_question_title": "❓ Pergunta Científica Central",
        "sci_question": "\"O uso de compostos químicos agrícolas e vetoriais nas regiões Sul de Minas Gerais, Vale do Paraíba (SP) e Região Central do Paraná está correlacionado com a mortalidade de colônias de abelhas entre 2016 e 2022?\"",
        "pipeline_label": "PIPELINE DE DADOS",
        "steps": [
            ("1", "Coleta — Entrevistas de Campo", "Entrevistas com 9 apicultores/meliponicultores via WhatsApp, Instagram e e-mail. Retorno efetivo de 4 produtores (anonimato assegurado por protocolo). Identificados como Produtor A (MG), B (SP), C e D (PR)."),
            ("2", "Coleta — Revisão Bibliográfica", "Levantamento de literatura científica sobre CCD (Colony Collapse Disorder), compostos organofosforados, neonicotinoides e fungicidas. Bases: Google Acadêmico, IBAMA, EMBRAPA, APTA, artigos SCIELO."),
            ("3", "Processamento — Tabulação", "Dados das entrevistas tabulados em Microsoft Excel. Cruzamento com mapa regional do Vale do Paraíba (IBGE 2006) e dados de uso de agrotóxicos por município (Bombardini, 2017 — FFLCH/USP)."),
            ("4", "Processamento — Georreferenciamento", "Localidades associadas a coordenadas geográficas para mapeamento com Folium. Cálculo de raios de forrageamento por espécie (Jataí: 600m; Apis mellifera: 5km) conforme EMBRAPA (2021)."),
            ("5", "Análise — Abordagem Quali-Quantitativa", "Método hipotético-dedutivo. Análise descritiva das perdas por ano, produtor e causa. Cruzamento entre padrão de mortalidade e padrão de uso de compostos químicos identificado na literatura (RT25/RT40 — IBAMA 2012)."),
            ("6", "Visualização & Publicação", "Dashboard interativo desenvolvido em Python (Streamlit + Plotly + Folium). Mapeamento geoespacial com marcadores proporcionais às perdas. Publicado como projeto de portfólio ambiental."),
        ],
        "species_title": "🐝 Espécies e Raios de Forrageamento",
        "species_text": "• <b>Jataí</b> (Tetragonisca angustula): até 600m — 1,13 km²<br>• <b>Mandaguari</b> (Scaptotrigona xanthotricha): até 900m — 2,54 km²<br>• <b>Mandaçaia</b> (Melipona quadrifasciata): até 2.500m — 19,63 km²<br>• <b>Apis mellifera</b>: até 5.000m — 78,5 km²",
        "species_source": "Fonte: EMBRAPA, 2021",
        "compounds_title": "⚗️ Categorias de Compostos Identificados",
        "compounds_text": "• <b>Agente Urbano Vetorial</b>: inseticida organofosforado utilizado no controle de mosquitos vetores em centros urbanos. Aplicado por veículos municipais.<br>• <b>Composto Herbicida Sistêmico</b>: herbicida de largo espectro utilizado em terrenos baldios e bordas de propriedades. Elimina fontes de néctar.<br>• <b>Inseticida de Monocultura</b>: defensivo agrícola utilizado em culturas de soja e milho próximas a apiários. Contato direto via deriva de pulverização.",
        "compounds_note": "Nomes comerciais omitidos — ver nota de protocolo no topo da página",
        "discovery_label": "RESULTADOS DA PESQUISA", "discovery_title": "O que os Dados Revelaram",
        "discoveries": [
            ("🔴", "Pico de mortalidade em 2019", "O Produtor D (PR) perdeu 300 colmeias em um único ano — aproximadamente 18 milhões de abelhas. O evento foi associado à pulverização de inseticida em plantação de monocultura adjacente. Representa 88,9% de todas as perdas registradas no período 2016-2022."),
            ("🟠", "Subnotificação sistêmica identificada", "Dos 9 produtores contatados, apenas 4 responderam. O principal obstáculo foi o temor de represálias: 62,5% das perdas nunca foram comunicadas a órgãos competentes (GEDAVE, Polícia Ambiental). Isso sugere que o problema real é significativamente maior que os dados disponíveis."),
            ("🟡", "Ambiente urbano como vetor de risco", "O Produtor A (MG) foi afetado 3 vezes em 7 anos pelo agente vetorial municipal de controle de mosquitos. 50% dos apiários afetados estavam próximos de mata nativa — não de lavouras — indicando contaminação por deriva a distâncias superiores a 1km."),
            ("🟢", "Subregistro no sistema oficial", "Nenhum dado oficial nacional havia sido publicado sobre mortalidade de abelhas no Vale do Paraíba antes desta pesquisa. O levantamento pioneiro via formulário Google (Alves, 2022) confirmou mortalidade crescente entre 2015-2022 na região, sem registro acadêmico prévio."),
            ("🔵", "Enchentes do RS amplificam o cenário (2024)", "As enchentes de maio/junho de 2024 no Rio Grande do Sul devastaram mais de 6.300 colmeias, adicionando eventos climáticos extremos como novo vetor de risco para a apicultura brasileira."),
        ],
        "conclusion_label": "CONCLUSÃO CIENTÍFICA",
        "conclusion_title": "Confirmação da Hipótese",
        "conclusion_text": "O uso de compostos químicos agrícolas e vetoriais foi confirmado como principal causa da mortalidade de colônias de abelhas nas regiões estudadas. Os dados corroboram a hipótese de que o Brasil — maior consumidor mundial de agrotóxicos — enfrenta um processo de Síndrome do Colapso das Colônias (CCD) regionalmente distribuído, agravado pela ausência de sistemas oficiais de notificação e pelo temor de represálias que inibe o registro das perdas.",
        "conclusion_author": "Amauri Almeida — TCC Gestão Ambiental, FATEC Jundiaí, 2022",
        "impact_title": "Abelhas perdidas por evento (escala logarítmica)",
        "field_label": "PESQUISA APLICADA", "field_title": "A Pesquisa que Saiu da Tela",
        "photos": [
            {
                "emoji": "🏛️",
                "titulo": "Museu das Abelhas — Cotia / Embu das Artes, SP",
                "desc": "Visita ao Museu das Abelhas. Colmeia de Apis mellifera em exposição — espécie central desta pesquisa.",
                "path": "assets/foto_01_museu_apis.jpg",
                "legenda": "Colmeia de Apis mellifera · Museu das Abelhas · Cotia / Embu das Artes, SP"
            },
            {
                "emoji": "💀",
                "titulo": "Abelhas Mortas — Guaratinguetá, SP · Out/2021",
                "desc": "Abelhas mortas em apiário localizado no município de Guaratinguetá, outubro de 2021. Evidência direta do evento de colapso registrado nesta pesquisa.",
                "path": "assets/foto_02_mortas_guaratingueta.jpg",
                "legenda": "Abelhas mortas em Guaratinguetá · Out/2021 · Foto: J.F.A."
            },
            {
                "emoji": "🗺️",
                "titulo": "O Mundo das Abelhas — Mapa Interativo da Vida",
                "desc": "Painel interativo do Museu das Abelhas com o resumo completo do ciclo de vida das abelhas. Base educacional utilizada como referência no TCC.",
                "path": "assets/foto_03_museu_mapa_vida.jpg",
                "legenda": "Mapa interativo do ciclo de vida · Museu das Abelhas · Cotia / Embu das Artes, SP"
            },
            {
                "emoji": "🌻",
                "titulo": "Apis mellifera em Girassol — FATEC Jundiaí",
                "desc": "Abelha Apis mellifera em girassol no jardim da FATEC Jundiaí, onde foi defendido o TCC e concluída a Graduação em Gestão Ambiental (3º ENADE).",
                "path": "assets/foto_04_apis_girassol_fatec.jpg",
                "legenda": "Apis mellifera em girassol · Jardim da FATEC Jundiaí · SP"
            },
            {
                "emoji": "🔬",
                "titulo": "O Mundo das Abelhas — Anatomia",
                "desc": "Painel do Museu das Abelhas com mapa detalhado da anatomia das abelhas. Referência morfológica utilizada na caracterização das espécies estudadas.",
                "path": "assets/foto_05_museu_anatomia.jpg",
                "legenda": "Mapa de anatomia das abelhas · Museu das Abelhas · Cotia / Embu das Artes, SP"
            },
            {
                "emoji": "🏺",
                "titulo": "Pintura Rupestre — 500 a.C. · Coleta de Mel",
                "desc": "Pintura rupestre de 500 a.C. mostrando pessoas coletando mel. A relação humana com as abelhas é documentada há milênios.",
                "path": "assets/foto_06_rupestre_500ac.jpg",
                "legenda": "Pintura rupestre · 500 a.C. · Relação humana com abelhas"
            },
            {
                "emoji": "🌍",
                "titulo": "Caçador de Mel — Rodésia, África do Sul · 8.000 anos",
                "desc": "Painel retratando um Caçador de Mel na Rodésia (atual Zimbábue), na África do Sul. Arte datada de aproximadamente 8.000 anos.",
                "path": "assets/foto_07_cacador_mel_rodesia.jpg",
                "legenda": "Caçador de Mel · Rodésia, África do Sul · ~8.000 anos"
            },
            {
                "emoji": "🪨",
                "titulo": "Pintura Rupestre — Castellón, Espanha · +10.000 anos",
                "desc": "Pintura rupestre descoberta em Castellón, Espanha. Desenho paleolítico com mais de 10 mil anos representando coleta de mel — uma das primeiras representações humanas da apicultura.",
                "path": "assets/foto_08_rupestre_castellon.jpg",
                "legenda": "Desenho paleolítico · Castellón, Espanha · +10.000 anos"
            },
        ],
        "field_instrucoes_title": "📌 Como adicionar as fotos ao projeto",
        "field_instrucoes": "Crie uma pasta <code>assets/</code> na raiz do projeto Streamlit e faça upload das fotos com os nomes exatos listados abaixo de cada card. As imagens serão exibidas automaticamente.",
        "timeline_field_label": "CONTEXTO DAS ENTREVISTAS",
        "timeline_field_items": [
            ("Abr 2022", "Entrevista Produtor A", "Sul de Minas Gerais · WhatsApp e e-mail · Apiário próximo a área residencial afetado por agente vetorial municipal"),
            ("Abr 2022", "Entrevista Produtor B", "Vale do Paraíba, SP · Instagram e e-mail · Apiário próximo a terrenos com herbicida sistêmico"),
            ("Mai 2022", "Entrevista Produtor C", "Região Central do Paraná · Instagram e e-mail · Grande apiário próximo a monocultura"),
            ("Jun 2022", "Entrevista Produtor D", "Região Central do Paraná · Instagram e e-mail · Maior perda individual: 300 colmeias em 2019"),
            ("Jun 2022", "Defesa do TCC", "FATEC Jundiaí, SP · Orientador: Prof. Me. Claudio da Cunha · Curso de Gestão Ambiental"),
            ("Out 2021", "Visita ao Museu das Abelhas", "Cotia / Embu das Artes, SP · Coleta de registros fotográficos e referências científicas para o TCC"),
        ],
        "sources_label": "REFERÊNCIAS CIENTÍFICAS", "sources_title": "Fontes & Base de Dados",
        "tech_label": "TECNOLOGIAS UTILIZADAS",
        "footer_title": "🐝 Amauri Almeida",
        "footer_desc": "Tecnólogo em Gestão Ambiental · FATEC Jundiaí (3º ENADE)<br>Pós-Graduação em IA, Machine Learning & Data Science · Pós-Graduação em Ciência de Dados & Big Data<br>Análise e Desenvolvimento de Sistemas · FACINT Maringá",
        "footer_links": "📍 Brasil · Chile · Argentina",
    },
 
    "es": {
        "page_title": "Síndrome de Colapso de Colonias · Brasil",
        "hero_tag": "TFG · FATEC Jundiaí · Gestión Ambiental · 2022",
        "hero_title": "Síndrome de Colapso\nde Colonias de Abejas",
        "hero_subtitle": "Análisis de la mortalidad de abejas por compuestos químicos agrícolas y eventos climáticos en 3 regiones brasileñas (2016–2022). Investigación con 338 colmenas y ~20 millones de abejas.",
        "badge1": "🐝 338 Colmenas", "badge2": "~20M Abejas", "badge3": "MG · SP · PR · RS",
        "badge4": "2016 — 2022", "badge5": "FATEC JUNDIAÍ · 3° ENADE",
        "protocol_title": "📋 Nota de Protocolo Científico:",
        "protocol_text": "Los nombres comerciales de los compuestos químicos identificados en esta investigación fueron omitidos a pedido de los productores entrevistados y por precaución legal, sustituidos por categorías técnicas genéricas. Los datos completos están disponibles en el TFG original depositado en FATEC Jundiaí (2022).",
        "m1": "Colmenas perdidas", "m2": "Abejas perdidas (est.)", "m3": "Productores monitoreados", "m4": "Colmenas RS (2024)",
        "tab1": "🗺️ Mapa & Análisis", "tab2": "🔬 Metodología & Pipeline",
        "tab3": "💡 Lo que Descubrimos", "tab4": "📷 En Campo", "tab5": "📚 Fuentes & Créditos",
        "map_label": "VISUALIZACIÓN GEOESPACIAL", "map_title": "Distribución de las Pérdidas en Brasil",
        "map_hint": "🐝 <strong>Interacción:</strong> Haga clic en cualquier marcador del mapa para ver los detalles de la localidad y el radio de forrajeo de 2km de la <em>Apis mellifera</em>.",
        "temporal_label": "ANÁLISIS TEMPORAL", "temporal_title": "Evolución de las Pérdidas por Año",
        "bar_title": "Colmenas perdidas por año (2016–2022)", "bar_y": "Colmenas perdidas",
        "prod_title": "Total por Productor", "pie_title": "Distribución por Categoría de Causa",
        "timeline_label": "LÍNEA DE TIEMPO POR PRODUCTOR", "timeline_title": "Historial Detallado de Eventos",
        "select_producer": "Seleccione el productor",
        "method_label": "INVESTIGACIÓN CIENTÍFICA", "method_title": "Pregunta & Metodología",
        "sci_question_title": "❓ Pregunta Científica Central",
        "sci_question": "\"¿El uso de compuestos químicos agrícolas y vectoriales en las regiones Sur de Minas Gerais, Vale do Paraíba (SP) y Región Central de Paraná está correlacionado con la mortalidad de colonias de abejas entre 2016 y 2022?\"",
        "pipeline_label": "PIPELINE DE DATOS",
        "steps": [
            ("1", "Recolección — Entrevistas de Campo", "Entrevistas con 9 apicultores/meliponicultores vía WhatsApp, Instagram y correo electrónico. Respuesta efectiva de 4 productores (anonimato garantizado por protocolo)."),
            ("2", "Recolección — Revisión Bibliográfica", "Levantamiento de literatura científica sobre CCD (Colony Collapse Disorder), compuestos organofosforados, neonicotinoides y fungicidas. Bases: Google Académico, IBAMA, EMBRAPA, APTA."),
            ("3", "Procesamiento — Tabulación", "Datos de entrevistas tabulados en Microsoft Excel. Cruce con mapa regional del Vale do Paraíba (IBGE 2006) y datos de uso de plaguicidas por municipio (Bombardini, 2017 — FFLCH/USP)."),
            ("4", "Procesamiento — Georreferenciación", "Localidades asociadas a coordenadas geográficas para mapeo con Folium. Cálculo de radios de forrajeo por especie (Jataí: 600m; Apis mellifera: 5km) según EMBRAPA (2021)."),
            ("5", "Análisis — Enfoque Cuali-Cuantitativo", "Método hipotético-deductivo. Análisis descriptivo de pérdidas por año, productor y causa. Cruce entre patrón de mortalidad y patrón de uso de compuestos químicos identificado en la literatura."),
            ("6", "Visualización & Publicación", "Dashboard interactivo desarrollado en Python (Streamlit + Plotly + Folium). Mapeo geoespacial con marcadores proporcionales a las pérdidas."),
        ],
        "species_title": "🐝 Especies y Radios de Forrajeo",
        "species_text": "• <b>Jataí</b> (Tetragonisca angustula): hasta 600m — 1,13 km²<br>• <b>Mandaguari</b> (Scaptotrigona xanthotricha): hasta 900m — 2,54 km²<br>• <b>Mandaçaia</b> (Melipona quadrifasciata): hasta 2.500m — 19,63 km²<br>• <b>Apis mellifera</b>: hasta 5.000m — 78,5 km²",
        "species_source": "Fuente: EMBRAPA, 2021",
        "compounds_title": "⚗️ Categorías de Compuestos Identificados",
        "compounds_text": "• <b>Agente Urbano Vectorial</b>: insecticida organofosforado para control de mosquitos en centros urbanos. Aplicado por vehículos municipales.<br>• <b>Compuesto Herbicida Sistémico</b>: herbicida de amplio espectro en terrenos baldíos. Elimina fuentes de néctar.<br>• <b>Insecticida de Monocultivo</b>: defensivo agrícola en cultivos de soja y maíz próximos a apiarios.",
        "compounds_note": "Nombres comerciales omitidos — ver nota de protocolo al inicio de la página",
        "discovery_label": "RESULTADOS DE LA INVESTIGACIÓN", "discovery_title": "Lo que los Datos Revelaron",
        "discoveries": [
            ("🔴", "Pico de mortalidad en 2019", "El Productor D (PR) perdió 300 colmenas en un solo año — aproximadamente 18 millones de abejas. El evento fue asociado a la pulverización de insecticida en plantación de monocultivo adyacente. Representa el 88,9% de todas las pérdidas registradas en el período 2016-2022."),
            ("🟠", "Subnotificación sistémica identificada", "De los 9 productores contactados, solo 4 respondieron. El principal obstáculo fue el temor a represalias: el 62,5% de las pérdidas nunca fueron comunicadas a órganos competentes (GEDAVE, Policía Ambiental)."),
            ("🟡", "Ambiente urbano como vector de riesgo", "El Productor A (MG) fue afectado 3 veces en 7 años por el agente vectorial municipal de control de mosquitos. El 50% de los apiarios afectados estaban próximos a bosque nativo — no a cultivos — indicando contaminación por deriva a distancias superiores a 1km."),
            ("🟢", "Subregistro en el sistema oficial", "Ningún dato oficial había sido publicado sobre mortalidad de abejas en el Vale do Paraíba antes de esta investigación. El primer relevamiento vía formulario Google (Alves, 2022) confirmó mortalidad creciente entre 2015-2022."),
            ("🔵", "Inundaciones de RS amplifican el escenario (2024)", "Las inundaciones de mayo/junio de 2024 en Rio Grande do Sul devastaron más de 6.300 colmenas, añadiendo eventos climáticos extremos como nuevo vector de riesgo para la apicultura brasileña."),
        ],
        "conclusion_label": "CONCLUSIÓN CIENTÍFICA",
        "conclusion_title": "Confirmación de la Hipótesis",
        "conclusion_text": "El uso de compuestos químicos agrícolas y vectoriales fue confirmado como principal causa de la mortalidad de colonias de abejas en las regiones estudiadas. Los datos corroboran la hipótesis de que Brasil — mayor consumidor mundial de plaguicidas — enfrenta un proceso de Síndrome de Colapso de Colonias (CCD) regionalmente distribuido.",
        "conclusion_author": "Amauri Almeida — TFG Gestión Ambiental, FATEC Jundiaí, 2022",
        "impact_title": "Abejas perdidas por evento (escala logarítmica)",
        "field_label": "INVESTIGACIÓN APLICADA", "field_title": "La Investigación que Salió de la Pantalla",
        "photos": [
            {"emoji": "🏛️", "titulo": "Museo de las Abejas — Cotia / Embu das Artes, SP", "desc": "Visita al Museo de las Abejas. Colmena de Apis mellifera en exposición — especie central de esta investigación.", "path": "assets/foto_01_museu_apis.jpg", "legenda": "Colmena de Apis mellifera · Museo de las Abejas · Cotia / Embu das Artes, SP"},
            {"emoji": "💀", "titulo": "Abejas Muertas — Guaratinguetá, SP · Oct/2021", "desc": "Abejas muertas en apiario localizado en el municipio de Guaratinguetá, octubre de 2021. Evidencia directa del evento de colapso registrado en esta investigación.", "path": "assets/foto_02_mortas_guaratingueta.jpg", "legenda": "Abejas muertas en Guaratinguetá · Oct/2021 · Foto: J.F.A."},
            {"emoji": "🗺️", "titulo": "El Mundo de las Abejas — Mapa Interactivo de la Vida", "desc": "Panel interactivo del Museo de las Abejas con el resumen completo del ciclo de vida de las abejas.", "path": "assets/foto_03_museu_mapa_vida.jpg", "legenda": "Mapa interactivo del ciclo de vida · Museo de las Abejas · SP"},
            {"emoji": "🌻", "titulo": "Apis mellifera en Girasol — FATEC Jundiaí", "desc": "Abeja Apis mellifera en girasol en el jardín de la FATEC Jundiaí, donde se defendió el TFG y se completó la Graduación en Gestión Ambiental.", "path": "assets/foto_04_apis_girassol_fatec.jpg", "legenda": "Apis mellifera en girasol · Jardín de la FATEC Jundiaí · SP"},
            {"emoji": "🔬", "titulo": "El Mundo de las Abejas — Anatomía", "desc": "Panel del Museo de las Abejas con mapa detallado de la anatomía de las abejas.", "path": "assets/foto_05_museu_anatomia.jpg", "legenda": "Mapa de anatomía de las abejas · Museo de las Abejas · SP"},
            {"emoji": "🏺", "titulo": "Pintura Rupestre — 500 a.C. · Recolección de Miel", "desc": "Pintura rupestre de 500 a.C. mostrando personas recolectando miel.", "path": "assets/foto_06_rupestre_500ac.jpg", "legenda": "Pintura rupestre · 500 a.C. · Relación humana con abejas"},
            {"emoji": "🌍", "titulo": "Cazador de Miel — Rodesia, Sudáfrica · 8.000 años", "desc": "Panel retratando un Cazador de Miel en Rodesia (actual Zimbabue), África del Sur. Arte datado de aproximadamente 8.000 años.", "path": "assets/foto_07_cacador_mel_rodesia.jpg", "legenda": "Cazador de Miel · Rodesia, Sudáfrica · ~8.000 años"},
            {"emoji": "🪨", "titulo": "Pintura Rupestre — Castellón, España · +10.000 años", "desc": "Pintura rupestre descubierta en Castellón, España. Dibujo paleolítico de más de 10.000 años que representa la recolección de miel.", "path": "assets/foto_08_rupestre_castellon.jpg", "legenda": "Dibujo paleolítico · Castellón, España · +10.000 años"},
        ],
        "field_instrucoes_title": "📌 Cómo añadir las fotos al proyecto",
        "field_instrucoes": "Cree una carpeta <code>assets/</code> en la raíz del proyecto Streamlit y suba las fotos con los nombres exactos que aparecen debajo de cada tarjeta.",
        "timeline_field_label": "CONTEXTO DE LAS ENTREVISTAS",
        "timeline_field_items": [
            ("Abr 2022", "Entrevista Productor A", "Sur de Minas Gerais · WhatsApp y correo · Apiario próximo a área residencial afectado por agente vectorial municipal"),
            ("Abr 2022", "Entrevista Productor B", "Vale do Paraíba, SP · Instagram y correo · Apiario próximo a terrenos con herbicida sistémico"),
            ("May 2022", "Entrevista Productor C", "Región Central de Paraná · Instagram y correo · Gran apiario próximo a monocultivo"),
            ("Jun 2022", "Entrevista Productor D", "Región Central de Paraná · Instagram y correo · Mayor pérdida individual: 300 colmenas en 2019"),
            ("Jun 2022", "Defensa del TFG", "FATEC Jundiaí, SP · Orientador: Prof. Me. Claudio da Cunha · Gestión Ambiental"),
            ("Oct 2021", "Visita al Museo de las Abejas", "Cotia / Embu das Artes, SP · Registros fotográficos y referencias científicas para el TFG"),
        ],
        "sources_label": "REFERENCIAS CIENTÍFICAS", "sources_title": "Fuentes & Base de Datos",
        "tech_label": "TECNOLOGÍAS UTILIZADAS",
        "footer_title": "🐝 Amauri Almeida",
        "footer_desc": "Tecnólogo en Gestión Ambiental · FATEC Jundiaí (3° ENADE)<br>Posgrado en IA, Machine Learning & Data Science · Posgrado en Ciencia de Datos & Big Data<br>Análisis y Desarrollo de Sistemas · FACINT Maringá",
        "footer_links": "📍 Brasil · Chile · Argentina",
    },
 
    "en": {
        "page_title": "Colony Collapse Disorder · Brazil",
        "hero_tag": "Thesis · FATEC Jundiaí · Environmental Management · 2022",
        "hero_title": "Colony Collapse\nDisorder in Brazil",
        "hero_subtitle": "Analysis of bee mortality from agricultural chemical compounds and climate events across 3 Brazilian regions (2016–2022). Research covering 338 hives and ~20 million bees.",
        "badge1": "🐝 338 Hives", "badge2": "~20M Bees", "badge3": "MG · SP · PR · RS",
        "badge4": "2016 — 2022", "badge5": "FATEC JUNDIAÍ · 3rd ENADE",
        "protocol_title": "📋 Scientific Protocol Note:",
        "protocol_text": "Commercial names of the chemical compounds identified in this research have been omitted at the request of interviewed producers and for legal caution, replaced by generic technical categories. Full data are available in the original thesis deposited at FATEC Jundiaí (2022).",
        "m1": "Hives lost", "m2": "Bees lost (est.)", "m3": "Producers monitored", "m4": "RS hives (2024)",
        "tab1": "🗺️ Map & Analysis", "tab2": "🔬 Methodology & Pipeline",
        "tab3": "💡 What We Found", "tab4": "📷 Field Research", "tab5": "📚 Sources & Credits",
        "map_label": "GEOSPATIAL VISUALIZATION", "map_title": "Loss Distribution in Brazil",
        "map_hint": "🐝 <strong>Interaction:</strong> Click any marker to see locality details and the 2km foraging radius of <em>Apis mellifera</em>.",
        "temporal_label": "TEMPORAL ANALYSIS", "temporal_title": "Loss Evolution by Year",
        "bar_title": "Hives lost per year (2016–2022)", "bar_y": "Hives lost",
        "prod_title": "Total by Producer", "pie_title": "Distribution by Cause Category",
        "timeline_label": "TIMELINE BY PRODUCER", "timeline_title": "Detailed Event History",
        "select_producer": "Select producer",
        "method_label": "SCIENTIFIC RESEARCH", "method_title": "Question & Methodology",
        "sci_question_title": "❓ Central Scientific Question",
        "sci_question": "\"Is the use of agricultural and urban chemical compounds in Southern Minas Gerais, Vale do Paraíba (SP) and Central Paraná correlated with bee colony mortality between 2016 and 2022?\"",
        "pipeline_label": "DATA PIPELINE",
        "steps": [
            ("1", "Collection — Field Interviews", "Interviews with 9 beekeepers via WhatsApp, Instagram and email. Effective response from 4 producers (anonymity guaranteed by protocol). Identified as Producer A (MG), B (SP), C and D (PR)."),
            ("2", "Collection — Literature Review", "Scientific literature survey on CCD (Colony Collapse Disorder), organophosphates, neonicotinoids and fungicides. Databases: Google Scholar, IBAMA, EMBRAPA, APTA."),
            ("3", "Processing — Tabulation", "Interview data tabulated in Microsoft Excel. Cross-referenced with regional map of Vale do Paraíba (IBGE 2006) and pesticide use data by municipality (Bombardini, 2017 — FFLCH/USP)."),
            ("4", "Processing — Georeferencing", "Localities associated with geographic coordinates for Folium mapping. Foraging radius calculations by species (Jataí: 600m; Apis mellifera: 5km) per EMBRAPA (2021)."),
            ("5", "Analysis — Quali-Quantitative Approach", "Hypothetical-deductive method. Descriptive analysis of losses by year, producer and cause. Cross-referencing between mortality patterns and chemical compound use patterns from literature (RT25/RT40 — IBAMA 2012)."),
            ("6", "Visualization & Publication", "Interactive dashboard developed in Python (Streamlit + Plotly + Folium). Geospatial mapping with markers proportional to losses."),
        ],
        "species_title": "🐝 Species and Foraging Radii",
        "species_text": "• <b>Jataí</b> (Tetragonisca angustula): up to 600m — 1.13 km²<br>• <b>Mandaguari</b> (Scaptotrigona xanthotricha): up to 900m — 2.54 km²<br>• <b>Mandaçaia</b> (Melipona quadrifasciata): up to 2,500m — 19.63 km²<br>• <b>Apis mellifera</b>: up to 5,000m — 78.5 km²",
        "species_source": "Source: EMBRAPA, 2021",
        "compounds_title": "⚗️ Identified Compound Categories",
        "compounds_text": "• <b>Urban Vector Agent</b>: organophosphate insecticide used for mosquito control in urban centers. Applied by municipal vehicles.<br>• <b>Systemic Herbicide Compound</b>: broad-spectrum herbicide used on vacant lots and property edges. Eliminates nectar sources.<br>• <b>Monoculture Insecticide</b>: agricultural pesticide used on soy and corn crops near apiaries. Direct contact via spray drift.",
        "compounds_note": "Commercial names omitted — see protocol note at the top of the page",
        "discovery_label": "RESEARCH RESULTS", "discovery_title": "What the Data Revealed",
        "discoveries": [
            ("🔴", "Mortality peak in 2019", "Producer D (PR) lost 300 hives in a single year — approximately 18 million bees. The event was linked to insecticide spraying on an adjacent monoculture plantation. Represents 88.9% of all losses recorded in 2016-2022."),
            ("🟠", "Systemic underreporting identified", "Of 9 producers contacted, only 4 responded. The main obstacle was fear of retaliation: 62.5% of losses were never reported to competent authorities (GEDAVE, Environmental Police)."),
            ("🟡", "Urban environment as risk vector", "Producer A (MG) was affected 3 times in 7 years by the municipal mosquito control vector agent. 50% of affected apiaries were near native forest — not crops — indicating contamination by drift at distances over 1km."),
            ("🟢", "Underregistration in official systems", "No official national data had been published on bee mortality in Vale do Paraíba before this research. The pioneering Google Forms survey (Alves, 2022) confirmed growing mortality between 2015-2022 with no prior academic record."),
            ("🔵", "RS floods amplify the scenario (2024)", "The May/June 2024 floods in Rio Grande do Sul devastated more than 6,300 hives, adding extreme climate events as a new risk vector for Brazilian beekeeping."),
        ],
        "conclusion_label": "SCIENTIFIC CONCLUSION",
        "conclusion_title": "Hypothesis Confirmed",
        "conclusion_text": "The use of agricultural and urban chemical compounds was confirmed as the main cause of bee colony mortality in the studied regions. The data corroborate the hypothesis that Brazil — the world's largest pesticide consumer — faces a regionally distributed Colony Collapse Disorder (CCD) process, aggravated by the absence of official reporting systems and fear of retaliation that inhibits loss reporting.",
        "conclusion_author": "Amauri Almeida — Environmental Management Thesis, FATEC Jundiaí, 2022",
        "impact_title": "Bees lost by event (logarithmic scale)",
        "field_label": "APPLIED RESEARCH", "field_title": "Research That Left the Screen",
        "photos": [
            {"emoji": "🏛️", "titulo": "Bee Museum — Cotia / Embu das Artes, SP", "desc": "Visit to the Bee Museum. Apis mellifera hive on display — the central species of this research.", "path": "assets/foto_01_museu_apis.jpg", "legenda": "Apis mellifera hive · Bee Museum · Cotia / Embu das Artes, SP"},
            {"emoji": "💀", "titulo": "Dead Bees — Guaratinguetá, SP · Oct/2021", "desc": "Dead bees in an apiary located in Guaratinguetá municipality, October 2021. Direct evidence of the collapse event recorded in this research.", "path": "assets/foto_02_mortas_guaratingueta.jpg", "legenda": "Dead bees in Guaratinguetá · Oct/2021 · Photo: J.F.A."},
            {"emoji": "🗺️", "titulo": "The World of Bees — Interactive Life Map", "desc": "Interactive panel at the Bee Museum with a complete summary of the bee life cycle. Educational reference used in the thesis.", "path": "assets/foto_03_museu_mapa_vida.jpg", "legenda": "Interactive life cycle map · Bee Museum · SP"},
            {"emoji": "🌻", "titulo": "Apis mellifera on Sunflower — FATEC Jundiaí", "desc": "Apis mellifera bee on sunflower in the FATEC Jundiaí garden, where the thesis was defended and the Environmental Management degree completed (3rd ENADE).", "path": "assets/foto_04_apis_girassol_fatec.jpg", "legenda": "Apis mellifera on sunflower · FATEC Jundiaí garden · SP"},
            {"emoji": "🔬", "titulo": "The World of Bees — Anatomy", "desc": "Bee Museum panel with detailed map of bee anatomy. Morphological reference used to characterize the species studied.", "path": "assets/foto_05_museu_anatomia.jpg", "legenda": "Bee anatomy map · Bee Museum · SP"},
            {"emoji": "🏺", "titulo": "Cave Painting — 500 BC · Honey Gathering", "desc": "Cave painting from 500 BC showing people collecting honey. The human relationship with bees is documented for millennia.", "path": "assets/foto_06_rupestre_500ac.jpg", "legenda": "Cave painting · 500 BC · Human relationship with bees"},
            {"emoji": "🌍", "titulo": "Honey Hunter — Rhodesia, South Africa · 8,000 years", "desc": "Panel depicting a Honey Hunter in Rhodesia (now Zimbabwe), South Africa. Art dated to approximately 8,000 years ago.", "path": "assets/foto_07_cacador_mel_rodesia.jpg", "legenda": "Honey Hunter · Rhodesia, South Africa · ~8,000 years"},
            {"emoji": "🪨", "titulo": "Cave Painting — Castellón, Spain · +10,000 years", "desc": "Cave painting discovered in Castellón, Spain. Paleolithic drawing over 10,000 years old depicting honey collection — one of the earliest human depictions of beekeeping.", "path": "assets/foto_08_rupestre_castellon.jpg", "legenda": "Paleolithic drawing · Castellón, Spain · +10,000 years"},
        ],
        "field_instrucoes_title": "📌 How to add photos to the project",
        "field_instrucoes": "Create an <code>assets/</code> folder in the Streamlit project root and upload photos with the exact names shown below each card.",
        "timeline_field_label": "INTERVIEW CONTEXT",
        "timeline_field_items": [
            ("Apr 2022", "Interview Producer A", "Southern Minas Gerais · WhatsApp and email · Apiary near residential area affected by municipal vector agent"),
            ("Apr 2022", "Interview Producer B", "Vale do Paraíba, SP · Instagram and email · Apiary near lots with systemic herbicide"),
            ("May 2022", "Interview Producer C", "Central Paraná · Instagram and email · Large apiary near monoculture"),
            ("Jun 2022", "Interview Producer D", "Central Paraná · Instagram and email · Largest individual loss: 300 hives in 2019"),
            ("Jun 2022", "Thesis Defense", "FATEC Jundiaí, SP · Advisor: Prof. Me. Claudio da Cunha · Environmental Management"),
            ("Oct 2021", "Bee Museum Visit", "Cotia / Embu das Artes, SP · Photographic records and scientific references for the thesis"),
        ],
        "sources_label": "SCIENTIFIC REFERENCES", "sources_title": "Sources & Database",
        "tech_label": "TECHNOLOGIES USED",
        "footer_title": "🐝 Amauri Almeida",
        "footer_desc": "Environmental Management Technologist · FATEC Jundiaí (3rd ENADE)<br>Post-Grad in AI, Machine Learning & Data Science · Post-Grad in Data Science & Big Data<br>Systems Analysis and Development · FACINT Maringá",
        "footer_links": "📍 Brazil · Chile · Argentina",
    },
}
 
# ============================================================
# SELETOR DE IDIOMA — TOPO
# ============================================================
def render_lang_selector():
    col_space, col_pt, col_es, col_en = st.columns([8, 1, 1, 1])
    with col_pt:
        if st.button("🇧🇷 PT", use_container_width=True,
                     type="primary" if st.session_state.lang == "pt" else "secondary"):
            st.session_state.lang = "pt"
            st.rerun()
    with col_es:
        if st.button("🇪🇸 ES", use_container_width=True,
                     type="primary" if st.session_state.lang == "es" else "secondary"):
            st.session_state.lang = "es"
            st.rerun()
    with col_en:
        if st.button("🇺🇸 EN", use_container_width=True,
                     type="primary" if st.session_state.lang == "en" else "secondary"):
            st.session_state.lang = "en"
            st.rerun()
 
render_lang_selector()
T = TRANSLATIONS[st.session_state.lang]
 
# ============================================================
# ESTILOS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&family=DM+Mono&display=swap');
:root{--honey:#F5A623;--honey-dark:#C47D0E;--forest:#1A3A2A;--forest-mid:#2D5A3D;--forest-light:#3D7A52;--cream:#FDF8F0;--warm-gray:#8C7B6B;--danger:#C0392B;--danger-soft:#F8D7DA;--black:#0D1117;}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background-color:var(--cream);color:var(--black);}
.hero-wrap{background:linear-gradient(135deg,var(--forest) 0%,var(--forest-mid) 60%,#1E4D30 100%);border-radius:20px;padding:3rem 2.5rem 2rem;margin-bottom:2rem;position:relative;overflow:hidden;}
.hero-wrap::before{content:"🐝";font-size:180px;position:absolute;right:-20px;top:-20px;opacity:0.06;}
.hero-tag{background:var(--honey);color:var(--forest);font-family:'DM Mono',monospace;font-size:0.7rem;font-weight:bold;letter-spacing:2px;padding:4px 12px;border-radius:4px;display:inline-block;margin-bottom:1rem;text-transform:uppercase;}
.hero-title{font-family:'Playfair Display',serif;font-size:2.8rem;font-weight:900;color:#fff;line-height:1.15;margin-bottom:0.8rem;white-space:pre-line;}
.hero-subtitle{font-size:1rem;color:rgba(255,255,255,0.75);max-width:600px;line-height:1.6;margin-bottom:1.5rem;}
.hero-badges{display:flex;gap:10px;flex-wrap:wrap;}
.badge{background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.85);font-size:0.72rem;font-family:'DM Mono',monospace;padding:5px 12px;border-radius:20px;letter-spacing:0.5px;}
.badge-honey{background:rgba(245,166,35,0.2);border-color:var(--honey);color:var(--honey);}
.metric-box{background:white;border-radius:16px;padding:1.4rem 1.2rem;border-top:4px solid var(--honey);box-shadow:0 2px 12px rgba(0,0,0,0.06);text-align:center;}
.metric-box.danger{border-top-color:var(--danger);}
.metric-box.forest{border-top-color:var(--forest-light);}
.metric-val{font-family:'Playfair Display',serif;font-size:2.1rem;font-weight:900;color:var(--forest);line-height:1;margin-bottom:0.3rem;}
.metric-label{font-size:0.75rem;color:var(--warm-gray);text-transform:uppercase;letter-spacing:1px;}
.section-label{font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--honey-dark);text-transform:uppercase;letter-spacing:3px;margin-bottom:0.3rem;}
.section-title{font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:700;color:var(--forest);margin-bottom:1.2rem;line-height:1.2;}
.info-card{background:white;border-radius:16px;padding:1.5rem;box-shadow:0 2px 12px rgba(0,0,0,0.05);border-left:4px solid var(--forest-light);margin-bottom:1rem;}
.info-card.honey{border-left-color:var(--honey);}
.info-card.danger{border-left-color:var(--danger);}
.timeline-item{display:flex;gap:1rem;padding:1rem 0;border-bottom:1px solid #f0ebe2;}
.timeline-year{font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;color:var(--honey);min-width:70px;}
.timeline-content{flex:1;}
.timeline-title{font-weight:500;color:var(--forest);margin-bottom:0.2rem;}
.timeline-desc{font-size:0.85rem;color:var(--warm-gray);}
.source-badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:0.8rem;}
.source-badge{background:var(--forest);color:white;font-family:'DM Mono',monospace;font-size:0.65rem;padding:4px 10px;border-radius:4px;letter-spacing:1px;text-transform:uppercase;}
.method-step{display:flex;align-items:flex-start;gap:1rem;padding:1rem;background:white;border-radius:12px;margin-bottom:0.8rem;box-shadow:0 1px 6px rgba(0,0,0,0.04);}
.step-num{background:var(--honey);color:white;font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.step-content{flex:1;}
.step-title{font-weight:500;color:var(--forest);font-size:0.95rem;}
.step-desc{font-size:0.82rem;color:var(--warm-gray);margin-top:0.2rem;}
.discovery-box{background:linear-gradient(135deg,#FFF9F0 0%,#FFF3DC 100%);border:2px solid var(--honey);border-radius:16px;padding:1.8rem;margin:1rem 0;}
.discovery-title{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:var(--forest);margin-bottom:0.5rem;}
.footer-wrap{background:var(--forest);border-radius:20px;padding:2rem;color:rgba(255,255,255,0.8);text-align:center;margin-top:3rem;}
.footer-title{font-family:'Playfair Display',serif;color:var(--honey);font-size:1.2rem;margin-bottom:0.5rem;}
.alert-box{background:var(--danger-soft);border-left:4px solid var(--danger);border-radius:8px;padding:1rem 1.2rem;margin:1rem 0;font-size:0.9rem;}
.photo-card{background:white;border-radius:16px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.08);margin-bottom:1rem;}
.photo-placeholder{background:#f0ebe2;border:2px dashed var(--honey-dark);border-radius:12px;padding:2rem;text-align:center;min-height:180px;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.photo-emoji{font-size:2.5rem;}
.photo-title{font-weight:600;color:var(--forest);margin:0.5rem 0 0.2rem;font-size:0.9rem;}
.photo-desc{font-size:0.78rem;color:var(--warm-gray);line-height:1.5;}
.photo-path{font-size:0.65rem;color:var(--honey-dark);font-family:'DM Mono',monospace;margin-top:0.5rem;}
.photo-legenda{font-size:0.72rem;color:var(--warm-gray);font-style:italic;padding:0.5rem 0.8rem;background:#faf7f2;text-align:center;}
</style>
""", unsafe_allow_html=True)
 
# ============================================================
# DADOS
# ============================================================
dados_produtores = [
    {"produtor": "Produtor A", "localidade": "Extrema - MG", "lat": -22.8514, "lon": -46.3178, "regiao": "Sul de Minas Gerais", "tipo": "Meliponicultor",
     "historico": [{"ano": 2016, "colmeias": 1, "abelhas": 1400, "causa": "Agente_urbano_vetorial"}, {"ano": 2017, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2018, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2019, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2020, "colmeias": 1, "abelhas": 3000, "causa": "Agente_urbano_vetorial"}, {"ano": 2021, "colmeias": 1, "abelhas": 3600, "causa": "Agente_urbano_vetorial"}, {"ano": 2022, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}]},
    {"produtor": "Produtor B", "localidade": "Guaratinguetá - SP", "lat": -22.8078, "lon": -45.1936, "regiao": "Vale do Paraíba - SP", "tipo": "Apicultor",
     "historico": [{"ano": 2016, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2017, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2018, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2019, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2020, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2021, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2022, "colmeias": 5, "abelhas": 300000, "causa": "Composto_herbicida_sistêmico"}]},
    {"produtor": "Produtor C", "localidade": "Turvo - PR", "lat": -25.0433, "lon": -51.5286, "regiao": "Região Central do Paraná", "tipo": "Apicultor",
     "historico": [{"ano": 2016, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2017, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2018, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2019, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2020, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2021, "colmeias": 30, "abelhas": 1800000, "causa": "Inseticida_monocultura"}, {"ano": 2022, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}]},
    {"produtor": "Produtor D", "localidade": "Prudentópolis - PR", "lat": -25.2133, "lon": -50.9775, "regiao": "Região Central do Paraná", "tipo": "Apicultor",
     "historico": [{"ano": 2016, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2017, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2018, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2019, "colmeias": 300, "abelhas": 18000000, "causa": "Inseticida_monocultura"}, {"ano": 2020, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2021, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}, {"ano": 2022, "colmeias": 0, "abelhas": 0, "causa": "Sem perdas"}]},
]
dados_rs = [
    {"localidade": "Porto Alegre - RS", "lat": -30.0331, "lon": -51.2300, "colmeias": 2500},
    {"localidade": "Canoas - RS", "lat": -29.9200, "lon": -51.1800, "colmeias": 1500},
    {"localidade": "Cachoeirinha - RS", "lat": -29.9300, "lon": -51.0900, "colmeias": 750},
    {"localidade": "Eldorado do Sul - RS", "lat": -30.0800, "lon": -51.3100, "colmeias": 800},
    {"localidade": "Encantado - RS", "lat": -29.2400, "lon": -51.8700, "colmeias": 300},
]
df_list = []
for p in dados_produtores:
    for h in p['historico']:
        if h['colmeias'] > 0:
            df_list.append({"produtor": p['produtor'], "localidade": p['localidade'], "lat": p['lat'], "lon": p['lon'], "regiao": p['regiao'], "tipo": p['tipo'], "ano": h['ano'], "colmeias": h['colmeias'], "abelhas": h['abelhas'], "causa": h['causa']})
df_perdas = pd.DataFrame(df_list)
cores_causa = {"Agente_urbano_vetorial": "#E67E22", "Composto_herbicida_sistêmico": "#C0392B", "Inseticida_monocultura": "#8E44AD"}
 
# ============================================================
# HERO
# ============================================================
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-tag">{T['hero_tag']}</div>
    <div class="hero-title">{T['hero_title']}</div>
    <div class="hero-subtitle">{T['hero_subtitle']}</div>
    <div class="hero-badges">
        <span class="badge badge-honey">{T['badge1']}</span>
        <span class="badge badge-honey">{T['badge2']}</span>
        <span class="badge">{T['badge3']}</span>
        <span class="badge">{T['badge4']}</span>
        <span class="badge">{T['badge5']}</span>
    </div>
</div>
""", unsafe_allow_html=True)
 
st.markdown(f"""<div class="alert-box"><strong>{T['protocol_title']}</strong> {T['protocol_text']}</div>""", unsafe_allow_html=True)
 
col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown(f'<div class="metric-box danger"><div class="metric-val">338</div><div class="metric-label">{T["m1"]}</div></div>', unsafe_allow_html=True)
with col2: st.markdown(f'<div class="metric-box danger"><div class="metric-val">~20M</div><div class="metric-label">{T["m2"]}</div></div>', unsafe_allow_html=True)
with col3: st.markdown(f'<div class="metric-box"><div class="metric-val">4</div><div class="metric-label">{T["m3"]}</div></div>', unsafe_allow_html=True)
with col4: st.markdown(f'<div class="metric-box forest"><div class="metric-val">6.300+</div><div class="metric-label">{T["m4"]}</div></div>', unsafe_allow_html=True)
 
st.markdown("<br>", unsafe_allow_html=True)
 
# ============================================================
# ABAS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([T['tab1'], T['tab2'], T['tab3'], T['tab4'], T['tab5']])
 
# ── TAB 1: MAPA ──────────────────────────────────────────────
with tab1:
    st.markdown(f'<div class="section-label">{T["map_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["map_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card honey">{T["map_hint"]}</div>', unsafe_allow_html=True)
 
    mapa = folium.Map(location=[-23.5, -50.5], zoom_start=6, tiles='CartoDB positron')
    for p in dados_produtores:
        for h in p['historico']:
            if h['colmeias'] > 0:
                raio = max(8, min(45, h['colmeias'] / 8))
                cor = cores_causa.get(h['causa'], "#F5A623")
                popup_html = f"<div style='font-family:sans-serif;min-width:200px;padding:8px'><h4 style='color:#1A3A2A;margin:0 0 6px'>{p['produtor']}</h4><p style='margin:2px 0;font-size:13px'>📍 {p['localidade']}</p><p style='margin:2px 0;font-size:13px'>📅 {h['ano']}</p><p style='margin:2px 0;font-size:13px'>🏠 {h['colmeias']:,}</p><p style='margin:2px 0;font-size:13px'>🐝 {h['abelhas']:,}</p></div>"
                folium.CircleMarker(location=[p['lat'], p['lon']], radius=raio, color=cor, fill=True, fill_color=cor, fill_opacity=0.6, popup=folium.Popup(popup_html, max_width=250), tooltip=f"🐝 {p['produtor']} — {h['ano']}: {h['colmeias']} colmeias").add_to(mapa)
                folium.Circle(location=[p['lat'], p['lon']], radius=2000, color="#F5A623", fill=False, weight=1, dash_array='5 5', opacity=0.4).add_to(mapa)
    for r in dados_rs:
        folium.CircleMarker(location=[r['lat'], r['lon']], radius=max(8, min(50, r['colmeias'] / 60)), color='#2980B9', fill=True, fill_color='#2980B9', fill_opacity=0.5, tooltip=f"🌊 {r['localidade']}: {r['colmeias']}").add_to(mapa)
    folium_static(mapa, width=1100, height=520)
 
    st.markdown(f"<br><div class='section-label'>{T['temporal_label']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>{T['temporal_title']}</div>", unsafe_allow_html=True)
 
    perdas_ano = df_perdas.groupby('ano').agg({'colmeias': 'sum'}).reset_index()
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=perdas_ano['ano'], y=perdas_ano['colmeias'], marker=dict(color=perdas_ano['colmeias'], colorscale=[[0,'#FDF8F0'],[0.3,'#F5A623'],[0.7,'#C0392B'],[1,'#8E1515']], line=dict(width=0)), text=perdas_ano['colmeias'], textposition='outside', hovertemplate='<b>%{x}</b><br>%{y}<extra></extra>'))
    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family='DM Sans'), height=360, xaxis=dict(showgrid=False, tickfont=dict(size=13)), yaxis=dict(showgrid=True, gridcolor='#f0ebe2', title=T['bar_y']), title=dict(text=T['bar_title'], font=dict(size=15, family='Playfair Display')), margin=dict(t=50,b=20))
    st.plotly_chart(fig_bar, use_container_width=True)
 
    col_a, col_b = st.columns(2)
    with col_a:
        fig_prod = px.bar(df_perdas.groupby('produtor')['colmeias'].sum().reset_index(), x='produtor', y='colmeias', title=T['prod_title'], color='colmeias', color_continuous_scale='Oranges', text='colmeias')
        fig_prod.update_traces(textposition='outside')
        fig_prod.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, height=340, coloraxis_showscale=False, font=dict(family='DM Sans'), title=dict(font=dict(size=14, family='Playfair Display')), margin=dict(t=50,b=20))
        st.plotly_chart(fig_prod, use_container_width=True)
    with col_b:
        causa_resumo = df_perdas.groupby('causa')['colmeias'].sum().reset_index()
        causa_map = {"Agente_urbano_vetorial": "Agente Urbano Vetorial", "Composto_herbicida_sistêmico": "Composto Herbicida", "Inseticida_monocultura": "Inseticida Monocultura"}
        causa_resumo['causa_label'] = causa_resumo['causa'].map(causa_map)
        fig_pie = px.pie(causa_resumo, values='colmeias', names='causa_label', title=T['pie_title'], color_discrete_sequence=['#F5A623','#C0392B','#8E44AD'])
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=340, font=dict(family='DM Sans'), title=dict(font=dict(size=14, family='Playfair Display')), margin=dict(t=50,b=20))
        st.plotly_chart(fig_pie, use_container_width=True)
 
    st.markdown(f"<div class='section-label'>{T['timeline_label']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>{T['timeline_title']}</div>", unsafe_allow_html=True)
    produtor_sel = st.selectbox(T['select_producer'], [p['produtor'] for p in dados_produtores])
    p_data = next(p for p in dados_produtores if p['produtor'] == produtor_sel)
    anos_p = [h['ano'] for h in p_data['historico']]
    colmeias_p = [h['colmeias'] for h in p_data['historico']]
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=anos_p, y=colmeias_p, mode='lines+markers', line=dict(color='#F5A623', width=3), marker=dict(size=10, color=['#C0392B' if c > 0 else '#3D7A52' for c in colmeias_p], line=dict(width=2, color='white')), fill='tozeroy', fillcolor='rgba(245,166,35,0.1)', hovertemplate='<b>%{x}</b><br>%{y}<extra></extra>'))
    fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280, font=dict(family='DM Sans'), xaxis=dict(showgrid=False, tickmode='array', tickvals=anos_p), yaxis=dict(showgrid=True, gridcolor='#f0ebe2'), title=dict(text=f"{produtor_sel} — {p_data['localidade']}", font=dict(size=14, family='Playfair Display')), margin=dict(t=50,b=20))
    st.plotly_chart(fig_line, use_container_width=True)
 
# ── TAB 2: METODOLOGIA ────────────────────────────────────────
with tab2:
    st.markdown(f'<div class="section-label">{T["method_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["method_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="discovery-box"><div class="discovery-title">{T["sci_question_title"]}</div><p style="font-size:1.05rem;color:#2D5A3D;line-height:1.7"><em>{T["sci_question"]}</em></p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-label" style="margin-top:1.5rem">{T["pipeline_label"]}</div>', unsafe_allow_html=True)
    for num, title, desc in T['steps']:
        st.markdown(f'<div class="method-step"><div class="step-num">{num}</div><div class="step-content"><div class="step-title">{title}</div><div class="step-desc">{desc}</div></div></div>', unsafe_allow_html=True)
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f'<div class="info-card"><strong>{T["species_title"]}</strong><br><br><div style="font-size:0.88rem;line-height:2">{T["species_text"]}</div><div style="font-size:0.78rem;color:#8C7B6B;margin-top:0.5rem">{T["species_source"]}</div></div>', unsafe_allow_html=True)
    with col_m2:
        st.markdown(f'<div class="info-card honey"><strong>{T["compounds_title"]}</strong><br><br><div style="font-size:0.88rem;line-height:2">{T["compounds_text"]}</div><div style="font-size:0.78rem;color:#8C7B6B;margin-top:0.5rem">{T["compounds_note"]}</div></div>', unsafe_allow_html=True)
 
# ── TAB 3: DESCOBERTAS ────────────────────────────────────────
with tab3:
    st.markdown(f'<div class="section-label">{T["discovery_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["discovery_title"]}</div>', unsafe_allow_html=True)
    for emoji, titulo, texto in T['discoveries']:
        st.markdown(f'<div class="discovery-box" style="margin-bottom:0.8rem"><div style="display:flex;align-items:flex-start;gap:1rem"><span style="font-size:1.5rem">{emoji}</span><div><div class="discovery-title">{titulo}</div><p style="color:#3D4D3A;line-height:1.65;font-size:0.93rem;margin:0">{texto}</p></div></div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-label" style="margin-top:1.5rem">{T["conclusion_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card" style="border-left-color:#1A3A2A;background:linear-gradient(135deg,#F0F8F3,#E8F4EC)"><strong style="color:#1A3A2A;font-size:1rem">{T["conclusion_title"]}</strong><br><br><p style="color:#2D5A3D;line-height:1.7;font-size:0.93rem">{T["conclusion_text"]}</p><p style="color:#3D7A52;font-size:0.82rem;margin-bottom:0"><em>{T["conclusion_author"]}</em></p></div>', unsafe_allow_html=True)
 
    fig_impact = go.Figure()
    eventos = ["Inseticida\nMonocultura PR\n(2019)", "Inseticida\nMonocultura PR\n(2021)", "Composto\nHerbicida SP\n(2022)", "Agente\nVetorial MG"]
    valores = [18000000, 1800000, 300000, 8000]
    fig_impact.add_trace(go.Bar(y=eventos, x=valores, orientation='h', marker=dict(color=['#C0392B','#C0392B','#8E44AD','#E67E22'], line=dict(width=0)), text=[f"{v/1e6:.1f}M" if v > 100000 else f"{v:,}" for v in valores], textposition='outside', hovertemplate='<b>%{y}</b><br>%{x:,}<extra></extra>'))
    fig_impact.update_layout(title=dict(text=T['impact_title'], font=dict(size=14, family='Playfair Display')), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=340, font=dict(family='DM Sans'), xaxis=dict(type='log', showgrid=True, gridcolor='#f0ebe2'), yaxis=dict(showgrid=False), margin=dict(t=50,b=20,r=80))
    st.plotly_chart(fig_impact, use_container_width=True)
 
# ── TAB 4: EM CAMPO ───────────────────────────────────────────
with tab4:
    st.markdown(f'<div class="section-label">{T["field_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["field_title"]}</div>', unsafe_allow_html=True)
 
    photos = T['photos']
    # Grade 3 colunas
    for row_start in range(0, len(photos), 3):
        row_photos = photos[row_start:row_start+3]
        cols = st.columns(len(row_photos))
        for col, foto in zip(cols, row_photos):
            with col:
                exists = os.path.exists(foto['path'])
                if exists:
                    st.image(foto['path'], use_container_width=True)
                    st.markdown(f'<div class="photo-legenda">{foto["legenda"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="photo-placeholder">
                        <div class="photo-emoji">{foto['emoji']}</div>
                        <div class="photo-title">{foto['titulo']}</div>
                        <div class="photo-desc">{foto['desc']}</div>
                        <div class="photo-path">{foto['path']}</div>
                    </div>
                    <div class="photo-legenda">{foto['legenda']}</div>
                    """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
 
    st.markdown(f'<div class="info-card" style="margin-top:1rem"><strong>{T["field_instrucoes_title"]}</strong><br><div style="font-size:0.88rem;color:#3D4D3A;margin-top:0.5rem">{T["field_instrucoes"]}</div></div>', unsafe_allow_html=True)
 
    # Timeline
    st.markdown(f"<br><div class='section-label'>{T['timeline_field_label']}</div>", unsafe_allow_html=True)
    for data, titulo, desc in T['timeline_field_items']:
        st.markdown(f'<div class="timeline-item"><div class="timeline-year">{data}</div><div class="timeline-content"><div class="timeline-title">{titulo}</div><div class="timeline-desc">{desc}</div></div></div>', unsafe_allow_html=True)
 
# ── TAB 5: FONTES ─────────────────────────────────────────────
with tab5:
    st.markdown(f'<div class="section-label">{T["sources_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["sources_title"]}</div>', unsafe_allow_html=True)
    fontes = [
        ("IBAMA", "Instituto Brasileiro do Meio Ambiente e dos Recursos Naturais Renováveis", "Relatório técnico de pesticidas e efeitos nas abelhas (2012). Dados de uso de agrotóxicos no Brasil.", "#1A3A2A"),
        ("EMBRAPA", "Empresa Brasileira de Pesquisa Agropecuária", "Meliponicultura Urbana (2021). Dados de raio de forrageamento por espécie.", "#2D5A3D"),
        ("APTA", "Agência Paulista de Tecnologia dos Agronegócios", "Síndrome do Colapso das Colônias das abelhas pesquisada pela APTA (2015).", "#3D7A52"),
        ("FFLCH-USP", "Faculdade de Filosofia, Letras e Ciências Humanas – USP", "Bombardini, L.M. (2017) — Geografia do Uso de Agrotóxicos no Brasil.", "#4A8B5E"),
        ("IBGE", "Instituto Brasileiro de Geografia e Estatística", "Mapa regional do Vale do Paraíba (2006).", "#1A3A2A"),
        ("UNITAU", "Universidade de Taubaté — Pós-Graduação em Apicultura e Meliponicultura", "Alves, J.F.G. (2022) — Levantamento de Mortalidade de Abelhas por Agrotóxicos no Vale do Paraíba.", "#2D5A3D"),
        ("FATEC JUNDIAÍ", "Faculdade de Tecnologia de Jundiaí — Centro Paula Souza", "TCC: Almeida, A. (2022) — A Problemática da Síndrome das Colônias de Abelhas. 3º ENADE.", "#C0392B"),
    ]
    for sigla, nome, desc, cor in fontes:
        st.markdown(f'<div class="info-card" style="border-left-color:{cor}"><div style="display:flex;align-items:flex-start;gap:1rem"><div style="background:{cor};color:white;font-family:\'DM Mono\',monospace;font-size:0.65rem;padding:4px 8px;border-radius:4px;white-space:nowrap;flex-shrink:0;margin-top:2px;letter-spacing:1px;font-weight:bold">{sigla}</div><div><div style="font-weight:500;font-size:0.9rem;color:#1A3A2A">{nome}</div><div style="font-size:0.82rem;color:#8C7B6B;margin-top:0.2rem">{desc}</div></div></div></div>', unsafe_allow_html=True)
 
    st.markdown(f"<br><div class='section-label'>{T['tech_label']}</div>", unsafe_allow_html=True)
    techs = ["Python 3.11", "Streamlit", "Plotly", "Folium", "Pandas", "NumPy", "Google Forms"]
    badges_html = "".join([f'<span class="source-badge">{t}</span>' for t in techs])
    st.markdown(f'<div class="source-badges">{badges_html}</div>', unsafe_allow_html=True)
 
    st.markdown(f"""
    <div class="footer-wrap" style="margin-top:2rem">
        <div class="footer-title">{T['footer_title']}</div>
        <p style="margin:0.5rem 0;font-size:0.9rem">{T['footer_desc']}</p>
        <p style="margin:1rem 0 0.5rem;font-size:0.85rem;opacity:0.7">
        {T['footer_links']} &nbsp;|&nbsp;
        🌐 <a href="https://amaurialmeida.github.io/environmental-portfolio/" style="color:#F5A623">Portfólio</a> &nbsp;|&nbsp;
        🐙 <a href="https://github.com/amaurialmeida" style="color:#F5A623">GitHub</a>
        </p>
        <p style="font-size:0.75rem;opacity:0.5;margin:0">© 2026 · Observatório do Colapso de Colmeias · Pesquisa Acadêmica</p>
    </div>
    """, unsafe_allow_html=True)