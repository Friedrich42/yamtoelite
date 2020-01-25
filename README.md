# yandex_music_2_telegram_channel
Setup:
In the root directory of project, run  
```
py -m venv venv
source venv/bin/activate
pip install -r rqm.txt
pip install -e .
```

Then go to conf_.py and rename it to conf.py 
 
Enter your own credentials:
```
API_TOKEN_TELEGRAM = "YOUR TELEGRAM API TOKEN"
API_TOKEN_YANDEX_MUSIC_CLIENT = "YOUR YANDEX MUSIC CLIENT TOKEN"

CHANNEL_ID_FOR_BOT = "YOUR TELEGRAM CHANNEL ID" 
```