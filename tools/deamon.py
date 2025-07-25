import os
import utils.Settings


script = input( "Enter the python filename that you want to run: " )
if " " in script or "/" in script or "\\" in script:
	print( "ERROR: invalid filename" )
	exit()


desc = input( "Describe your project (optional but recommended): " )

name = input( "Enter a name for your program (Must contain only letters (A-Z and a-z) and numbers): " )
if not name.isalnum():
	print( "ERROR: the name has to contain only letters and numbers" )
	exit()


with open("bot.service", "w") as f:
    f.write(f"""
[Unit]
Description= { desc }
After=network.target
[Service]
Type=simple
User={ os.environ[ "USER" ] }
WorkingDirectory={ os.getcwd() }
Environment="PATH={ os.getcwd() }"
ExecStart=/usr/bin/python3 -u { os.getcwd() }/{script}
[Install]
WantedBy=multi-user.target
""")

if os.path.exists( f"/etc/systemd/system/{name}.service" ):
	print( f"ERROR: {name} is already an existing program running in background" )
	exit()


os.system(f"sudo mv bot.service /etc/systemd/system/{name}.service")

os.system(f"sudo systemctl stop {name}.service")
os.system(f"sudo systemctl reload {name}.service")
os.system(f"sudo systemctl start {name}.service")
os.system(f"sudo systemctl enable {name}.service")


utils.Settings.configs[""]