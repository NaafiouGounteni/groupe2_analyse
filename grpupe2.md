# 🌍 Analyse des maladies et indicateurs de santé en Afrique

Ce projet analyse la situation sanitaire des pays africains à partir de données officielles de la **Banque Mondiale** via la bibliothèque API `wbdata` et déploie une application interactive via **Streamlit**.

L’objectif est de comprendre comment les maladies infectieuses, les maladies chroniques, la prévention vaccinale et les conditions économiques influencent la santé des populations (espérance de vie, structures de mortalité, etc.).

---

# 🎯 Objectif du projet

Ce projet cherche à répondre à des questions clés :

- Quels pays d'Afrique de l'Ouest et de l'Est sont les plus touchés par les grandes endémies ?
- Observe-t-on une transition épidémiologique vers les maladies chroniques ?
- L'augmentation des dépenses publiques de santé et de la vaccination améliore-t-elle directement l'espérance de vie ?
- Comment les profils sanitaires diffèrent-ils dynamiquement d'un pays à l'autre ?

---

# 📊 Données utilisées

Les données proviennent de la base mondiale de la **World Bank (DataBank)**, qui centralise des statistiques validées par l’OMS, les ministères de la santé nationaux et diverses organisations internationales.

---

# 🦠 Explication des indicateurs

Voici les variables exploitées dans le projet après phase de nettoyage :

---

## 🧬 VIH — SH.DYN.AIDS.ZS
👉 **Prévalence du VIH (% de la population adulte âgée de 15 à 49 ans)**

- Indique la proportion de personnes vivant avec le VIH.
- Mesure l'impact à long terme d'une maladie transmissible chronique.

---

## 🫁 Tuberculose — SH.TBS.INCD
👉 **Incidence de la tuberculose (pour 100 000 habitants)**

- Nombre de nouveaux cas détectés chaque année.
- Révèle la vitesse de propagation de la maladie et l'efficacité des systèmes de détection.

---

## 🦟 Paludisme — SH.MLR.INCD
👉 **Incidence du paludisme (pour 1 000 personnes à risque)**

- Très important pour les pays tropicaux africains.
- Dépend fortement des facteurs environnementaux, du climat et des infrastructures d'assainissement.

---

## 💉 Hépatite B — SH.IMM.HEPB
👉 **Couverture vaccinale contre l'Hépatite B (% des enfants de 12 à 23 mois)**

- Mesure le taux d'enfants ayant reçu la troisième dose du vaccin (HepB3).
- Représente un indicateur clé de l'effort de prévention des maladies transmissibles par les gouvernements.

---

## 🩺 Maladies Chroniques — SH.DTH.NCOM.ZS
👉 **Mortalité due aux maladies non transmissibles (% du total des décès)**

- Regroupe les décès liés au cancer, aux maladies cardiovasculaires, au diabète et aux maladies respiratoires chroniques.
- Permet d'analyser l'émergence des maladies de structures face aux maladies infectieuses.

---

## 👶 Espérance de vie — SP.DYN.LE00.IN
👉 **Espérance de vie à la naissance (en années)**

- Indicateur global synthétisant la qualité de vie, l'accès aux soins, la nutrition et la sécurité sanitaire globale d'un pays.

---

## 💰 Dépenses de santé — SH.XPD.CHEX.GD.ZS
👉 **Dépenses de santé courantes (% du PIB)**

- Reflète le niveau de priorité financière accordé par un pays à son système de santé par rapport à sa richesse nationale.

---

## 👥 Population — SP.POP.TOTL
👉 **Population totale**

- Utilisée pour contextualiser la taille démographique des pays étudiés et pondérer l'importance des analyses graphiques (ex: graphiques à bulles).

💡 *Note sur le nettoyage : L'indicateur initial `SH.DTH.COMM.ZS` (Mortalité maladies transmissibles) présentait un taux de valeurs manquantes trop élevé (79 %) et a été volontairement supprimé pour maintenir la rigueur scientifique de l'étude.*

---

# 🌍 Zone d’étude

Le projet se concentre sur un échantillon ciblé de 9 pays d'Afrique subsaharienne :

- Togo 🇹🇬
- Bénin 🇧🇯
- Burkina Faso 🇧🇫
- Cameroun 🇨🇲
- Côte d'Ivoire 🇨🇮
- Ghana 🇬🇭
- Kenya 🇰🇪
- Nigeria 🇳🇬
- Sénégal 🇸🇳

---