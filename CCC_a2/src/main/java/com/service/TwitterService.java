package com.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.repository.TwitterRepository;
import com.couchdb.service.CouchdbCRUD;
import com.model.Twitter;

@Service
public class TwitterService {
	@Autowired
	private CouchdbCRUD crud;
	//@Autowired
	private TwitterRepository twitterRepository;
	
	@Autowired
	public TwitterService(TwitterRepository twitterRepository){
		this.twitterRepository = twitterRepository;
	}
	
	//Services
	public Twitter getTwitterById(String id) throws Exception{
		return twitterRepository.get(id);
	}
	//1388282335590715392
}
