# 🐝 Bee Colony Collapse Disorder — Brazil (2016–2022)

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?logo=streamlit&logoColor=white)](https://bee-colony-collapse-brazil.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: Academic](https://img.shields.io/badge/License-Academic-blue.svg)]()
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

🌐 **Languages:** English | [Português](README.pt-BR.md) | [Español](README.es.md)

**Undergraduate Thesis (TCC) — Environmental Management**
FATEC Jundiaí · São Paulo, Brazil · 2022
**Author:** Amauri Almeida de Souza Junior · **Advisor:** Prof. Me. Claudio da Cunha

> 📋 **Scientific protocol note:** The commercial names of the chemical compounds identified in this research were withheld from this publication at the request of the interviewed producers, and as a legal precaution — replaced here with generic technical categories. Complete data is available in the original thesis on file at FATEC Jundiaí (2022); academic access can be requested via the contact form.

---

## ❓ Research Question

> "Is the use of agricultural and vector-control chemical compounds in southern Minas Gerais, the Paraíba Valley (SP), and central Paraná correlated with bee colony mortality between 2016 and 2022?"

**Answer:** Yes. Chemical compound exposure — both agricultural and municipal vector-control — was confirmed as the primary driver of colony mortality across the studied regions. The findings support the hypothesis that Brazil, the world's largest consumer of agrochemicals, faces a regionally distributed Colony Collapse Disorder (CCD) process, worsened by the absence of official reporting systems and by producers' fear of retaliation, which suppresses loss reporting.

---

## 📊 Data Summary

| Indicator | Value |
|---|---|
| Hives lost (studied sample, 2016–2022) | 338 |
| Estimated bees lost | ~20,000,000 |
| Regions studied | Minas Gerais, São Paulo (Paraíba Valley), Paraná |
| Producers contacted / responded | 9 contacted → 4 responded |
| Monitoring period | 2016–2022 |
| RS floods (2024) — additional hives lost | 6,300+ |

---

## 🔵 Key Findings

- **Mortality peak in 2019** — Producer D (PR) lost 300 hives in a single year — approximately 18 million bees — linked to insecticide spraying on an adjacent monoculture farm, representing 88.9% of all losses recorded in the 2016–2022 period.
- **Systemic underreporting identified** — of 9 producers contacted, only 4 responded; the main barrier was fear of retaliation, with 62.5% of losses never reported to relevant authorities (GEDAVE, Environmental Police) — suggesting the real scale of the problem is significantly larger than available data shows.
- **Urban environment as a risk vector** — Producer A (MG) was affected three times in seven years by a municipal mosquito-control vector agent; 50% of affected apiaries were near native forest rather than farmland, indicating spray drift contamination beyond 1 km.
- **No prior official record** — no national data on bee mortality in the Paraíba Valley existed before this research; a pioneering Google Forms survey (Alves, 2022) confirmed rising mortality in the region from 2015–2022, with no prior academic record.
- **2024 Rio Grande do Sul floods amplify the risk landscape** — the May/June 2024 floods devastated 6,300+ additional hives, adding extreme weather events as a new risk vector for Brazilian beekeeping.

---

## 🗺️ Species & Foraging Radius

| Species | Foraging Radius | Coverage Area |
|---|---|---|
| Jataí (*Tetragonisca angustula*) | up to 600 m | 1.13 km² |
| Mandaguari (*Scaptotrigona xanthotricha*) | up to 900 m | 2.54 km² |
| Mandaçaia (*Melipona quadrifasciata*) | up to 2,500 m | 19.63 km² |
| *Apis mellifera* | up to 5,000 m | 78.5 km² |

*Source: EMBRAPA, 2021*

---

## ⚗️ Compound Categories Identified

- **Urban vector-control agent** — organophosphate insecticide used for mosquito control in urban centers, applied by municipal vehicles.
- **Systemic herbicide compound** — broad-spectrum herbicide used on vacant lots and property borders, eliminating nectar sources.
- **Monoculture insecticide** — agricultural pesticide used on soybean and corn crops near apiaries, with direct contact via spray drift.

*Commercial names withheld — see protocol note above.*

---

## 🔬 Methodology

```
Collection        →  Field interviews with 9 beekeepers/meliponiculturists via
                      WhatsApp, Instagram, and email; effective response from
                      4 producers (anonymity assured by protocol), identified
                      as Producer A (MG), B (SP), C and D (PR)

Literature review  →  Scientific literature on CCD (Colony Collapse Disorder),
                      organophosphates, neonicotinoids, and fungicides —
                      Google Scholar, IBAMA, EMBRAPA, APTA, SciELO articles

Processing         →  Interview data tabulated in Microsoft Excel; cross-
                      referenced with regional Paraíba Valley mapping
                      (IBGE 2006) and municipal pesticide-use data
                      (Bombardini, 2017 — FFLCH/USP)

Georeferencing      →  Locations geocoded for Folium mapping; foraging-radius
                      calculations per species (Jataí: 600m; Apis mellifera:
                      5km) per EMBRAPA (2021)

Analysis            →  Qualitative-quantitative, hypothetical-deductive
                      approach; descriptive analysis of losses by year,
                      producer, and cause; cross-referenced against known
                      chemical-use patterns (IBAMA RT25/RT40, 2012)

Visualization        →  Interactive dashboard (Streamlit + Plotly + Folium)
                      with loss-proportional geospatial markers
```

---

## 🖥️ Dashboard Overview

The Streamlit app is organized into five tabs:

1. **🗺️ Map & Analysis** — geospatial distribution of losses across Brazil, with clickable markers showing location details and *Apis mellifera*'s 2 km foraging radius.
2. **🔬 Methodology & Pipeline** — the six-step research pipeline, species foraging-radius reference table, and identified compound categories.
3. **💡 What We Found** — the five key findings above, plus the scientific conclusion and a log-scale chart of bees lost per event.
4. **📷 In the Field** — field photos and historical context, including a Bee Museum visit, direct evidence from a 2021 colony-loss event, and cave paintings depicting honey collection dating back over 10,000 years.
5. **📚 Sources & Credits** — full interview timeline, scientific references, and author credentials.

The full interface — labels, chart titles, and narrative text — is natively trilingual (PT/EN/ES), switchable from the sidebar.

---

## 🛠️ Tech Stack

| Technology | Use |
|---|---|
| Python 3.11 | Core language |
| Streamlit | Dashboard framework |
| Folium + streamlit-folium | Interactive geospatial loss mapping |
| Plotly (Express & Graph Objects) | Temporal, per-producer, and log-scale charts |
| Pandas / NumPy | Data processing |

---

## 📁 Repository Structure

```
bee-colony-collapse-brazil/
├── app.py                    # Main dashboard (5 tabs, PT/EN/ES)
├── requirements.txt          # Python dependencies
├── README.md                   # This file (English)
├── README.pt-BR.md             # Portuguese version
├── README.es.md                # Spanish version
└── assets/
    ├── foto_01_museu_apis.jpg
    ├── foto_02_mortas_guaratingueta.jpg
    ├── foto_03_museu_mapa_vida.jpg
    ├── foto_04_apis_girassol_fatec.jpg
    ├── foto_05_museu_anatomia.jpg
    ├── foto_06_rupestre_500ac.jpg
    ├── foto_07_cacador_mel_rodesia.jpg
    └── foto_08_rupestre_castellon.jpg
```

---

## 🚀 Run Locally

```bash
# Clone the repository
git clone https://github.com/amaurialmeida/bee-colony-collapse-brazil.git
cd bee-colony-collapse-brazil

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

---

## 🌐 Live App

🔗 **[bee-colony-collapse-brazil.streamlit.app](https://bee-colony-collapse-brazil.streamlit.app/)**

Available in 🇧🇷 Portuguese, 🇺🇸 English, and 🇪🇸 Spanish.

---

## 📚 References

- Bombardini, L. (2017) — Pesticide use mapping in the Paraíba Valley. FFLCH/USP.
- IBAMA (2012) — RT25/RT40 technical reports on agrochemical toxicity.
- EMBRAPA (2021) — Foraging radius reference for native and *Apis* bee species.
- Alves (2022) — Pioneering regional bee-mortality survey, Paraíba Valley.

---

## 🔗 Academic / Professional Links

| Platform | Link |
|---|---|
| Lattes | http://lattes.cnpq.br/9545242042800090 |
| Escavador | https://www.escavador.com/sobre/8577779/amauri-almeida-de-souza-junior |

---

## 🌿 Environmental Portfolio

This project is part of the author's environmental research and data science portfolio.
🔗 [amaurialmeida.github.io/environmental-portfolio](https://amaurialmeida.github.io/environmental-portfolio)

---

© 2022–2026 · Amauri Almeida de Souza Junior · Academic Research · FATEC Jundiaí
