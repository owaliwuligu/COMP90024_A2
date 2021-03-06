package com;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@SpringBootApplication(exclude=DataSourceAutoConfiguration.class) // Spring Boot项目的核心注解，主要目的是开启自动配置
//@Controller // 标明这是一个SpringMVC的Controller控制器
//@ComponentScan(value = "com")
//@EnableAutoConfiguration(exclude={DataSourceAutoConfiguration.class})
public class test {
	@RequestMapping("/hello")
	@ResponseBody
	public String hello() {
		return "hello world";
	}

	// 在main方法中启动一个应用，即：这个应用的入口
	public static void main(String[] args) {
		SpringApplication.run(test.class, args);
	}
}
