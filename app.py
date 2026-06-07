import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib

st.set_page_config(page_title="Dashboard DDDM - Logistique", layout="wide", page_icon="🍔")

@st.cache_data
def load_data():
    df = pd.read_csv('df_livraisons.csv')
    
    return df

df = load_data()

st.sidebar.title("Navigation")
st.sidebar.markdown("Sélectionnez le profil utilisateur :")
vue = st.sidebar.radio("", [
    "📊 1. Direction (KPIs)", 
    "🗺️ 2. Opérations (Carte)", 
    "⭐ 3. Marketing (Satisfaction)", 
    "🛵 4. RH (Flotte)", 
    "🤖 5. Simulateur IA"
])

st.sidebar.markdown("---")
st.sidebar.info("Projet Data-Driven Decision Making\n\nJuin 2026")

#  VUE 1 : DIRECTION 
if vue == "📊 1. Direction (KPIs)":
    st.title("Vue Direction : Performances Globales")
    
    taux_retard = df['is_late'].mean() * 100
    cout_penalite_unitaire = 5.50
    cout_total = df['is_late'].sum() * cout_penalite_unitaire
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Volume de Commandes", f"{len(df):,}")
    col2.metric("Taux de Retard Critique (>45m)", f"{taux_retard:.1f}%", "- Objectif: < 15%", delta_color="inverse")
    col3.metric("Coût Estimé des Pénalités", f"{cout_total:,.2f} €")
    
    st.markdown("### Répartition des Statuts de Livraison")
    fig = px.pie(df, names='is_late', title="Proportion des commandes en retard", color='is_late',
                 color_discrete_map={True: 'red', False: 'green'}, labels={True: 'En Retard', False: 'À l\'heure'})
    st.plotly_chart(fig, use_container_width=True)

# VUE 2 : OPÉRATIONS
elif vue == "🗺️ 2. Opérations (Carte)":
    st.title("Vue Opérations : Analyse Terrain")
    st.markdown("Cartographie des points de livraison pour identifier les zones à risque.")
    
    # On affiche sur la carte uniquement les livraisons en retard
    df_retards = df[df['is_late'] == True].copy()

    df_map = df_retards.rename(columns={
        'Delivery_location_latitude': 'lat',
        'Delivery_location_longitude': 'lon'
    })

    df_map = df_map.dropna(subset=['lat', 'lon'])

    st.map(df_map[['lat', 'lon']])
    
    st.markdown("### Impact de la distance sur le temps de trajet")

    fig = px.scatter(df, x="Distance_km", y="Time_taken(min)", color="Precip Type", 
                     trendline="ols", title="Corrélation Distance / Temps selon la Météo")
    st.plotly_chart(fig, use_container_width=True)

# VUE 3 : MARKETING
elif vue == "⭐ 3. Marketing (Satisfaction)":
    st.title("Vue Marketing : Impact sur l'expérience client")
    
    avg_rating_on_time = df[df['is_late'] == False]['Delivery_person_Ratings'].mean()
    avg_rating_delayed = df[df['is_late'] == True]['Delivery_person_Ratings'].mean()
    
    col1, col2 = st.columns(2)
    col1.metric("Note moyenne (À l'heure)", f"{avg_rating_on_time:.2f} ⭐")
    col2.metric("Note moyenne (En retard)", f"{avg_rating_delayed:.2f} ⭐", delta=f"{avg_rating_delayed - avg_rating_on_time:.2f}")
    
    fig = px.histogram(df, x="Delivery_person_Ratings", color="is_late", barmode="overlay",
                       title="Distribution des notes selon le respect des délais")
    st.plotly_chart(fig, use_container_width=True)

# VUE 4 : RH & FLOTTE
elif vue == "🛵 4. RH (Flotte)":
    st.title("Vue Gestion de Flotte : Performance par Véhicule")
    
    fig = px.box(df, x="Type_of_vehicle", y="Time_taken(min)", color="Type_of_vehicle",
                 title="Dispersion des temps de livraison selon le véhicule")
    st.plotly_chart(fig, use_container_width=True)

# VUE 5 : SIMULATEUR
elif vue == "🤖 5. Simulateur IA":
    st.title("Simulateur d'Aide à la Décision")
    st.markdown("Saisissez les paramètres pour évaluer le risque avec notre modèle Machine Learning.")

    # Chargement du modèle et des colonnes (en cache pour la performance)
    @st.cache_resource
    def charger_modele():
        modele = joblib.load('modele_livraison.pkl')
        colonnes = joblib.load('colonnes_modele.pkl')
        return modele, colonnes

    try:
        modele, colonnes_entrainement = charger_modele()
        modele_charge = True
    except FileNotFoundError:
        st.error("⚠️ Fichiers du modèle introuvables. Avez-vous bien exécuté la dernière cellule du Notebook ?")
        modele_charge = False

    if modele_charge:
        with st.form("simulateur_form"):
            st.markdown("#### Paramètres de la course")
            col1, col2, col3 = st.columns(3)
            distance = col1.slider("Distance (km)", 1.0, 25.0, 5.0)
            vehicule = col2.selectbox("Véhicule", ["motorcycle", "scooter", "bicycle"])
            meteo = col3.selectbox("Météo", ["Clear", "Rain", "Snow", "Fog", "Windy"]) # Ajuste selon tes vraies données
            
            st.markdown("#### Profil du Livreur")
            col4, col5 = st.columns(2)
            age = col4.slider("Âge du livreur", 18, 65, 30)
            rating = col5.slider("Note du livreur", 1.0, 5.0, 4.5, step=0.1)

            submit = st.form_submit_button("Évaluer le risque avec l'IA")

            if submit:
                # 1. Sécurité : on initialise tout à 0
                input_dict = {col: 0 for col in colonnes_entrainement}
                
                # 2. Variables numériques (les curseurs)
                if 'Distance_km' in input_dict:
                    input_dict['Distance_km'] = distance
                # Ajuste les noms ici ('Delivery_person_Age', etc.) selon les vrais noms dans ton DataFrame
                if 'Delivery_person_Age' in input_dict:
                    input_dict['Delivery_person_Age'] = age
                if 'Delivery_person_Ratings' in input_dict:
                    input_dict['Delivery_person_Ratings'] = rating

                # 3. Variables catégorielles (One-Hot Encoding)
                col_vehicule = f"Type_of_vehicle_{vehicule}"
                if col_vehicule in input_dict:
                    input_dict[col_vehicule] = 1
                    
                col_meteo = f"Precip Type_{meteo}"
                if col_meteo in input_dict:
                    input_dict[col_meteo] = 1

                # 4. Conversion et Prédiction
                input_df = pd.DataFrame([input_dict])
                proba_retard = modele.predict_proba(input_df)[0][1]
                risque = round(proba_retard * 100, 1)

                # 5. Affichage du résultat
                st.markdown("### Résultat de l'analyse IA")
                if risque > 60:
                    st.error(f"🚨 **Alerte Risque Élevé : {risque}% de probabilité de retard.**")
                    st.markdown("*Recommandation : Assigner un livreur mieux noté ou utiliser un véhicule motorisé.*")
                elif risque > 30:
                    st.warning(f"⚠️ **Risque Modéré : {risque}% de probabilité de retard.**")
                else:
                    st.success(f"✅ **Risque Faible : {risque}% de probabilité de retard.**")