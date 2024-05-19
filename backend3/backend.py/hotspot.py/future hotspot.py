import folium
from folium.plugins import MarkerCluster
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import numpy as np

# Load the dataset containing latitude and longitude data
data = pd.read_csv('summary_data.csv')

# Prompt user to input the type of crime group
crime_group = input("Enter the type of crime group: ")

# Filter data for the specified type of crime group
crime_group_data = data[data['Max_Percentage_Crime_Group'] == crime_group]

# Split the data into features (latitude and longitude) and target (crime group)
X = crime_group_data[['lattitude', 'longitude']]
y = crime_group_data['Max_Percentage_Crime_Group']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train machine learning models
models = {
    'Random Forest': RandomForestClassifier(random_state=42),
    'K-Nearest Neighbors': KNeighborsClassifier(),
    'Support Vector Machine': SVC(probability=True)
}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy of {name}: {accuracy}")

# Create a map centered around a specific location
map_center = [12.9716, 77.5946]  # Bangalore coordinates
map_zoom = 10
mymap = folium.Map(location=map_center, zoom_start=map_zoom)

# Create a MarkerCluster to handle large amounts of markers
marker_cluster = MarkerCluster().add_to(mymap)

# Define a function to get predictions for a given location
def get_prediction(latitude, longitude):
    features = np.array([[latitude, longitude]])
    predictions = {}
    for name, model in models.items():
        predictions[name] = model.predict(features)[0]
    return predictions

# Define a function to handle click events on the map
def on_click(event):
    lat, lon = event.latlng
    predictions = get_prediction(lat, lon)
    popup_text = f"<b>Location:</b> Latitude: {lat}, Longitude: {lon}<br>"
    for name, prediction in predictions.items():
        popup_text += f"<b>{name} Prediction:</b> {prediction}<br>"
    folium.Marker(
        location=[lat, lon],
        popup=popup_text
    ).add_to(mymap)

# Attach click event handler to the map
mymap.on_click(on_click)

# Iterate over the filtered crime group data and add markers for each location
for index, row in crime_group_data.iterrows():
    # Extract latitude, longitude, district, and hotspot values for each row
    lat = row['lattitude']
    lon = row['longitude']
    district = row['District']

    # Define the popup text with HTML formatting for district
    popup_text = f"<b>{district}</b>"

    # Add marker to the MarkerCluster
    folium.Marker(
        location=[lat, lon],
        popup=popup_text
    ).add_to(marker_cluster)

# Display the map in the notebook
mymap

