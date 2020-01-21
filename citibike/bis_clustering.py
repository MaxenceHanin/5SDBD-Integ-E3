"""
Clustering stations using Spectral clustering
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
import math

from sklearn.cluster import KMeans, SpectralClustering
from sklearn.preprocessing import MinMaxScaler
import sklearn.metrics as metrics

# https://towardsdatascience.com/understanding-bixi-commuters-an-analysis-of-montreals-bike-share-system-in-python-cb34de0e2304

trips_file = "../datasets/201801-citibike-tripdata.csv"
stations_file = "../datasets/all_stations.csv"

def read_db(fname):
    return pd.read_csv(fname)

#### Data Processing

def trip_data_processing(data):
    #filtering out trips that were less than 2 minutes
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

    #adding a column to split the departures in 20 min groups (8h-8h20 = 480; 8h20-8h40 = 500; 8h40-9h = 520)
    data["time_slice"] = data["starttime"].dt.hour * 60 + np.floor(data["starttime"].dt.minute/20)*20
    pd.options.mode.chained_assignment = None
    data["time_slice"] = data["time_slice"].astype("int64")

    return data

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
def visualizePerHourEnd(data, column_name, color='#0000FF', title='Average Number of Trips Per Hour During the Weekend - January 2018'):
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
def visualizePerHourWeek(data, column_name, color='#0000FF', title='Average Number of Trips Per Hour During the Week - January 2018'):
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

#creates a bar chart with the departures per day of week
def visualizePerTimeslice(data, column_name, color='#0000FF', title='Departure per timeslot'):
    plt.figure(figsize=(20, 10))
    ax = (data[column_name].groupby(data['time_slice'])
                         .count()).plot(kind="bar", color=color)
    ax.set_facecolor('#eeeeee')
    # ax.set_xlim(0,1420)
    ax.set_xlabel("Timeslot")
    ax.set_ylabel("Number of trips")
    ax.set_title(title)
    plt.show()

#counts the number of departures and arrivals for each station during a specific timeslot during the week
def flowCount(data, start_time, end_time):
    stations = read_db(stations_file)

    #drop weekends
    data = data.drop(data[data['week_day_b'] == 0].index)

    #select time slot
    data = data.drop(data[data['time_slice'].between(0,start_time)].index)
    data = data.drop(data[data['time_slice'].between(end_time, 1420)].index)

    #agregate the number of departures per stations
    data_s = data.groupby('start station id').size().to_frame('departures_cnt').reset_index()
    data_s = data_s.rename(columns={'start station id':'id'})
    data_e = data.groupby('end station id').size().to_frame('arrivals_cnt').reset_index()
    data_e = data_e.rename(columns={'end station id':'id'})

    #add a net departure column
    stations = pd.merge(stations, data_s, on='id')
    stations = pd.merge(stations, data_e, on='id')
    stations['net_departures'] = pd.Series( index=data.index)
    stations['net_departures'] = stations['departures_cnt'] - stations['arrivals_cnt']

    #replace stations with 0 net_departures by 1 to avoid calcultions using 0
    stations.loc[stations['net_departures'].eq(0), 'net_departures'] = 1

    return stations

#creates a map with the stations colored based on the flow (red=more departures/net outflux, green=more arrivals/net influx)
def densityMap(stations, start_time, end_time):
    #generate a new map
    Nyc = [40.730610,-73.935242]
    map = folium.Map(location = Nyc,
                zoom_start = 12,
                tiles = "CartoDB positron")

    #calculate stations radius
    stations['radius'] = pd.Series( index=data.index)
    stations['radius'] = np.abs(stations['net_departures'])
    stations['radius'] = stations['radius'].astype(float)

    #set stations color
    stations['color'] = '#E80018' # red
    stations.loc[stations['net_departures'].between(-math.inf,0), 'color'] = '#00E85C' # green

    lat = stations['latitude'].values
    lon = stations['longitude'].values
    name = stations['name'].values
    rad = stations['radius'].values
    color = stations['color'].values
    net_dep = stations['net_departures']

    #populate map
    for _lat, _lon, _rad, _color, _name, _nd in zip(lat, lon, rad, color, name, net_dep):
        folium.Circle(location = [_lat,_lon],
                            radius = _rad/5,
                            color = _color,
                            tooltip = _name + " / net. dep:" +str(_nd),
                            fill = True).add_to(map)

    #save map
    f = 'maps/map_density_' + str(start_time) + '_' + str(end_time) + '.html'
    map.save(f)

#### Clustering

#return an afinity matrix
def stations_connectivity(data):
    outbound = pd.crosstab(data["start station id"], data["end station id"])
    inbound = pd.crosstab(data["end station id"], data["start station id"])
    #using the sum gives us an undirected affinity
    #this makes the matrix symmetrical across the diagonal, required by spectral clustering
    connectivity = inbound + outbound
    #spectral clustering also requires the diagonal to be zero
    np.fill_diagonal(connectivity.values, 0)
    connectivity[np.isnan(connectivity)] = 0
    return connectivity

#List stations in each cluster
def cluster_labels_to_station_ids(connectivity, labels):
    no_clusters = len(set(labels))

    # get station ids from the columns of the connectivity matrix
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

# Kmeans Clustering : Simple, facile à mettre en oeuvre, mais limité
def cluster_kmeans(data, n_clusters = range(2, 20), metric = "db"):
    #drop weekends
    data = data.drop(data[data['week_day_b'] == 0].index)

    #only keep spatial and temporal features
    df = data[["start station latitude", "start station longitude", "end station latitude", "end station longitude","time_slice"]]

    #normalize values
    scaler = MinMaxScaler()
    scaled_values = scaler.fit_transform(df)
    df.loc[:,:] = scaled_values
    # print(df)

    #Clustering
    model = None
    
    if hasattr(n_clusters, "__iter__"):
        # Metrics parameters
        if metric == "db":
            sense = 1
            method = metrics.davies_bouldin_score
        elif metric == "sil":
            sense = -1
            method = metrics.silhouette_score
        else:
            raise ValueError("Bad metrics provided to cluster_kmeans()")
        
        best_score = sense * 10000
        best_model = None
        
        for n in n_clusters:
            cluster = KMeans(n_clusters=n, init = 'k-means++')
            labels = cluster.fit_predict(df)
            score = method(df, labels)
            print("kmeans: n_cluster == %d, score == %f" % (n, score))
            
            if (sense * best_score > sense * score):
                best_score = score
                best_model = cluster
                
        print("best_score is %f for n = %d" % (best_score, best_model.n_clusters))
        model = best_model
    else:
        model = KMeans(n_clusters=n_clusters, init = 'k-means++')
        
    labels = model.fit_predict(df)
    values, counts = np.unique(labels, return_counts=True)
    print("number for each label")
    print(counts)

    #inverse normalization
    unscaled = scaler.inverse_transform(df)
    df.loc[:,:] = unscaled

    #add cluster to data
    se = pd.Series(labels)
    df['cluster'] = se.values
    print(df)

    return df
    
def get_cluster_count(df):
    return max(df["cluster"]) + 1

# HDBSCAN clustering : Plus complexe, outsiders, meilleurs résultats ?
def cluster_hdbscan(data):
    pass

#Create stations from clusters
def stations_labels(data):
    no_clusters = len(set(data['cluster']))
    in_station_clusters = [ set() for n in range(0, no_clusters)]
    out_station_clusters = [ set() for n in range(0, no_clusters)]

    for l in range(no_clusters):
        in_station_clusters[l] = set(zip(data.loc[data['cluster']==l,'start station latitude'], data.loc[data['cluster']==l,'start station longitude']))
        out_station_clusters[l] = set(zip(data.loc[data['cluster']==l,'end station latitude'], data.loc[data['cluster']==l,'end station longitude']))

    return(in_station_clusters,out_station_clusters)

def map_cluster_trips(in_st,out_st,label):
    # Create base map
    Nyc = [40.730610,-73.935242]
    map = folium.Map(location = Nyc,
                     zoom_start = 12,
                     titles = "CartoDB positron")

    lat = [pos[0] for pos in out_st[label]] + [pos[0] for pos in in_st[label]]
    lon = [pos[1] for pos in out_st[label]] + [pos[1] for pos in in_st[label]]
    color = ["#FF0000" for pos in out_st[label]] + ["#32CD32" for pos in in_st[label]]

    # Plot markers for stations
    for _lat, _lon, _color in zip(lat, lon, color):
        folium.Circle(location = [_lat, _lon],
                            radius = 30,
                            color = _color).add_to(map)

    f = './maps/imap_cluster-' + str(label) + '.html'
    map.save(f)

#Add cluster to stations
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

    f = './maps/map_station_clustered_10.html'
    map.save(f)


if __name__ == '__main__':

    data = read_db(trips_file)
    stations = read_db(stations_file)

    #### Processing
    data = trip_data_processing(data)

    todo = ["spectral"]

    #### Visualization
    # visualizePerDayWeek(data, 'starttime')
    # visualizePerDayMonth(data,'starttime')
    # visualizePerHourWeek(data, 'starttime')
    # visualizePerHourEnd(data, 'starttime')
    # 14h = 840; 21h = 1260
    # 7h-7h20 = 420; 9h40-10h = 580
    # stations_flow = flowCount(data, 420, 580)
    # densityMap(stations_flow, 420, 580)
    # 16h-16h20 = 960; 19h40-20h = 1180
    # stations_flow = flowCount(data, 960, 1180)
    # densityMap(stations_flow, 960, 1180)

    #### Clustering
    if "spectral" in todo:
        connectivity =  stations_connectivity(data)
        # print(connectivity)
        clustered = cluster_spectral(data, n_clusters=10)
        # print(clustered)
        stations_clustered = sations_clust(stations, clustered)
        map_clustured(stations_clustered)
        stations_clustered.to_csv('../datasets/clustered_stations.csv')

    if "kmeans" in todo:
        df = cluster_kmeans(data, n_clusters=2)
        cluster_count = get_cluster_count(df)
        print("%d clusters" % cluster_count)
        
        for l in range(cluster_count):
            (st,en) = stations_labels(df)
            map_cluster_trips(st,en,l)
            visualizePerTimeslice(df.drop(df[df['cluster'] != l].index),'time_slice')
