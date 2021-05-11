# COMP90024_A2
## 1. Openstack PW need to be copied for connecting to MRC
NTBlOTUzYWUxZDY1NGU5
## 2. Deploy Instances
https://youtu.be/l-dD9ifIqnU
## 3. Since step 2, we have the host.ini file to store our instance IPs.
[all:vars]

ansible_user=ubuntu
[instance1-frontend]

172.26.131.76

[instance2-backend]

172.26.133.169

[instance3-backend]

172.26.129.90

[instance4-analysis]

172.26.133.30

## 4. Deploy Environment and other necessary applications
https://youtu.be/TJZ4j1viZbE


## 5. Need to be deleted before the final check:
The Team61 Key locates in /COMP90024_A2/Key directory.
Need to add this key to ssh for convenient concerns.

Command in terminal:

(sudo chmod 600 Team61)  ## Only needed while error

ssh-add Team61  ## While you are now in the directory which contains keys

## 6. Other notes
May update later when we met other problems.