# COMP90024_A2
## 1. Openstack PW need to be copied for connecting to MRC
NTBlOTUzYWUxZDY1NGU5
## 2. Deploy Instances
https://youtu.be/l-dD9ifIqnU
## 3. Since step 2, we have the host.ini file to store our instance IPs.
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

## 4. Deploy Environment and other necessary applications
https://youtu.be/TJZ4j1viZbE


## 5. Need to be deleted before the final check:
The Team61 Key locates in /COMP90024_A2/Key directory.
Need to add this key to ssh for convenient concerns.

---
Command in terminal:

(<b>sudo chmod 600 Team61</b>)  ## Only needed while next step errors.

---
<b>ssh-add Team61</b>  ## While you are now in the directory which contains keys.

---
Without adding key to ssh:

<b>ssh -i ./Team61 ubuntu@<instance_IP_address></b>

---

In instance 1, I installed nginx and couchdb (clustered with others).

In other instance, I install couchdb (clustered with others).

Other necessary packages, such as vim, pip, etc., I installed them at the beginning.

If there are other packages needed, please contact me asap.

---

When you log into couchdb:

<b>user: admin

pw: 616161

cookie: team61cookie</b>


## 6. Other notes
May update later when we met other problems.