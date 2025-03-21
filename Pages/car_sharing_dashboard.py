import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    voyages = pd.read_csv("data/voyages.csv")
    voitures = pd.read_csv("data/voitures.csv")
    villes = pd.read_csv("data/villes.csv")
    return voyages, voitures, villes
