package fr.insa.integ.NYCBike.Predictions;

import java.io.BufferedReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

@Path("predict")
public class Predict {

	String rscurl = "http://localhost:8081/5sdbd-integ-e3.fr/storage/ml/";
	int mid = 42;
	String path = "C:\\Users\\linam\\Documents\\INSA\\5A\\Projet_Integrateur\\5SDBD-Integ-E3\\services\\";

	@GET
	@Path("/next_station/{station-id}")
	@Produces(MediaType.TEXT_PLAIN)
	public int predict_next_station(@PathParam("station-id") int idS, @QueryParam("hour") int h,
			@QueryParam("weekday") int w, @QueryParam("month") int m, @QueryParam("age") int age,
			@QueryParam("gender") int gender) {

		Client client = ClientBuilder.newClient();

		Response resp = client.target(rscurl + "models/" + mid).request().get();
		String ml = resp.readEntity(String.class); //
		System.out.println("Reponse get model: " + ml);

		// Parse JSON object
		JSONParser parser = new JSONParser();
		JSONObject obj;
		try {
			obj = (JSONObject) parser.parse(ml);
			String mname = (String) obj.get("name");
			System.out.println("model name: " + mname);

			// Save JSON Object
			FileWriter file = new FileWriter(path + "response.json");
			file.write(obj.toString());
			file.close();

		} catch (ParseException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

		// Run python script
		Process process;
		try {
			process = Runtime.getRuntime().exec("python " + path + "make_prediction.py " + path + "response.json " + idS
					+ " " + h + " " + w + " " + m + " " + "1 " + gender + " " + age);
			InputStream stdout = process.getInputStream();
			BufferedReader reader = new BufferedReader(new InputStreamReader(stdout, StandardCharsets.UTF_8));
			String line;
			int prediction = 0;
			while ((line = reader.readLine()) != null) {
				System.out.println("stdout: " + line);
				prediction = Integer.parseInt(line);
			}
			return prediction;
		} catch (IOException e) {
			e.printStackTrace();
		}

		return 0;
	}
}
