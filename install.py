import os
import json
import base64
import utils.Settings
import utils.PrintLog







print( "\n\nGo to https://t.me/BotFather on Telegram and follow the instructions on how to get your telegram bot token" )

telegram_token = input( "\nEnter your Telegram bot token:  " )
print( "    Splendid!!" )

url_api_key = base64.urlsafe_b64encode( os.urandom(32) ).rstrip(b"=").decode(encoding="utf-8")

domain = input( "\nEnter the domain name of this server:  " )
print( "    Perfect!!" )


chat_id = int(input( "\nEnter the chat id of where you want this program to stream the readings:  " ))


configs = {
    "telegram-bot-token" : telegram_token,
    "api-url-token" : url_api_key,
    "domain" : domain,
    "chat-id" : chat_id,
    "language" : "english",
    "unit" : "mg/dl",
    "listen" : "0.0.0.0",
    "port" : 5000
}

with open( "config1.json" , "w" ) as f:
    f.write( json.dumps( configs , indent=4 ) )



exit()



desc = "SweetMeter the NightScout API compatible CGM monitoring server"
script = "server.py"
current_dir = os.getcwd()

with open("sweetmeter.service", "w") as f:
    f.write(f"""
[Unit]
Description= { desc }
After=network.target
StartLimitIntervalSec=500
StartLimitBurst=5

[Service]
Restart=on-failure
RestartSec=5s
User={ os.environ[ "USER" ] }
WorkingDirectory={ current_dir }
Environment="PATH={ os.environ[ "PATH" ] }"
ExecStart={current_dir}/venv/bin/python3 -u { os.getcwd() }/{script}
[Install]
WantedBy=multi-user.target
""")


os.system(f"sudo mv sweetmeter.service /etc/systemd/system/sweetmeter.service")

os.system( "sudo systemctl daemon-reexec" )
os.system( "sudo systemctl daemon-reload" )
os.system( "sudo systemctl enable --now sweetmeter.service" )






api_url_token = utils.Settings.configs["api-url-token"]
domain = utils.Settings.configs["domain"]

utils.PrintLog.print( f"\n\nuse https://{domain}/{api_url_token}/status.json in XDrip+ Cloud sync\n" )

