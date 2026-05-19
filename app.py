import streamlit as st
import wbdata
import plotly.express as px
from datetime import datetime

# Configuration de la page Streamlit
st.set_page_config(page_title="Dashboard Santé BM - ESGIS", layout="wide")

# 1. Titre de l'application
st.title("📊 Dashboard Dynamique : Analyse Comparée de la Santé en Afrique")
st.write("Projet d'Analyse et Visualisation de Données — Données issues de la Banque Mondiale")

# 2. Récupération et cache des données pour éviter de recharger l'API à chaque clic
@st.cache_data
def charger_donnees():
    countries = ["BEN", "BFA", "CMR", "CIV", "GHA", "KEN", "NGA", "SEN", "TGO"]
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
    
    # Récupération dynamique de l'année en cours
    annee_actuelle = datetime.now().year
    
    # Appel API Banque Mondiale
    #df_brut = wbdata.get_dataframe(indicators, country=countries, date=(datetime(2000, 1, 1), datetime(2024, 1, 1)))
    df_brut = wbdata.get_dataframe(indicators, date=(datetime(2000, 1, 1), datetime(annee_actuelle, 1, 1)))
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

# 4. Organisation de l'affichage en colonnes
col1, col2 = st.columns(2)

with col1:
    # VISUALISATION 1 : Espérance de vie
    fig1 = px.line(
        df_pays, x="Annee", y="Esperance_Vie", 
        title="Évolution de l'espérance de vie", 
        markers=True, template="plotly_white"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # VISUALISATION 2 : Focus isolé - Prévalence du VIH (Graphique en escalier)
    fig_vih = px.line(
        df_pays, x="Annee", y="VIH_Prevalence",
        title="Détail : Prévalence du VIH (% population 15-49 ans)",
        line_shape="hv", markers=True,
        color_discrete_sequence=["#E74C3C"], template="plotly_white"
    )
    st.plotly_chart(fig_vih, use_container_width=True)

    # VISUALISATION 3 : Couverture vaccinale Hépatite B (Graphique à points reliés)
    fig3 = px.scatter(
        df_pays, x="Annee", y="Vaccination_Hepatite_B",
        title="Couverture vaccinale Hépatite B (% enfants 12-23 mois)",
        labels={"Vaccination_Hepatite_B": "Taux (%)"},
        color_discrete_sequence=["#2ECC71"], template="plotly_white"
    )
    fig3.update_traces(mode='lines+markers')
    fig3.update_yaxes(range=[0, 100])
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # VISUALISATION 4 : Vue d'ensemble comparative (Courbes superposées)
    fig2 = px.line(
        df_pays, x="Annee", 
        y=["VIH_Prevalence", "Tuberculose_Incidence", "Malaria_Incidence"],
        title="Comparaison des tendances épidémiologiques (Échelle globale)",
        labels={"value": "Indice", "variable": "Pathologie"},
        markers=True
    )
    st.plotly_chart(fig2, use_container_width=True)

    # VISUALISATION 5 : Mortalité due aux maladies chroniques (Diagramme en bâtons)
    fig4 = px.bar(
        df_pays, x="Annee", y="Mortalite_Maladies_Chroniques",
        title="Mortalité liée aux maladies non transmissibles (% décès)",
        labels={"Mortalite_Maladies_Chroniques": "Part des décès (%)"},
        color_discrete_sequence=["#8E44AD"]
    )
    fig4.update_layout(xaxis_type='category')
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.subheader("📊 Focus Pathologies & Axes Indépendants")

# VISUALISATION 6 : Graphique à facettes (Prend toute la largeur de la page)
df_maladies = df_pays.melt(
    id_vars=["Annee"], 
    value_vars=["VIH_Prevalence", "Tuberculose_Incidence", "Malaria_Incidence"],
    var_name="Maladie", 
    value_name="Valeur"
)
fig_facettes = px.line(
    df_maladies, x="Annee", y="Valeur", 
    facet_col="Maladie", color="Maladie",
    title="Analyses individuelles des pathologies (Axes Y autonomes)",
    markers=True, template="plotly_white",
    height=450
)
fig_facettes.update_yaxes(matches=None, autorange=True)
st.plotly_chart(fig_facettes, use_container_width=True)

st.markdown("---")
st.subheader("🧬 Corrélations et Facteurs Économiques")

col3, col4 = st.columns([3, 2])

with col3:
    # VISUALISATION 7 : Matrice de corrélation complète (Heatmap)
    colonnes_corr = [
        "VIH_Prevalence", "Tuberculose_Incidence", "Malaria_Incidence", 
        "Mortalite_Maladies_Chroniques", "Vaccination_Hepatite_B", 
        "Esperance_Vie", "Depenses_Sante", "Population"
    ]
    colonnes_presentes = [c for c in colonnes_corr if c in df_pays.columns]
    matrice_corr = df_pays[colonnes_presentes].corr()
    
    fig6 = px.imshow(
        matrice_corr, text_auto=".2f", 
        color_continuous_scale='RdBu_r',
        title="Matrice de corrélation des indicateurs"
    )
    st.plotly_chart(fig6, use_container_width=True)

with col4:
    # VISUALISATION 8 : Dépenses de santé vs Espérance de vie (Nuage de points)
    fig5 = px.scatter(
        df_pays, x="Depenses_Sante", y="Esperance_Vie",
        size="Population", hover_data=["Annee"],
        title="Analyse Investissements Santé vs Longévité",
        labels={"Depenses_Sante": "Dépenses (% PIB)", "Esperance_Vie": "Espérance de vie (ans)"}
    )
    st.plotly_chart(fig5, use_container_width=True)