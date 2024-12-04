import requests
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Télécharger les données JSON depuis l'URL et ajouter des utilisateurs fictifs
def charger_utilisateurs():
    url = 'https://jsonplaceholder.typicode.com/users'
    response = requests.get(url)
    
    if response.status_code == 200:
        utilisateurs = response.json()
        
        # Ajouter des utilisateurs fictifs
        utilisateurs.append({
            "id": 11,
            "name": "Utilisateur Fictif 1",
            "address": {"city": "Paris", "geo": {"lat": "48.8566", "lng": "2.3522"}}
        })
        utilisateurs.append({
            "id": 12,
            "name": "Utilisateur Fictif 2",
            "address": {"city": "New York", "geo": {"lat": "40.7128", "lng": "-74.0060"}}
        })
        utilisateurs.append({
            "id": 13,
            "name": "Votre Nom",
            "address": {"city": "Marseille", "geo": {"lat": "43.2965", "lng": "5.3698"}}
        })
        return utilisateurs
    else:
        st.error(f"Erreur lors du téléchargement des données: {response.status_code}")
        return []

# Fonction pour afficher une carte
def afficher_carte(lat, lng, nom):
    carte = folium.Map(location=[lat, lng], zoom_start=10)
    folium.Marker([lat, lng], popup=f"{nom}").add_to(carte)
    st_folium(carte, width=700, height=500)

# Interface utilisateur Streamlit
def main():
    st.title("Recherche d'utilisateurs par ville ou nom")
    
    # Charger les utilisateurs
    utilisateurs = charger_utilisateurs()
    if not utilisateurs:
        return

    # Convertir les données en DataFrame
    data = [
        {
            "Nom": u["name"],
            "Ville": u["address"]["city"],
            "Latitude": float(u["address"]["geo"]["lat"]),
            "Longitude": float(u["address"]["geo"]["lng"])
        }
        for u in utilisateurs
    ]
    df = pd.DataFrame(data)

    # Sélection de la ville ou du nom
    recherche_ville = st.text_input("Rechercher par ville")
    recherche_nom = st.text_input("Rechercher par nom")

    # Filtrer les résultats
    if recherche_ville:
        resultats = df[df["Ville"].str.contains(recherche_ville, case=False, na=False)]
    elif recherche_nom:
        resultats = df[df["Nom"].str.contains(recherche_nom, case=False, na=False)]
    else:
        resultats = df

    # Afficher les résultats
    st.write("### Résultats de la recherche")
    st.dataframe(resultats)

    # Sélectionner un utilisateur
    if not resultats.empty:
        utilisateur_selectionne = st.selectbox("Sélectionnez un utilisateur", resultats["Nom"])
        if utilisateur_selectionne:
            utilisateur = df[df["Nom"] == utilisateur_selectionne].iloc[0]
            afficher_carte(utilisateur["Latitude"], utilisateur["Longitude"], utilisateur_selectionne)
    else:
        st.warning("Aucun résultat trouvé.")

if __name__ == "__main__":
    main()
