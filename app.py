import streamlit as pd
import streamlit as st
import wbdata
import plotly.express as px
from datetime import datetime

# Configuration de la page Streamlit
st.set_page_config(page_title="Dashboard Santé BM - ESGIS", layout="wide")

# 1. Titre de l'application
st.title("📊 Dashboard Dynamique : Analyse Comparée de la Santé des pays couverts par la banque mondiales")
st.write("Projet d'Analyse et Visualisation de Données - Données issues de la Banque Mondiale")

# 2. Récupération et cache des données pour éviter de recharger l'API à chaque clic
@st.cache_data
def charger_donnees():
    ##on peut definir les pays voulus
    countries = ["BEN", "BFA", "CMR", "CIV", "GHA", "KEN", "NGA", "SEN", "TGO"]
    ##Les differentes indications que nous souhaitons recuperee
    indicators = {
        "SH.DYN.AIDS.ZS": "VIH_Prevalence",
        "SH.TBS.INCD": "Tuberculose_Incidence",
        "SH.MLR.INCD.P3": "Malaria_Incidence",
        "SH.DTH.NCOM.ZS": "Mortalite_Maladies_Chroniques",
        "SH.IMM.HEPB": "Vaccination_Hepatite_B",
        "SP.DYN.LE00.IN": "Esperance_Vie",
        "SH.XPD.CHEX.GD.ZS": "Depenses_Sante",
        "SP.POP.TOTL": "Population"
    }
    
    # Appel API Banque Mondiale
    #df_brut = wbdata.get_dataframe(indicators, country=countries, date=(datetime(2000, 1, 1), datetime(2024, 1, 1)))
    df_brut = wbdata.get_dataframe(indicators, date=(datetime(2000, 1, 1), datetime(2024, 1, 1)))
    df_clean = df_brut.reset_index()
    df_clean['date'] = df_clean['date'].astype(int)
    df_clean.rename(columns={'country': 'Pays', 'date': 'Annee'}, inplace=True)
    return df_clean

# Chargement du dataframe
df = charger_donnees()

# 3. Barre latérale (Sidebar) pour le choix dynamique du pays
liste_pays = sorted(df['Pays'].unique())
pays_choisi = st.sidebar.selectbox("🌍 Choisir un Pays :", liste_pays)

# Filtrage du dataframe selon le choix de l'utilisateur
df_pays = df[df['Pays'] == pays_choisi].sort_values(by="Annee")

st.subheader(f"📈 Analyse épidémiologique pour le pays : {pays_choisi}")
st.markdown("---")

# 4. Organisation de l'affichage en colonnes (Layout Streamlit)
col1, col2 = st.columns(2)

with col1:
    # VISUALISATION 1 : Espérance de vie
    fig1 = px.line(df_pays, x="Annee", y="Esperance_Vie", title="Évolution de l'espérance de vie", markers=True, template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

    # VISUALISATION 2 : Focus Hépatite B
    fig3 = px.line(df_pays, x="Annee", y="Vaccination_Hepatite_B", title="Couverture vaccinale contre l'Hépatite B (%)", markers=True, color_discrete_sequence=["#2ecc71"])
    fig3.update_yaxes(range=[0, 100])
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # VISUALISATION 3 : Maladies Infectieuses
    fig2 = px.line(df_pays, x="Annee", y=["VIH_Prevalence", "Tuberculose_Incidence", "Malaria_Incidence"], title="Trajectoires des maladies infectieuses", labels={"value": "Taux / Incidence", "variable": "Maladies"})
    st.plotly_chart(fig2, use_container_width=True)

    # VISUALISATION 4 : Maladies Chroniques
    fig4 = px.line(df_pays, x="Annee", y="Mortalite_Maladies_Chroniques", title="Part de la mortalité due aux maladies chroniques (%)", markers=True, color_discrete_sequence=["#e74c3c"])
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.subheader("🧬 Corrélations et Facteurs Économiques")

col3, col4 = st.columns([3, 2])

with col3:
    # VISUALISATION 5 : Matrice de corrélation
    colonnes_corr = ["VIH_Prevalence", "Tuberculose_Incidence", "Malaria_Incidence", "Mortalite_Maladies_Chroniques", "Vaccination_Hepatite_B", "Esperance_Vie", "Depenses_Sante", "Population"]
    colonnes_presentes = [c for c in colonnes_corr if c in df_pays.columns]
    corr_pays = df_pays[colonnes_presentes].corr()
    fig5 = px.imshow(corr_pays, text_auto=True, color_continuous_scale='RdBu_r', title="Matrice de corrélation des facteurs de santé")
    st.plotly_chart(fig5, use_container_width=True)

with col4:
    # VISUALISATION 6 : Dépenses de santé
    fig6 = px.scatter(df_pays, x="Depenses_Sante", y="Esperance_Vie", size="Population", hover_data=["Annee"], title="Dépenses de Santé vs Espérance de Vie")
    st.plotly_chart(fig6, use_container_width=True)