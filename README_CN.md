# COMP90024_A2
## 1. Openstack  密码
NTBlOTUzYWUxZDY1NGU5

## 2. 建立instance

https://youtu.be/l-dD9ifIqnU

## 3. ini文件 在 COMP90024_A2/MRC/inventory里

[all:vars]

ansible_user=ubuntu

### [instance1-frontend]

<b>172.26.131.76</b>

### [instance2-backend]

<b>172.26.133.169</b>

### [instance3-backend]

<b>172.26.129.90</b>

### [instance4-analysis]

<b>172.26.133.30</b>

## 4. 环境部署，包括一些软件包

https://youtu.be/TJZ4j1viZbE

## 5. 一些方法

登陆instance:

私钥： Team61

位置： COMP90024_A2/Key

第一步： 把Team61权限改成600

<b>sudo chmod 600 Team61</b>

第二步： 把Team61 加到ssh里（这个方法只是临时的，每次进入本机系统就会消失，需要再次添加。如果有解决方法，及时交流。似乎是ssh config?）

<b>ssh-add Team61</b>

第三步： 登陆instance

<b>ssh -i Team61 ubuntu@<instance_IP_address></b>



其他事项：

在所有instance上部署了必需的包

python 3.8.5 需要用python3调用而不是python。例如：**python3 --version**

pip同理 **pip3 list**

现已安装的包：

**ubuntu**: 

'vim', 'unzip', 'git', 'python3-pip', 'curl', 'libicu-dev','libcurl4-openssl-dev','erlang','pkg-config','build-essential'

**python**:

'pandas', 'numpy'

另外：instance1 安装了nginx

有新的需求及时交流



关于couchdb:

进入http界面：

<IP地址>:5984/_utils

用户名：admin

密码：616161

cookie: team61cookie 



