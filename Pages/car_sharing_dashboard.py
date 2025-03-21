import streamlit as st
import pandas as pd

st.title("🚗 Car Sharing Dashboard")
st.write("This dashboard provides insights into the car sharing dataset.")

# Function to load CSV files into dataframes
@st.cache_data
def load_data():
    cars = pd.read_csv("Datasets/cars.csv")
    trips = pd.read_csv("Datasets/trips.csv")
    cities = pd.read_csv("Datasets/cities.csv")
    return cars, trips, cities

# Load datasets
cars_df, trips_df, cities_df = load_data()

# Merge trips with cars using appropriate keys
trips_df_merged = trips_df.merge(cars_df, left_on='car_id', right_on='id', how='left')

# Merge trips_df_merged with cities
trips_df_merged = trips_df_merged.merge(cities_df, on='city_id', how='left')

# Drop unnecessary columns
trips_df_merged = trips_df_merged.drop(columns=["id_x", "id_y", "car_id", "customer_id", "city_id"])

# Convert pickup_time and dropoff_time to datetime
trips_df_merged["pickup_time"] = pd.to_datetime(trips_df_merged["pickup_time"])
trips_df_merged["dropoff_time"] = pd.to_datetime(trips_df_merged["dropoff_time"])

# Create a new column 'pickup_date' by extracting only the date
trips_df_merged["pickup_date"] = trips_df_merged["pickup_time"].dt.date

# Sidebar filter - Car Brand
cars_brand = st.sidebar.multiselect(
    "Select Car Brand",
    options=trips_df_merged["brand"].unique(),
    default=trips_df_merged["brand"].unique()
)

# Filter data by selected brands
if cars_brand:
    trips_df_merged = trips_df_merged[trips_df_merged["brand"].isin(cars_brand)]

# Business Metrics Calculation
total_trips = len(trips_df_merged)
total_distance = trips_df_merged["distance"].sum()
top_car = trips_df_merged.groupby("model")["revenue"].sum().idxmax()

# Display Metrics in Columns
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Trips", value=total_trips)
with col2:
    st.metric(label="Top Car Model by Revenue", value=top_car)
with col3:
    st.metric(label="Total Distance (km)", value=f"{total_distance:,.2f}")

# Final DataFrame Preview
st.write("✅ Final Merged DataFrame Preview:", trips_df_merged.head())

st.subheader("📊 Data Visualizations")

# 1️⃣ Trips Over Time
trips_over_time = trips_df_merged.groupby("pickup_date").size()
st.write("### Trips Over Time")
st.line_chart(trips_over_time)

# 2️⃣ Revenue Per Car Model
revenue_per_model = trips_df_merged.groupby("model")["revenue"].sum().sort_values(ascending=False)
st.write("### Revenue Per Car Model")
st.bar_chart(revenue_per_model)

# 3️⃣ Cumulative Revenue Growth Over Time
revenue_over_time = trips_df_merged.groupby("pickup_date")["revenue"].sum().cumsum()
st.write("### Cumulative Revenue Growth Over Time")
st.area_chart(revenue_over_time)

# Bonus: Number of Trips Per Car Model
trips_df_per_model = trips_df_merged["model"].value_counts().reset_index()
trips_df_per_model.columns = ["model", "trip_count"]
st.subheader("🚘 Number of Trips Per Car Model")
st.bar_chart(trips_df_per_model.set_index("model"))