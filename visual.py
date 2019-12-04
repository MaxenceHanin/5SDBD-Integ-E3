import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

START_STATION = "start station id"
START_X = "start station longitude"
START_Y = "start station latitude"
END_STATION = "end station id"
END_X = "end station longitude"
END_Y = "end station latitude"

def load_dataset(filename):
    data = pd.read_csv(filename)
    return data

def visualize_stations(data, station_x, station_y, station_count):
    sns.relplot(x=station_x, y=station_y, size=station_count, data=data)

def visualize_trips(data):
    pass

""" Returns a dataset with columns:
start_station (-, _x, _y), end_station (-, _x, _y), count
"""
def group_by_trajectory(data):
    pass

""" Returns a dataset with columns:
station, x, y, start_count, end_count
"""    
def group_by_station(data):
    start = data.groupby([START_STATION, START_X, START_Y])["bikeid"].count().reset_index(name="count")
    end = data.groupby([END_STATION, END_X, END_Y])["bikeid"].count().reset_index(name="count")
    result = pd.merge(start, end, left_on=[START_STATION, START_X, START_Y], right_on=[END_STATION, END_X, END_Y])
    result = result.rename(columns={START_STATION: "station", START_X: "x", START_Y: "y", "count_x": "start_count", "count_y": "end_count"})
    result = result[["station", "x", "y", "start_count", "end_count"]]
    return result

if __name__ == "__main__":
    data = load_dataset("datasets/JC-201909-citibike-tripdata.csv")
    grouped = group_by_station(data)
    visualize_stations(grouped, "x", "y", "start_count")
    visualize_stations(grouped, "x", "y", "end_count")
    plt.show()
    visualize_trips(data)