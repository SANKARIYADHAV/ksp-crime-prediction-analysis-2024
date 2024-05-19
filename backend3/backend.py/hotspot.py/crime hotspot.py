import folium
import pandas as pd
from sklearn.cluster import KMeans

# Load the dataset containing latitude and longitude data
data = pd.read_csv('summary_data.csv')

# Extract latitude and longitude data
X = data[['lattitude', 'longitude']]

# Perform K-means clustering
num_clusters = 4  # You can adjust this parameter based on your data
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
data['cluster'] = kmeans.fit_predict(X)

# Get cluster centers
cluster_centers = kmeans.cluster_centers_

# Create a map centered around a specific location
map_center = [12.9716, 77.5946]  # Bangalore coordinates
map_zoom = 10
mymap = folium.Map(location=map_center, zoom_start=map_zoom)

# Define marker colors based on clusters
colors = ['red', 'blue', 'green', 'orange']  # You can customize colors as needed

# Add markers for each location
for index, row in data.iterrows():
    # Extract latitude, longitude, district, and cluster values for each row
    lat = row['lattitude']
    lon = row['longitude']
    district = row['District']
    cluster = row['cluster']

    # Define the popup text with HTML formatting for district and cluster
    popup_text = f"<b>{district}</b><br>Cluster: {cluster}"

    # Add marker to the map
    folium.Marker(
        location=[lat, lon],
        popup=popup_text,
        icon=folium.Icon(color=colors[cluster])
    ).add_to(mymap)

# Add cluster centers to the map
for i, center in enumerate(cluster_centers):
    folium.CircleMarker(
        location=center,
        radius=10,
        popup=f"Cluster Center {i}",
        color='black',
        fill=True,
        fill_color='white',
        fill_opacity=1
    ).add_to(mymap)

# Add interactive legend
legend_html = '''
     <div style="position: fixed; 
                 bottom: 50px; left: 50px; width: 120px; height: 130px; 
                 border:2px solid grey; z-index:9999; font-size:14px;
                 background-color:white;
                 ">
     &nbsp; Cluster Legend <br>
     &nbsp; Cluster 0 &nbsp; <i class="fa fa-circle" style="color:red"></i><br>
     &nbsp; Cluster 1 &nbsp; <i class="fa fa-circle" style="color:blue"></i><br>
     &nbsp; Cluster 2 &nbsp; <i class="fa fa-circle" style="color:green"></i><br>
     &nbsp; Cluster 3 &nbsp; <i class="fa fa-circle" style="color:orange"></i><br>
      </div>
     '''
mymap.get_root().html.add_child(folium.Element(legend_html))

# Display the map in the notebook
mymap
