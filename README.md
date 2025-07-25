
> Documantation is still in beta

# SweetMeter 🍬📈 

**SweetMeter** is a lightweight, self-hostable CGM (Continuous Glucose Monitoring) API server compatible with the [Nightscout API](https://github.com/nightscout/cgm-remote-monitor). It’s built in Python for speed, simplicity, and extremely low resource usage — even small $5/month VPS instances can run it effortlessly.

> **SweetMeter v1.0.1**

## 🚀 Features

- ✅ Focused on critical CGM functionality  
- ✅ XDrip+ integration
- ⭕ juggluco (in progress)
- ✅ Lightweight and resource-friendly  
- ✅ Streams real-time glucose readings  
- ✅ Optional Telegram integration  
- ✅ Supports 35+ languages with graceful fallback  
- ✅ Designed for personal and clinic use(if glocuse readings are accurate from the transmitter)

## 🧰 Requirements

- Python 3.9 or newer  
- A small VPS or local machine  
- Telegram Bot Token

## ⚙️ Installation

```
git clone https://github.com/Hussein-L-AlMadhachi/SweetMeter.git

cd sweetmeter
sh install.sh
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
ExecStart=/usr/bin/python3 /path/to/sweetmeter/server.py
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

## XDrip+ integration

use the url `https:yourdomain.com/your-api-url-token-in-config-json/` for XDrip+ and it will work automatically

## 🌍 Localization

SweetMeter supports over 35 languages using JSON-based translation files.

- Automatically selects language via Accept-Language header  
- Falls back to English if a word is missing  
- Add your own translations in the localization/
- use existing files

##### builtin supported languages:
* `english`
* `arabic`
* `amharic`
* `czech`
* `french`
* `hausa`
* `italian`
* `kurdish_kurmanji`
* `marathi`
* `persian`
* `romanian`
* `swahili`
* `telugu`
* `ukrainian`
* `dutch`
* `german`
* `hindi`
* `japanese`
* `kurdish_sorani`
* `mongolian`
* `polish`
* `russian`
* `tagalog`
* `thai`
* `urdu`
* `bengali`
* `greek`
* `indonesian`
* `korean`
* `mandarin`
* `pashto`
* `portuguese`
* `spanish`
* `tamil`
* `turkish`
* `vietnamese`

just put any of those in the `language` field in `config.json` and it will work

> check `sweetmeter.log` for any errors


## 🔒 Privacy Focused

- No analytics, trackers, or telemetry what-so-ever
- Ideal for personal and clinical use if glocuse readings are accurate  

## 🧪 Battle-Tested

SweetMeter has been actively used and refined for over 2 years. It’s stable, efficient, and built for real-world deployments.

## 📄 License

```
MIT License

Copyright (c) 2025 Hussein Layth AlMadhachi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

