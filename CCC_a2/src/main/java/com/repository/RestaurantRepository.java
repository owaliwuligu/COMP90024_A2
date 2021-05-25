package com.repository;

import com.couchdb.config.CouchDBConfig;
import com.model.Twitter;
import com.model.User;
import com.model.Restaurant;
import org.ektorp.CouchDbConnector;
import org.ektorp.support.CouchDbRepositorySupport;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

@Repository
public class RestaurantRepository extends CouchDbRepositorySupport<Restaurant>{
	
	@Autowired
    protected RestaurantRepository(CouchDbConnector db){
    	super(Restaurant.class, db, true);
    	System.out.println("test0");
        initStandardDesignDocument();
    }
}
