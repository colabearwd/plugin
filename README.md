# plugin
Please put this folder in plugin.  
You can use git to get this repository.

This is the repository about the timing script.This is repository is long-time timing script.We use ping & curl to get the result, and return the result to the server.  


```
project
│   README.md   
│	auto.sh
└───get-args
│   60_get_curl_args.py  
│   60_get_ping_args.py  
|
└───get-res
|   60_get_curl_res.py   
|   60_get_ping_res.py
│   
└───ubuntu-plugin
│   60_curl_multi.py  
│   60_ping_multi.py
|
└───rasp-plugin
|   60_dht.py 
│   60_curl_multi.py  
│   60_ping_multi.py
```



# What script in these folder 
##auto.sh
change the script ip,can auto make this folder script 

##config.py
you need to modify this file,for other script to use

## get-args folder
this folder include the script get the args-list from the server.  
those script put args-list in */opt* folder

## get-res folder
this folder include script transfer the open-falcon data to myproject database

## ubuntu-plugin folder
this folder inculde the script can run in ubuntu-server

## rasp-plugin folder
this folder inculde the script can run in rasp-client

     

# How to install this model

## Step 1 These script need install some package in Client-Server
* apt install curl
* apt install iputils-ping

## Step 2 Modify agent config file in Client-Server


    "plugin": {
        "enabled": true,
        "dir": "./plugin",
        "git": "https://github.com/colabearwd/plugin.git",
        "logs": "./logs"
    }

## Step 3 Run these script in Control-Server Dashboard

### Step 3.1 Add HostGroup in Control-Server Dashboard

### Step 3.2 Binding Hosts to HostGroup

### Step 3.3 Add script dir to HostGroup plugins model


## Step 4 Config your Control-Server ip address in script file

**please don`t change the script file name,these name make the OpenFalcon run them automatically**




