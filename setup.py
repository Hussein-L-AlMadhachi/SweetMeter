import os
import sys
import json





# loading settings
try:

    with open( "sync_config.json" , "r" ) as f:
        settings = json.loads( f.read() )
        host_user = settings["user"]
        host = settings["host"]
        host_port = settings["ssh_port"]
        host_service_name = settings["systemctl_service"]
        host_service_path = settings["remote_project_path"]
        local_service_path = settings["local_project_path"]
        rclone_remote_name = settings["rclone_name"]

except FileNotFoundError:
    print( "  [!]  File \"sync_config.json\" not found in this directory (no project file here)" )
    exit(1)

except Exception as error:
    print( "  [!]  File \"sync_config.json\" (project file) cannot be read because" , error )
    exit(2)

del settings






# important functionalities

def remote_exec( commands ):
    return os.system( f"ssh {host_user}@{host} -p {host_port} {commands}" )


def start_shell():
    return os.system( f"ssh {host_user}@{host} -p {host_port}" )



def restart_service():
    return remote_exec( f"systemctl restart {host_service_name}" )



def stop_service():
    return remote_exec( f"systemctl stop {host_service_name}" )


def status_service():
    return remote_exec( f"systemctl status {host_service_name}" )


def sync_project():
    return os.system( f"rclone sync --checksum {local_service_path} {rclone_remote_name}:{host_service_path}" )



def upload_to_project( file_path ):
    return os.system( f"rclone sync --checksum -P {host_port} -r {local_service_path}/{file_path} {host_user}@{host}:{host_service_path}/{file_path}" )


def new_project( project_name ):
    if os.system( f"mkdir {project_name}" ) != 0:
        print( "\n  [!]  failed to create new project" )
        exit(-3)

    settings = {
        "host":"your-domain.com",
        "ssh_port":22,
        "user":"root",
        "service":" name of your service in systemctl ",
        "rclone_name":"the name you decide to use for rclone remote host",
        "host_path":"/root",
        "local_path": os.path.join( str(os.getcwd()) , project_name )
    }

    try:

        with open( f"{project_name}/sync_config.json" , "w" ) as f:
            f.write( json.dumps( settings ) )
        
        print( "project created successfully." )
        print( f"generated \"sync_config.json\" file for your project inside {projectname}/, please fill your information in it." )
        exit(0)

    except Exception as error:
    
        print( "failed to create new project because" , error )
        exit(-3)






# main program

help_message = """
Available commands:
    new <new-project>\t\tstart new project called \"new-project\"
    sync\t\t\tsynchronize project files with remote server project files
    
    up\t\t\t\tstart/restart the background service for the project
    down\t\t\ttake down the background service for the project
    status\t\t\tdisplay the status of the background service for the project 
    
    shell\t\t\tstart a remote shell on the remote server
    run <command>\t\trun a particular remote shell command on the remote server
"""

if len(sys.argv) == 2 and sys.argv[1] == "sync":

    if sync_project() != 0:
        print( "\n  [!] failed SYNC" )
        exit( -2 )
        
    print(  "\n  [*] Successful SYNC." )
    exit( 0 )


elif len(sys.argv) == 2 and  sys.argv[1] == "shell":

    if start_shell() != 0:
        print( "\n  [!] SHELL failed" )
        exit( -2 )
    
    print( "\n  [*] Successful SHELL" )
    exit( 0 )


elif len(sys.argv) == 2 and sys.argv[1] == "up":
    
    if restart_service() != 0:
        print(  "\n  [!] failed DOWN." )
        exit( -2 )

    print( "\n  [*] Successful UP" )


elif len(sys.argv) == 2 and sys.argv[1] == "down":
    
    if stop_service() != 0:
        print(  "\n  [!] failed DOWN." )
        exit( -2 )
    
    print( "\n  [*] Successful DOWN" )


elif len(sys.argv) == 2 and sys.argv[1] == "status":
    
    if status_service() != 0:
        print(  "\n  [!] failed STATUS." )
        exit( -2 )
    
    print( "\n  [*] Successful STATUS" )

elif len(sys.argv) > 2 and sys.argv[1] == "run":
    if remote_exec( " ".join(sys.argv[2:]) ) != 0:
        print(  "\n  [!] failed RUN." )
        exit( -2 )
    
    print( "\n  [*] Successful RUN" )

elif len(sys.argv) == 3 and sys.argv[1] == "new":
    new_project( sys.argv[2] )

elif len(sys.argv) == 3 and sys.argv[1] == "addfile":

    if upload_to_project( sys.argv[2] ) != 0:
        print(  "\n  [!] failed DOWN." )
        exit( -2 )


else:
    print( f"  [!]  bad command usage for {sys.argv[0]}" )
    print( help_message )
    exit( -1 )




