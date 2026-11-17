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
        "field_instrucoes_title": "Como esta pesquisa foi realizada",
        "field_instrucoes": "Entrevistas realizadas via WhatsApp, Instagram e e-mail com apicultores das regiões de MG, SP e PR. Os produtores mantiveram anonimato conforme protocolo científico. Dados tabulados em Excel e cruzados com literatura científica (Google Acadêmico, IBAMA, EMBRAPA, APTA).",
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
        "field_instrucoes_title": "Cómo se realizó esta investigación",
        "field_instrucoes": "Entrevistas realizadas vía WhatsApp, Instagram y correo electrónico con apicultores de las regiones de MG, SP y PR. Los productores mantuvieron el anonimato según protocolo científico. Datos tabulados en Excel y cruzados con literatura científica (Google Académico, IBAMA, EMBRAPA, APTA).",
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
        "field_instrucoes_title": "How this research was conducted",
        "field_instrucoes": "Interviews conducted via WhatsApp, Instagram and email with beekeepers from the MG, SP and PR regions. Producers maintained anonymity as per scientific protocol. Data tabulated in Excel and cross-referenced with scientific literature (Google Scholar, IBAMA, EMBRAPA, APTA).",
        "tech_label": "TECHNOLOGIES USED",
        "footer_title": "🐝 Amauri Almeida",
        "footer_desc": "Environmental Management Technologist · FATEC Jundiaí (3rd ENADE)<br>Post-Grad in AI, Machine Learning & Data Science · Post-Grad in Data Science & Big Data<br>Systems Analysis and Development · FACINT Maringá",
        "footer_links": "📍 Brazil · Chile · Argentina",
    },

    'it': {'page_title': 'Disturbo da collasso delle colonie · Brasile',
 'hero_tag': 'Tesi · FATEC Jundiaí · Gestione ambientale · 2022',
 'hero_title': 'Disturbo da collasso\n delle colonie in Brasile',
 'hero_subtitle': 'Analisi della mortalità delle api causata da composti chimici agricoli ed eventi climatici in 3 '
                  'regioni brasiliane (2016–2022). Ricerca condotta su 338 alveari e ~20 milioni di api.',
 'badge1': '🐝 338 alveari',
 'badge2': '~20M api',
 'badge3': 'MG · SP · PR · RS',
 'badge4': '2016 — 2022',
 'badge5': 'FATEC JUNDIAÍ · 3° ENADE',
 'protocol_title': '📋 Nota sul protocollo scientifico:',
 'protocol_text': 'I nomi commerciali dei composti chimici identificati in questa ricerca sono stati omessi su '
                  'richiesta dei produttori intervistati e per prudenza legale, e sostituiti con categorie tecniche '
                  'generiche. I dati completi sono disponibili nella tesi originale depositata presso FATEC Jundiaí '
                  '(2022).',
 'm1': 'Alveari persi',
 'm2': 'Api perse (stima)',
 'm3': 'Produttori monitorati',
 'm4': 'Alveari in RS (2024)',
 'tab1': '🗺️ Mappa e analisi',
 'tab2': '🔬 Metodologia e flusso di lavoro',
 'tab3': '💡 Risultati della ricerca',
 'tab4': '📷 Ricerca sul campo',
 'tab5': '📚 Fonti e crediti',
 'map_label': 'VISUALIZZAZIONE GEO SPAZIALE',
 'map_title': 'Distribuzione delle perdite in Brasile',
 'map_hint': '🐝 <strong>Interazione:</strong> fai clic su un indicatore per visualizzare i dettagli della località e '
             'il raggio di bottinamento di 2 km di <em>Apis mellifera</em>.',
 'temporal_label': 'ANALISI TEMPORALE',
 'temporal_title': 'Andamento delle perdite per anno',
 'bar_title': 'Alveari persi per anno (2016–2022)',
 'bar_y': 'Alveari persi',
 'prod_title': 'Totale per produttore',
 'pie_title': 'Distribuzione per categoria di causa',
 'timeline_label': 'CRONOLOGIA PER PRODUTTORE',
 'timeline_title': 'Cronologia dettagliata degli eventi',
 'select_producer': 'Seleziona un produttore',
 'method_label': 'RICERCA SCIENTIFICA',
 'method_title': 'Domanda e metodologia',
 'sci_question_title': '❓ Quesito scientifico centrale',
 'sci_question': '"L\'uso di composti chimici agricoli e urbani nel Sud del Minas Gerais, nella Vale do Paraíba (SP) e '
                 'nel Paraná centrale è correlato alla mortalità delle colonie di api tra il 2016 e il 2022?"',
 'pipeline_label': 'FLUSSO DEI DATI',
 'steps': [['1',
            'Raccolta — Interviste sul campo',
            'Interviste a 9 apicoltori tramite WhatsApp, Instagram ed e-mail. Risposta effettiva da parte di 4 '
            'produttori (anonimato garantito dal protocollo). Identificati come Produttore A (MG), B (SP), C e D '
            '(PR).'],
           ['2',
            'Raccolta — Revisione della letteratura',
            'Ricerca bibliografica scientifica sul CCD (Colony Collapse Disorder), sugli organofosfati, sui '
            'neonicotinoidi e sui fungicidi. Banche dati: Google Scholar, IBAMA, EMBRAPA, APTA.'],
           ['3',
            'Elaborazione — Tabulazione',
            'I dati delle interviste sono stati tabulati in Microsoft Excel. Confronto con la mappa regionale della '
            "Vale do Paraíba (IBGE 2006) e con i dati sull'uso dei pesticidi per comune (Bombardini, 2017 — "
            'FFLCH/USP).'],
           ['4',
            'Elaborazione — Georeferenziazione',
            'Le località sono state associate a coordinate geografiche per la mappatura con Folium. Calcolo dei raggi '
            'di bottinamento per specie (Jataí: 600 m; Apis mellifera: 5 km) secondo EMBRAPA (2021).'],
           ['5',
            'Analisi — Approccio quali-quantitativo',
            'Metodo ipotetico-deduttivo. Analisi descrittiva delle perdite per anno, produttore e causa. Confronto tra '
            'i modelli di mortalità e quelli di utilizzo dei composti chimici riportati in letteratura (RT25/RT40 — '
            'IBAMA 2012).'],
           ['6',
            'Visualizzazione e pubblicazione',
            'Dashboard interattiva sviluppata in Python (Streamlit + Plotly + Folium). Mappatura geospaziale con '
            'indicatori proporzionali alle perdite.']],
 'species_title': '🐝 Specie e raggi di bottinamento',
 'species_text': '• <b>Jataí</b> (Tetragonisca angustula): fino a 600 m — 1.13 km²<br>• <b>Mandaguari</b> '
                 '(Scaptotrigona xanthotricha): fino a 900 m — 2.54 km²<br>• <b>Mandaçaia</b> (Melipona '
                 'quadrifasciata): fino a 2,500 m — 19.63 km²<br>• <b>Apis mellifera</b>: fino a 5,000 m — 78.5 km²',
 'species_source': 'Fonte: EMBRAPA, 2021',
 'compounds_title': '⚗️ Categorie di composti identificate',
 'compounds_text': '• <b>Agente urbano di controllo dei vettori</b>: insetticida organofosforico utilizzato per il '
                   'controllo delle zanzare nei centri urbani. Applicato tramite veicoli comunali.<br>• <b>Composto '
                   'erbicida sistemico</b>: erbicida ad ampio spettro utilizzato su terreni incolti e ai margini delle '
                   'proprietà. Elimina le fonti di nettare.<br>• <b>Insetticida per monocolture</b>: pesticida '
                   'agricolo utilizzato nelle coltivazioni di soia e mais in prossimità degli apiari. Contatto diretto '
                   'tramite deriva degli irroramenti.',
 'compounds_note': 'Nomi commerciali omessi — vedere la nota sul protocollo in cima alla pagina',
 'discovery_label': 'RISULTATI DELLA RICERCA',
 'discovery_title': 'Cosa hanno rivelato i dati',
 'discoveries': [['🔴',
                  'Picco di mortalità nel 2019',
                  "Il Produttore D (PR) ha perso 300 alveari in un solo anno — circa 18 milioni di api. L'evento è "
                  "stato associato all'irrorazione di insetticidi in una piantagione di monocoltura adiacente. "
                  "Rappresenta l'88.9% di tutte le perdite registrate nel periodo 2016-2022."],
                 ['🟠',
                  'Rilevata una sottosegnalazione sistematica',
                  'Dei 9 produttori contattati, solo 4 hanno risposto. Il principale ostacolo era il timore di '
                  'ritorsioni: il 62.5% delle perdite non è mai stato segnalato alle autorità competenti (GEDAVE, '
                  'Polizia ambientale).'],
                 ['🟡',
                  "L'ambiente urbano come vettore di rischio",
                  "Il Produttore A (MG) è stato colpito 3 volte in 7 anni dall'agente comunale per il controllo delle "
                  'zanzare. Il 50% degli apiari colpiti si trovava vicino a foreste native — non a coltivazioni — '
                  'indicando una contaminazione da deriva a distanze superiori a 1 km.'],
                 ['🟢',
                  'Sottoregistrazione nei sistemi ufficiali',
                  'Prima di questa ricerca non erano stati pubblicati dati ufficiali nazionali sulla mortalità delle '
                  "api nella Vale do Paraíba. L'indagine pionieristica tramite Google Forms (Alves, 2022) ha "
                  'confermato un aumento della mortalità tra il 2015-2022, in assenza di precedenti registrazioni '
                  'accademiche.'],
                 ['🔵',
                  'Le alluvioni in RS aggravano il quadro (2024)',
                  'Le alluvioni di maggio/giugno 2024 nel Rio Grande do Sul hanno devastato più di 6,300 alveari, '
                  "aggiungendo gli eventi climatici estremi ai nuovi fattori di rischio per l'apicoltura brasiliana."]],
 'conclusion_label': 'CONCLUSIONE SCIENTIFICA',
 'conclusion_title': 'Ipotesi confermata',
 'conclusion_text': "L'uso di composti chimici agricoli e urbani è stato confermato come causa principale della "
                    "mortalità delle colonie di api nelle regioni studiate. I dati corroborano l'ipotesi che il "
                    'Brasile — il principale consumatore di pesticidi al mondo — stia affrontando un processo di '
                    "Disturbo da collasso delle colonie (CCD) diffuso a livello regionale, aggravato dall'assenza di "
                    'sistemi ufficiali di segnalazione e dal timore di ritorsioni che inibisce la denuncia delle '
                    'perdite.',
 'conclusion_author': 'Amauri Almeida — Tesi in Gestione ambientale, FATEC Jundiaí, 2022',
 'impact_title': 'Api perse per evento (scala logaritmica)',
 'field_label': 'RICERCA APPLICATA',
 'field_title': 'Una ricerca che è uscita dallo schermo',
 'photos': [{'emoji': '🏛️',
             'titulo': 'Museo delle Api — Cotia / Embu das Artes, SP',
             'desc': 'Visita al Museo delle Api. Alveare di Apis mellifera in esposizione — la specie centrale di '
                     'questa ricerca.',
             'path': 'assets/foto_01_museu_apis.jpg',
             'legenda': 'Alveare di Apis mellifera · Museo delle Api · Cotia / Embu das Artes, SP'},
            {'emoji': '💀',
             'titulo': 'Api morte — Guaratinguetá, SP · ott/2021',
             'desc': 'Api morte in un apiario situato nel comune di Guaratinguetá, ottobre 2021. Prova diretta '
                     "dell'evento di collasso documentato in questa ricerca.",
             'path': 'assets/foto_02_mortas_guaratingueta.jpg',
             'legenda': 'Api morte a Guaratinguetá · ott/2021 · Foto: J.F.A.'},
            {'emoji': '🗺️',
             'titulo': 'Il mondo delle api — Mappa interattiva della vita',
             'desc': 'Pannello interattivo al Museo delle Api con una sintesi completa del ciclo vitale delle api. '
                     'Riferimento didattico utilizzato nella tesi.',
             'path': 'assets/foto_03_museu_mapa_vida.jpg',
             'legenda': 'Mappa interattiva del ciclo vitale · Museo delle Api · SP'},
            {'emoji': '🌻',
             'titulo': 'Apis mellifera su girasole — FATEC Jundiaí',
             'desc': 'Ape Apis mellifera su un girasole nel giardino di FATEC Jundiaí, dove è stata discussa la tesi e '
                     'conseguita la laurea in Gestione ambientale (3° ENADE).',
             'path': 'assets/foto_04_apis_girassol_fatec.jpg',
             'legenda': 'Apis mellifera su girasole · Giardino di FATEC Jundiaí · SP'},
            {'emoji': '🔬',
             'titulo': 'Il mondo delle api — Anatomia',
             'desc': "Pannello del Museo delle Api con una mappa dettagliata dell'anatomia delle api. Riferimento "
                     'morfologico utilizzato per caratterizzare le specie studiate.',
             'path': 'assets/foto_05_museu_anatomia.jpg',
             'legenda': "Mappa dell'anatomia delle api · Museo delle Api · SP"},
            {'emoji': '🏺',
             'titulo': 'Pittura rupestre — 500 a.C. · Raccolta del miele',
             'desc': 'Pittura rupestre del 500 a.C. che raffigura persone intente a raccogliere miele. Il rapporto tra '
                     'esseri umani e api è documentato da millenni.',
             'path': 'assets/foto_06_rupestre_500ac.jpg',
             'legenda': 'Pittura rupestre · 500 a.C. · Rapporto tra esseri umani e api'},
            {'emoji': '🌍',
             'titulo': 'Cacciatore di miele — Rhodesia, Sudafrica · 8,000 anni',
             'desc': "Pannello raffigurante un cacciatore di miele in Rhodesia (oggi Zimbabwe), in Sudafrica. L'opera "
                     'risale a circa 8,000 anni fa.',
             'path': 'assets/foto_07_cacador_mel_rodesia.jpg',
             'legenda': 'Cacciatore di miele · Rhodesia, Sudafrica · ~8,000 anni'},
            {'emoji': '🪨',
             'titulo': 'Pittura rupestre — Castellón, Spagna · +10,000 anni',
             'desc': 'Pittura rupestre scoperta a Castellón, in Spagna. Disegno paleolitico di oltre 10,000 anni fa '
                     'che raffigura la raccolta del miele — una delle più antiche rappresentazioni umane '
                     "dell'apicoltura.",
             'path': 'assets/foto_08_rupestre_castellon.jpg',
             'legenda': 'Disegno paleolitico · Castellón, Spagna · +10,000 anni'}],
 'timeline_field_label': 'CONTESTO DELLE INTERVISTE',
 'timeline_field_items': [['apr 2022',
                           'Intervista al Produttore A',
                           'Sud del Minas Gerais · WhatsApp ed e-mail · Apiario vicino a zona residenziale colpita '
                           "dall'agente comunale di controllo dei vettori"],
                          ['apr 2022',
                           'Intervista al Produttore B',
                           'Vale do Paraíba, SP · Instagram ed e-mail · Apiario vicino a terreni trattati con erbicida '
                           'sistemico'],
                          ['mag 2022',
                           'Intervista al Produttore C',
                           'Paraná centrale · Instagram ed e-mail · Grande apiario vicino a una monocoltura'],
                          ['giu 2022',
                           'Intervista al Produttore D',
                           'Paraná centrale · Instagram ed e-mail · Maggiore perdita individuale: 300 alveari nel '
                           '2019'],
                          ['giu 2022',
                           'Discussione della tesi',
                           'FATEC Jundiaí, SP · Relatore: Prof. Me. Claudio da Cunha · Gestione ambientale'],
                          ['ott 2021',
                           'Visita al Museo delle Api',
                           'Cotia / Embu das Artes, SP · Documentazione fotografica e riferimenti scientifici per la '
                           'tesi']],
 'sources_label': 'RIFERIMENTI SCIENTIFICI',
 'sources_title': 'Fonti e banca dati',
 'field_instrucoes_title': 'Come è stata condotta questa ricerca',
 'field_instrucoes': 'Interviste condotte tramite WhatsApp, Instagram ed e-mail con apicoltori delle regioni MG, SP e '
                     "PR. L'anonimato dei produttori è stato mantenuto in conformità al protocollo scientifico. Dati "
                     'tabulati in Excel e confrontati con la letteratura scientifica (Google Scholar, IBAMA, EMBRAPA, '
                     'APTA).',
 'tech_label': 'TECNOLOGIE UTILIZZATE',
 'footer_title': '🐝 Amauri Almeida',
 'footer_desc': 'Tecnologo in Gestione ambientale · FATEC Jundiaí (3° ENADE)<br>Specializzazione post-laurea in IA, '
                'Machine Learning e Data Science · Specializzazione post-laurea in Data Science e Big Data<br>Analisi '
                'e sviluppo di sistemi · FACINT Maringá',
 'footer_links': '📍 Brasile · Cile · Argentina'},

    'zh': {'page_title': '蜂群崩溃失调 · 巴西',
 'hero_tag': '毕业论文 · FATEC Jundiaí · 环境管理 · 2022',
 'hero_title': '巴西的蜂群崩溃\n失调',
 'hero_subtitle': '分析巴西3个地区（2016–2022年）农业化学物质和气候事件导致的蜜蜂死亡情况。研究涵盖338个蜂箱和约2,000万只蜜蜂。',
 'badge1': '🐝 338个蜂箱',
 'badge2': '约2,000万只蜜蜂',
 'badge3': 'MG · SP · PR · RS',
 'badge4': '2016 — 2022',
 'badge5': 'FATEC JUNDIAÍ · ENADE第3名',
 'protocol_title': '📋 科学研究方案说明：',
 'protocol_text': '应受访养蜂人的要求并出于法律审慎考虑，本研究未列出所识别化学物质的商品名称，而以通用技术类别替代。完整数据见存档于FATEC Jundiaí的原始毕业论文（2022）。',
 'm1': '损失蜂箱数',
 'm2': '损失蜜蜂数（估算）',
 'm3': '受监测养蜂人',
 'm4': 'RS蜂箱数（2024）',
 'tab1': '🗺️ 地图与分析',
 'tab2': '🔬 方法与流程',
 'tab3': '💡 研究发现',
 'tab4': '📷 实地研究',
 'tab5': '📚 来源与致谢',
 'map_label': '地理空间可视化',
 'map_title': '巴西损失分布',
 'map_hint': '🐝 <strong>交互：</strong>点击任意标记，查看当地详情以及<em>Apis mellifera</em>的2km采集半径。',
 'temporal_label': '时间分析',
 'temporal_title': '逐年损失变化',
 'bar_title': '逐年损失蜂箱数（2016–2022）',
 'bar_y': '损失蜂箱数',
 'prod_title': '养蜂人损失总数',
 'pie_title': '按原因类别划分的分布',
 'timeline_label': '按养蜂人划分的时间线',
 'timeline_title': '事件详细记录',
 'select_producer': '选择养蜂人',
 'method_label': '科学研究',
 'method_title': '研究问题与方法',
 'sci_question_title': '❓ 核心科学问题',
 'sci_question': '“2016至2022年间，南米纳斯吉拉斯、Vale do Paraíba（SP）和巴拉那州中部地区农业及城市化学物质的使用，是否与蜂群死亡相关？”',
 'pipeline_label': '数据处理流程',
 'steps': [['1',
            '数据收集 — 实地访谈',
            '通过 WhatsApp、Instagram 和电子邮件访谈了9位养蜂人。4位养蜂人有效回应（依照研究方案保证匿名）。分别标记为养蜂人A（MG）、B（SP）、C和D（PR）。'],
           ['2', '数据收集 — 文献综述', '检索有关CCD（蜂群崩溃失调）、有机磷酸酯、新烟碱类杀虫剂和杀菌剂的科学文献。数据库：Google Scholar、IBAMA、EMBRAPA、APTA。'],
           ['3',
            '数据处理 — 数据制表',
            '使用 Microsoft Excel 对访谈数据进行制表。并与Vale do Paraíba区域地图（IBGE 2006）及按市镇划分的农药使用数据（Bombardini, 2017 — '
            'FFLCH/USP）进行交叉比对。'],
           ['4', '数据处理 — 地理配准', '将地点与地理坐标关联，以便使用 Folium 制图。依据 EMBRAPA（2021）按物种计算采集半径（Jataí：600m；Apis mellifera：5km）。'],
           ['5', '分析 — 定性与定量相结合的方法', '采用假设演绎法。按年份、养蜂人和原因对损失进行描述性分析。将死亡模式与文献中化学物质的使用模式进行交叉比对（RT25/RT40 — IBAMA 2012）。'],
           ['6', '可视化与发布', '使用 Python（Streamlit + Plotly + Folium）开发交互式仪表板。通过与损失数量成比例的标记进行地理空间制图。']],
 'species_title': '🐝 蜜蜂物种与采集半径',
 'species_text': '• <b>Jataí</b> (Tetragonisca angustula)：最远600m — 1.13 km²<br>• <b>Mandaguari</b> (Scaptotrigona '
                 'xanthotricha)：最远900m — 2.54 km²<br>• <b>Mandaçaia</b> (Melipona quadrifasciata)：最远2,500m — 19.63 '
                 'km²<br>• <b>Apis mellifera</b>：最远5,000m — 78.5 km²',
 'species_source': '来源：EMBRAPA, 2021',
 'compounds_title': '⚗️ 已识别的化学物质类别',
 'compounds_text': '• <b>城市病媒防治药剂</b>：用于城市中心蚊虫防治的有机磷杀虫剂。由市政车辆施用。<br>• <b>内吸性除草剂</b>：用于空置地块和房产边缘的广谱除草剂。会清除蜜源。<br>• '
                   '<b>单一种植杀虫剂</b>：用于蜂场附近大豆和玉米作物的农业杀虫剂。喷雾飘移可造成直接接触。',
 'compounds_note': '商品名称已省略 — 请参阅页面顶部的研究方案说明',
 'discovery_label': '研究结果',
 'discovery_title': '数据揭示的情况',
 'discoveries': [['🔴',
                  '2019年死亡高峰',
                  '养蜂人D（PR）在单一年内损失了300个蜂箱，约相当于1,800万只蜜蜂。该事件与相邻单一种植园喷洒杀虫剂有关，占2016–2022年记录的全部损失的88.9%。'],
                 ['🟠', '发现系统性漏报', '联系的9位养蜂人中，只有4位作出回应。主要障碍是担心遭到报复：62.5%的损失从未向主管部门（GEDAVE、环境警察）报告。'],
                 ['🟡', '城市环境成为风险来源', '养蜂人A（MG）在7年内3次受到市政蚊虫防治药剂影响。受影响蜂场中有50%位于原生林附近，而非农作物附近，表明污染物可能飘移至1km以外。'],
                 ['🟢',
                  '官方系统存在漏报',
                  '在本研究开展之前，尚无关于Vale do Paraíba蜜蜂死亡情况的全国官方数据发布。Alves（2022）开创性的 Google Forms '
                  '调查证实，2015–2022年间蜜蜂死亡情况日益严重，但此前没有学术记录。'],
                 ['🔵', 'RS洪灾加剧了这一局面（2024）', '2024年5月/6月Rio Grande do Sul洪灾摧毁了6,300多个蜂箱，使极端气候事件成为巴西养蜂业新的风险来源。']],
 'conclusion_label': '科学结论',
 'conclusion_title': '假设得到证实',
 'conclusion_text': '研究证实，农业和城市化学物质的使用是所研究地区蜂群死亡的主要原因。数据支持以下假设：作为全球农药消费量最大的国家，巴西正面临区域分布广泛的蜂群崩溃失调（CCD），而缺乏官方报告系统以及对遭受报复的担忧，进一步加剧了这一问题并抑制损失报告。',
 'conclusion_author': 'Amauri Almeida — 环境管理毕业论文，FATEC Jundiaí, 2022',
 'impact_title': '按事件划分的蜜蜂损失数（对数刻度）',
 'field_label': '应用研究',
 'field_title': '走出屏幕的研究',
 'photos': [{'emoji': '🏛️',
             'titulo': '蜜蜂博物馆 — Cotia / Embu das Artes, SP',
             'desc': '参观蜜蜂博物馆。展出的 Apis mellifera 蜂箱——本研究的核心物种。',
             'path': 'assets/foto_01_museu_apis.jpg',
             'legenda': 'Apis mellifera 蜂箱 · 蜜蜂博物馆 · Cotia / Embu das Artes, SP'},
            {'emoji': '💀',
             'titulo': '死蜂 — Guaratinguetá, SP · 2021年10月',
             'desc': '2021年10月，在Guaratinguetá市一处蜂场发现死蜂。本研究记录的蜂群崩溃事件的直接证据。',
             'path': 'assets/foto_02_mortas_guaratingueta.jpg',
             'legenda': 'Guaratinguetá的死蜂 · 2021年10月 · 照片：J.F.A.'},
            {'emoji': '🗺️',
             'titulo': '蜜蜂世界 — 互动生命地图',
             'desc': '蜜蜂博物馆的互动展板，全面概述蜜蜂生命周期。毕业论文采用的教育参考资料。',
             'path': 'assets/foto_03_museu_mapa_vida.jpg',
             'legenda': '互动生命周期地图 · 蜜蜂博物馆 · SP'},
            {'emoji': '🌻',
             'titulo': '向日葵上的 Apis mellifera — FATEC Jundiaí',
             'desc': 'FATEC Jundiaí花园中的 Apis mellifera 蜜蜂。毕业论文在此答辩，环境管理学位亦于此完成（ENADE第3名）。',
             'path': 'assets/foto_04_apis_girassol_fatec.jpg',
             'legenda': '向日葵上的 Apis mellifera · FATEC Jundiaí花园 · SP'},
            {'emoji': '🔬',
             'titulo': '蜜蜂世界 — 解剖结构',
             'desc': '蜜蜂博物馆展示蜜蜂解剖结构详细图谱的展板。用于描述研究物种特征的形态学参考资料。',
             'path': 'assets/foto_05_museu_anatomia.jpg',
             'legenda': '蜜蜂解剖结构图 · 蜜蜂博物馆 · SP'},
            {'emoji': '🏺',
             'titulo': '洞穴壁画 — 公元前500年 · 采集蜂蜜',
             'desc': '一幅绘于公元前500年的洞穴壁画，描绘人们采集蜂蜜的场景。人类与蜜蜂的关系已有数千年的文字记载。',
             'path': 'assets/foto_06_rupestre_500ac.jpg',
             'legenda': '洞穴壁画 · 公元前500年 · 人类与蜜蜂的关系'},
            {'emoji': '🌍',
             'titulo': '采蜜者 — 南非罗得西亚 · 约8,000年前',
             'desc': '描绘南非罗得西亚（现津巴布韦）采蜜者的展板。作品年代约为8,000年前。',
             'path': 'assets/foto_07_cacador_mel_rodesia.jpg',
             'legenda': '采蜜者 · 南非罗得西亚 · 约8,000年前'},
            {'emoji': '🪨',
             'titulo': '洞穴壁画 — 西班牙 Castellón · 10,000多年前',
             'desc': '在西班牙 Castellón 发现的洞穴壁画。这幅旧石器时代绘画距今已有10,000多年，描绘了采集蜂蜜的场景，是人类最早描绘养蜂活动的作品之一。',
             'path': 'assets/foto_08_rupestre_castellon.jpg',
             'legenda': '旧石器时代绘画 · 西班牙 Castellón · 10,000多年前'}],
 'timeline_field_label': '访谈背景',
 'timeline_field_items': [['2022年4月', '访谈养蜂人A', '南米纳斯吉拉斯 · WhatsApp和电子邮件 · 蜂场靠近住宅区，受到市政病媒防治药剂影响'],
                          ['2022年4月', '访谈养蜂人B', 'Vale do Paraíba, SP · Instagram和电子邮件 · 蜂场靠近使用内吸性除草剂的地块'],
                          ['2022年5月', '访谈养蜂人C', '巴拉那州中部 · Instagram和电子邮件 · 靠近单一种植区的大型蜂场'],
                          ['2022年6月', '访谈养蜂人D', '巴拉那州中部 · Instagram和电子邮件 · 个体损失最高：2019年损失300个蜂箱'],
                          ['2022年6月', '毕业论文答辩', 'FATEC Jundiaí, SP · 指导教师：Claudio da Cunha 硕士教授 · 环境管理'],
                          ['2021年10月', '参观蜜蜂博物馆', 'Cotia / Embu das Artes, SP · 为毕业论文收集照片记录和科学参考资料']],
 'sources_label': '科学参考文献',
 'sources_title': '来源与数据库',
 'field_instrucoes_title': '本研究的实施方式',
 'field_instrucoes': '通过 WhatsApp、Instagram 和电子邮件，对来自MG、SP和PR地区的养蜂人进行了访谈。依照科学研究方案，对养蜂人身份予以匿名处理。数据使用 Excel '
                     '制表，并与科学文献（Google Scholar、IBAMA、EMBRAPA、APTA）进行交叉比对。',
 'tech_label': '所用技术',
 'footer_title': '🐝 Amauri Almeida',
 'footer_desc': '环境管理技术专业毕业生 · FATEC Jundiaí（ENADE第3名）<br>人工智能、机器学习与数据科学研究生学历 · 数据科学与大数据研究生学历<br>系统分析与开发 · FACINT '
                'Maringá',
 'footer_links': '📍 巴西 · 智利 · 阿根廷'},

    'fr': {'page_title': 'Trouble d’effondrement des colonies · Brésil',
 'hero_tag': 'Mémoire · FATEC Jundiaí · Gestion environnementale · 2022',
 'hero_title': 'Trouble d’effondrement\ndes colonies au Brésil',
 'hero_subtitle': 'Analyse de la mortalité des abeilles due aux composés chimiques agricoles et aux événements '
                  'climatiques dans 3 régions brésiliennes (2016–2022). Recherche portant sur 338 ruches et ~20 '
                  'millions d’abeilles.',
 'badge1': '🐝 338 ruches',
 'badge2': '~20 M d’abeilles',
 'badge3': 'MG · SP · PR · RS',
 'badge4': '2016 — 2022',
 'badge5': 'FATEC JUNDIAÍ · 3e ENADE',
 'protocol_title': '📋 Note sur le protocole scientifique :',
 'protocol_text': 'Les noms commerciaux des composés chimiques identifiés dans cette recherche ont été omis à la '
                  'demande des producteurs interrogés et par prudence juridique, et remplacés par des catégories '
                  'techniques génériques. Les données complètes sont disponibles dans le mémoire original déposé à la '
                  'FATEC Jundiaí (2022).',
 'm1': 'Ruches perdues',
 'm2': 'Abeilles perdues (est.)',
 'm3': 'Producteurs suivis',
 'm4': 'Ruches dans le RS (2024)',
 'tab1': '🗺️ Carte et analyse',
 'tab2': '🔬 Méthodologie et processus',
 'tab3': '💡 Résultats',
 'tab4': '📷 Recherche de terrain',
 'tab5': '📚 Sources et crédits',
 'map_label': 'VISUALISATION GÉOSPATIALE',
 'map_title': 'Répartition des pertes au Brésil',
 'map_hint': '🐝 <strong>Interaction :</strong> Cliquez sur un marqueur pour afficher les détails du lieu et le rayon '
             'de butinage de 2 km d’<em>Apis mellifera</em>.',
 'temporal_label': 'ANALYSE TEMPORELLE',
 'temporal_title': 'Évolution des pertes par année',
 'bar_title': 'Ruches perdues par année (2016–2022)',
 'bar_y': 'Ruches perdues',
 'prod_title': 'Total par producteur',
 'pie_title': 'Répartition par catégorie de cause',
 'timeline_label': 'CHRONOLOGIE PAR PRODUCTEUR',
 'timeline_title': 'Historique détaillé des événements',
 'select_producer': 'Sélectionner un producteur',
 'method_label': 'RECHERCHE SCIENTIFIQUE',
 'method_title': 'Question et méthodologie',
 'sci_question_title': '❓ Question scientifique centrale',
 'sci_question': '« L’utilisation de composés chimiques agricoles et urbains dans le sud du Minas Gerais, la Vale do '
                 'Paraíba (SP) et le centre du Paraná est-elle corrélée à la mortalité des colonies d’abeilles entre '
                 '2016 et 2022 ? »',
 'pipeline_label': 'PROCESSUS DE TRAITEMENT DES DONNÉES',
 'steps': [['1',
            'Collecte — Entretiens de terrain',
            'Entretiens avec 9 apiculteurs via WhatsApp, Instagram et courriel. Réponse effective de 4 producteurs '
            '(anonymat garanti par le protocole). Identifiés comme producteur A (MG), B (SP), C et D (PR).'],
           ['2',
            'Collecte — Revue de la littérature',
            'Revue de la littérature scientifique sur le CCD (trouble d’effondrement des colonies), les '
            'organophosphorés, les néonicotinoïdes et les fongicides. Bases de données : Google Scholar, IBAMA, '
            'EMBRAPA, APTA.'],
           ['3',
            'Traitement — Mise en tableaux',
            'Données des entretiens mises en tableaux dans Microsoft Excel. Croisement avec la carte régionale de la '
            'Vale do Paraíba (IBGE 2006) et les données sur l’utilisation des pesticides par municipalité (Bombardini, '
            '2017 — FFLCH/USP).'],
           ['4',
            'Traitement — Géoréférencement',
            'Lieux associés à des coordonnées géographiques pour la cartographie avec Folium. Calcul des rayons de '
            'butinage par espèce (Jataí : 600 m ; Apis mellifera : 5 km), selon EMBRAPA (2021).'],
           ['5',
            'Analyse — Approche quali-quantitative',
            'Méthode hypothético-déductive. Analyse descriptive des pertes par année, producteur et cause. Croisement '
            'des schémas de mortalité avec les schémas d’utilisation des composés chimiques documentés dans la '
            'littérature (RT25/RT40 — IBAMA 2012).'],
           ['6',
            'Visualisation et publication',
            'Tableau de bord interactif développé en Python (Streamlit + Plotly + Folium). Cartographie géospatiale '
            'avec des marqueurs proportionnels aux pertes.']],
 'species_title': '🐝 Espèces et rayons de butinage',
 'species_text': '• <b>Jataí</b> (Tetragonisca angustula) : jusqu’à 600 m — 1.13 km²<br>• <b>Mandaguari</b> '
                 '(Scaptotrigona xanthotricha) : jusqu’à 900 m — 2.54 km²<br>• <b>Mandaçaia</b> (Melipona '
                 'quadrifasciata) : jusqu’à 2,500 m — 19.63 km²<br>• <b>Apis mellifera</b> : jusqu’à 5,000 m — 78.5 '
                 'km²',
 'species_source': 'Source : EMBRAPA, 2021',
 'compounds_title': '⚗️ Catégories de composés identifiées',
 'compounds_text': '• <b>Agent de lutte antivectorielle en milieu urbain</b> : insecticide organophosphoré utilisé '
                   'pour lutter contre les moustiques dans les centres urbains. Appliqué par des véhicules '
                   'municipaux.<br>• <b>Composé herbicide systémique</b> : herbicide à large spectre utilisé sur les '
                   'terrains vagues et en bordure de propriétés. Élimine les sources de nectar.<br>• <b>Insecticide '
                   'pour monocultures</b> : pesticide agricole utilisé sur les cultures de soja et de maïs à proximité '
                   'des ruchers. Contact direct par dérive de pulvérisation.',
 'compounds_note': 'Noms commerciaux omis — voir la note sur le protocole en haut de la page',
 'discovery_label': 'RÉSULTATS DE LA RECHERCHE',
 'discovery_title': 'Ce que les données ont révélé',
 'discoveries': [['🔴',
                  'Pic de mortalité en 2019',
                  'Le producteur D (PR) a perdu 300 ruches en une seule année — environ 18 millions d’abeilles. '
                  'L’événement a été associé à la pulvérisation d’insecticide dans une plantation de monoculture '
                  'adjacente. Cela représente 88.9% de l’ensemble des pertes enregistrées entre 2016-2022.'],
                 ['🟠',
                  'Sous-déclaration systémique mise en évidence',
                  'Sur les 9 producteurs contactés, seuls 4 ont répondu. Le principal obstacle était la crainte de '
                  'représailles : 62.5% des pertes n’ont jamais été signalées aux autorités compétentes (GEDAVE, '
                  'Police environnementale).'],
                 ['🟡',
                  'Le milieu urbain comme vecteur de risque',
                  'Le producteur A (MG) a été touché 3 fois en 7 ans par l’agent municipal de lutte antivectorielle '
                  'contre les moustiques. 50% des ruchers touchés se trouvaient près de forêts indigènes — et non de '
                  'cultures — ce qui indique une contamination par dérive à des distances supérieures à 1 km.'],
                 ['🟢',
                  'Sous-enregistrement dans les systèmes officiels',
                  'Aucune donnée nationale officielle sur la mortalité des abeilles dans la Vale do Paraíba n’avait '
                  'été publiée avant cette recherche. L’enquête pionnière menée via Google Forms (Alves, 2022) a '
                  'confirmé une hausse de la mortalité entre 2015-2022, sans qu’aucun relevé universitaire antérieur '
                  'n’existe.'],
                 ['🔵',
                  'Les inondations dans le RS aggravent la situation (2024)',
                  'Les inondations de mai/juin 2024 dans le Rio Grande do Sul ont dévasté plus de 6,300 ruches, '
                  'ajoutant les événements climatiques extrêmes aux nouveaux facteurs de risque pour l’apiculture '
                  'brésilienne.']],
 'conclusion_label': 'CONCLUSION SCIENTIFIQUE',
 'conclusion_title': 'Hypothèse confirmée',
 'conclusion_text': 'L’utilisation de composés chimiques agricoles et urbains a été confirmée comme la principale '
                    'cause de mortalité des colonies d’abeilles dans les régions étudiées. Les données corroborent '
                    'l’hypothèse selon laquelle le Brésil — premier consommateur de pesticides au monde — est '
                    'confronté à un processus de trouble d’effondrement des colonies (CCD) réparti à l’échelle '
                    'régionale, aggravé par l’absence de systèmes officiels de signalement et par la crainte de '
                    'représailles, qui freine la déclaration des pertes.',
 'conclusion_author': 'Amauri Almeida — Mémoire de gestion environnementale, FATEC Jundiaí, 2022',
 'impact_title': 'Abeilles perdues par événement (échelle logarithmique)',
 'field_label': 'RECHERCHE APPLIQUÉE',
 'field_title': 'Une recherche qui sort de l’écran',
 'photos': [{'emoji': '🏛️',
             'titulo': 'Musée des abeilles — Cotia / Embu das Artes, SP',
             'desc': 'Visite du Musée des abeilles. Ruche d’Apis mellifera exposée — l’espèce centrale de cette '
                     'recherche.',
             'path': 'assets/foto_01_museu_apis.jpg',
             'legenda': 'Ruche d’Apis mellifera · Musée des abeilles · Cotia / Embu das Artes, SP'},
            {'emoji': '💀',
             'titulo': 'Abeilles mortes — Guaratinguetá, SP · oct./2021',
             'desc': 'Abeilles mortes dans un rucher situé dans la municipalité de Guaratinguetá, octobre 2021. Preuve '
                     'directe de l’événement d’effondrement documenté dans cette recherche.',
             'path': 'assets/foto_02_mortas_guaratingueta.jpg',
             'legenda': 'Abeilles mortes à Guaratinguetá · oct./2021 · Photo : J.F.A.'},
            {'emoji': '🗺️',
             'titulo': 'Le monde des abeilles — Carte interactive de la vie',
             'desc': 'Panneau interactif au Musée des abeilles présentant un résumé complet du cycle de vie de '
                     'l’abeille. Référence pédagogique utilisée dans le mémoire.',
             'path': 'assets/foto_03_museu_mapa_vida.jpg',
             'legenda': 'Carte interactive du cycle de vie · Musée des abeilles · SP'},
            {'emoji': '🌻',
             'titulo': 'Apis mellifera sur un tournesol — FATEC Jundiaí',
             'desc': 'Abeille Apis mellifera sur un tournesol dans le jardin de la FATEC Jundiaí, où le mémoire a été '
                     'soutenu et le diplôme de gestion environnementale obtenu (3e ENADE).',
             'path': 'assets/foto_04_apis_girassol_fatec.jpg',
             'legenda': 'Apis mellifera sur un tournesol · Jardin de la FATEC Jundiaí · SP'},
            {'emoji': '🔬',
             'titulo': 'Le monde des abeilles — Anatomie',
             'desc': 'Panneau du Musée des abeilles présentant une carte détaillée de l’anatomie de l’abeille. '
                     'Référence morphologique utilisée pour caractériser les espèces étudiées.',
             'path': 'assets/foto_05_museu_anatomia.jpg',
             'legenda': 'Carte de l’anatomie de l’abeille · Musée des abeilles · SP'},
            {'emoji': '🏺',
             'titulo': 'Peinture rupestre — 500 av. J.-C. · Récolte du miel',
             'desc': 'Peinture rupestre datant de 500 av. J.-C. représentant des personnes récoltant du miel. La '
                     'relation entre les humains et les abeilles est documentée depuis des millénaires.',
             'path': 'assets/foto_06_rupestre_500ac.jpg',
             'legenda': 'Peinture rupestre · 500 av. J.-C. · Relation entre les humains et les abeilles'},
            {'emoji': '🌍',
             'titulo': 'Chasseur de miel — Rhodésie, Afrique du Sud · 8,000 ans',
             'desc': 'Panneau représentant un chasseur de miel en Rhodésie (aujourd’hui le Zimbabwe), en Afrique du '
                     'Sud. Œuvre datée d’environ 8,000 ans.',
             'path': 'assets/foto_07_cacador_mel_rodesia.jpg',
             'legenda': 'Chasseur de miel · Rhodésie, Afrique du Sud · ~8,000 ans'},
            {'emoji': '🪨',
             'titulo': 'Peinture rupestre — Castellón, Espagne · +10,000 ans',
             'desc': 'Peinture rupestre découverte à Castellón, en Espagne. Dessin paléolithique vieux de plus de '
                     '10,000 ans représentant la récolte du miel — l’une des plus anciennes représentations humaines '
                     'de l’apiculture.',
             'path': 'assets/foto_08_rupestre_castellon.jpg',
             'legenda': 'Dessin paléolithique · Castellón, Espagne · +10,000 ans'}],
 'timeline_field_label': 'CONTEXTE DES ENTRETIENS',
 'timeline_field_items': [['avr. 2022',
                           'Entretien avec le producteur A',
                           'Sud du Minas Gerais · WhatsApp et courriel · Rucher près d’une zone résidentielle touchée '
                           'par l’agent municipal de lutte antivectorielle'],
                          ['avr. 2022',
                           'Entretien avec le producteur B',
                           'Vale do Paraíba, SP · Instagram et courriel · Rucher près de terrains traités avec un '
                           'herbicide systémique'],
                          ['mai 2022',
                           'Entretien avec le producteur C',
                           'Centre du Paraná · Instagram et courriel · Grand rucher à proximité d’une monoculture'],
                          ['juin 2022',
                           'Entretien avec le producteur D',
                           'Centre du Paraná · Instagram et courriel · Plus grande perte individuelle : 300 ruches en '
                           '2019'],
                          ['juin 2022',
                           'Soutenance du mémoire',
                           'FATEC Jundiaí, SP · Directeur : Prof. Me. Claudio da Cunha · Gestion environnementale'],
                          ['oct. 2021',
                           'Visite du Musée des abeilles',
                           'Cotia / Embu das Artes, SP · Documents photographiques et références scientifiques pour le '
                           'mémoire']],
 'sources_label': 'RÉFÉRENCES SCIENTIFIQUES',
 'sources_title': 'Sources et base de données',
 'field_instrucoes_title': 'Déroulement de la recherche',
 'field_instrucoes': 'Entretiens menés via WhatsApp, Instagram et courriel avec des apiculteurs des régions MG, SP et '
                     'PR. L’anonymat des producteurs a été préservé conformément au protocole scientifique. Données '
                     'mises en tableaux dans Excel et croisées avec la littérature scientifique (Google Scholar, '
                     'IBAMA, EMBRAPA, APTA).',
 'tech_label': 'TECHNOLOGIES UTILISÉES',
 'footer_title': '🐝 Amauri Almeida',
 'footer_desc': 'Technologue en gestion environnementale · FATEC Jundiaí (3e ENADE)<br>Études supérieures de '
                'spécialisation en IA, apprentissage automatique et science des données · Études supérieures de '
                'spécialisation en science des données et Big Data<br>Analyse et développement de systèmes · FACINT '
                'Maringá',
 'footer_links': '📍 Brésil · Chili · Argentine'},

    'ar': {'page_title': 'اضطراب انهيار المستعمرات · البرازيل',
 'hero_tag': 'أطروحة · FATEC Jundiaí · الإدارة البيئية · 2022',
 'hero_title': 'اضطراب انهيار\nالمستعمرات في البرازيل',
 'hero_subtitle': 'تحليل نفوق النحل الناجم عن المركبات الكيميائية الزراعية والأحداث المناخية في 3 مناطق برازيلية '
                  '(2016–2022). يشمل البحث 338 خلية ونحو 20 مليون نحلة.',
 'badge1': '🐝 338 خلية',
 'badge2': 'نحو 20 مليون نحلة',
 'badge3': 'MG · SP · PR · RS',
 'badge4': '2016 — 2022',
 'badge5': 'FATEC JUNDIAÍ · ENADE، المرتبة الثالثة',
 'protocol_title': '📋 ملاحظة بشأن البروتوكول العلمي:',
 'protocol_text': 'حُذفت الأسماء التجارية للمركبات الكيميائية التي حُدّدت في هذا البحث، بناءً على طلب المنتجين الذين '
                  'أُجريت معهم المقابلات وحرصًا على تجنب المخاطر القانونية، واستُعيض عنها بفئات تقنية عامة. تتوفر '
                  'البيانات كاملةً في الأطروحة الأصلية المودعة لدى FATEC Jundiaí (2022).',
 'm1': 'الخلايا المفقودة',
 'm2': 'النحل النافق (تقديريًا)',
 'm3': 'المنتجون الذين شملتهم المتابعة',
 'm4': 'خلايا RS (2024)',
 'tab1': '🗺️ الخريطة والتحليل',
 'tab2': '🔬 المنهجية ومسار العمل',
 'tab3': '💡 ما توصلنا إليه',
 'tab4': '📷 البحث الميداني',
 'tab5': '📚 المصادر والتقديرات',
 'map_label': 'التصور الجغرافي المكاني',
 'map_title': 'توزيع الخسائر في البرازيل',
 'map_hint': '🐝 <strong>التفاعل:</strong> انقر على أي علامة للاطلاع على تفاصيل الموقع ونطاق الطيران البالغ 2km لنحل '
             '<em>Apis mellifera</em>.',
 'temporal_label': 'التحليل الزمني',
 'temporal_title': 'تطور الخسائر حسب السنة',
 'bar_title': 'الخلايا المفقودة سنويًا (2016–2022)',
 'bar_y': 'الخلايا المفقودة',
 'prod_title': 'الإجمالي حسب المنتج',
 'pie_title': 'التوزيع حسب فئة السبب',
 'timeline_label': 'الخط الزمني حسب المنتج',
 'timeline_title': 'السجل التفصيلي للأحداث',
 'select_producer': 'اختر منتجًا',
 'method_label': 'البحث العلمي',
 'method_title': 'السؤال والمنهجية',
 'sci_question_title': '❓ السؤال العلمي المحوري',
 'sci_question': '"هل يرتبط استخدام المركبات الكيميائية الزراعية والحضرية في جنوب ميناس جيرايس وفالي دو بارايبا (SP) '
                 'ووسط بارانا بنفوق مستعمرات النحل بين عامي 2016 و2022؟"',
 'pipeline_label': 'مسار معالجة البيانات',
 'steps': [['1',
            'جمع البيانات — المقابلات الميدانية',
            'مقابلات مع 9 من مربي النحل عبر WhatsApp وInstagram والبريد الإلكتروني. استجاب فعليًا 4 منتجين (وضِمن '
            'البروتوكول الحفاظ على سرية هوياتهم). أُشير إليهم بالمنتج A (MG)، وB (SP)، وC وD (PR).'],
           ['2',
            'جمع البيانات — مراجعة الأدبيات',
            'مسح للأدبيات العلمية حول CCD (اضطراب انهيار المستعمرات)، ومركبات الفوسفات العضوية والنيونيكوتينويدات '
            'ومبيدات الفطريات. قواعد البيانات: Google Scholar، IBAMA، EMBRAPA، APTA.'],
           ['3',
            'المعالجة — التبويب',
            'جُدولت بيانات المقابلات في Microsoft Excel. وقورنت بالخريطة الإقليمية لفالي دو بارايبا (IBGE 2006) '
            'وبيانات استخدام مبيدات الآفات حسب البلدية (Bombardini, 2017 — FFLCH/USP).'],
           ['4',
            'المعالجة — الإسناد الجغرافي',
            'رُبطت المواقع بإحداثيات جغرافية لإعداد الخرائط باستخدام Folium. وحُسبت أنصاف أقطار نطاق الطيران حسب النوع '
            '(Jataí: 600m؛ Apis mellifera: 5km) وفقًا لـ EMBRAPA (2021).'],
           ['5',
            'التحليل — المنهج النوعي والكمي',
            'المنهج الافتراضي الاستنباطي. تحليل وصفي للخسائر حسب السنة والمنتج والسبب. ومقارنة أنماط النفوق بأنماط '
            'استخدام المركبات الكيميائية الواردة في الأدبيات (RT25/RT40 — IBAMA 2012).'],
           ['6',
            'التصور والنشر',
            'طُوّرت لوحة معلومات تفاعلية باستخدام Python (Streamlit + Plotly + Folium). ورُسمت الخرائط الجغرافية '
            'المكانية بعلامات تتناسب أحجامها مع الخسائر.']],
 'species_title': '🐝 الأنواع وأنصاف أقطار نطاق الطيران',
 'species_text': '• <b>Jataí</b> (Tetragonisca angustula): حتى 600m — 1.13 km²<br>• <b>Mandaguari</b> (Scaptotrigona '
                 'xanthotricha): حتى 900m — 2.54 km²<br>• <b>Mandaçaia</b> (Melipona quadrifasciata): حتى 2,500m — '
                 '19.63 km²<br>• <b>Apis mellifera</b>: حتى 5,000m — 78.5 km²',
 'species_source': 'المصدر: EMBRAPA، 2021',
 'compounds_title': '⚗️ فئات المركبات المحددة',
 'compounds_text': '• <b>مادة مكافحة النواقل الحضرية</b>: مبيد حشري من الفوسفات العضوية يُستخدم لمكافحة البعوض في '
                   'المراكز الحضرية. تطبقه مركبات البلدية.<br>• <b>مركب مبيد أعشاب جهازي</b>: مبيد أعشاب واسع الطيف '
                   'يُستخدم في الأراضي الخالية وعلى أطراف الممتلكات. يقضي على مصادر الرحيق.<br>• <b>مبيد حشري للزراعة '
                   'الأحادية</b>: مبيد آفات زراعي يُستخدم في محاصيل الصويا والذرة بالقرب من المناحل. يحدث التماس '
                   'المباشر عبر انجراف الرذاذ.',
 'compounds_note': 'حُذفت الأسماء التجارية — راجع ملاحظة البروتوكول في أعلى الصفحة',
 'discovery_label': 'نتائج البحث',
 'discovery_title': 'ما كشفته البيانات',
 'discoveries': [['🔴',
                  'ذروة النفوق في 2019',
                  'فقد المنتج D (PR) 300 خلية في سنة واحدة — أي نحو 18 مليون نحلة. وارتبطت الحادثة برش مبيد حشري في '
                  'مزرعة زراعة أحادية مجاورة. وتمثل هذه الخسائر 88.9% من إجمالي الخسائر المسجلة خلال 2016-2022.'],
                 ['🟠',
                  'رُصد قصور منهجي في الإبلاغ',
                  'لم يستجب سوى 4 من أصل 9 منتجين جرى التواصل معهم. وكانت العقبة الرئيسية الخوف من الانتقام: إذ لم '
                  'يُبلّغ عن 62.5% من الخسائر للجهات المختصة (GEDAVE، والشرطة البيئية).'],
                 ['🟡',
                  'البيئة الحضرية بوصفها مصدرًا للمخاطر',
                  'تأثر المنتج A (MG) 3 مرات خلال 7 سنوات بمادة مكافحة النواقل التي تستخدمها البلدية لمكافحة البعوض. '
                  'وكانت 50% من المناحل المتضررة قريبة من غابة طبيعية — لا من محاصيل — ما يشير إلى التلوث بفعل انجراف '
                  'الرذاذ إلى مسافات تتجاوز 1km.'],
                 ['🟢',
                  'نقص التسجيل في الأنظمة الرسمية',
                  'لم تكن قد نُشرت أي بيانات وطنية رسمية عن نفوق النحل في فالي دو بارايبا قبل هذا البحث. وأكد المسح '
                  'الريادي باستخدام Google Forms (Alves, 2022) تزايد النفوق بين 2015-2022، من دون سجل أكاديمي سابق.'],
                 ['🔵',
                  'فيضانات RS تفاقم الوضع (2024)',
                  'دمّرت فيضانات مايو/يونيو 2024 في ريو غراندي دو سول أكثر من 6,300 خلية، مضيفةً الأحداث المناخية '
                  'المتطرفة إلى قائمة مصادر المخاطر الجديدة على تربية النحل في البرازيل.']],
 'conclusion_label': 'الخلاصة العلمية',
 'conclusion_title': 'تأكيد الفرضية',
 'conclusion_text': 'تأكد أن استخدام المركبات الكيميائية الزراعية والحضرية هو السبب الرئيسي لنفوق مستعمرات النحل في '
                    'المناطق المدروسة. وتؤيد البيانات الفرضية القائلة إن البرازيل — أكبر مستهلك لمبيدات الآفات في '
                    'العالم — تواجه حالة من اضطراب انهيار المستعمرات (CCD) تتوزع إقليميًا، وتفاقمها غياب أنظمة الإبلاغ '
                    'الرسمية والخوف من الانتقام، ما يثني عن الإبلاغ عن الخسائر.',
 'conclusion_author': 'Amauri Almeida — أطروحة الإدارة البيئية، FATEC Jundiaí، 2022',
 'impact_title': 'النحل النافق حسب الحادثة (مقياس لوغاريتمي)',
 'field_label': 'بحث تطبيقي',
 'field_title': 'بحث تجاوز حدود الشاشة',
 'photos': [{'emoji': '🏛️',
             'titulo': 'متحف النحل — Cotia / Embu das Artes, SP',
             'desc': 'زيارة إلى متحف النحل. خلية Apis mellifera معروضة — النوع المحوري في هذا البحث.',
             'path': 'assets/foto_01_museu_apis.jpg',
             'legenda': 'خلية Apis mellifera · متحف النحل · Cotia / Embu das Artes, SP'},
            {'emoji': '💀',
             'titulo': 'نحل نافق — Guaratinguetá, SP · Oct/2021',
             'desc': 'نحل نافق في منحل يقع في بلدية Guaratinguetá، في أكتوبر 2021. دليل مباشر على حادثة الانهيار '
                     'المسجلة في هذا البحث.',
             'path': 'assets/foto_02_mortas_guaratingueta.jpg',
             'legenda': 'نحل نافق في Guaratinguetá · Oct/2021 · الصورة: J.F.A.'},
            {'emoji': '🗺️',
             'titulo': 'عالم النحل — خريطة تفاعلية للحياة',
             'desc': 'لوحة تفاعلية في متحف النحل تقدم ملخصًا شاملًا لدورة حياة النحل. مرجع تثقيفي استُخدم في الأطروحة.',
             'path': 'assets/foto_03_museu_mapa_vida.jpg',
             'legenda': 'خريطة تفاعلية لدورة الحياة · متحف النحل · SP'},
            {'emoji': '🌻',
             'titulo': 'Apis mellifera على زهرة دوار الشمس — FATEC Jundiaí',
             'desc': 'نحلة Apis mellifera على زهرة دوار الشمس في حديقة FATEC Jundiaí، حيث نوقشت الأطروحة وأُنجزت شهادة '
                     'الإدارة البيئية (المرتبة الثالثة في ENADE).',
             'path': 'assets/foto_04_apis_girassol_fatec.jpg',
             'legenda': 'Apis mellifera على زهرة دوار الشمس · حديقة FATEC Jundiaí · SP'},
            {'emoji': '🔬',
             'titulo': 'عالم النحل — التشريح',
             'desc': 'لوحة في متحف النحل تتضمن خريطة مفصلة لتشريح النحلة. مرجع مورفولوجي استُخدم لوصف الأنواع '
                     'المدروسة.',
             'path': 'assets/foto_05_museu_anatomia.jpg',
             'legenda': 'خريطة تشريح النحلة · متحف النحل · SP'},
            {'emoji': '🏺',
             'titulo': 'رسم كهفي — 500 قبل الميلاد · جمع العسل',
             'desc': 'رسم كهفي يعود إلى 500 قبل الميلاد يصور أشخاصًا يجمعون العسل. توثّق العلاقة بين البشر والنحل منذ '
                     'آلاف السنين.',
             'path': 'assets/foto_06_rupestre_500ac.jpg',
             'legenda': 'رسم كهفي · 500 قبل الميلاد · علاقة البشر بالنحل'},
            {'emoji': '🌍',
             'titulo': 'صائد العسل — Rhodesia، جنوب أفريقيا · 8,000 سنة',
             'desc': 'لوحة تصور صائد عسل في Rhodesia (زيمبابوي حاليًا)، جنوب أفريقيا. يعود تاريخ العمل الفني إلى نحو '
                     '8,000 سنة.',
             'path': 'assets/foto_07_cacador_mel_rodesia.jpg',
             'legenda': 'صائد العسل · Rhodesia، جنوب أفريقيا · نحو 8,000 سنة'},
            {'emoji': '🪨',
             'titulo': 'رسم كهفي — Castellón، إسبانيا · +10,000 سنة',
             'desc': 'رسم كهفي اكتُشف في Castellón، إسبانيا. رسم من العصر الحجري القديم يعود إلى أكثر من 10,000 سنة، '
                     'ويصور جمع العسل — وهو من أقدم التصاوير البشرية لتربية النحل.',
             'path': 'assets/foto_08_rupestre_castellon.jpg',
             'legenda': 'رسم من العصر الحجري القديم · Castellón، إسبانيا · +10,000 سنة'}],
 'timeline_field_label': 'سياق المقابلات',
 'timeline_field_items': [['Apr 2022',
                           'مقابلة المنتج A',
                           'جنوب ميناس جيرايس · WhatsApp والبريد الإلكتروني · منحل قرب منطقة سكنية تأثرت بمادة مكافحة '
                           'النواقل البلدية'],
                          ['Apr 2022',
                           'مقابلة المنتج B',
                           'فالي دو بارايبا، SP · Instagram والبريد الإلكتروني · منحل قرب قطع أراضٍ عولجت بمبيد أعشاب '
                           'جهازي'],
                          ['May 2022',
                           'مقابلة المنتج C',
                           'وسط بارانا · Instagram والبريد الإلكتروني · منحل كبير قرب منطقة زراعة أحادية'],
                          ['Jun 2022',
                           'مقابلة المنتج D',
                           'وسط بارانا · Instagram والبريد الإلكتروني · أكبر خسارة فردية: 300 خلية في 2019'],
                          ['Jun 2022',
                           'مناقشة الأطروحة',
                           'FATEC Jundiaí, SP · المشرف: Prof. Me. Claudio da Cunha · الإدارة البيئية'],
                          ['Oct 2021',
                           'زيارة متحف النحل',
                           'Cotia / Embu das Artes, SP · سجلات فوتوغرافية ومراجع علمية للأطروحة']],
 'sources_label': 'المراجع العلمية',
 'sources_title': 'المصادر وقواعد البيانات',
 'field_instrucoes_title': 'كيفية إجراء هذا البحث',
 'field_instrucoes': 'أُجريت مقابلات مع مربي نحل من مناطق MG وSP وPR عبر WhatsApp وInstagram والبريد الإلكتروني. '
                     'وحُفظت سرية هويات المنتجين وفقًا للبروتوكول العلمي. جُدولت البيانات في Excel وقورنت بالأدبيات '
                     'العلمية (Google Scholar، IBAMA، EMBRAPA، APTA).',
 'tech_label': 'التقنيات المستخدمة',
 'footer_title': '🐝 Amauri Almeida',
 'footer_desc': 'اختصاصي تقني في الإدارة البيئية · FATEC Jundiaí (المرتبة الثالثة في ENADE)<br>دراسات عليا في الذكاء '
                'الاصطناعي والتعلم الآلي وعلوم البيانات · دراسات عليا في علوم البيانات والبيانات الضخمة<br>تحليل النظم '
                'وتطويرها · FACINT Maringá',
 'footer_links': '📍 البرازيل · تشيلي · الأرجنتين'},

    'de': {'page_title': 'Bienensterben · Brasilien',
 'hero_tag': 'Abschlussarbeit · FATEC Jundiaí · Umweltmanagement · 2022',
 'hero_title': 'Bienensterben\nin Brasilien',
 'hero_subtitle': 'Analyse des Bienensterbens infolge landwirtschaftlicher chemischer Verbindungen und Klimaereignisse '
                  'in 3 brasilianischen Regionen (2016–2022). Die Forschung umfasst 338 Bienenstöcke und ~20 Millionen '
                  'Bienen.',
 'badge1': '🐝 338 Bienenstöcke',
 'badge2': '~20 Mio. Bienen',
 'badge3': 'MG · SP · PR · RS',
 'badge4': '2016 — 2022',
 'badge5': 'FATEC JUNDIAÍ · 3. ENADE',
 'protocol_title': '📋 Hinweis zum wissenschaftlichen Protokoll:',
 'protocol_text': 'Die Handelsnamen der in dieser Forschung identifizierten chemischen Verbindungen wurden auf Wunsch '
                  'der befragten Imkerinnen und Imker sowie aus rechtlichen Vorsichtsgründen weggelassen und durch '
                  'allgemeine technische Kategorien ersetzt. Die vollständigen Daten sind in der '
                  'Originalabschlussarbeit verfügbar, die bei FATEC Jundiaí hinterlegt ist (2022).',
 'm1': 'Verlorene Bienenstöcke',
 'm2': 'Verlorene Bienen (geschätzt)',
 'm3': 'Überwachte Imkerinnen und Imker',
 'm4': 'Bienenstöcke in RS (2024)',
 'tab1': '🗺️ Karte & Analyse',
 'tab2': '🔬 Methodik & Prozessablauf',
 'tab3': '💡 Erkenntnisse',
 'tab4': '📷 Feldforschung',
 'tab5': '📚 Quellen & Danksagungen',
 'map_label': 'GEORÄUMLICHE VISUALISIERUNG',
 'map_title': 'Verteilung der Verluste in Brasilien',
 'map_hint': '🐝 <strong>Interaktion:</strong> Klicken Sie auf eine Markierung, um Details zum Standort und den '
             'Sammelradius von 2 km für <em>Apis mellifera</em> anzuzeigen.',
 'temporal_label': 'ZEITLICHE ANALYSE',
 'temporal_title': 'Entwicklung der Verluste nach Jahr',
 'bar_title': 'Verlorene Bienenstöcke pro Jahr (2016–2022)',
 'bar_y': 'Verlorene Bienenstöcke',
 'prod_title': 'Gesamtzahl nach Imker/in',
 'pie_title': 'Verteilung nach Ursachenkategorie',
 'timeline_label': 'ZEITACHSE NACH IMKER/IN',
 'timeline_title': 'Detaillierter Ereignisverlauf',
 'select_producer': 'Imker/in auswählen',
 'method_label': 'WISSENSCHAFTLICHE FORSCHUNG',
 'method_title': 'Fragestellung & Methodik',
 'sci_question_title': '❓ Zentrale wissenschaftliche Fragestellung',
 'sci_question': '„Besteht zwischen der Verwendung landwirtschaftlicher und städtischer chemischer Verbindungen in '
                 'Süd-Minas Gerais, Vale do Paraíba (SP) und Zentralparaná ein Zusammenhang mit der Sterblichkeit von '
                 'Bienenvölkern zwischen 2016 und 2022?“',
 'pipeline_label': 'DATENPROZESS',
 'steps': [['1',
            'Datenerhebung — Feldinterviews',
            'Interviews mit 9 Imkerinnen und Imkern über WhatsApp, Instagram und E-Mail. Rückmeldungen von 4 Personen '
            '(Anonymität gemäß Protokoll gewährleistet). Bezeichnet als Imker/in A (MG), B (SP), C und D (PR).'],
           ['2',
            'Datenerhebung — Literaturrecherche',
            'Recherche wissenschaftlicher Literatur zu CCD (Colony Collapse Disorder), Organophosphaten, '
            'Neonicotinoiden und Fungiziden. Datenbanken: Google Scholar, IBAMA, EMBRAPA, APTA.'],
           ['3',
            'Datenverarbeitung — Tabellierung',
            'Interviewdaten wurden in Microsoft Excel tabellarisch erfasst. Abgleich mit einer regionalen Karte des '
            'Vale do Paraíba (IBGE 2006) und Daten zum Pestizideinsatz nach Gemeinde (Bombardini, 2017 — FFLCH/USP).'],
           ['4',
            'Datenverarbeitung — Georeferenzierung',
            'Orte wurden geografischen Koordinaten zugeordnet, um sie mit Folium auf einer Karte darzustellen. '
            'Berechnung der Sammelradien nach Art (Jataí: 600 m; Apis mellifera: 5 km) gemäß EMBRAPA (2021).'],
           ['5',
            'Analyse — Qualitativ-quantitativer Ansatz',
            'Hypothetisch-deduktive Methode. Deskriptive Analyse der Verluste nach Jahr, Imker/in und Ursache. '
            'Abgleich der Sterblichkeitsmuster mit den in der Literatur beschriebenen Mustern des Einsatzes chemischer '
            'Verbindungen (RT25/RT40 — IBAMA 2012).'],
           ['6',
            'Visualisierung & Veröffentlichung',
            'Interaktives Dashboard, entwickelt mit Python (Streamlit + Plotly + Folium). Georäumliche Kartierung mit '
            'Markierungen, deren Größe proportional zu den Verlusten ist.']],
 'species_title': '🐝 Arten und Sammelradien',
 'species_text': '• <b>Jataí</b> (Tetragonisca angustula): bis zu 600 m — 1.13 km²<br>• <b>Mandaguari</b> '
                 '(Scaptotrigona xanthotricha): bis zu 900 m — 2.54 km²<br>• <b>Mandaçaia</b> (Melipona '
                 'quadrifasciata): bis zu 2,500 m — 19.63 km²<br>• <b>Apis mellifera</b>: bis zu 5,000 m — 78.5 km²',
 'species_source': 'Quelle: EMBRAPA, 2021',
 'compounds_title': '⚗️ Identifizierte Verbindungskategorien',
 'compounds_text': '• <b>Städtisches Vektorkontrollmittel</b>: Organophosphat-Insektizid zur Mückenbekämpfung in '
                   'städtischen Gebieten. Ausgebracht durch kommunale Fahrzeuge.<br>• <b>Systemisches Herbizid</b>: '
                   'Breitbandherbizid, das auf unbebauten Grundstücken und an Grundstücksrändern eingesetzt wird. '
                   'Beseitigt Nektarquellen.<br>• <b>Insektizid für Monokulturen</b>: Landwirtschaftliches Pestizid, '
                   'das auf Soja- und Maisfeldern in der Nähe von Bienenständen eingesetzt wird. Direkter Kontakt '
                   'durch Abdrift beim Spritzen.',
 'compounds_note': 'Handelsnamen weggelassen — siehe Hinweis zum Protokoll oben auf der Seite',
 'discovery_label': 'FORSCHUNGSERGEBNISSE',
 'discovery_title': 'Was die Daten zeigten',
 'discoveries': [['🔴',
                  'Höchststand der Sterblichkeit im Jahr 2019',
                  'Imker/in D (PR) verlor in einem einzigen Jahr 300 Bienenstöcke — etwa 18 Millionen Bienen. Das '
                  'Ereignis stand im Zusammenhang mit dem Versprühen von Insektiziden auf einer angrenzenden '
                  'Monokulturplantage. Dies entspricht 88.9% aller im Zeitraum 2016-2022 erfassten Verluste.'],
                 ['🟠',
                  'Systematische Untererfassung festgestellt',
                  'Von 9 kontaktierten Imkerinnen und Imkern antworteten nur 4. Das größte Hindernis war die Angst vor '
                  'Repressalien: 62.5% der Verluste wurden den zuständigen Behörden (GEDAVE, Umweltpolizei) nie '
                  'gemeldet.'],
                 ['🟡',
                  'Städtische Umwelt als Risikofaktor',
                  'Imker/in A (MG) war innerhalb von 7 Jahren dreimal dem kommunalen Mittel zur Mückenbekämpfung '
                  'ausgesetzt. 50% der betroffenen Bienenstände lagen in der Nähe von Naturwald — nicht von '
                  'Anbauflächen —, was auf Kontamination durch Abdrift über Entfernungen von mehr als 1 km hindeutet.'],
                 ['🟢',
                  'Unvollständige Erfassung in offiziellen Systemen',
                  'Vor dieser Forschung waren keine offiziellen nationalen Daten zur Bienensterblichkeit im Vale do '
                  'Paraíba veröffentlicht worden. Die wegweisende Google-Forms-Erhebung (Alves, 2022) bestätigte eine '
                  'zunehmende Sterblichkeit zwischen 2015-2022, die zuvor in keiner wissenschaftlichen Arbeit '
                  'dokumentiert worden war.'],
                 ['🔵',
                  'Überschwemmungen in RS verschärfen die Lage (2024)',
                  'Die Überschwemmungen im Mai/Juni 2024 in Rio Grande do Sul zerstörten mehr als 6,300 Bienenstöcke '
                  'und machten extreme Klimaereignisse zu einem neuen Risikofaktor für die brasilianische Imkerei.']],
 'conclusion_label': 'WISSENSCHAFTLICHES FAZIT',
 'conclusion_title': 'Hypothese bestätigt',
 'conclusion_text': 'Die Verwendung landwirtschaftlicher und städtischer chemischer Verbindungen wurde als '
                    'Hauptursache für die Sterblichkeit von Bienenvölkern in den untersuchten Regionen bestätigt. Die '
                    'Daten stützen die Hypothese, dass Brasilien — der weltweit größte Pestizidverbraucher — mit einem '
                    'regional verbreiteten Prozess des Bienensterbens (CCD) konfrontiert ist, der durch das Fehlen '
                    'offizieller Meldesysteme und die Angst vor Repressalien, die von Verlustmeldungen abhält, '
                    'verschärft wird.',
 'conclusion_author': 'Amauri Almeida — Abschlussarbeit im Fach Umweltmanagement, FATEC Jundiaí, 2022',
 'impact_title': 'Verlorene Bienen nach Ereignis (logarithmische Skala)',
 'field_label': 'ANGEWANDTE FORSCHUNG',
 'field_title': 'Forschung außerhalb des Bildschirms',
 'photos': [{'emoji': '🏛️',
             'titulo': 'Bienenmuseum — Cotia / Embu das Artes, SP',
             'desc': 'Besuch im Bienenmuseum. Ausgestellter Bienenstock von Apis mellifera — der zentralen Art dieser '
                     'Forschung.',
             'path': 'assets/foto_01_museu_apis.jpg',
             'legenda': 'Bienenstock von Apis mellifera · Bienenmuseum · Cotia / Embu das Artes, SP'},
            {'emoji': '💀',
             'titulo': 'Tote Bienen — Guaratinguetá, SP · Okt./2021',
             'desc': 'Tote Bienen in einem Bienenstand in der Gemeinde Guaratinguetá, Oktober 2021. Direkter Beleg für '
                     'das in dieser Forschung dokumentierte Zusammenbruchereignis.',
             'path': 'assets/foto_02_mortas_guaratingueta.jpg',
             'legenda': 'Tote Bienen in Guaratinguetá · Okt./2021 · Foto: J.F.A.'},
            {'emoji': '🗺️',
             'titulo': 'Die Welt der Bienen — Interaktive Lebenskarte',
             'desc': 'Interaktive Tafel im Bienenmuseum mit einer vollständigen Übersicht über den Lebenszyklus der '
                     'Bienen. Pädagogische Referenz in der Abschlussarbeit.',
             'path': 'assets/foto_03_museu_mapa_vida.jpg',
             'legenda': 'Interaktive Karte des Lebenszyklus · Bienenmuseum · SP'},
            {'emoji': '🌻',
             'titulo': 'Apis mellifera auf einer Sonnenblume — FATEC Jundiaí',
             'desc': 'Biene der Art Apis mellifera auf einer Sonnenblume im Garten der FATEC Jundiaí, wo die '
                     'Abschlussarbeit verteidigt und das Studium des Umweltmanagements abgeschlossen wurde (3. ENADE).',
             'path': 'assets/foto_04_apis_girassol_fatec.jpg',
             'legenda': 'Apis mellifera auf einer Sonnenblume · Garten der FATEC Jundiaí · SP'},
            {'emoji': '🔬',
             'titulo': 'Die Welt der Bienen — Anatomie',
             'desc': 'Tafel im Bienenmuseum mit einer detaillierten Darstellung der Bienenanatomie. Morphologische '
                     'Referenz zur Charakterisierung der untersuchten Arten.',
             'path': 'assets/foto_05_museu_anatomia.jpg',
             'legenda': 'Karte der Bienenanatomie · Bienenmuseum · SP'},
            {'emoji': '🏺',
             'titulo': 'Höhlenmalerei — 500 v. Chr. · Honigsammlung',
             'desc': 'Höhlenmalerei aus dem Jahr 500 v. Chr., die Menschen beim Honigsammeln zeigt. Die Beziehung '
                     'zwischen Mensch und Biene ist seit Jahrtausenden dokumentiert.',
             'path': 'assets/foto_06_rupestre_500ac.jpg',
             'legenda': 'Höhlenmalerei · 500 v. Chr. · Beziehung zwischen Mensch und Biene'},
            {'emoji': '🌍',
             'titulo': 'Honigjäger — Rhodesien, Südafrika · vor 8,000 Jahren',
             'desc': 'Tafel mit der Darstellung eines Honigjägers in Rhodesien (heute Simbabwe), Südafrika. Das '
                     'Kunstwerk wird auf ein Alter von etwa 8,000 Jahren datiert.',
             'path': 'assets/foto_07_cacador_mel_rodesia.jpg',
             'legenda': 'Honigjäger · Rhodesien, Südafrika · ~8,000 Jahre'},
            {'emoji': '🪨',
             'titulo': 'Höhlenmalerei — Castellón, Spanien · über 10,000 Jahre',
             'desc': 'In Castellón, Spanien, entdeckte Höhlenmalerei. Mehr als 10,000 Jahre alte paläolithische '
                     'Zeichnung, die das Sammeln von Honig darstellt — eine der frühesten menschlichen Darstellungen '
                     'der Imkerei.',
             'path': 'assets/foto_08_rupestre_castellon.jpg',
             'legenda': 'Paläolithische Zeichnung · Castellón, Spanien · über 10,000 Jahre'}],
 'timeline_field_label': 'KONTEXT DER INTERVIEWS',
 'timeline_field_items': [['Apr. 2022',
                           'Interview mit Imker/in A',
                           'Süd-Minas Gerais · WhatsApp und E-Mail · Bienenstand in der Nähe eines Wohngebiets, '
                           'betroffen durch ein kommunales Mittel zur Vektorkontrolle'],
                          ['Apr. 2022',
                           'Interview mit Imker/in B',
                           'Vale do Paraíba, SP · Instagram und E-Mail · Bienenstand in der Nähe von Grundstücken, auf '
                           'denen systemische Herbizide eingesetzt wurden'],
                          ['Mai 2022',
                           'Interview mit Imker/in C',
                           'Zentralparaná · Instagram und E-Mail · Großer Bienenstand in der Nähe einer Monokultur'],
                          ['Juni 2022',
                           'Interview mit Imker/in D',
                           'Zentralparaná · Instagram und E-Mail · Größter Einzelverlust: 300 Bienenstöcke im Jahr '
                           '2019'],
                          ['Juni 2022',
                           'Verteidigung der Abschlussarbeit',
                           'FATEC Jundiaí, SP · Betreuer: Prof. Me. Claudio da Cunha · Umweltmanagement'],
                          ['Okt. 2021',
                           'Besuch im Bienenmuseum',
                           'Cotia / Embu das Artes, SP · Fotodokumentation und wissenschaftliche Referenzen für die '
                           'Abschlussarbeit']],
 'sources_label': 'WISSENSCHAFTLICHE REFERENZEN',
 'sources_title': 'Quellen & Datenbank',
 'field_instrucoes_title': 'Durchführung der Forschung',
 'field_instrucoes': 'Interviews mit Imkerinnen und Imkern aus den Regionen MG, SP und PR über WhatsApp, Instagram und '
                     'E-Mail. Die Anonymität der Befragten wurde gemäß wissenschaftlichem Protokoll gewahrt. Die Daten '
                     'wurden in Excel tabellarisch erfasst und mit wissenschaftlicher Literatur abgeglichen (Google '
                     'Scholar, IBAMA, EMBRAPA, APTA).',
 'tech_label': 'VERWENDETE TECHNOLOGIEN',
 'footer_title': '🐝 Amauri Almeida',
 'footer_desc': 'Technologe für Umweltmanagement · FATEC Jundiaí (3. ENADE)<br>Postgraduiertenabschluss in KI, '
                'maschinellem Lernen & Data Science · Postgraduiertenabschluss in Data Science & Big '
                'Data<br>Systemanalyse und -entwicklung · FACINT Maringá',
 'footer_links': '📍 Brasilien · Chile · Argentinien'},

    'el': {'page_title': 'Κατάρρευση Αποικιών · Βραζιλία',
 'hero_tag': 'Διπλωματική εργασία · FATEC Jundiaí · Περιβαλλοντική Διαχείριση · 2022',
 'hero_title': 'Κατάρρευση Αποικιών\nστη Βραζιλία',
 'hero_subtitle': 'Ανάλυση της θνησιμότητας των μελισσών από χημικές ενώσεις γεωργικής χρήσης και κλιματικά φαινόμενα '
                  'σε 3 περιοχές της Βραζιλίας (2016–2022). Η έρευνα καλύπτει 338 κυψέλες και ~20 εκατομμύρια '
                  'μέλισσες.',
 'badge1': '🐝 338 Κυψέλες',
 'badge2': '~20M Μέλισσες',
 'badge3': 'MG · SP · PR · RS',
 'badge4': '2016 — 2022',
 'badge5': 'FATEC JUNDIAÍ · 3η ENADE',
 'protocol_title': '📋 Σημείωση επιστημονικού πρωτοκόλλου:',
 'protocol_text': 'Οι εμπορικές ονομασίες των χημικών ενώσεων που εντοπίστηκαν στην παρούσα έρευνα παραλείφθηκαν '
                  'κατόπιν αιτήματος των παραγωγών που συμμετείχαν στις συνεντεύξεις και για λόγους νομικής '
                  'προφύλαξης, και αντικαταστάθηκαν από γενικές τεχνικές κατηγορίες. Τα πλήρη δεδομένα είναι διαθέσιμα '
                  'στην πρωτότυπη διπλωματική εργασία που έχει κατατεθεί στη FATEC Jundiaí (2022).',
 'm1': 'Απωλεσθείσες κυψέλες',
 'm2': 'Απωλεσθείσες μέλισσες (εκτ.)',
 'm3': 'Παραγωγοί υπό παρακολούθηση',
 'm4': 'Κυψέλες στο RS (2024)',
 'tab1': '🗺️ Χάρτης & Ανάλυση',
 'tab2': '🔬 Μεθοδολογία & Ροή εργασιών',
 'tab3': '💡 Τι ανακαλύψαμε',
 'tab4': '📷 Επιτόπια έρευνα',
 'tab5': '📚 Πηγές & Συντελεστές',
 'map_label': 'ΓΕΩΧΩΡΙΚΗ ΑΠΕΙΚΟΝΙΣΗ',
 'map_title': 'Κατανομή απωλειών στη Βραζιλία',
 'map_hint': '🐝 <strong>Αλληλεπίδραση:</strong> Κάντε κλικ σε οποιονδήποτε δείκτη για να δείτε λεπτομέρειες της '
             'τοποθεσίας και την ακτίνα συλλογής τροφής 2km της <em>Apis mellifera</em>.',
 'temporal_label': 'ΧΡΟΝΙΚΗ ΑΝΑΛΥΣΗ',
 'temporal_title': 'Εξέλιξη απωλειών ανά έτος',
 'bar_title': 'Απωλεσθείσες κυψέλες ανά έτος (2016–2022)',
 'bar_y': 'Απωλεσθείσες κυψέλες',
 'prod_title': 'Σύνολο ανά παραγωγό',
 'pie_title': 'Κατανομή ανά κατηγορία αιτίας',
 'timeline_label': 'ΧΡΟΝΟΛΟΓΙΟ ΑΝΑ ΠΑΡΑΓΩΓΟ',
 'timeline_title': 'Αναλυτικό ιστορικό συμβάντων',
 'select_producer': 'Επιλέξτε παραγωγό',
 'method_label': 'ΕΠΙΣΤΗΜΟΝΙΚΗ ΕΡΕΥΝΑ',
 'method_title': 'Ερευνητικό ερώτημα & μεθοδολογία',
 'sci_question_title': '❓ Κεντρικό επιστημονικό ερώτημα',
 'sci_question': '«Συσχετίζεται η χρήση χημικών ενώσεων γεωργικής και αστικής χρήσης στη νότια Minas Gerais, στην Vale '
                 'do Paraíba (SP) και στην κεντρική Paraná με τη θνησιμότητα αποικιών μελισσών μεταξύ 2016 και 2022;»',
 'pipeline_label': 'ΡΟΗ ΕΠΕΞΕΡΓΑΣΙΑΣ ΔΕΔΟΜΕΝΩΝ',
 'steps': [['1',
            'Συλλογή — Επιτόπιες συνεντεύξεις',
            'Συνεντεύξεις με 9 μελισσοκόμους μέσω WhatsApp, Instagram και ηλεκτρονικού ταχυδρομείου. Απάντησαν 4 '
            'παραγωγοί (η ανωνυμία διασφαλίστηκε βάσει πρωτοκόλλου). Ταυτοποιήθηκαν ως Παραγωγός A (MG), B (SP), C και '
            'D (PR).'],
           ['2',
            'Συλλογή — Βιβλιογραφική ανασκόπηση',
            'Επισκόπηση της επιστημονικής βιβλιογραφίας σχετικά με το CCD (Colony Collapse Disorder), τα '
            'οργανοφωσφορικά, τα νεονικοτινοειδή και τα μυκητοκτόνα. Βάσεις δεδομένων: Google Scholar, IBAMA, EMBRAPA, '
            'APTA.'],
           ['3',
            'Επεξεργασία — Καταχώριση δεδομένων',
            'Τα δεδομένα των συνεντεύξεων καταχωρίστηκαν στο Microsoft Excel. Διασταυρώθηκαν με τον περιφερειακό χάρτη '
            'της Vale do Paraíba (IBGE 2006) και τα δεδομένα χρήσης φυτοφαρμάκων ανά δήμο (Bombardini, 2017 — '
            'FFLCH/USP).'],
           ['4',
            'Επεξεργασία — Γεωαναφορά',
            'Οι τοποθεσίες συσχετίστηκαν με γεωγραφικές συντεταγμένες για χαρτογράφηση μέσω Folium. Οι ακτίνες '
            'συλλογής τροφής υπολογίστηκαν ανά είδος (Jataí: 600m· Apis mellifera: 5km), σύμφωνα με την EMBRAPA '
            '(2021).'],
           ['5',
            'Ανάλυση — Ποιοτική και ποσοτική προσέγγιση',
            'Υποθετικοπαραγωγική μέθοδος. Περιγραφική ανάλυση των απωλειών ανά έτος, παραγωγό και αιτία. Διασταύρωση '
            'των προτύπων θνησιμότητας με τα πρότυπα χρήσης χημικών ενώσεων που καταγράφονται στη βιβλιογραφία '
            '(RT25/RT40 — IBAMA 2012).'],
           ['6',
            'Οπτικοποίηση & δημοσίευση',
            'Ανάπτυξη διαδραστικού πίνακα ελέγχου σε Python (Streamlit + Plotly + Folium). Γεωχωρική χαρτογράφηση με '
            'δείκτες ανάλογους προς τις απώλειες.']],
 'species_title': '🐝 Είδη και ακτίνες συλλογής τροφής',
 'species_text': '• <b>Jataí</b> (Tetragonisca angustula): έως 600m — 1.13 km²<br>• <b>Mandaguari</b> (Scaptotrigona '
                 'xanthotricha): έως 900m — 2.54 km²<br>• <b>Mandaçaia</b> (Melipona quadrifasciata): έως 2,500m — '
                 '19.63 km²<br>• <b>Apis mellifera</b>: έως 5,000m — 78.5 km²',
 'species_source': 'Πηγή: EMBRAPA, 2021',
 'compounds_title': '⚗️ Κατηγορίες ενώσεων που εντοπίστηκαν',
 'compounds_text': '• <b>Παράγοντας αστικού ελέγχου διαβιβαστών</b>: οργανοφωσφορικό εντομοκτόνο που χρησιμοποιείται '
                   'για τον έλεγχο των κουνουπιών σε αστικά κέντρα. Εφαρμόζεται από δημοτικά οχήματα.<br>• '
                   '<b>Συστημικό ζιζανιοκτόνο</b>: ζιζανιοκτόνο ευρέος φάσματος που χρησιμοποιείται σε αδόμητα '
                   'οικόπεδα και στα όρια ιδιοκτησιών. Εξαλείφει τις πηγές νέκταρος.<br>• <b>Εντομοκτόνο '
                   'μονοκαλλιεργειών</b>: γεωργικό φυτοφάρμακο που χρησιμοποιείται σε καλλιέργειες σόγιας και '
                   'καλαμποκιού κοντά σε μελισσοκομεία. Άμεση επαφή μέσω μεταφοράς ψεκαστικού νέφους.',
 'compounds_note': 'Οι εμπορικές ονομασίες παραλείπονται — δείτε τη σημείωση πρωτοκόλλου στην κορυφή της σελίδας',
 'discovery_label': 'ΕΡΕΥΝΗΤΙΚΑ ΑΠΟΤΕΛΕΣΜΑΤΑ',
 'discovery_title': 'Τι αποκάλυψαν τα δεδομένα',
 'discoveries': [['🔴',
                  'Κορύφωση θνησιμότητας το 2019',
                  'Ο Παραγωγός D (PR) έχασε 300 κυψέλες σε ένα μόνο έτος — περίπου 18 εκατομμύρια μέλισσες. Το συμβάν '
                  'συνδέθηκε με ψεκασμό εντομοκτόνου σε παρακείμενη φυτεία μονοκαλλιέργειας. Αντιστοιχεί στο 88.9% του '
                  'συνόλου των απωλειών που καταγράφηκαν την περίοδο 2016-2022.'],
                 ['🟠',
                  'Διαπιστώθηκε συστηματική υποκαταγραφή',
                  'Από τους 9 παραγωγούς που προσεγγίστηκαν, απάντησαν μόνο 4. Το κυριότερο εμπόδιο ήταν ο φόβος '
                  'αντιποίνων: το 62.5% των απωλειών δεν αναφέρθηκε ποτέ στις αρμόδιες αρχές (GEDAVE, Περιβαλλοντική '
                  'Αστυνομία).'],
                 ['🟡',
                  'Το αστικό περιβάλλον ως παράγοντας κινδύνου',
                  'Ο Παραγωγός A (MG) επηρεάστηκε 3 φορές μέσα σε 7 χρόνια από τον παράγοντα ελέγχου διαβιβαστών που '
                  'χρησιμοποιούσε ο δήμος για την καταπολέμηση των κουνουπιών. Το 50% των μελισσοκομείων που '
                  'επηρεάστηκαν βρίσκονταν κοντά σε αυτοφυές δάσος — όχι σε καλλιέργειες — γεγονός που υποδηλώνει '
                  'μόλυνση από μεταφορά ψεκαστικού νέφους σε αποστάσεις άνω του 1km.'],
                 ['🟢',
                  'Υποκαταγραφή στα επίσημα συστήματα',
                  'Πριν από την παρούσα έρευνα, δεν είχαν δημοσιευτεί επίσημα εθνικά δεδομένα για τη θνησιμότητα των '
                  'μελισσών στην Vale do Paraíba. Η πρωτοποριακή έρευνα μέσω Google Forms (Alves, 2022) επιβεβαίωσε '
                  'την αύξηση της θνησιμότητας μεταξύ 2015-2022, χωρίς προηγούμενη ακαδημαϊκή καταγραφή.'],
                 ['🔵',
                  'Οι πλημμύρες στο RS επιδεινώνουν την κατάσταση (2024)',
                  'Οι πλημμύρες του Μαΐου/Ιουνίου 2024 στο Rio Grande do Sul κατέστρεψαν περισσότερες από 6,300 '
                  'κυψέλες, προσθέτοντας τα ακραία κλιματικά φαινόμενα ως νέο παράγοντα κινδύνου για τη μελισσοκομία '
                  'της Βραζιλίας.']],
 'conclusion_label': 'ΕΠΙΣΤΗΜΟΝΙΚΟ ΣΥΜΠΕΡΑΣΜΑ',
 'conclusion_title': 'Η υπόθεση επιβεβαιώθηκε',
 'conclusion_text': 'Η χρήση χημικών ενώσεων γεωργικής και αστικής χρήσης επιβεβαιώθηκε ως κύρια αιτία θνησιμότητας '
                    'των αποικιών μελισσών στις περιοχές που μελετήθηκαν. Τα δεδομένα επιβεβαιώνουν την υπόθεση ότι η '
                    'Βραζιλία — η χώρα με τη μεγαλύτερη κατανάλωση φυτοφαρμάκων παγκοσμίως — αντιμετωπίζει μια '
                    'περιφερειακά κατανεμημένη διαδικασία Κατάρρευσης Αποικιών (CCD), η οποία επιδεινώνεται από την '
                    'απουσία επίσημων συστημάτων αναφοράς και τον φόβο αντιποίνων που αποθαρρύνει την αναφορά '
                    'απωλειών.',
 'conclusion_author': 'Amauri Almeida — Διπλωματική εργασία Περιβαλλοντικής Διαχείρισης, FATEC Jundiaí, 2022',
 'impact_title': 'Απωλεσθείσες μέλισσες ανά συμβάν (λογαριθμική κλίμακα)',
 'field_label': 'ΕΦΑΡΜΟΣΜΕΝΗ ΕΡΕΥΝΑ',
 'field_title': 'Η έρευνα πέρασε από την οθόνη στην πράξη',
 'photos': [{'emoji': '🏛️',
             'titulo': 'Μουσείο Μελισσών — Cotia / Embu das Artes, SP',
             'desc': 'Επίσκεψη στο Μουσείο Μελισσών. Κυψέλη Apis mellifera σε έκθεση — το κεντρικό είδος της παρούσας '
                     'έρευνας.',
             'path': 'assets/foto_01_museu_apis.jpg',
             'legenda': 'Κυψέλη Apis mellifera · Μουσείο Μελισσών · Cotia / Embu das Artes, SP'},
            {'emoji': '💀',
             'titulo': 'Νεκρές μέλισσες — Guaratinguetá, SP · Οκτ/2021',
             'desc': 'Νεκρές μέλισσες σε μελισσοκομείο στον δήμο Guaratinguetá, Οκτώβριος 2021. Άμεση τεκμηρίωση του '
                     'συμβάντος κατάρρευσης που καταγράφηκε στην παρούσα έρευνα.',
             'path': 'assets/foto_02_mortas_guaratingueta.jpg',
             'legenda': 'Νεκρές μέλισσες στην Guaratinguetá · Οκτ/2021 · Φωτογραφία: J.F.A.'},
            {'emoji': '🗺️',
             'titulo': 'Ο κόσμος των μελισσών — Διαδραστικός χάρτης ζωής',
             'desc': 'Διαδραστικό έκθεμα στο Μουσείο Μελισσών με πλήρη επισκόπηση του κύκλου ζωής της μέλισσας. '
                     'Εκπαιδευτικό υλικό αναφοράς που χρησιμοποιήθηκε στη διπλωματική εργασία.',
             'path': 'assets/foto_03_museu_mapa_vida.jpg',
             'legenda': 'Διαδραστικός χάρτης κύκλου ζωής · Μουσείο Μελισσών · SP'},
            {'emoji': '🌻',
             'titulo': 'Apis mellifera σε ηλίανθο — FATEC Jundiaí',
             'desc': 'Μέλισσα Apis mellifera σε ηλίανθο στον κήπο της FATEC Jundiaí, όπου υποστηρίχθηκε η διπλωματική '
                     'εργασία και ολοκληρώθηκε το πρόγραμμα Περιβαλλοντικής Διαχείρισης (3η ENADE).',
             'path': 'assets/foto_04_apis_girassol_fatec.jpg',
             'legenda': 'Apis mellifera σε ηλίανθο · Κήπος FATEC Jundiaí · SP'},
            {'emoji': '🔬',
             'titulo': 'Ο κόσμος των μελισσών — Ανατομία',
             'desc': 'Έκθεμα του Μουσείου Μελισσών με λεπτομερή χάρτη της ανατομίας της μέλισσας. Μορφολογικό υλικό '
                     'αναφοράς που χρησιμοποιήθηκε για τον χαρακτηρισμό των ειδών που μελετήθηκαν.',
             'path': 'assets/foto_05_museu_anatomia.jpg',
             'legenda': 'Χάρτης ανατομίας μέλισσας · Μουσείο Μελισσών · SP'},
            {'emoji': '🏺',
             'titulo': 'Βραχογραφία — 500 π.Χ. · Συλλογή μελιού',
             'desc': 'Βραχογραφία του 500 π.Χ. που απεικονίζει ανθρώπους να συλλέγουν μέλι. Η ανθρώπινη σχέση με τις '
                     'μέλισσες τεκμηριώνεται εδώ και χιλιετίες.',
             'path': 'assets/foto_06_rupestre_500ac.jpg',
             'legenda': 'Βραχογραφία · 500 π.Χ. · Ανθρώπινη σχέση με τις μέλισσες'},
            {'emoji': '🌍',
             'titulo': 'Κυνηγός μελιού — Ροδεσία, Νότια Αφρική · 8,000 χρόνια',
             'desc': 'Έκθεμα που απεικονίζει έναν κυνηγό μελιού στη Ροδεσία (σημερινή Ζιμπάμπουε), στη νότια Αφρική. '
                     'Το έργο χρονολογείται περίπου 8,000 χρόνια πριν.',
             'path': 'assets/foto_07_cacador_mel_rodesia.jpg',
             'legenda': 'Κυνηγός μελιού · Ροδεσία, Νότια Αφρική · ~8,000 χρόνια'},
            {'emoji': '🪨',
             'titulo': 'Βραχογραφία — Castellón, Ισπανία · +10,000 χρόνια',
             'desc': 'Βραχογραφία που ανακαλύφθηκε στο Castellón της Ισπανίας. Παλαιολιθική απεικόνιση ηλικίας άνω των '
                     '10,000 ετών, που παρουσιάζει τη συλλογή μελιού — μία από τις παλαιότερες ανθρώπινες απεικονίσεις '
                     'της μελισσοκομίας.',
             'path': 'assets/foto_08_rupestre_castellon.jpg',
             'legenda': 'Παλαιολιθική απεικόνιση · Castellón, Ισπανία · +10,000 χρόνια'}],
 'timeline_field_label': 'ΠΛΑΙΣΙΟ ΣΥΝΕΝΤΕΥΞΕΩΝ',
 'timeline_field_items': [['Απρ 2022',
                           'Συνέντευξη με τον Παραγωγό A',
                           'Νότια Minas Gerais · WhatsApp και ηλεκτρονικό ταχυδρομείο · Μελισσοκομείο κοντά σε '
                           'κατοικημένη περιοχή, επηρεασμένο από τον δημοτικό παράγοντα ελέγχου διαβιβαστών'],
                          ['Απρ 2022',
                           'Συνέντευξη με τον Παραγωγό B',
                           'Vale do Paraíba, SP · Instagram και ηλεκτρονικό ταχυδρομείο · Μελισσοκομείο κοντά σε '
                           'οικόπεδα όπου χρησιμοποιήθηκε συστημικό ζιζανιοκτόνο'],
                          ['Μάι 2022',
                           'Συνέντευξη με τον Παραγωγό C',
                           'Κεντρική Paraná · Instagram και ηλεκτρονικό ταχυδρομείο · Μεγάλο μελισσοκομείο κοντά σε '
                           'μονοκαλλιέργεια'],
                          ['Ιούν 2022',
                           'Συνέντευξη με τον Παραγωγό D',
                           'Κεντρική Paraná · Instagram και ηλεκτρονικό ταχυδρομείο · Η μεγαλύτερη μεμονωμένη απώλεια: '
                           '300 κυψέλες το 2019'],
                          ['Ιούν 2022',
                           'Υποστήριξη διπλωματικής εργασίας',
                           'FATEC Jundiaí, SP · Επιβλέπων: Prof. Me. Claudio da Cunha · Περιβαλλοντική Διαχείριση'],
                          ['Οκτ 2021',
                           'Επίσκεψη στο Μουσείο Μελισσών',
                           'Cotia / Embu das Artes, SP · Φωτογραφική τεκμηρίωση και επιστημονικές αναφορές για τη '
                           'διπλωματική εργασία']],
 'sources_label': 'ΕΠΙΣΤΗΜΟΝΙΚΕΣ ΑΝΑΦΟΡΕΣ',
 'sources_title': 'Πηγές & βάση δεδομένων',
 'field_instrucoes_title': 'Πώς διεξήχθη η έρευνα',
 'field_instrucoes': 'Οι συνεντεύξεις πραγματοποιήθηκαν μέσω WhatsApp, Instagram και ηλεκτρονικού ταχυδρομείου με '
                     'μελισσοκόμους από τις περιοχές MG, SP και PR. Οι παραγωγοί παρέμειναν ανώνυμοι σύμφωνα με το '
                     'επιστημονικό πρωτόκολλο. Τα δεδομένα καταχωρίστηκαν στο Excel και διασταυρώθηκαν με την '
                     'επιστημονική βιβλιογραφία (Google Scholar, IBAMA, EMBRAPA, APTA).',
 'tech_label': 'ΤΕΧΝΟΛΟΓΙΕΣ ΠΟΥ ΧΡΗΣΙΜΟΠΟΙΗΘΗΚΑΝ',
 'footer_title': '🐝 Amauri Almeida',
 'footer_desc': 'Τεχνολόγος Περιβαλλοντικής Διαχείρισης · FATEC Jundiaí (3η ENADE)<br>Μεταπτυχιακές σπουδές στην ΤΝ, '
                'τη Μηχανική Μάθηση & την Επιστήμη Δεδομένων · Μεταπτυχιακές σπουδές στην Επιστήμη Δεδομένων & τα '
                'Μεγάλα Δεδομένα<br>Ανάλυση και Ανάπτυξη Συστημάτων · FACINT Maringá',
 'footer_links': '📍 Βραζιλία · Χιλή · Αργεντινή'},

    'af': {'page_title': 'Kolonie-ineenstortingsversteuring · Brasilië',
 'hero_tag': 'Verhandeling · FATEC Jundiaí · Omgewingsbestuur · 2022',
 'hero_title': 'Kolonie-ineenstortingsversteuring\nin Brasilië',
 'hero_subtitle': 'Ontleding van byesterftes weens landbouchemiese verbindings en klimaatgebeure in 3 Brasiliaanse '
                  'streke (2016–2022). Navorsing oor 338 korwe en ~20 miljoen bye.',
 'badge1': '🐝 338 Korwe',
 'badge2': '~20M Bye',
 'badge3': 'MG · SP · PR · RS',
 'badge4': '2016 — 2022',
 'badge5': 'FATEC JUNDIAÍ · 3de ENADE',
 'protocol_title': '📋 Nota oor wetenskaplike protokol:',
 'protocol_text': 'Kommersiële name van die chemiese verbindings wat in hierdie navorsing geïdentifiseer is, is op '
                  'versoek van die produsente met wie onderhoude gevoer is, en uit regsoorwegings weggelaat en deur '
                  'generiese tegniese kategorieë vervang. Volledige data is beskikbaar in die oorspronklike '
                  'verhandeling wat by FATEC Jundiaí (2022) gedeponeer is.',
 'm1': 'Korwe verloor',
 'm2': 'Bye verloor (beram.)',
 'm3': 'Produsente gemonitor',
 'm4': 'RS-korwe (2024)',
 'tab1': '🗺️ Kaart & ontleding',
 'tab2': '🔬 Metodologie & pyplyn',
 'tab3': '💡 Wat ons gevind het',
 'tab4': '📷 Veldnavorsing',
 'tab5': '📚 Bronne & erkennings',
 'map_label': 'GEOSPATIALE VISUALISERING',
 'map_title': 'Verspreiding van verliese in Brasilië',
 'map_hint': '🐝 <strong>Interaksie:</strong> Klik op enige merker om besonderhede oor die ligging en die '
             '2km-vreetradius van <em>Apis mellifera</em> te sien.',
 'temporal_label': 'TYDELIKE ONTLEDING',
 'temporal_title': 'Ontwikkeling van verliese per jaar',
 'bar_title': 'Korwe per jaar verloor (2016–2022)',
 'bar_y': 'Korwe verloor',
 'prod_title': 'Totaal per produsent',
 'pie_title': 'Verspreiding volgens oorsaakkategorie',
 'timeline_label': 'TYDLYN PER PRODUSENT',
 'timeline_title': 'Gedetailleerde gebeurtenisgeskiedenis',
 'select_producer': 'Kies produsent',
 'method_label': 'WETENSKAPLIKE NAVORSING',
 'method_title': 'Navorsingsvraag & metodologie',
 'sci_question_title': '❓ Sentrale wetenskaplike vraag',
 'sci_question': '"Is die gebruik van landbou- en stedelike chemiese verbindings in Suid-Minas Gerais, Vale do Paraíba '
                 '(SP) en Sentraal-Paraná gekorreleer met byekoloniesterftes tussen 2016 en 2022?"',
 'pipeline_label': 'DATAPYPLYN',
 'steps': [['1',
            'Insameling — veldonderhoude',
            'Onderhoude met 9 byeboere via WhatsApp, Instagram en e-pos. Effektiewe reaksie van 4 produsente '
            '(anonimiteit gewaarborg deur protokol). Geïdentifiseer as Produsent A (MG), B (SP), C en D (PR).'],
           ['2',
            'Insameling — literatuuroorsig',
            'Oorsig van wetenskaplike literatuur oor CCD (Colony Collapse Disorder), organofosfate, neonikotinoïede en '
            'swamdoders. Databasisse: Google Scholar, IBAMA, EMBRAPA, APTA.'],
           ['3',
            'Verwerking — tabulering',
            'Onderhoudsdata is in Microsoft Excel getabuleer. Gekruisverwys met die streekskaart van Vale do Paraíba '
            '(IBGE 2006) en data oor plaagdodergebruik per munisipaliteit (Bombardini, 2017 — FFLCH/USP).'],
           ['4',
            'Verwerking — geoverwysing',
            'Ligginge is aan geografiese koördinate gekoppel vir kartering met Folium. Berekeninge van vreetradiusse '
            'per spesie (Jataí: 600m; Apis mellifera: 5km) volgens EMBRAPA (2021).'],
           ['5',
            'Ontleding — kwalitatief-kwantitatiewe benadering',
            'Hipoteties-deduktiewe metode. Beskrywende ontleding van verliese per jaar, produsent en oorsaak. '
            'Kruisverwysing tussen sterftepatrone en patrone van chemiese-verbindingsgebruik uit die literatuur '
            '(RT25/RT40 — IBAMA 2012).'],
           ['6',
            'Visualisering & publikasie',
            'Interaktiewe paneel ontwikkel in Python (Streamlit + Plotly + Folium). Georuimtelike kartering met '
            'merkers wat eweredig is aan verliese.']],
 'species_title': '🐝 Spesies en vreetradiusse',
 'species_text': '• <b>Jataí</b> (Tetragonisca angustula): tot 600m — 1.13 km²<br>• <b>Mandaguari</b> (Scaptotrigona '
                 'xanthotricha): tot 900m — 2.54 km²<br>• <b>Mandaçaia</b> (Melipona quadrifasciata): tot 2,500m — '
                 '19.63 km²<br>• <b>Apis mellifera</b>: tot 5,000m — 78.5 km²',
 'species_source': 'Bron: EMBRAPA, 2021',
 'compounds_title': '⚗️ Geïdentifiseerde verbindingskategorieë',
 'compounds_text': '• <b>Stedelike vektormiddel</b>: organofosfaat-insekdoder wat vir muskietbeheer in stedelike '
                   'sentra gebruik word. Word deur munisipale voertuie toegedien.<br>• <b>Sistemiese '
                   'onkruiddoderverbinding</b>: breëspektrumonkruiddoder wat op onbeboude erwe en langs eiendomsgrense '
                   'gebruik word. Skakel nektarbronne uit.<br>• <b>Monokultuur-insekdoder</b>: landbouplaagdoder wat '
                   'op sojaboon- en mieliegewasse naby byeplase gebruik word. Direkte kontak deur '
                   'spuitnewelverspreiding.',
 'compounds_note': 'Kommersiële name weggelaat — sien protokolnota boaan die bladsy',
 'discovery_label': 'NAVORSINGSRESULTATE',
 'discovery_title': 'Wat die data aan die lig gebring het',
 'discoveries': [['🔴',
                  'Sterftepiek in 2019',
                  'Produsent D (PR) het 300 korwe in ’n enkele jaar verloor — ongeveer 18 miljoen bye. Die gebeurtenis '
                  'is verbind met die bespuiting van insekdoder op ’n aangrensende monokultuurplantasie. Dit '
                  'verteenwoordig 88.9% van alle verliese wat in 2016-2022 aangeteken is.'],
                 ['🟠',
                  'Stelselmatige onderaanmelding geïdentifiseer',
                  'Van die 9 produsente wat gekontak is, het slegs 4 gereageer. Die grootste struikelblok was vrees '
                  'vir vergelding: 62.5% van verliese is nooit by bevoegde owerhede (GEDAVE, Omgewingspolisie) '
                  'aangemeld nie.'],
                 ['🟡',
                  'Stedelike omgewing as risikovektor',
                  'Produsent A (MG) is binne 7 jaar 3 keer deur die munisipale muskietbeheermiddel geraak. 50% van die '
                  'geaffekteerde byeplase was naby inheemse woud — nie gewasse nie — wat op besoedeling deur '
                  'spuitnewelverspreiding oor afstande van meer as 1km dui.'],
                 ['🟢',
                  'Onderregistrasie in amptelike stelsels',
                  'Geen amptelike nasionale data oor byesterftes in Vale do Paraíba is voor hierdie navorsing '
                  'gepubliseer nie. Die baanbrekersopname met Google Forms (Alves, 2022) het toenemende sterftes '
                  'tussen 2015-2022 bevestig, sonder enige voorafgaande akademiese dokumentasie.'],
                 ['🔵',
                  'RS-vloede vererger die situasie (2024)',
                  'Die vloede in Rio Grande do Sul in Mei/Junie 2024 het meer as 6,300 korwe verwoes en uiterste '
                  'klimaatgebeure as ’n nuwe risikovektor vir Brasiliaanse byeboerdery bygevoeg.']],
 'conclusion_label': 'WETENSKAPLIKE GEVOLGTREKKING',
 'conclusion_title': 'Hipotese bevestig',
 'conclusion_text': 'Die gebruik van landbou- en stedelike chemiese verbindings is bevestig as die hoofoorsaak van '
                    'byekoloniesterftes in die bestudeerde streke. Die data staaf die hipotese dat Brasilië — die '
                    'wêreld se grootste verbruiker van plaagdoders — ’n proses van kolonie-ineenstortingsversteuring '
                    '(CCD) ervaar wat streeksgewys versprei is en vererger word deur die afwesigheid van amptelike '
                    'aanmeldstelsels en die vrees vir vergelding wat die aanmelding van verliese belemmer.',
 'conclusion_author': 'Amauri Almeida — Verhandeling in Omgewingsbestuur, FATEC Jundiaí, 2022',
 'impact_title': 'Bye verloor per gebeurtenis (logaritmiese skaal)',
 'field_label': 'TOEGEPASTE NAVORSING',
 'field_title': 'Navorsing wat die skerm verlaat het',
 'photos': [{'emoji': '🏛️',
             'titulo': 'Byemuseum — Cotia / Embu das Artes, SP',
             'desc': 'Besoek aan die Byemuseum. ’n Apis mellifera-korf ten toon gestel — die sentrale spesie in '
                     'hierdie navorsing.',
             'path': 'assets/foto_01_museu_apis.jpg',
             'legenda': 'Apis mellifera-korf · Byemuseum · Cotia / Embu das Artes, SP'},
            {'emoji': '💀',
             'titulo': 'Dooie bye — Guaratinguetá, SP · Okt/2021',
             'desc': 'Dooie bye in ’n byeplaas in die munisipaliteit Guaratinguetá, Oktober 2021. Direkte bewys van '
                     'die ineenstortingsgebeurtenis wat in hierdie navorsing aangeteken is.',
             'path': 'assets/foto_02_mortas_guaratingueta.jpg',
             'legenda': 'Dooie bye in Guaratinguetá · Okt/2021 · Foto: J.F.A.'},
            {'emoji': '🗺️',
             'titulo': 'Die wêreld van bye — interaktiewe lewensikluskaart',
             'desc': 'Interaktiewe paneel by die Byemuseum met ’n volledige opsomming van die by se lewensiklus. '
                     'Opvoedkundige verwysingsbron wat in die verhandeling gebruik is.',
             'path': 'assets/foto_03_museu_mapa_vida.jpg',
             'legenda': 'Interaktiewe lewensikluskaart · Byemuseum · SP'},
            {'emoji': '🌻',
             'titulo': 'Apis mellifera op sonneblom — FATEC Jundiaí',
             'desc': 'Apis mellifera-by op ’n sonneblom in die tuin van FATEC Jundiaí, waar die verhandeling verdedig '
                     'is en die graad in Omgewingsbestuur voltooi is (3de ENADE).',
             'path': 'assets/foto_04_apis_girassol_fatec.jpg',
             'legenda': 'Apis mellifera op sonneblom · FATEC Jundiaí-tuin · SP'},
            {'emoji': '🔬',
             'titulo': 'Die wêreld van bye — anatomie',
             'desc': 'Paneel by die Byemuseum met ’n gedetailleerde kaart van by-anatomie. Morfologiese verwysing wat '
                     'gebruik is om die bestudeerde spesies te karakteriseer.',
             'path': 'assets/foto_05_museu_anatomia.jpg',
             'legenda': 'Kaart van by-anatomie · Byemuseum · SP'},
            {'emoji': '🏺',
             'titulo': 'Rotstekening — 500 v.C. · Heuningversameling',
             'desc': 'Rotstekening uit 500 v.C. wat mense wys wat heuning versamel. Die mens se verhouding met bye is '
                     'al millennia lank gedokumenteer.',
             'path': 'assets/foto_06_rupestre_500ac.jpg',
             'legenda': 'Rotstekening · 500 v.C. · Mens se verhouding met bye'},
            {'emoji': '🌍',
             'titulo': 'Heuningjagter — Rhodesië, Suid-Afrika · 8,000 jaar',
             'desc': 'Paneel wat ’n heuningjagter in Rhodesië (nou Zimbabwe), Suid-Afrika, uitbeeld. Die kunswerk '
                     'dateer uit ongeveer 8,000 jaar gelede.',
             'path': 'assets/foto_07_cacador_mel_rodesia.jpg',
             'legenda': 'Heuningjagter · Rhodesië, Suid-Afrika · ~8,000 jaar'},
            {'emoji': '🪨',
             'titulo': 'Rotstekening — Castellón, Spanje · +10,000 jaar',
             'desc': 'Rotstekening wat in Castellón, Spanje, ontdek is. Paleolitiese tekening van meer as 10,000 jaar '
                     'oud wat heuningversameling uitbeeld — een van die vroegste menslike uitbeeldings van '
                     'byeboerdery.',
             'path': 'assets/foto_08_rupestre_castellon.jpg',
             'legenda': 'Paleolitiese tekening · Castellón, Spanje · +10,000 jaar'}],
 'timeline_field_label': 'ONDERHOUDSKONTEKS',
 'timeline_field_items': [['Apr 2022',
                           'Onderhoud met produsent A',
                           'Suid-Minas Gerais · WhatsApp en e-pos · Byeplaas naby woongebied wat deur munisipale '
                           'vektormiddel geraak is'],
                          ['Apr 2022',
                           'Onderhoud met produsent B',
                           'Vale do Paraíba, SP · Instagram en e-pos · Byeplaas naby erwe waarop sistemiese '
                           'onkruiddoder gebruik is'],
                          ['Mei 2022',
                           'Onderhoud met produsent C',
                           'Sentraal-Paraná · Instagram en e-pos · Groot byeplaas naby monokultuur'],
                          ['Jun 2022',
                           'Onderhoud met produsent D',
                           'Sentraal-Paraná · Instagram en e-pos · Grootste individuele verlies: 300 korwe in 2019'],
                          ['Jun 2022',
                           'Verhandelingverdediging',
                           'FATEC Jundiaí, SP · Studieleier: Prof. Me. Claudio da Cunha · Omgewingsbestuur'],
                          ['Okt 2021',
                           'Besoek aan die Byemuseum',
                           'Cotia / Embu das Artes, SP · Fotografiese dokumentasie en wetenskaplike verwysings vir die '
                           'verhandeling']],
 'sources_label': 'WETENSKAPLIKE VERWYSINGS',
 'sources_title': 'Bronne & databasis',
 'field_instrucoes_title': 'Hoe hierdie navorsing uitgevoer is',
 'field_instrucoes': 'Onderhoude is via WhatsApp, Instagram en e-pos gevoer met byeboere uit die MG-, SP- en '
                     'PR-streke. Produsente se anonimiteit is volgens wetenskaplike protokol gehandhaaf. Data is in '
                     'Excel getabuleer en met wetenskaplike literatuur gekruisverwys (Google Scholar, IBAMA, EMBRAPA, '
                     'APTA).',
 'tech_label': 'GEBRUIKTE TEGNOLOGIEË',
 'footer_title': '🐝 Amauri Almeida',
 'footer_desc': 'Tegnoloog in Omgewingsbestuur · FATEC Jundiaí (3de ENADE)<br>Nagraadse kwalifikasie in KI, '
                'Masjienleer & Datawetenskap · Nagraadse kwalifikasie in Datawetenskap & Big Data<br>Stelselontleding '
                'en -ontwikkeling · FACINT Maringá',
 'footer_links': '📍 Brasilië · Chili · Argentinië'}
}
 
