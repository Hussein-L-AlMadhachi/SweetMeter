
# SweetMeter 🍬📈

**SweetMeter** is a lightweight, self-hostable CGM (Continuous Glucose Monitoring) API server compatible with the [Nightscout API](https://github.com/nightscout/cgm-remote-monitor). It’s built in Python for speed, simplicity, and extremely low resource usage — even small $5/month VPS instances can run it effortlessly.

## 🚀 Features

- ✅ Focused on critical CGM functionality  
- ✅ Lightweight and resource-friendly  
- ✅ Streams real-time glucose readings  
- ✅ Optional Telegram integration  
- ✅ Supports 35+ languages with graceful fallback  
- ✅ Designed for personal and clinic use  

## 🧰 Requirements

- Python 3.9 or newer  
- A small VPS or local machine  
- Telegram Bot Token

## ⚙️ Installation

```
git clone https://github.com/Hussein-L-AlMadhachi/SweetMeter.git

cd sweetmeter
pip install -r requirements.txt
# Edit config.json to suit your setup
python server.py
```
you need to create `config.json` like so:
```
{
    "telegram-bot-token" : telegram-bot-api-token,
    "api-url-token" : any-random-32-character,
    "language" : "english",
    "chat-id" : telegram-chat-id,
    "unit" : "mg/dl",
    "port" : 5000
}
```

## 🛡️ Run as a systemd Service (Optional)

Create a systemd unit file at /etc/systemd/system/sweetmeter.service:
```
[Unit]
Description=SweetMeter CGM Server
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/sweetmeter/main.py
WorkingDirectory=/path/to/sweetmeter
Restart=always
User=nobody
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```
Then enable and start it:
```
sudo systemctl daemon-reexec  
sudo systemctl enable sweetmeter  
sudo systemctl start sweetmeter  
```
## 🌍 Localization

SweetMeter supports over 35 languages using JSON-based translation files.

- Automatically selects language via Accept-Language header  
- Falls back to English if a word is missing  
- Add your own translations in the locales/ folder  

## 🔒 Privacy Focused

- No analytics, trackers, or telemetry  
- 100% offline-capable  
- Ideal for personal and clinical use if glocuse readings are accurate  

## 🧪 Battle-Tested

SweetMeter has been actively used and refined for over 2 years. It’s stable, efficient, and built for real-world deployments.

## 📄 License

MIT License

