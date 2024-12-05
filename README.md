# nucleus-private-projects



## Description
The project-tool tool was created to demo a possible way to organize a folder structure that limits what normal 'users' can see and access. This type of behaviour is somewhat a mimic of the /Users folder structure. In that case all non-admin users can see the folder the folder '/Users' but in that folder they can only see the sub-folder for their user-id.

This tool can be used to create/manage a new folder structure that can be used to hide sub-folders from all users that are not part of that folders ACL group.

This tool was created to do the folllowing 
- create a base 'Projects' folder at the root of Nucleus. In this architecture, all users can see this folder in Omniverse applicatons, Navigator iagor or Nucleus web page on Launcher.


## Prereqs

### Clone this repo
The following documetation is based on creating a directory called ***omniverse*** somewhere on the client **local** filesystem. The name of this directory is up to the user.




<details>
  <summary>Windows</summary>

```
PS > cd C:\
PS > mkdir omniverse
PS > cd C:\omniverse
PS > git clone repo ssh://git@gitlab-master.nvidia.com:12051/nves/omniveres/nucleus-private-projects.git
```
</details>
<details>
  <summary>Linux</summary>

```
$ cd ~
$ mkdir omniverse
$ cd omniverse
$ git clone repo ssh://git@gitlab-master.nvidia.com:12051/nves/omniveres/nucleus-private-projects.git
```
</details>

### Install Omnivese Connect Samples

Download and build the Omniverse Connect Samples. Site to get Connect SDK https://github.com/NVIDIA-Omniverse/connect-samples/releases. Use this site to get a pointer to the current archive. Place this download zip/tar.gz on client local filesystem.

> Note: Windows -> The SDK cannot be installed in a OneDrive location or any other drive other than C:

<details>
  <summary>Windows</summary>

```
PS > cd C:\omniverse\nucleus-private-projects 
PS > wget https://github.com/NVIDIA-Omniverse/connect-samples/archive/refs/tags/v205.0.0.zip -OutFile connect-sdk.zip
PS > Expand-Archive .\connect-sdk.zip
PS > rm connect-sdk.zip
PS > cd connect-sdk\connect-samples-205.0.0
PS > ./build.bat
```
</details>
<details>
  <summary>Linux</summary>

```
$ cd ~/omniverse/nucleus-private-projects
$ wget https://github.com/NVIDIA-Omniverse/connect-samples/archive/refs/tags/v205.0.0.tar.gz  -O connect-sdk.tar.gz
$ mkdir -p connect-sdk && tar -xvf connect-sdk.tar.gz -C connect-sdk/
$ rm connect-sdk.tar.gz
$ cd connect-sdk/connect-samples-205.0.0/
$ ./build.sh
```
</details>




## Setup
Once the Omniverse Connect Samples has been downloaded and built, update the `project-tool.bat` or `project-tool.sh` to define the path to the root of the Omniverse Connect Samples. These scripts have comments to where to make the modifications. Following is snippet from `project-tool.bat`

```
::
::  Change this line to point to the downloaded (and built)
::  Client library root dir. 
::
set CLIENT_LIB_SDK_DIR=C:\omniverse\nucleus-private-projects\connect-sdk\connect-samples-205.0.0\
```

## Usage
```
$ ./project-tool.bat  -h
usage: project-tool.py [-h] [-u USER_ID] [-p PASSWORD] [-M METHOD] [-O OPERATION] [pos_args ...]

Python Client to setup private project infrastructure

positional arguments:
  pos_args              positional args
                        1. Nucleus_server (ex: ov-elysium.redshiftltd.com)
                        2. Project_root (ex: 'NVEX_Projects')
                        3. Project_name (ex: 'Project_C'
                        4. User_name (ex: 'mike')

options:
  -h, --help            show this help message and exit
  -u USER_ID, --user_id USER_ID
  -p PASSWORD, --password PASSWORD
  -M METHOD, --method METHOD

                        Tool method
                        values 0-3
                        Mike
  -O OPERATION, --operation OPERATION

                        operation mode
                        values 0,1
                        0=add (default)
                        1=delete
```




### Example 
#### Create a Root Project
Create a Root Project folder called 'NVEX_projects'
```
./project-tool -u nuc_user_name -p xxxxx -M 1 -O 0 ov-elysium.redshiftltd.com NVEX_Projects  
```
The -M 1 option is used to denote a root project folder operation, the -O 0 means add (use -O 1 to delete). One needs to do this only once for every major root project folder creation. After this is done, one can add any number of sub-projects to this root project folder. 

#### Create a Sub-Project under root
The following example shows how to add a sub-project under the root project folder called Project_C:

```
./project-tool -u nuc_user_name -p xxxxx -M 2 -O 0 ov-elysium.redshiftltd.com NVEX_Projects Project_C
```

#### Add user to Sub-project
```
./project-tool -u nuc_user_name -p xxxx -M 3 -O 0 ov-elysium.redshiftltd.com NVEX_Projects Project_C user_a   
```



## Support
TBD.


## Authors and acknowledgment
TBD.

## License
For open source projects, say how it is licensed.





