package com.model;
import java.util.Date;

//import lombok.*;
//import javax.persistence.Entity;
//import javax.validation.constraints.NotNull;
import com.fasterxml.jackson.annotation.JsonProperty;

public class Twitter {
	
	private String id;
	private String rev;
	//private Date created_time;
	//private String text;
	//private User user;
	//private User in_reply_to_user;
	@JsonProperty(value = "_id")
	public String getId() {
		return id;
	}
	@JsonProperty(value = "_id")
	public void setId(String id) {
		this.id = id;
	}
	/*
	public Date getCreated_time() {
		return created_time;
	}
	public void setCreated_time(Date created_time) {
		this.created_time = created_time;
	}
	public String getText() {
		return text;
	}
	public void setText(String text) {
		this.text = text;
	}
	public User getUser() {
		return user;
	}
	public void setUser(User user) {
		this.user = user;
	}
	public User getIn_reply_to_user() {
		return in_reply_to_user;
	}
	public void setIn_reply_to_user(User in_reply_to_user) {
		this.in_reply_to_user = in_reply_to_user;
	}
	*/
	@JsonProperty(value = "_rev")
	public String getRev() {
		return rev;
	}
	@JsonProperty(value = "_rev")
	public void setRev(String rev) {
		this.rev = rev;
	}
}
