package test;

import org.junit.Test;
//import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.boot.test.context.SpringBootTest;
//import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.junit.Assert;
import com.couchdb.config.CouchDBConfig;
import org.ektorp.CouchDbConnector;

import com.test;
import com.model.Twitter;
import com.service.TwitterService;
import com.repository.TwitterRepository;
import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.context.web.WebAppConfiguration;

@RunWith(SpringRunner.class)
@SpringBootTest(classes = {test.class})
@WebAppConfiguration
public class testTwitterService {

	@Autowired
	CouchDbConnector db;

	@Autowired
	TwitterService twitterService;
	
	@Test
	public void testGetTwitterById() throws Exception{

		Twitter twitter = twitterService.getTwitterById("1388282335590715392");
	}
}
