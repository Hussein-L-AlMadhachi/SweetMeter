sudo apt install nginx
sudo apt install python3 python3-dev python3-venv python3-pip

# set virtual environment
python3 -m venv venv/

./venv/bin/pip3 install -r requirements.txt



sudo python3 ./install.py

sudo systemctl restart nginx
sudo systemctl enable nginx


