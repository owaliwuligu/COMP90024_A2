package com.model;

import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Restaurant {
	private String id;
	private String rev;
	private String name;
	private Map<String, Long> scores;
	private Coordinate coordinates;
	
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

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public String getRev() {
		return rev;
	}

	public void setRev(String rev) {
		this.rev = rev;
	}

	public Map<String, Long> getScores() {
		return scores;
	}

	public void setScores(Map<String, Long> scores) {
		this.scores = scores;
	}

	public Coordinate getCoordinates() {
		return coordinates;
	}

	public void setCoordinates(Coordinate coordinates) {
		this.coordinates = coordinates;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
	
}
