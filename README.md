# yandex_music_2_telegram_channel
Setup:
```
py -m venv venv
source venv/bin/activate
pip install rqm.txt
```
Go to conf_.py and rename it to conf.py 
 
Enter your own credentials:
```
API_TOKEN_TELEGRAM = "YOUR TELEGRAM API TOKEN"
API_TOKEN_YANDEX_MUSIC_CLIENT = "YOUR YANDEX MUSIC CLIENT TOKEN"

CHANNEL_ID_FOR_BOT = "YOUR TELEGRAM CHANNEL ID" 
```