package fr.insa.integ.NYCBike.DataStorage.model;

import java.util.ArrayList;

/**
 * */
public class Stations {

	private static Stations stations = null;

	private ArrayList<Station> bdd;

	/**
	 * 
	 */
	private Stations() {
		setBdd(new ArrayList<Station>());
		System.out.println("Instantiate bdd...");
	}

	public static Stations getInstance() {
		if (stations == null) {
			stations = new Stations();
		}

		return stations;
	}

	/**
	 * @return the bdd
	 */
	public ArrayList<Station> getBdd() {
		return bdd;
	}

	/**
	 * @param bdd the bdd to set
	 */
	public void setBdd(ArrayList<Station> bdd) {
		this.bdd = bdd;
	}
}
