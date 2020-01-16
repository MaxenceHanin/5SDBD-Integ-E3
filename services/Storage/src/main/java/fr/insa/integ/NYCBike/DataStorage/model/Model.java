/**
 * 
 */
package fr.insa.integ.NYCBike.DataStorage.model;

import java.util.UUID;

import org.bson.BsonBinary;
import org.bson.types.ObjectId;

/**
 *
 */
public class Model {
	
	private ObjectId id;
	private int idS;
	private BsonBinary model;
	private String name;
	
	public Model() {}
	
	/**
	 * @param id
	 * @param idS
	 * @param model
	 * @param name
	 */
	public Model(ObjectId id, int idS, BsonBinary model, String name) {
		super();
		this.id = id;
		this.idS = idS;
		this.model = model;
		this.name = name;
	}
	
	/**
	 * @param model
	 * @param name
	 */
	public Model(BsonBinary model, String name) {
		super();
		this.idS = UUID.randomUUID().hashCode();
		this.model = model;
		this.name = name;
	}

	public ObjectId getId() {
		return id;
	}

	public void setId(ObjectId id) {
		this.id = id;
	}

	public int getIdS() {
		return idS;
	}

	public void setIdS(int idS) {
		this.idS = idS;
	}

	public BsonBinary getModel() {
		return model;
	}

	public void setModel(BsonBinary model) {
		this.model = model;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
}
