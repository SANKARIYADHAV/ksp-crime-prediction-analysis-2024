import pandas as pd
import folium
from sklearn.svm import SVC
from IPython.display import IFrame
from sklearn.neighbors import KernelDensity
import numpy as np

# Load the dataset containing latitude, longitude, max percentage value, and other relevant data
data = pd.read_csv('summary_data.csv')

# Define features (X) and labels (y)
X = data[['lattitude', 'longitude']]  # Assuming latitude and longitude are used as features
y = data['Max_Percentage_Crime_Group']  # Assuming 'Max_Percentage_Crime_Group' is the target variable

# Train an SVM model on the entire dataset
svm_model = SVC(kernel='linear')
svm_model.fit(X, y)

# Now, suppose you want to predict future hotspots based on the same dataset
# Extract features for prediction (use the same dataset)
X_future = X  # You can use the same features for prediction

# Make predictions using the trained SVM model
future_predictions = svm_model.predict(X_future)

# Add the predicted hotspots to the dataframe
data['Predicted_Hotspot'] = future_predictions

# Calculate the density of predicted hotspots
hotspot_density = KernelDensity(bandwidth=0.01)
hotspot_density.fit(data[data['Predicted_Hotspot'] == 1][['lattitude', 'longitude']])

# Generate grid points for heatmap
x = np.linspace(data['lattitude'].min(), data['lattitude'].max(), 100)
y = np.linspace(data['longitude'].min(), data['longitude'].max(), 100)
X_grid, Y_grid = np.meshgrid(x, y)
grid_points = np.array([X_grid.ravel(), Y_grid.ravel()]).T

# Calculate the density values for grid points
densities = np.exp(hotspot_density.score_samples(grid_points)).reshape(X_grid.shape)

# Create a map centered around a specific location
map_center = [data['lattitude'].mean(), data['longitude'].mean()]  # Mean coordinates of the dataset
mymap = folium.Map(location=map_center, zoom_start=10)

# Iterate over the predicted hotspots and add markers to the map
for index, row in data.iterrows():
    lat = row['lattitude']
    lon = row['longitude']
    hotspot = row['Predicted_Hotspot']
    district = row['District']  # Assuming 'District' is a column in your dataset
    
    # Define the popup text with HTML formatting for hotspot and district
    popup_text = f"District: {district}<br>Predicted Hotspot: {hotspot}"
    
    # Add marker to the map
    folium.Marker(
        location=[lat, lon],
        popup=popup_text,
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(mymap)

# Add heatmap layer to the map
folium.plugins.HeatMap(densities, 
                        min_opacity=0.2, 
                        max_val=densities.max(),
                        radius=15, 
                        blur=10,
                        gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'}).add_to(mymap)

# Add a legend for the heatmap
legend_html = '''
     <div style="position: fixed; 
                 bottom: 50px; left: 50px; width: 120px; height: 130px; 
                 border:2px solid grey; z-index:9999; font-size:14px;
                 background-color:white;
                 ">
     &nbsp; Heatmap Legend <br>
     &nbsp; Low Density &nbsp; <i class="fa fa-circle" style="color:blue"></i><br>
     &nbsp; Medium Density &nbsp; <i class="fa fa-circle" style="color:lime"></i><br>
     &nbsp; High Density &nbsp; <i class="fa fa-circle" style="color:red"></i><br>
      </div>
     '''
mymap.get_root().html.add_child(folium.Element(legend_html))

# Add fullscreen control to the map
folium.plugins.Fullscreen().add_to(mymap)

# Add layer control to toggle heatmap and markers
folium.LayerControl().add_to(mymap)

# Save the map to an HTML file
mymap.save('predicted_hotspots_map_with_heatmap.html')

# Display the map in the notebook using an iframe
IFrame(src='predicted_hotspots_map_with_heatmap.html', width=700, height=600)