# ============================================================
# SELETOR DE IDIOMA — TOPO
# ============================================================
LANGUAGE_BUTTONS = [
    ("pt", "🇧🇷 PT"), ("es", "🇪🇸 ES"), ("en", "🇺🇸 EN"),
    ("it", "🇮🇹 IT"), ("zh", "🇨🇳 ZH"), ("fr", "🇫🇷 FR"),
    ("ar", "🇸🇦 AR"), ("de", "🇩🇪 DE"), ("el", "🇬🇷 EL"),
    ("af", "🇿🇦 AF"),
]

def render_lang_selector():
    # Mantém o seletor alinhado no topo e permite que os dez idiomas tenham o mesmo peso visual.
    columns = st.columns(len(LANGUAGE_BUTTONS))
    for column, (code, label) in zip(columns, LANGUAGE_BUTTONS):
        with column:
            if st.button(
                label,
                key=f"language_{code}",
                use_container_width=True,
                type="primary" if st.session_state.lang == code else "secondary",
            ):
                st.session_state.lang = code
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
 
    # A chave fica no Streamlit Secrets, nunca no código público.
    try:
        carto_key = st.secrets.get("CARTO_API_KEY", "")
    except Exception:
        carto_key = ""

    # tiles=None impede o Folium de adicionar uma camada base automaticamente.
    mapa = folium.Map(
        location=[-23.5, -50.5],
        zoom_start=6,
        tiles=None,
        control_scale=True,
    )

    if carto_key:
        folium.TileLayer(
            tiles=(
                "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/"
                "{z}/{x}/{y}{r}.png?key=" + carto_key
            ),
            attr=(
                '&copy; <a href="https://www.openstreetmap.org/copyright">'
                "OpenStreetMap</a> contributors &copy; "
                '<a href="https://carto.com/attributions">CARTO</a>'
            ),
            name="CARTO Voyager",
            subdomains="abcd",
            max_zoom=20,
            overlay=False,
            control=True,
        ).add_to(mapa)
    else:
        # Fallback: o app continua funcional sem o Secret configurado.
        folium.TileLayer(
            "OpenStreetMap",
            name="OpenStreetMap",
            attr=(
                '&copy; <a href="https://www.openstreetmap.org/copyright">'
                "OpenStreetMap</a> contributors"
            ),
            control=True,
        ).add_to(mapa)
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
