window.onload = function() {
    
    predict_next_station = document.getElementById("predict-next-station");
    
    predict_next_station.addEventListener("on-submit", function() {
        formData = new FormData(predict_next_station)
        station_id = parseInt(formData.get("station"))
        date = Date.parse(formData.get("date"))
        
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                response = JSON.parse(xhr.responseText);
                resultStr = "";
                
                // Returns each station id, name, latitude and longitude
                for (val in response) {
                    resultStr += response["id"] + ": " + response["name"] + "(" + response["latitude"] + ", " + response["longitude"] + ")<br/>";
                }
                
                document.getElementById("result").innerHTML = resultStr;
            }
            else {
                console.log("This is an error you got there");
            }
        };
        xhr.open('GET', "http://FUUUUUU");
        xhr.send();
        
        return false;
    });
    
}
