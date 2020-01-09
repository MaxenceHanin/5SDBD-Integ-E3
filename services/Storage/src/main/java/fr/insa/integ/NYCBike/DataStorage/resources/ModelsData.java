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

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

import fr.insa.integ.NYCBike.DataStorage.model.Model;

/**
 *
 */
@Path("ml")
public class ModelsData extends StorageResource<Model> {
			
	@Override
	protected MongoCollection<Model> getCollection(MongoDatabase db) {
		return db.getCollection("Models", Model.class);
	}
	
	/**
	 * @return list of all models
	 */
	@GET
	@Path("/models")
	@Produces(MediaType.APPLICATION_JSON)
	public ArrayList<Model> list() {
		return listGen();
	}
	
	/**
	 * Get a model
	 * @param id of the model
	 * @return model
	 */
	@GET
	@Path("/models/{model-ID}")
	@Produces(MediaType.APPLICATION_JSON)
	public Model get(@PathParam("model-ID") int id) {
		return getGen(id);
	}
}
