sudo apt install nginx

# set virtual environment
python3 -m venv venv/

./venv/bin/pip3 install -r requirements.txt


python3 ./install.py

sudo systemctl restart nginx
sudo systemctl enable nginx

exit 0

