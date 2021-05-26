package com.repository;

import com.couchdb.config.CouchDBConfig;
import com.model.Twitter;
import org.ektorp.CouchDbConnector;
import org.ektorp.support.CouchDbRepositorySupport;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

@Repository
public class TwitterRepository extends CouchDbRepositorySupport<Twitter> {
	@Autowired
    CouchDBConfig couchDBConfig;
	
	@Autowired
    protected TwitterRepository(CouchDbConnector db){
    	super(Twitter.class, db, true);
    	System.out.println("test0");
        initStandardDesignDocument();
    }
}
