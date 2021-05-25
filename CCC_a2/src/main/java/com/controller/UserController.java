package com.controller;

import com.model.User;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.model.Area;
import com.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/infouser")
public class UserController {
	
	@Autowired
	UserService userService;
	
	@RequestMapping("/areas")
	public String getUserNumForAreas() throws JsonProcessingException{
		return userService.countUsersForAreas();
	}
	
	@RequestMapping("/test")
	public String testPage(){
		return "test!";
	}
	
	@RequestMapping("/test2")
	public String testPage2() throws Exception{
		User user = userService.getUserById("1000230050736701441");
		System.out.println(user.getUser_info());
		return user.getRev()+" "+user.getUser_info().getName()+" "+user.getUser_info().getFriends_count();
		
	}
}
