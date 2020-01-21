package fr.insa.integ.NYCBike.DataStorage;

import static org.junit.jupiter.api.Assertions.*;

import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.junit.jupiter.api.Test;

class StationsServiceTest {

	String rscurl = "http://localhost:8081/5sdbd-integ-e3.fr/storage/data/";
	
	@Test
	void testStationsList() {
		Client client = ClientBuilder.newClient();

		Response resp = client.target(rscurl + "stations").request().get();
		
		assertEquals(200, resp.getStatus());
		assertEquals(0,resp.getMediaType().toString().compareTo(MediaType.APPLICATION_JSON));
	}

	@Test
	void testStationsGetValid() {
		Client client = ClientBuilder.newClient();

		Response resp = client.target(rscurl + "stations/296").request().get();
		
		assertEquals(200, resp.getStatus());
		assertEquals(0,resp.getMediaType().toString().compareTo(MediaType.APPLICATION_JSON));
	}
	
	@Test
	void testStationsGetInvalid() {
		Client client = ClientBuilder.newClient();

		Response resp = client.target(rscurl + "stations/123456").request().get();
		
		assertEquals(204, resp.getStatus());
	}

	@Test
	void testStationsGetaroundValid() {
		Client client = ClientBuilder.newClient();

		Response resp = client.target(rscurl + "stations/296?radius=500").request().get();
		
		assertEquals(200, resp.getStatus());
		assertEquals(0,resp.getMediaType().toString().compareTo(MediaType.APPLICATION_JSON));
	}
	
	@Test
	void testStationsGetaroundInvalid() {
		Client client = ClientBuilder.newClient();

		Response resp = client.target(rscurl + "stations/29677?radius=1").request().get();
		
		assertEquals(204, resp.getStatus());
	}
}
