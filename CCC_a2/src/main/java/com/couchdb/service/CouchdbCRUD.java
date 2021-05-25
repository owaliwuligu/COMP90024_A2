package com.couchdb.service;

import com.model.Twitter;
import com.model.User;
import com.couchdb.service.CouchdbCRUD;
import org.ektorp.CouchDbConnector;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class CouchdbCRUD {
	
	@Autowired
	private CouchDbConnector connector;
	
	public Twitter getTwitter(String id) throws Exception{
		Twitter twitter = connector.get(Twitter.class, id);
		return twitter;
	}
	
	public User getUser(String id) throws Exception{
		User user = connector.get(User.class, id);
		return user;
	}
}
