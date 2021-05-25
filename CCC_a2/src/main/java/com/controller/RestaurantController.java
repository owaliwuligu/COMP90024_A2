package com.controller;

import com.model.Restaurant;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.model.Area;
import com.service.RestaurantService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


@RestController
@RequestMapping("/")
public class RestaurantController {
	@Autowired
	RestaurantService restaurantService;
	
	@RequestMapping("/map")
	public String getAllRestaurants() throws JsonProcessingException{
		ObjectMapper objectMapper = new ObjectMapper();
		String restaurantsStr = objectMapper.writeValueAsString(restaurantService.getAllRestaurants());
		return restaurantsStr;
	}
	
	@RequestMapping("/hot_users")
	public String getHotUsers(String res_name, int top_n) throws JsonProcessingException{
		ObjectMapper objectMapper = new ObjectMapper();
		String hotUsersStr = objectMapper.writeValueAsString(restaurantService.getNeighborUsers(res_name, top_n));
		return hotUsersStr;
	}
}
