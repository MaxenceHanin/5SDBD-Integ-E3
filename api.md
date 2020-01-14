# Services API definition

## Storage Service

The storage service aims to provide the models, e.g. for the prediction service and data about New York Citibike stations. The resources types are `Model` and `Station`.

### Models
*URL: https://5sdbd-integ-e3.fr/storage/ml/*

| Method | HTTP Request | Description |
|---|---|---|
| list | GET /models | Returns a list of available models |
| get | GET /models/[model-ID] | Returns model metadata and URL (json format) |

### Stations
*URL: https://5sdbd-integ-e3.fr/storage/data/*

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
| predict_next_station | GET /next_station/[station_id] | Returns a prediction of the arrival station.<br>**Parameters**:<br> - date: date of the prediction (default: now) <br> - age: age of the user <br> - gender: gender of the user|
