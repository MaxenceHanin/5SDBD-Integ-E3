"""
Clustering stations using Spectral clustering
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

from sklearn.cluster import KMeans, SpectralClustering
import sklearn.metrics as metrics

# https://towardsdatascience.com/understanding-bixi-commuters-an-analysis-of-montreals-bike-share-system-in-python-cb34de0e2304

data = pd.read_csv("../datasets/201801-citibike-tripdata.csv")

#### Data Processing

#filtering out trips that were less tha
data = data.drop(data[data["tripduration"] < 120].index)

#parsing through date data
data["starttime"] = pd.to_datetime(data["starttime"], format="%Y-%m-%d %H:%M:%S.%f", errors="coerce")
data["stoptime"] = pd.to_datetime(data["stoptime"], format="%Y-%m-%d %H:%M:%S.%f", errors="coerce")

#adding a day number column to identify days of the week
data["day_number"] = pd.to_datetime(data["starttime"]).dt.dayofweek

#adding a boolean week day column
data["week_day_b"] = pd.Series(index=data.index)
data["week_day_b"] = 1
data.loc[data["day_number"].isin([5, 6]), "week_day_b"] = 0

#adding a column for to split the departures in 20 min groups
data["time_slice"] = data["starttime"].dt.hour * 60 + np.floor(data["starttime"].dt.minute/20)*20
pd.options.mode.chained_assignment = None
data["time_slice"] = data["time_slice"].astype("int64")

#### Visualization

#creates a bar chart with the departures per day of month
def visualizePerDayMonth(data, column_name, color='#0000FF', title='Departure per day of month'):
    plt.figure(figsize=(20, 10))
    ax = (data[column_name].groupby(data[column_name].dt.day)
                         .count()).plot(kind="bar", color=color)
    ax.set_facecolor('#eeeeee')
    ax.set_xlabel("Day")
    ax.set_ylabel("Number of trips")
    ax.set_title(title)
    plt.show()

#creates a bar chart with the departures per day of week
def visualizePerDayWeek(data, column_name, color='#0000FF', title='Departure per day of week'):
    plt.figure(figsize=(20, 10))
    ax = (data[column_name].groupby(data['day_number'])
                         .count()).plot(kind="bar", color=color)
    ax.set_facecolor('#eeeeee')
    ax.set_xlabel("Day")
    ax.set_ylabel("Number of trips")
    ax.set_title(title)
    plt.show()

#creates a bar chart with the departures per hour during the weekend
def visualizePerHourEnd(data, column_name, color='#0000FF', title='Avreage Number of Trips Per Hour During the Weekend - January 2018'):
    #WEEKEND
    dataWeekend = data.drop(data[data['week_day_b'] == 1].index)
    plt.figure(figsize=(20, 10))
    ax = ((dataWeekend[column_name].groupby(dataWeekend[column_name].dt.hour)
                         .count())).plot(kind="bar", color=color)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Number of Trips")
    ax.set_title(title)
    plt.rcParams.update({'font.size': 22})
    plt.show()

#creates a bar chart with the departures per hour during the week
def visualizePerHourWeek(data, column_name, color='#0000FF', title='Avreage Number of Trips Per Hour During the Week - January 2018'):
    #WEEK
    dataWeek = data.drop(data[data['week_day_b'] == 0].index)
    plt.figure(figsize=(20, 10))
    ax = ((dataWeek[column_name].groupby(dataWeek[column_name].dt.hour)
                         .count())).plot(kind="bar", color=color)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Number of Trips")
    ax.set_title(title)
    plt.rcParams.update({'font.size': 22})
    plt.show()

# visualizePerDayWeek(data, 'starttime')
# visualizePerDayMonth(data,'starttime')
# visualizePerHourWeek(data, 'starttime')
# visualizePerHourEnd(data, 'starttime')

#### Clustering
#return an afinity matrix
def stations_connectivity(data):
    outbound = pd.crosstab(data["start station id"], data["end station id"])
    inbound = pd.crosstab(data["end station id"], data["start station id"])
    #using the sum gives us and undirected affinity
    #this makes the matrix symmetrical across the diagonal, required by spectral clustering
    connectivity = inbound + outbound
    #spectral clustering also requires the diagonal to be zero
    np.fill_diagonal(connectivity.values, 0)
    connectivity[np.isnan(connectivity)] = 0
    return connectivity

def cluster_labels_to_station_ids(connectivity, labels):
    no_clusters = len(set(labels))

    station_clusters = [ [] for n in range(0, no_clusters)]
    for idx, label in enumerate(labels):
        station = connectivity.columns[idx]
        station_clusters[label].append(station)

    #largest cluster first
    station_clusters = sorted(station_clusters, key=len, reverse=True)
    return station_clusters

#Perform clustering using spectral clustering
def cluster_spectral(data, n_clusters):
    connectivity =  stations_connectivity(data)
    cluster = SpectralClustering(n_clusters=n_clusters, affinity ='precomputed')
    labels = cluster.fit_predict(connectivity)

    station_clusters = cluster_labels_to_station_ids(connectivity, labels)

    return station_clusters

def sations_clust(stations, clustered):
    stations['cluster'] = pd.Series(index=data.index)
    i = 0
    for list in clustered:
        for x in list:
            stations.loc[stations['id'] == x, 'cluster'] = i
        i = i + 1
    #color by cluster
    stations['color'] = pd.Series( index=data.index)
    stations.loc[stations['cluster'] == 0, 'color'] = "#0000FF" #blue
    stations.loc[stations['cluster'] == 1, 'color'] = "#FF0000" #red
    stations.loc[stations['cluster'] == 2, 'color'] = "#4B0082" #purple
    stations.loc[stations['cluster'] == 3, 'color'] = "#FF1493" #pink
    stations.loc[stations['cluster'] == 4, 'color'] = "#32CD32" #green
    stations.loc[stations['cluster'] == 5, 'color'] = "#FF4500" #orange
    stations.loc[stations['cluster'] == 6, 'color'] = "#FFFF00" #yellow
    stations.loc[stations['cluster'] == 7, 'color'] = "#800000" #brown
    stations.loc[stations['cluster'] == 8, 'color'] = "#000000" #black
    stations.loc[stations['cluster'] == 9, 'color'] = "#00FFFF" #aqua
    stations.loc[stations['cluster'] == 10, 'color'] = "#A9A9A9" #gray
    stations.loc[stations['cluster'] == 11, 'color'] = "#FFA07A" #salmon
    stations.loc[stations['cluster'] == 12, 'color'] = "#006400" #dark green

    return stations

def map_clustured(stations):
    # Create base map
    Nyc = [40.730610,-73.935242]
    map = folium.Map(location = Nyc,
                     zoom_start = 12,
                     titles = "CartoDB positron")

    lat = stations['latitude'].values
    lon = stations['longitude'].values
    name = stations['name'].values
    color = stations['color'].values

    # Plot markers for stations
    for _lat, _lon, _name, _color in zip(lat, lon, name, color):
        folium.Circle(location = [_lat, _lon],
                            radius = 30,
                            popup = _name,
                            color = _color).add_to(map)

    f = './map_station_clustered_10.html'
    map.save(f)

# connectivity =  stations_connectivity(data)
# print(connectivity)
clustered = cluster_spectral(data, n_clusters=10)
print(clustered)
stations = pd.read_csv("../../all_stations.csv")
stations_clustered = sations_clust(stations, clustered)
map_clustured(stations_clustered)
