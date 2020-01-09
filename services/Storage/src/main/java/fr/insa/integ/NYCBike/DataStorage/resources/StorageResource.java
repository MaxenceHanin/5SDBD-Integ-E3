/**
 * 
 */
package fr.insa.integ.NYCBike.DataStorage.resources;

import static org.bson.codecs.configuration.CodecRegistries.fromProviders;
import static org.bson.codecs.configuration.CodecRegistries.fromRegistries;

import java.util.ArrayList;

import org.bson.codecs.configuration.CodecRegistry;
import org.bson.codecs.pojo.PojoCodecProvider;

import com.mongodb.BasicDBObject;
import com.mongodb.Block;
import com.mongodb.MongoClient;
import com.mongodb.MongoClientSettings;
import com.mongodb.MongoClientURI;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

/**
 * Methods for connecting to MongoDB
 *
 */
public abstract class StorageResource<T> {

	protected String dbName = "CitiBike";

	protected MongoClient connectMongoDB() {
		MongoClientURI uri = new MongoClientURI(
				"mongodb+srv://MaxenceHanin:Revente21*@predmodel-4pwxr.mongodb.net/test?retryWrites=true&w=majority");

		return new MongoClient(uri);
	}

	protected CodecRegistry createCodecReg() {
		return fromRegistries(MongoClientSettings.getDefaultCodecRegistry(),
				fromProviders(PojoCodecProvider.builder().automatic(true).build()));
	}

	protected abstract MongoCollection<T> getCollection(MongoDatabase db);
	
	public ArrayList<T> listGen() {
		CodecRegistry pojoCodecRegistry = createCodecReg();

		MongoClient mongoClient = connectMongoDB();

		MongoDatabase database = mongoClient.getDatabase(dbName).withCodecRegistry(pojoCodecRegistry);

		MongoCollection<T> collection = getCollection(database);

		ArrayList<T> ret = new ArrayList<T>();

		Block<T> addElement = new Block<T>() {
			@Override
			public void apply(final T e) {
				ret.add(e);
			}
		};

		collection.find().forEach(addElement);

		mongoClient.close();
	
		return ret;
	}
	
	public T getGen(int id) {
		CodecRegistry pojoCodecRegistry = createCodecReg();
		
		MongoClient mongoClient = connectMongoDB();
		
		MongoDatabase database = mongoClient.getDatabase(dbName).withCodecRegistry(pojoCodecRegistry);
		
		MongoCollection<T> collection = getCollection(database);
		
		BasicDBObject whereQuery = new BasicDBObject();
		whereQuery.put("idS", id);

		T ret = collection.find(whereQuery).first();
		
		mongoClient.close();
				
		return ret;	
	}

}
