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


def get_all_tracks_from_yamusic(yandex_music_client, logger):
    """
    get all liked songs from yandex music

    @param logger: logger of the app
    @param yandex_music_client: yandex_music.client.Client object is required
    @return: list of Track objects
    """
    try:
        return list([Track(id_of_song=track.id, song_name=track.title,
                           artists=" ft. ".join([artist.name for artist in track.artists])[:100],  # cutting len of artists name
                           album_id=0 if not track.albums else track.albums[0].id,
                           local_path="", ) for track in yandex_music_client.tracks(
            [i.track_id for i in yandex_music_client.users_playlists(3)[0].tracks])])
    except Exception as e:
        logger.critical(e)


def on_new_song_detected(song, logger):
    """
    @param logger: logger of the app
    @param song: song that is detected to be new
    @return: 'ok' if all is ok, error otherwise
    """
    try:
        bot.send_audio(chat_id=main_channel_id, audio=open(song.local_path, "rb"))
        logger.info(f"New song sent {song.local_path}")
        return "ok"
    except Exception as e:
        logger.warning(e)


def worker(track_db_session, logger):
    try:
        while True:
            for track in get_all_tracks_from_yamusic(yam_client, logger):
                db_song = track_db_session.query(Track).filter_by(id_of_song=track.id_of_song).first()

                if db_song is None:
                    track_name = filter_filename(f"{track.artists} - {track.song_name}.mp3")
                    with in_dir(filter_filepath(f"tracks/{track.artists}")):
                        sleep(3)
                        yam_client.tracks([f'{track.id_of_song}:{track.album_id}'])[0].download(track_name)

                    track.local_path = filter_filepath(f"tracks/{track.artists}/{track_name}")
                    try:
                        track_db_session.add(track)
                        track_db_session.commit()
                    except IntegrityError as e:
                        logger.warning(e)
                        track_db_session.rollback()
                        continue

                    r = on_new_song_detected(track, logger)  # just actions done on new song detected
                    if not r == "ok":
                        break
            sleep(20)
    except Exception as e:
        logger.critical(e)


def main(track_db_session, logger):
    worker_thread = threading.Thread(target=worker, args=(track_db_session, logger), daemon=True)
    logger.info("Starting worker thread...")
    worker_thread.start()
    logger.info("Worker thread started")

    try:
        logger.info("Starting telegram bot...")
        bot.polling(none_stop=True)
        logger.info("Bot started")
    except Exception as e:
        logger.critical(e)
