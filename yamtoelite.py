import threading
import telebot

import conf

from time import sleep
from yandex_music.client import Client
from TrackDB import Track, TrackDB

from functions import *

bot = telebot.TeleBot(conf.API_TOKEN_TELEGRAM)
yam_client = Client(conf.API_TOKEN_YANDEX_MUSIC_CLIENT)
track_db = TrackDB()

main_channel_id = conf.CHANNEL_ID_FOR_BOT


def get_songs_from_yamusic(yandex_music_client):
    try:
        return list([Track(id_of_song=song.track.id,
                           song_name=song.track.title,
                           artists=" ft. ".join([artist.name for artist in song.track.artists]),
                           album_id=song.album_id,
                           local_path="", ) for song in yandex_music_client.users_likes_tracks().tracks])
    except Exception as e:
        log_error(e)


def on_new_song_detected(song):
    try:
        bot.send_audio(chat_id=main_channel_id, audio=open(song.local_path, "rb"),
                       caption=f"{song.artists} - {song.song_name}")
        return "ok"
    except Exception as e:
        log_error(e)


def worker():
    try:
        while True:
            for song in get_songs_from_yamusic(yam_client):
                db_song = track_db.get_song(song.id_of_song)
                if db_song is None:
                    track_name = f"{song.artists} - {song.song_name}.mp3"
                    with in_dir(f"tracks/{song.artists}"):
                        sleep(5)
                        yam_client.tracks([f'{song.id_of_song}:{song.album_id}'])[0].download(track_name)
                    song.local_path = f"tracks/{song.artists}/{track_name}"
                    track_db.add_song(song)

                    r = on_new_song_detected(song)  # just actions done on new song detected
                    if not r == "ok":
                        break
            sleep(20)
    except Exception as e:
        log_error(e)


def main():
    worker_thread = threading.Thread(target=worker, daemon=True)
    worker_thread.start()

    try:
        bot.polling(none_stop=True)
    except Exception as e:
        log_error(e)


if __name__ == '__main__':
    main()
