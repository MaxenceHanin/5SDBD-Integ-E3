/**
 * 
 */
package fr.insa.integ.NYCBike.DataStorage.model;

import java.util.UUID;

import org.bson.types.ObjectId;

/**
 *
 */
public class Model {
	
	private ObjectId id;
	private int idS;
	private String type;
	private String name;
	
	public Model() {}
	
	/**
	 * @param id
	 * @param idS
	 * @param type
	 * @param name
	 */
	public Model(ObjectId id, int idS, String type, String name) {
		super();
		this.id = id;
		this.idS = idS;
		this.type = type;
		this.name = name;
	}
	
	/**
	 * @param type
	 * @param name
	 */
	public Model(String type, String name) {
		super();
		this.idS = UUID.randomUUID().hashCode();
		this.type = type;
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

	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
}
