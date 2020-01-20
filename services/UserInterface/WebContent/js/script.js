window.onload = function() {
    
    predict_next_station = document.getElementById("predict-next-station");
    
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
    
    $("#date").datepicker();
    
    sendGet("http://localhost:8080/5sdbd-integ-e3/storage/data/stations", function(responseText) {
    	response = JSON.parse(responseText);
        resultStr = "";
        
        for (key in response) {
            val = response[key];
        	stationList[val["stationName"]] = parseInt(val["idS"]);
        	
        	dropdown = document.getElementById("station");
        	
        	var option = document.createElement("option");
        	option.text = val["stationName"];
        	dropdown.add(option);
        }
    });
    
    predict_next_station.onsubmit = function() {
        formData = new FormData(predict_next_station);
        station_name = formData.get("station");
        station_id = stationList[station_name];
        date = Date.parse(formData.get("date"));
        
        if (!station_id) {
            document.getElementById("result").innerHTML = "Bad station id";
        }
        
        sendGet("http://localhost:8080/5sdbd-integ-e3/storage/data/stations/" + station_id, function(responseText) {
        	val = JSON.parse(responseText);
            // Returns station id, name, latitude and longitude
            resultStr = val["idS"] + ": " + val["stationName"] + " (" + val["latitude"] + ", " + val["longitude"] + ")<br/>";
            document.getElementById("result").innerHTML = resultStr;
        });
        
        return false;
    };
}
