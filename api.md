# Microservices API definition

## ML Storage Service

*URL: https://5sdbd-integ-e3.fr/storage/*

The ML storage service aims to provide the models, e.g. for the prediction service. The only resource type is `Model`.

| Method | HTTP Request | Description |
|---|---|---|
| list | GET /models | Returns a list of available models |
| get | GET /models/[model-ID] | Returns model metadata and URL (json format) |

## Data Storage Service

The data storage service provides data about new york citibike traffic and stations

### Stations

| Method | HTTP Request | Description |
|---|---|---|
| list | GET /stations | Returns a list of citibike stations in NYC |
| get | GET /stations/[station-ID] | Returns information on a specific station |
| get_around | GET /stations/[station-ID]/around | Returns the list of all the stations near the origin station.<br>**Parameters**:<br> - radius: All station must be in the given radius in meters |

## Predict Service

*URL: https://5sdbd-integ-e3.fr/predict/*

### From an origin station and the date

This service predicts the next station based on the origin station and the date.

| Method | HTTP Request | Description |
|---|---|---|
| predict_next_station | GET /next_station/[station_id] | Returns a prediction of the arrival station, based on given parameters.<br>**Parameters**:<br> - date: The date of the prediction (default: now) |
