# 🐝 Síndrome do Colapso das Colônias de Abelhas — Brasil

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bee-colony-collapse-brazil.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: Academic](https://img.shields.io/badge/License-Academic-green.svg)]()
[![FATEC Jundiaí](https://img.shields.io/badge/TCC-FATEC_Jundiaí_·_3º_ENADE-C0392B)]()

> **Trabalho de Conclusão de Curso** — Tecnólogo em Gestão Ambiental  
> FATEC Jundiaí "Deputado Ary Fossen" · Centro Paula Souza · 2022  
> Autor: **Amauri Almeida** · Orientador: Prof. Me. Claudio da Cunha

---

## ❓ Pergunta Científica

> *"O uso de compostos químicos agrícolas e vetoriais nas regiões Sul de Minas Gerais, Vale do Paraíba (SP) e Região Central do Paraná está correlacionado com a mortalidade de colônias de abelhas entre 2016 e 2022?"*

**Resposta:** Sim. Os dados confirmam a hipótese com evidências de 338 colmeias e ~20 milhões de abelhas perdidas em eventos diretamente associados a três categorias de compostos químicos.

---

## 📊 Resultados Principais

| Indicador | Valor |
|---|---|
| Colmeias perdidas (2016–2022) | **338** |
| Abelhas perdidas (estimado) | **~20.110.700** |
| Produtores entrevistados | 9 (retorno: 4) |
| Taxa de subnotificação | **62,5%** dos casos não comunicados |
| Regiões cobertas | MG · SP · PR · RS (enchentes 2024) |

### 🔴 Descobertas Críticas

1. **Pico em 2019** — Produtor D (PR) perdeu 300 colmeias em um único evento (18M abelhas)
2. **Subnotificação sistêmica** — produtores temem represálias de proprietários rurais
3. **Risco urbano** — agente vetorial municipal afetou apiários próximos a mata nativa 3x em 7 anos
4. **Dado pioneiro** — primeiro levantamento sobre mortalidade de abelhas no Vale do Paraíba

---

## 🗺️ Cobertura Geográfica

```
Sul de Minas Gerais    → Produtor A (Extrema - MG)
Vale do Paraíba - SP   → Produtor B (Guaratinguetá - SP)
Central do Paraná      → Produtor C (Turvo - PR)
Central do Paraná      → Produtor D (Prudentópolis - PR)
Rio Grande do Sul      → 7 municípios (Enchentes 2024)
```

---

## 🔬 Metodologia

```
Coleta           →   Entrevistas com apicultores + revisão bibliográfica
                     (IBAMA, EMBRAPA, APTA, FFLCH-USP)
                     
Processamento    →   Tabulação Excel + georreferenciamento (Folium)
                     Cruzamento com mapa de uso de agrotóxicos (Bombardini, 2017)
                     
Análise          →   Método hipotético-dedutivo · abordagem quali-quantitativa
                     Raio de forrageamento por espécie (EMBRAPA, 2021)
                     
Visualização     →   Dashboard Streamlit + Plotly + Folium
```

> **Nota de protocolo:** Os nomes comerciais dos compostos químicos identificados foram omitidos nesta publicação por protocolo de anonimato acordado com os produtores entrevistados. Os dados completos estão disponíveis no TCC depositado na FATEC Jundiaí (2022).

---

## 🛠️ Stack Tecnológica

| Tecnologia | Uso |
|---|---|
| `Python 3.11` | Linguagem principal |
| `Streamlit` | Dashboard interativo |
| `Plotly` | Gráficos dinâmicos |
| `Folium` | Mapeamento geoespacial |
| `Pandas / NumPy` | Processamento de dados |

---

## 🚀 Como Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/amaurialmeida/bee-colony-collapse-brazil.git
cd bee-colony-collapse-brazil

# Instale as dependências
pip install -r requirements.txt

# Execute
streamlit run app.py
```

---

## 📚 Referências

- **IBAMA** — Relatório técnico de pesticidas e efeitos nas abelhas (2012)
- **EMBRAPA** — Meliponicultura Urbana (2021)
- **Bombardini, L.M.** (2017) — Geografia do Uso de Agrotóxicos no Brasil — FFLCH/USP
- **Alves, J.F.G.** (2022) — Levantamento de Mortalidade de Abelhas — UNITAU
- **APTA** — Síndrome do Colapso das Colônias das abelhas pesquisada pela APTA (2015)

---

## 🌿 Portfólio Ambiental

Este projeto é parte do portfólio de pesquisa ambiental do autor.  
🔗 [amaurialmeida.github.io/environmental-portfolio](https://amaurialmeida.github.io/environmental-portfolio/)

---

*© 2022–2026 · Amauri Almeida · Pesquisa Acadêmica · FATEC Jundiaí*
