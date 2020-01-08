/**
 * 
 */
package fr.insa.integ.NYCBike.DataStorage.resources;

import java.util.ArrayList;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

import org.bson.codecs.configuration.CodecRegistry;
import org.bson.codecs.pojo.PojoCodecProvider;

import com.mongodb.Block;
import com.mongodb.MongoClient;
import com.mongodb.MongoClientSettings;
import com.mongodb.MongoClientURI;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

import static org.bson.codecs.configuration.CodecRegistries.fromProviders;
import static org.bson.codecs.configuration.CodecRegistries.fromRegistries;
import static com.mongodb.client.model.Filters.*;

import fr.insa.integ.NYCBike.DataStorage.model.Station;

/**
 * Root resource
 */
@Path("data")
public class StationsData {

	/**
	 */
	@GET
	@Path("/stations")
	@Produces(MediaType.APPLICATION_JSON)
	public ArrayList<Station> list() {
		
		CodecRegistry pojoCodecRegistry = fromRegistries(MongoClientSettings.getDefaultCodecRegistry(),
                fromProviders(PojoCodecProvider.builder().automatic(true).build()));

		MongoClientURI uri = new MongoClientURI(
				"mongodb+srv://MaxenceHanin:Revente21*@predmodel-4pwxr.mongodb.net/test?retryWrites=true&w=majority");

		MongoClient mongoClient = new MongoClient(uri);
		MongoDatabase database = mongoClient.getDatabase("CitiBike").withCodecRegistry(pojoCodecRegistry);
		
		MongoCollection<Station> collection = database.getCollection("Stations", Station.class);
		
		ArrayList<Station> ret = new ArrayList<Station>();
		
		Block<Station> addStation = new Block<Station>() {
		    @Override
		    public void apply(final Station station) {
		    	ret.add(station);
		    }
		};

		collection.find().forEach(addStation);
		
		mongoClient.close();
		
		for (Station tp:ret) {
			System.out.println(tp);
		}
		
		return ret;
	}
	
	@GET
	@Path("/stations/{station-ID}")
	@Produces(MediaType.APPLICATION_JSON)
	public Station get(@PathParam("station-ID") String stationID) {
		
		CodecRegistry pojoCodecRegistry = fromRegistries(MongoClientSettings.getDefaultCodecRegistry(),
                fromProviders(PojoCodecProvider.builder().automatic(true).build()));

		MongoClientURI uri = new MongoClientURI(
				"mongodb+srv://MaxenceHanin:Revente21*@predmodel-4pwxr.mongodb.net/test?retryWrites=true&w=majority");

		MongoClient mongoClient = new MongoClient(uri);
		MongoDatabase database = mongoClient.getDatabase("CitiBike").withCodecRegistry(pojoCodecRegistry);
		
		MongoCollection<Station> collection = database.getCollection("Stations", Station.class);

		Station ret = collection.find(eq("idS", stationID)).first();
		
		mongoClient.close();
		
		System.out.println(ret);
		
		return ret;
	}


}
