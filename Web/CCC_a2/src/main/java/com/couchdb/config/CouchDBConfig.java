package com.couchdb.config;

import org.ektorp.CouchDbConnector;
import org.ektorp.CouchDbInstance;
import org.ektorp.http.HttpClient;
import org.ektorp.http.StdHttpClient;
import org.ektorp.impl.StdCouchDbConnector;
import org.ektorp.impl.StdCouchDbInstance;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;

/**
 * CouchDB配置类
 *
 * @author Dongxu
 * @date 02/05/2021
 */
@Configuration
public class CouchDBConfig {

    @Autowired
    CouchDBInfo couchDBInfo;

    //@Bean(name = "CouchDbConnector")
    @Bean(name = "CouchDbConnector")
    public CouchDbConnector couchDbConnector() throws Exception {
    	System.out.println("test0");
        HttpClient httpClient = new StdHttpClient.Builder().url(couchDBInfo.getHost() + ":"+ couchDBInfo.getPort())
                .username(couchDBInfo.getUsername()).connectionTimeout(10000).socketTimeout(1000000)
                .password(couchDBInfo.getPassword()).build();
        System.out.println("test");
        CouchDbInstance couchDbInstance = new StdCouchDbInstance(httpClient);
        CouchDbConnector couchDbConnector = new StdCouchDbConnector(couchDBInfo.getDatabase(), couchDbInstance);
        couchDbConnector.createDatabaseIfNotExists();
        System.out.println("注入成功");
        return couchDbConnector;
    }


}
