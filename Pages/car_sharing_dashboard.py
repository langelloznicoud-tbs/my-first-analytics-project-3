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





