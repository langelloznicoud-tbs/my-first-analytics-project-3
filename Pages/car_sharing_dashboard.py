import streamlit as st
import pandas as pd

st.title("🚗 Car Sharing Dashboard")
st.write("This is where the dashboard for the car sharing dataset will go.")


# Function to load CSV files into dataframes
@st.cache_data
def load_data():
    cars = pd.read_csv("Datasets/cars.csv")
    trips = pd.read_csv("Datasets/trips.csv")
    cities = pd.read_csv("Datasets/cities.csv")
    return cars, trips, cities

cars_df, trips_df, cities_df = load_data()

st.write("Cars Dataset", cars_df.head())
st.write("Trips Dataset", trips_df.head())
st.write("Cities Dataset", cities_df.head())

# Fusionner trips avec cars en adaptant les clés de jointure
trips_df_merged = trips_df.merge(cars_df, left_on='car_id', right_on='id', how='left')


# Fusionner trips_merged avec cities
trips_df_merged = trips_df_merged.merge(cities_df, on='city_id', how='left')

# Vérifier la fusion
st.write("Aperçu des données fusionnées :", trips_df_merged.head())

# Supprimer les colonnes inutiles
trips_df_merged = trips_df_merged.drop(columns=["id_x", "id_y", "car_id", "customer_id", "city_id"])  

st.write("Données après nettoyage:", trips_df_merged.head())

# Convertir pickup_time et dropoff_time en datetime
trips_df_merged["pickup_time"] = pd.to_datetime(trips_df_merged["pickup_time"])
trips_df_merged["dropoff_time"] = pd.to_datetime(trips_df_merged["dropoff_time"])

# Créer une nouvelle colonne "pickup_date" en extrayant uniquement la date
trips_df_merged["pickup_date"] = trips_df_merged["pickup_time"].dt.date

# Vérifier si la transformation a bien fonctionné
st.write("Aperçu des données après conversion :", trips_df_merged[["pickup_time", "dropoff_time", "pickup_date"]].head())

# Création du filtre dans la barre latérale
cars_brand = st.sidebar.multiselect(
    "Select the Car Brand",
    options=trips_df_merged["brand"].unique(), # Liste des marques uniques
    default=trips_df_merged["brand"].unique() # Sélectionne toutes les marques par défaut
)

# Filtrer le dataframe en fonction des marques sélectionnées
if cars_brand:
    trips_df_merged = trips_df_merged[trips_df_merged["brand"].isin(cars_brand)]

# Affichage des données filtrées
st.write("Aperçu des trajets filtrés :", trips_df_merged.head())

# Calculer les métriques business
total_trips = len(trips_df_merged)  # Nombre total de trajets
total_distance = trips_df_merged["distance"].sum()  # Somme des distances des trajets

# Trouver le modèle de voiture générant le plus de revenus
top_car = trips_df_merged.groupby("model")["revenue"].sum().idxmax()  # Modèle avec le plus de revenus

# Afficher les métriques dans des colonnes
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Trips", value=total_trips)
with col2:
    st.metric(label="Top Car Model by Revenue", value=top_car)
with col3:
    st.metric(label="Total Distance (km)", value=f"{total_distance:,.2f}")

