# Services API definition

## Storage Service

The storage service aims to provide the models, e.g. for the prediction service and data about New York Citibike stations. The resources types are `Model` and `Station`.
The returned data is in JSON format.

### Models
*URL: https://5sdbd-integ-e3.fr/storage/ml/*

| Method | HTTP Request | Description |
|---|---|---|
| list | GET /models | Returns a list of available models |
| get | GET /models/[model-ID] | Returns the serialized model |

### Stations
*URL: https://5sdbd-integ-e3.fr/storage/data/*

| Method | HTTP Request | Description |
|---|---|---|
| list | GET /stations | Returns a list of citibike stations in NYC |
| get | GET /stations/[station-ID] | Returns information on a specific station |
| get_around | GET /stations/[station-ID]/around | Returns the list of all the stations near the origin station.<br>**Parameters**:<br> - radius: All station must be in the given radius in meters |

## Predict Service

*URL: https://5sdbd-integ-e3.fr/predictions/predict/*

### From an origin station, the date and user data

This service predicts the next station based on the origin station, the date and user data.
The type of the response is plain text.

| Method | HTTP Request | Description |
|---|---|---|
| predict_next_station | GET /next_station/[station_id] | Returns a prediction of the arrival station.<br>**Parameters**:<br> - hour: hour for the prediction <br> - weekday: day of the week for the prediction (integer within range [0, 6]) <br> - month: month for the prediction (in [1, 12]) <br> - age: age of the user <br> - gender: gender of the user (0 = unknown, 1 = male, 2 = female) |
