# Microservices API definition

## Storage Service

*URL: https://5sdbd-integ-e3.fr/storage/*

The storage service aims to provide the models, e.g. for the prediction service. The only resource type is `Model`.

| Method | HTTP Request | Description |
|---|---|---|
| list | GET /models | Returns a list of available models |
| get | GET /models/[model-ID] | Returns model metadata and URL (json format) |

## Predict service

*URL: https://5sdbd-integ-e3.fr/predict/*

### From an origin station and the date

This service predicts the next station based on the origin station and the date.

| Method | HTTP Request | Description |
|---|---|---|
| get | POST /next_station/[station_id] | Returns a prediction of the arrival station, based on given parameters. You can pass the date by parameters, otherwise the date is assumed to be now. |
