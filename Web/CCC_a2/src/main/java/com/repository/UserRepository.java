package com.repository;

import com.couchdb.config.CouchDBConfig;
import com.model.Twitter;
import com.model.User;
import org.ektorp.CouchDbConnector;
import org.ektorp.support.CouchDbRepositorySupport;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

@Repository
public class UserRepository extends CouchDbRepositorySupport<User>{

	@Autowired
    protected UserRepository(CouchDbConnector db){
    	super(User.class, db, true);
    	System.out.println("test0");
        initStandardDesignDocument();
    }
}
