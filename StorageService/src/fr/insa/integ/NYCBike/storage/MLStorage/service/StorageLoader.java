package fr.insa.integ.NYCBike.storage.MLStorage.service;


import java.util.ArrayList;
import java.util.Set;

import javax.websocket.server.PathParam;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

import org.bson.Document;

import com.mongodb.BasicDBObject;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.MongoIterable;



@Path("StorageLoader")
public class StorageLoader {
	public MongoDatabase ConnectDB(String DB_Name){
		MongoClientURI uri = new MongoClientURI(
			    "mongodb+srv://MaxenceHanin:Revente21*@predmodel-4pwxr.mongodb.net/"+DB_Name+"?retryWrites=true&w=majority");
		MongoClient mongoClient = new MongoClient(uri);
		MongoDatabase db = mongoClient.getDatabase(DB_Name);
//		mongoClient.close();
		return db;
	}
	
	@GET
	@Produces(MediaType.TEXT_PLAIN)
	public String getModelList(){
		ArrayList<String> modelsList = new ArrayList<String>();
		try{
	    	MongoDatabase db = ConnectDB("sample_mflix");
	    	// get list of collections
	    	MongoIterable<String> collections = db.listCollectionNames();

	    	for (String collectionName : collections) {
	    		modelsList.add(collectionName.toString());
	    	}
		} catch (Exception e) {
			e.printStackTrace();
		    }
	    return modelsList.toString();
	}
	@GET
	@Path("models/{model_ID}")
	@Produces(MediaType.TEXT_PLAIN)
	public String getModel(@PathParam("model_ID") String model_ID){
		String model = new String();
		try{
	    	MongoDatabase db = ConnectDB("sample_mflix");
	    	MongoCollection<Document> collection = db.getCollection(model_ID);
	    	
	    	BasicDBObject query = new BasicDBObject("name", "Olly");
	    	FindIterable<Document> cursor = collection.find(query);
	    	if(cursor.cursor().hasNext())
	    	{
	    	   model = cursor.cursor().next().toString();
	    	}
	    	
		} catch (Exception e) {
			e.printStackTrace();
		    }
		return model;
	}
	

}
