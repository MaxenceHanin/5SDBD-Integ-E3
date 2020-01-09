/**
 * 
 */
package fr.insa.integ.NYCBike.DataStorage.model;

import java.util.UUID;

import org.bson.types.ObjectId;

/**
 *
 */
public class Station {

    private ObjectId id;
	private int idS;
	private Double latitude;
	private Double longitude;
	private String stationName;
	private String address;
	private int docks;

	public Station() {}
	
	/**
	 * @param id
	 * @param idS
	 * @param latitude
	 * @param longitude
	 * @param stationName
	 * @param address
	 * @param docks
	 */
	public Station(ObjectId id, int idS, Double latitude, Double longitude, String stationName, String address,
			int docks) {
		super();
		this.id = id;
		this.idS = idS;
		this.latitude = latitude;
		this.longitude = longitude;
		this.stationName = stationName;
		this.address = address;
		this.docks = docks;
	}

	/**
	 * @param idS
	 * @param latitude
	 * @param longitude
	 * @param name
	 * @param address
	 * @param docks
	 */
	public Station(int idS, Double latitude, Double longitude, String name, String address, int docks) {
		super();
		this.idS = idS;
		this.latitude = latitude;
		this.longitude = longitude;
		this.stationName = name;
		this.address = address;
		this.docks = docks;
	}

	/**
	 * @param latitude
	 * @param longitude
	 * @param name
	 * @param docks
	 */
	public Station(Double latitude, Double longitude, String name, String address, int docks) {
		super();
		this.idS = UUID.randomUUID().hashCode();
		this.latitude = latitude;
		this.longitude = longitude;
		this.stationName = name;
		this.address = address;
		this.docks = docks;
	}

	public Double getLatitude() {
		return latitude;
	}

	public void setLatitude(final Double latitude) {
		this.latitude = latitude;
	}

	public Double getLongitude() {
		return longitude;
	}

	public void setLongitude(final Double longitude) {
		this.longitude = longitude;
	}

	public String getStationName() {
		return stationName;
	}

	public void setStationName(final String name) {
		this.stationName = name;
	}

	public String getAddress() {
		return address;
	}

	public void setAddress(final String address) {
		this.address = address;
	}

	public int getDocks() {
		return docks;
	}

	public void setDocks(final int docks) {
		this.docks = docks;
	}

	public int getIdS() {
		return idS;
	}
	
	public void setIdS(final int idS) {
		this.idS = idS;
	}
	
    public ObjectId getId() {
        return id;
    }

    public void setId(final ObjectId id) {
        this.id = id;
    }
    
    @Override
    public String toString() {
    	return "id: " + this.idS + " name: " + this.stationName + " address: " + this.address + " total docks: " + this.docks + " latitude: " + this.latitude + " longitude: " + this.longitude;
    }
    
    // from https://www.geeksforgeeks.org/program-distance-two-points-earth/
    /**
     * Distance between this station and another location
     * @param lat
     * @param lon
     * @return distance in meters
     */
    public double distance(double lat, double lon) {
		if ((this.latitude == lat) && (this.longitude == lon)) {
			return 0;
		}
		else {
	        double lon1 = Math.toRadians(this.longitude); 
	        double lon2 = Math.toRadians(lon); 
	        double lat1 = Math.toRadians(this.latitude); 
	        double lat2 = Math.toRadians(lat); 
	  
	        // Haversine formula  
	        double dlon = lon2 - lon1;  
	        double dlat = lat2 - lat1; 
	        double a = Math.pow(Math.sin(dlat / 2), 2) 
	                 + Math.cos(lat1) * Math.cos(lat2) 
	                 * Math.pow(Math.sin(dlon / 2),2); 
	              
	        double c = 2 * Math.asin(Math.sqrt(a)); 
	  
	        // Radius of earth in kilometers
	        double r = 6371; 
	  
	        // calculate the result in meters
	        return(c * r * 1000);
		}
	}
}
