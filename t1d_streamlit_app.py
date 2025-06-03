
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="T1D Cost Model", layout="centered")

st.title("Tyypin 1 diabeteksen kustannusvaikuttavuusmalli – Suomi")

st.sidebar.header("Säädettävät parametrit")

# Käyttäjän syötteet
population = st.sidebar.number_input("Väestö Suomessa", value=5536140, step=10000)
t1d_prevalence = st.sidebar.slider("T1D-esiintyvyys (%)", 0.1, 1.0, 0.5, 0.1) / 100
diagnosis_rate = st.sidebar.slider("Diagnosoidut tapaukset (%)", 50, 100, 85, 5) / 100
control_now = st.sidebar.slider("Hoitotasapaino (nykyinen, %)", 10, 90, 40, 5) / 100
control_target = st.sidebar.slider("Hoitotasapaino (tavoite, %)", 10, 90, 60, 5) / 100
visits_good = st.sidebar.number_input("Käynnit/vuosi (tasapainossa)", value=2)
visits_poor = st.sidebar.number_input("Käynnit/vuosi (ei tasapainossa)", value=6)
cost_per_visit = st.sidebar.number_input("Kustannus/käynti (€)", value=120)

# Laskelmat
total_t1d = int(population * t1d_prevalence)
diagnosed = int(total_t1d * diagnosis_rate)
undiagnosed = total_t1d - diagnosed

controlled_now = int(diagnosed * control_now)
uncontrolled_now = diagnosed - controlled_now
controlled_target = int(diagnosed * control_target)
uncontrolled_target = diagnosed - controlled_target

visits_now = controlled_now * visits_good + uncontrolled_now * visits_poor
visits_target = controlled_target * visits_good + uncontrolled_target * visits_poor

cost_now = visits_now * cost_per_visit
cost_target = visits_target * cost_per_visit
savings_annual = cost_now - cost_target
savings_3yr = savings_annual * 3

# Tulokset
st.subheader("Yhteenveto")

df = pd.DataFrame({
    "Mittari": [
        "Arvioitu T1D-potilaiden määrä",
        "Diagnosoidut potilaat",
        "Alidiagnosoidut potilaat",
        "Hoitotasapainossa (nykyinen)",
        "Ei hoitotasapainossa (nykyinen)",
        "Hoitotasapainossa (tavoite)",
        "Ei hoitotasapainossa (tavoite)",
        "Vuosittaiset lääkärikäynnit (nykyinen)",
        "Vuosittaiset lääkärikäynnit (tavoite)",
        "Vuosikustannus (nykyinen)",
        "Vuosikustannus (tavoite)",
        "Säästö vuodessa",
        "Säästö kolmessa vuodessa"
    ],
    "Arvo": [
        total_t1d, diagnosed, undiagnosed,
        controlled_now, uncontrolled_now,
        controlled_target, uncontrolled_target,
        visits_now, visits_target,
        f"€{cost_now:,.0f}", f"€{cost_target:,.0f}",
        f"€{savings_annual:,.0f}", f"€{savings_3yr:,.0f}"
    ]
})

st.dataframe(df)

# Kaavio: kustannukset ja käynnit
st.subheader("Vertailukaavio: nykytila vs. tavoitetila")

fig, ax = plt.subplots()
labels = ["Lääkärikäynnit", "Vuosikustannukset (€)"]
current = [visits_now, cost_now]
target = [visits_target, cost_target]
x = range(len(labels))

ax.bar(x, current, width=0.4, label="Nykyinen", align='center')
ax.bar([p + 0.4 for p in x], target, width=0.4, label="Tavoite", align='center')
ax.set_xticks([p + 0.2 for p in x])
ax.set_xticklabels(labels)
ax.set_ylabel("Määrä / Kustannus")
ax.set_title("Käynnit ja kustannukset: nykytila vs. tavoitetila")
ax.legend()
st.pyplot(fig)

# Huomautus Excel-yhteensopivuudesta
st.markdown("🔧 Tämä malli voidaan myös siirtää Exceliin, jos haluat jatkaa simulointia taulukkolaskennassa.")

