import os





nginx_path = "/etc/nginx/sites-available/default"





def setup_nginx_certbot_ssl():
    print( "\nfollow next instructions:\n" )

    os.system( """
sudo apt install python3 python3-dev python3-venv libaugeas-dev gcc &&
sudo python3 -m venv /opt/certbot/ &&
sudo /opt/certbot/bin/pip install --upgrade pip &&
sudo /opt/certbot/bin/pip install certbot certbot-nginx &&
sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot &&
sudo certbot certonly --nginx &&
echo "0 0,12 * * * root /opt/certbot/bin/python -c 'import random; import time; time.sleep(random.random() * 3600)' && sudo certbot renew -q" | sudo tee -a /etc/crontab > /dev/null
""" )




def setup_nginx( configs ):

    nginx_configs = f"""
server {{
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/{configs["domain"]}/fullchain.pem; # for Certbot
    ssl_certificate_key /etc/letsencrypt/live/{configs["domain"]}/privkey.pem; # for Certbot

    server_name {configs["domain"]};

    location /{configs["api-url-token"]} {{
		proxy_pass http://127.0.0.1:{configs["port"]};
		proxy_set_header X-Real-IP $remote_addr;
	}}

}}

server {{
    if ($host = {configs["domain"]}) {{
        return 301 https://$host$request_uri;
    }} # for Certbot


    listen 80;

    server_name {configs["domain"]};

    return 302 https://$server_name$request_uri;


}}

"""

    with open( nginx_path , "w" ) as f:
        f.write( nginx_configs )
    
    os.system( "sudo systemctl restart nginx" )

