package com.service;

import java.util.ArrayList;
import java.util.List;

import org.assertj.core.util.Arrays;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.model.Area;
import com.model.Restaurant;
import com.model.User;
import com.repository.RestaurantRepository;
import com.repository.UserRepository;

@Service
public class RestaurantService {
	private final RestaurantRepository restaurantRepository;
	private final UserRepository userRepository;
	
	@Autowired
	public RestaurantService(RestaurantRepository restaurantRepository, UserRepository userRepository){
		this.restaurantRepository = restaurantRepository;
		this.userRepository = userRepository;
	}
	
	//Services
	public Restaurant getRestaurantById(String id) throws Exception{
		return restaurantRepository.get(id);
	}
	
	public List<Restaurant> getAllRestaurants(){
		return restaurantRepository.getAll();
	}
	
	public Double getDistance(Double x1, Double y1, Double x2, Double y2){
		return Math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2));
	}
	
	public List<User> getNeighborUsers(String res_name, int top_n){
		List<User> user_list = userRepository.getAll();
		List<Restaurant> res_list = restaurantRepository.getAll();
		Restaurant restaurant = null;
		for(int i = 0;i<res_list.size();i++){
			if(res_list.get(i).getName()==res_name){
				restaurant = res_list.get(i);
				break;
			}
		}
		Double res_x = restaurant.getCoordinates().getCoordinates2().get(0);
		Double res_y = restaurant.getCoordinates().getCoordinates2().get(1);
		User []top_users = new User[top_n];
		Double []top_dis = new Double[top_n];
		for(int i = 0;i<top_n;i++){
			top_users[i] = user_list.get(i);
			top_dis[i] = this.getDistance(res_x, res_y, user_list.get(i).getCoordinates().getCoordinates2().get(0), user_list.get(i).getCoordinates().getCoordinates2().get(1));
		}
		for(int i = top_n;i<user_list.size();i++){
			User user = user_list.get(i);
			Double temp_dis = this.getDistance(res_x, res_y, user_list.get(i).getCoordinates().getCoordinates2().get(0), user_list.get(i).getCoordinates().getCoordinates2().get(1));
			for(int j = 0;j<top_dis.length;j++){
				if(temp_dis > top_dis[j]){
					top_users[j] = user_list.get(i);
					top_dis[j] = temp_dis;
					break;
				}
			}
		}
		
		List<User> user_results = new ArrayList<User>();
		for(int i = 0;i<top_users.length;i++){
			user_results.add(top_users[i]);
		}
		
		return user_results;
	}
}
