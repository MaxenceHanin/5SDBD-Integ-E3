package fr.insa.integ.NYCBike.DataStorage;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.junit.jupiter.api.Test;

class ModelsServiceTest {
	
	String rscurl = "http://localhost:8081/5sdbd-integ-e3.fr/storage/ml/";
	
	@Test
	void testModelsList() {
		Client client = ClientBuilder.newClient();

		Response resp = client.target(rscurl + "models").request().get();
		
		assertEquals(200, resp.getStatus());
		assertEquals(0,resp.getMediaType().toString().compareTo(MediaType.APPLICATION_JSON));
	}

	@Test
	void testModelsGetValid() {
		Client client = ClientBuilder.newClient();

		Response resp = client.target(rscurl + "models/42").request().get();
		
		assertEquals(200, resp.getStatus());
		assertEquals(0,resp.getMediaType().toString().compareTo(MediaType.APPLICATION_JSON));
	}
	
	@Test
	void testModelsGetInvalid() {
		Client client = ClientBuilder.newClient();

		Response resp = client.target(rscurl + "models/1234").request().get();
		
		assertEquals(204, resp.getStatus());
	}

}
