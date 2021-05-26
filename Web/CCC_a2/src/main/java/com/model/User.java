package com.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;
import java.util.Map;

//import lombok.*;
//import javax.persistence.Entity;
//import javax.validation.constraints.NotNull;

public class User {
	
	private String id;
	private String rev;
	private Coordinate coordinates;
	private User_info user_info;
	private Map<String, Double> food_preference;
	@JsonIgnore
	private Map<String, String> place;
	@JsonIgnore
	private Map<String, Long> tweet_count;
	
	public static class Coordinate{
		private String type;
		private List<Double> coordinates2;
		public String getType() {
			return type;
		}
		public void setType(String type) {
			this.type = type;
		}
		@JsonProperty(value = "coordinates")
		public List<Double> getCoordinates2() {
			return coordinates2;
		}
		@JsonProperty(value = "coordinates")
		public void setCoordinates2(List<Double> coordinates2) {
			this.coordinates2 = coordinates2;
		}
		
	}
	
	public static class User_info{
		private String lang;
		private Long favourites_count;
		private String screen_name;
		private Long friends_count;
		private String url;
		private String created_at;
		private Long followers_count;
		private String id_str;
		private String location;
		private boolean default_profile;
		private int statuses_count;
		private boolean geo_enabled;
		private int listed_count;
		private Long id;
		private String name;
		public String getLang() {
			return lang;
		}
		public void setLang(String lang) {
			this.lang = lang;
		}
		public Long getFavourites_count() {
			return favourites_count;
		}
		public void setFavourites_count(Long favourites_count) {
			this.favourites_count = favourites_count;
		}
		public String getScreen_name() {
			return screen_name;
		}
		public void setScreen_name(String screen_name) {
			this.screen_name = screen_name;
		}
		public Long getFriends_count() {
			return friends_count;
		}
		public void setFriends_count(Long friends_count) {
			this.friends_count = friends_count;
		}
		public String getUrl() {
			return url;
		}
		public void setUrl(String url) {
			this.url = url;
		}
		public String getCreated_at() {
			return created_at;
		}
		public void setCreated_at(String created_at) {
			this.created_at = created_at;
		}
		public Long getFollowers_count() {
			return followers_count;
		}
		public void setFollowers_count(Long followers_count) {
			this.followers_count = followers_count;
		}
		public String getId_str() {
			return id_str;
		}
		public void setId_str(String id_str) {
			this.id_str = id_str;
		}
		public String getLocation() {
			return location;
		}
		public void setLocation(String location) {
			this.location = location;
		}
		public boolean isDefault_profile() {
			return default_profile;
		}
		public void setDefault_profile(boolean default_profile) {
			this.default_profile = default_profile;
		}
		public int getStatuses_count() {
			return statuses_count;
		}
		public void setStatuses_count(int statuses_count) {
			this.statuses_count = statuses_count;
		}
		public boolean isGeo_enabled() {
			return geo_enabled;
		}
		public void setGeo_enabled(boolean geo_enabled) {
			this.geo_enabled = geo_enabled;
		}
		public int getListed_count() {
			return listed_count;
		}
		public void setListed_count(int listed_count) {
			this.listed_count = listed_count;
		}
		public Long getId() {
			return id;
		}
		public void setId(Long id) {
			this.id = id;
		}
		public String getName() {
			return name;
		}
		public void setWoodsy(String name) {
			this.name = name;
		}
		
		
	}
	
	@JsonProperty(value = "user")
	public User_info getUser_info() {
		return user_info;
	}
	@JsonProperty(value = "user")
	public void setUser_info(User_info user_info) {
		this.user_info = user_info;
	}
	public Map<String, Double> getFood_preference() {
		return food_preference;
	}
	public void setFood_preference(Map<String, Double> food_preference) {
		this.food_preference = food_preference;
	}
	
	public Coordinate getCoordinates() {
		return coordinates;
	}
	public void setCoordinates(Coordinate coordinates) {
		this.coordinates = coordinates;
	}
	
	@JsonProperty(value = "_id")
	public String getId() {
		return id;
	}
	
	@JsonProperty(value = "_id")
	public void setId(String id) {
		this.id = id;
	}
	@JsonProperty(value = "_rev")
	public String getRev() {
		return rev;
	}
	@JsonProperty(value = "_rev")
	public void setRev(String rev) {
		this.rev = rev;
	}
	public Map<String, String> getPlace() {
		return place;
	}
	public void setPlace(Map<String, String> place) {
		this.place = place;
	}
	public Map<String, Long> getTweet_count() {
		return tweet_count;
	}
	public void setTweet_count(Map<String, Long> tweet_count) {
		this.tweet_count = tweet_count;
	}

}


