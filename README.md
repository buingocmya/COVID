# COVIDINFO
Chức năng: Tra cứu thông tin, số liệu Covid của quốc gia theo ngày

Ngôn ngữ sử dụng: Python

1. Đăng nhập

	Client đăng nhập bằng cách gửi username, password cho sever. Server sẽ nhận thông tin và kiểm tra với thông tin đã lưu trữ tại server.

2. Đăng ký
    
    Client đăng ký bằng cách gửi username, password cho sever. Server sẽ nhận thông tin và kiểm tra với thông tin đã lưu trữ tại server, nếu đã tồn tại, gửi thông báo đến client, yêu cầu đăng ký tài khoản khác
     
	 ![image](https://user-images.githubusercontent.com/81601941/195975413-7b57a765-04fc-482a-8687-0e0672aa3901.png)
3. Tra cứu 
    
    Cho phép client tra cứu theo ngày với quốc gia (thế giới).
    Server sẽ kết nối tới một website khác (third party) để lấy thông tin (JSON), sau đó rút trích thông tin và lưu trữ dưới Server để phục vụ request của Client

	input:
	
	![image](https://user-images.githubusercontent.com/81601941/195975548-b23a8e2a-ccf4-4bbc-8c05-7d110d1d47fc.png)

	output: 
	
	![image](https://user-images.githubusercontent.com/81601941/195975567-bd866c0b-d3da-4d13-a8db-7b2c7e99f978.png)
