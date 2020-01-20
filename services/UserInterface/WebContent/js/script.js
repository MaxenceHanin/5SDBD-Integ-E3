window.onload = function() {
    
    function sendGet(address, callback, err) {
    	var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                callback(xhr.responseText);
            }
            else {
                console.log("ready state changed: " + xhr.readyState);
            }
        };
        xhr.open('GET', address);
        xhr.send();
    }
    
    // Key = station name, value = id
    var stationList = {};
    
    $(".datepicker").datepicker();
    
    function updateStationDD(response, dropdown) {
    	for (key in response) {
            val = response[key];
        	var option = document.createElement("option");
        	option.text = val["stationName"];
        	dropdown.add(option);
        }
    }
    
    sendGet("http://localhost:8080/5sdbd-integ-e3/storage/data/stations", function(responseText) {
    	response = JSON.parse(responseText);

    	for (key in response) {
            val = response[key];
        	stationList[val["stationName"]] = parseInt(val["idS"]);
        }

    	updateStationDD(response, document.getElementById("station1"));
    	updateStationDD(response, document.getElementById("station2"));
    });

    get_station_info = $("#get-station-info");
    get_station_info.submit(function(e) {
        e.preventDefault();
        
        formData = new FormData(get_station_info.get(0));
        station_name = formData.get("station");
        station_id = stationList[station_name];
        
        if (!station_id) {
            document.getElementById("result-station-info").innerHTML = "Bad station id";
        }
        
        sendGet("http://localhost:8080/5sdbd-integ-e3/storage/data/stations/" + station_id, function(responseText) {
        	val = JSON.parse(responseText);
            // Returns station id, name, latitude and longitude
            resultStr = val["idS"] + ": " + val["stationName"] + " (" + val["latitude"] + ", " + val["longitude"] + ")<br/>";
            document.getElementById("result-station-info").innerHTML = resultStr;
        });
        
        return false;
    });
    
    predict_next_station = $("#predict-next-station");
    predict_next_station.submit(function(e) {
    	e.preventDefault();
    	
        formData = new FormData(predict_next_station.get(0));
        station_name = formData.get("station");
        station_id = stationList[station_name];
        date = new Date(formData.get("date"));
        hour = parseInt(formData.get("hour"));
        
        if (!station_id) {
            document.getElementById("result-next-station").innerHTML = "Bad station id";
        }
        
        address = "http://localhost:8080/5sdbd-integ-e3/predictions/predict/next_station/"
    		+ station_id + "?hour=" + hour + "&weekday=" + date.getDay() + "&month=" + (date.getMonth() + 1)
    		+ "&age=0&gender=0";
        console.log(address);
        
        sendGet(address, function(responseText) {
        	val = JSON.parse(responseText);
            // Returns station id, name, latitude and longitude
            resultStr = val["idS"] + ": " + val["stationName"] + " (" + val["latitude"] + ", " + val["longitude"] + ")<br/>";
            document.getElementById("result-next-station").innerHTML = resultStr;
        });
        
        return false;
    });
    
}
