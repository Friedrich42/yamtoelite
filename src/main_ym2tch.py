import threading
from time import sleep

import telebot
from sqlalchemy.exc import IntegrityError
from yandex_music.client import Client

from src import conf
from src.Track import Track
from src.functions import *

bot = telebot.TeleBot(conf.API_TOKEN_TELEGRAM, threaded=False)
yam_client = Client(conf.API_TOKEN_YANDEX_MUSIC_CLIENT)

main_channel_id = conf.CHANNEL_ID_FOR_BOT


def get_all_tracks_from_yamusic(yandex_music_client):
    """
    get all liked songs from yandex music

    @param yandex_music_client: yandex_music.client.Client object is required
    @return: list of Track objects
    """
    try:
        return list([Track(id_of_song=track.id, song_name=track.title,
                           artists=" ft. ".join([artist.name for artist in track.artists])[:100],  # cutting len of artists name
                           album_id=track.albums[0].id,
                           local_path="", ) for track in yandex_music_client.tracks(
            [i.track_id for i in yandex_music_client.users_playlists(3)[0].tracks])])
    except Exception as e:
        log_error(e)


def on_new_song_detected(song):
    """
    @param song: song that is detected to be new
    @return: 'ok' if all is ok, error otherwise
    """
    try:
        bot.send_audio(chat_id=main_channel_id, audio=open(song.local_path, "rb"),
                       caption=f"{song.artists} - {song.song_name}")
        return "ok"
    except Exception as e:
        return log_error(e)


def worker(track_db_session):
    try:
        while True:
            for track in get_all_tracks_from_yamusic(yam_client):
                db_song = track_db_session.query(Track).filter_by(id_of_song=track.id_of_song).first()

                if db_song is None:
                    track_name = filter_filename(f"{track.artists} - {track.song_name}.mp3")
                    with in_dir(filter_filepath(f"tracks/{track.artists}")):
                        sleep(3)
                        yam_client.tracks([f'{track.id_of_song}:{track.album_id}'])[0].download(track_name)

                    track.local_path = filter_filepath("tracks/{track.artists}/{track_name}")
                    try:
                        track_db_session.add(track)
                        track_db_session.commit()
                    except IntegrityError as e:
                        log_error(e)
                        break

                    r = on_new_song_detected(track)  # just actions done on new song detected
                    if not r == "ok":
                        break
            sleep(20)
    except Exception as e:
        log_error(e)


def main(track_db_session):
    worker_thread = threading.Thread(target=worker, args=(track_db_session,), daemon=True)
    worker_thread.start()

    try:
        bot.polling(none_stop=True)
    except Exception as e:
        return log_error(e)
