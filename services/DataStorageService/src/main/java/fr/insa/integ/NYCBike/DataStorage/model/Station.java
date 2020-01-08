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
	private String idS;
	private Float latitude;
	private Float longitude;
	private String stationName;
	private String address;
	private int docks;

	public Station() {}
	
	/**
	 * @param id
	 * @param latitude
	 * @param longitude
	 * @param name
	 * @param address
	 * @param docks
	 */
	public Station(String idS, Float latitude, Float longitude, String name, String address, int docks) {
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
	public Station(Float latitude, Float longitude, String name, int docks) {
		super();
		this.idS = UUID.randomUUID().toString();
		this.latitude = latitude;
		this.longitude = longitude;
		this.stationName = name;
		this.docks = docks;
	}

	public Float getLatitude() {
		return latitude;
	}

	public void setLatitude(final Float latitude) {
		this.latitude = latitude;
	}

	public Float getLongitude() {
		return longitude;
	}

	public void setLongitude(final Float longitude) {
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

	public String getIdS() {
		return idS;
	}
	
	public void setIdS(final String idS) {
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
}
