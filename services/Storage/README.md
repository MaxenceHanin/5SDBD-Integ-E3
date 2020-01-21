## Import projects - Troubleshooting

- ["httpservlet clas not found"](https://howtodoinjava.com/eclipse/solved-the-superclass-javax-servlet-http-httpservlet-was-not-found-on-the-java-build-path-in-eclipse/)

- Set the context roots: 
	- **Predictions** : 5sdbd-integ-e3/predictions
	- **Storage** : 5sdbd-integ-e3/storage
	- **UserInterface** : citibike-app

## Help and tutorials

- [Test REST API with curl](https://www.baeldung.com/curl-rest)

```bash
# Get the list of all the stations
curl -v "http://localhost:8080//5sdbd-integ-e3/storage/data/stations"
# Get all stations around one station
curl -v "http://localhost:8080//5sdbd-integ-e3/storage/data/stations/320/"
# Prediction example
curl -v "http://localhost:8080/5sdbd-integ-e3/predictions/predict/next_station/32?hour=5&weekday=2&month=12&age=5&gender=1"
```

- **User interface**: 

go to the address `http://localhost:8080/citibike-app/`
