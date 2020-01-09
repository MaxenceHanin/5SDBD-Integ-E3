/**
 * 
 */
package fr.insa.integ.NYCBike.DataStorage.resources;

import java.util.ArrayList;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

import fr.insa.integ.NYCBike.DataStorage.model.Station;

/**
 * Root resource
 */
@Path("data")
public class StationsData extends StorageResource<Station> {
		
	@Override
	protected MongoCollection<Station> getCollection(MongoDatabase db) {
		return db.getCollection("Stations", Station.class);
	}

	/**
	 * @return list of all stations
	 */
	@GET
	@Path("/stations")
	@Produces(MediaType.APPLICATION_JSON)
	public ArrayList<Station> list() {
		return listGen();
	}
	
	/**
	 * Get a station
	 * @param id of the station
	 * @return station
	 */
	@GET
	@Path("/stations/{station-ID}")
	@Produces(MediaType.APPLICATION_JSON)
	public Station get(@PathParam("station-ID") int id) {
		return getGen(id);
	}
	
	/**
	 * Get all stations within radius meters to the station with given id
	 * @param id of the center station
	 * @param radius in meters
	 * @return list of stations
	 */
	@GET
	@Path("/stations/{station-ID}/around")
	@Produces(MediaType.APPLICATION_JSON)
	public ArrayList<Station> get_around(@PathParam("station-ID") int id, @QueryParam("radius") double radius) {
		ArrayList<Station> all_stations = listGen();
		ArrayList<Station> close_stations = new ArrayList<Station>();
		Station center = getGen(id);
		for(int i = 0; i<all_stations.size();i++) {
			double d = center.distance(all_stations.get(i).getLatitude(), all_stations.get(i).getLongitude());
			if (d <= radius && all_stations.get(i).getIdS() != center.getIdS()) {
				close_stations.add(all_stations.get(i));
			}
		}
		return close_stations;
	}
}
