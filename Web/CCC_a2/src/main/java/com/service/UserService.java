package com.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.model.Area;
import com.model.User;
import com.repository.UserRepository;

@Service
public class UserService {
	//@Autowired
	private final UserRepository userRepository;
	
	@Autowired
	public UserService(UserRepository userRepository){
		this.userRepository = userRepository;
	}
	
	//Services
	public User getUserById(String id) throws Exception{
		return userRepository.get(id);
	}
	
	public List<User> getAllUsers(){
		return userRepository.getAll();
	}
	
	public String countUsersForAreas() throws JsonProcessingException{
		System.out.println("test1111");
		ObjectMapper objectMapper = new ObjectMapper();
		System.out.println("test2222");
		List<User> user_list = getAllUsers();
		System.out.println("test3333");
		List<Area> area_list = new ArrayList<Area>();
		System.out.println("test4444");
		
		for(int i = 0;i<user_list.size();i++){
			int flag = 0;
			for(int j = 0;j<area_list.size();j++){
				if(area_list.get(j).getLocation().equals(user_list.get(i).getUser_info().getLocation())){
					Long user_num = area_list.get(j).getUser_num();
					area_list.get(j).setUser_num(user_num + 1);
					flag = 1;
					break;
				}
			}
			if(flag==0){
				Area new_area = new Area();
				new_area.setLocation(user_list.get(i).getUser_info().getLocation());
				new_area.setUser_num(1L);
				area_list.add(new_area);
			}
		}
		System.out.println("test5555");
		String areaJsonStr = objectMapper.writeValueAsString(area_list);
		
		return areaJsonStr;
	}
}
