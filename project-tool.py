import argparse
from argparse import RawTextHelpFormatter
from pathlib import Path

import omni.client
import time

g_1 = None 
g_2 = None

g_control_data = {
    'nucleus_user'      : 'omniverse',
    'nucleus_password'  : 'xxxxx',
}

g_operation = ['Add','Delete']
g_methods = ['Nothing','Root Project','Sub Project','User']



def printf(str,type = 0):
    types = ['Success','Error','Warn']
    print(f"[project-tool]: {types[type]} -- {str}")

def authentication_callback(url):
    print("[project-tool]: Authenticating to {}".format(url))
    return g_control_data["nucleus_user"], g_control_data["nucleus_password"]
   
def connectionStatusCallback(url, connectionStatus):
    print("[project-tool]: Connection status to {} is {}".format(url, connectionStatus))
    
def connect_to_nucleus():
    global g_1, g_2

    try:
        if not omni.client.initialize():
            return "Failed to initialize Omniverse Client"

        print("[project-tool]: Omniverse Client initialized" + omni.client.get_version()) # version 2.17

        g_1 = omni.client.register_authorize_callback(authentication_callback)
        g_2 = omni.client.register_connection_status_callback(connectionStatusCallback)

    except Exception as e:
        print("[project-tool]: The error is: ",e)
    
def get_nucleus_url():
    return f"omniverse://{g_control_data['nucleus']}"

def startupOmniverse():
    connect_to_nucleus()
    pass

def shutdownOmniverse():
    omni.client.sign_out(get_nucleus_url())
    omni.client.shutdown()




    
# tool -u -p -M 1 -O 0 nucleus_url Project_root   
# tool -u -p -M 2 -O 0 nucleus_url Project_root  Project_name
# tool -u -p -M 3 -O 0 nucleus_url Project_root  Project_name  User_name
 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Python Client to setup private project infrastructure', 
                                     formatter_class=RawTextHelpFormatter)

    parser.add_argument('pos_args', nargs='*', 
                        help="positional args \n1. Nucleus_server (ex: ov-elysium.redshiftltd.net)\n2. Project_root (ex: 'NVEX_Projects')\n3. Project_name (ex: 'Project_C' \n4. User_name (ex: 'mike')") 
  

    parser.add_argument("-u", "--user_id",  action='store', default="omniverse")
    parser.add_argument("-p", "--password", action='store', default="xxxxxx")
    parser.add_argument("-M", "--method",   type=int, default=0, help='\nTool method\nvalues 0-3\nMike' )
    parser.add_argument("-O", "--operation",type=int, default=0, help='\noperation mode\nvalues 0,1\n0=add (default)\n1=delete' )
 

    args = parser.parse_args()

    if len(args.pos_args) == 0:
        printf("Invalid number of positional arguments",1)
        parser.print_help()
        exit(0)


    g_control_data["nucleus"]           = args.pos_args[0]
    g_control_data["nucleus_user"]      = args.user_id
    g_control_data["nucleus_password"]  = args.password

    startupOmniverse()
    
    #   check to see if we are and Admin. This is dumb, must be a better way to figure this out.
    (res,_) = omni.client.remove_group(get_nucleus_url(),"dummyMiriceXYZ")
    if res.name == "ERROR_ACCESS_DENIED":
        printf("Must be an Admin Nucleus user to use this tool",1)
        exit(-1)



    # method root folder operations
    # use this method to create a root project folder. This will house
    # many sub-projects

    if g_methods[args.method] == 'Root Project':
        project_root_url = get_nucleus_url()+"/"+args.pos_args[1]
        res = None
        
        if args.operation == 0:
            res = omni.client.create_folder(project_root_url)
            if res.name != "OK":
                printf(f"Failure to create root level folder at '{project_root_url}' {res.name}",1)
                exit(-1)    
        else: 
            res = omni.client.delete_single(project_root_url)

        printf(f"Operation {g_methods[args.method]}:{g_operation[args.operation]}",0)

    if g_methods[args.method] == 'Sub Project':
        sub_project_folder_url = get_nucleus_url()+"/"+args.pos_args[1]+"/"+args.pos_args[2]
        sub_project_group_user = args.pos_args[1]+"_"+args.pos_args[2]+"_Users"
        
        if args.operation == 0:

            res = omni.client.create_folder(sub_project_folder_url)
            if res.name != "OK":
                printf(f"Failure to create project folder {sub_project_folder_url} {res.name}",1)
                exit(-1)     

            res = omni.client.create_group(get_nucleus_url(), sub_project_group_user)
            if res.name != "OK":
                printf(f"Failure to create user group {sub_project_group_user} {res.name}",1)
                res = omni.client.delete_single(sub_project_folder_url)
                exit(-1)     


            (res,new_acls) = omni.client.get_acls(sub_project_folder_url)
            
            new_acls.extend(
                [omni.client.AclEntry("users",0),
                 omni.client.AclEntry(sub_project_group_user,omni.client.AccessFlags.READ | omni.client.AccessFlags.WRITE)]
            )
            res = omni.client.set_acls(sub_project_folder_url,new_acls)
            if res.name != "OK":
                printf(f"Failure to set ACLs for {sub_project_group_user} {res.name}",1)
                res = omni.client.delete_single(sub_project_folder_url)

        else:
            res = omni.client.remove_group(get_nucleus_url(), sub_project_group_user)
            if res.name != "OK":
                printf(f"Cannot remove group '{sub_project_group_user}' Error = {res.name}",1)
                exit(0)
                
            res = omni.client.delete_single(sub_project_folder_url)
            if res.name != "OK":
                printf(f"Cannot delete sub-project '{sub_project_folder_url}' Error = {res.name}",1)
                exit(0)

        printf(f"Operation {g_methods[args.method]}:{g_operation[args.operation]}",0)


        

    # method manage user in a Project_root/Project. 
    # either add or remove. Note: existing_user must already be
    # present in nucleus

    if g_methods[args.method] == 'User':
        existing_user = args.pos_args[3]
        sub_project_group = args.pos_args[1]+"_"+args.pos_args[2]+"_Users"

        (res,list) = omni.client.get_users(get_nucleus_url())
        if res.name != "OK":
            printf("cannot get existing user list",1)
            exit(0)
    
        if existing_user not in list:
            printf(f"No existing user named '{existing_user}'",1)
            exit(0)

        if args.operation == 0:
            res = omni.client.add_user_to_group(
                get_nucleus_url(),
                existing_user,
                sub_project_group
            )
        else:
            res = omni.client.remove_user_from_group(
                get_nucleus_url(),
                existing_user,
                sub_project_group
            )
        if res.name != "OK":
            printf(f"Failed to {g_operation[args.operation]} '{existing_user}' from group '{sub_project_group}' \n error={res.name}")
            exit(0)
                  
        printf(f"Operation {g_methods[args.method]}:{g_operation[args.operation]}",0)



    shutdownOmniverse()
    
