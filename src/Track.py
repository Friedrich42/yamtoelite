import sqlalchemy as sqla

from src import Base


class Track(Base):
    __tablename__ = "tracks"

    pk = sqla.Column(sqla.Integer, primary_key=True)
    id_of_song = sqla.Column(sqla.Integer, unique=True, nullable=False)
    song_name = sqla.Column(sqla.String, nullable=False)
    artists = sqla.Column(sqla.String, nullable=False)
    album_id = sqla.Column(sqla.Integer, unique=True, nullable=False)
    local_path = sqla.Column(sqla.String, unique=True)

    def __repr__(self):
        return f"{self.pk=} {self.id_of_song=} {self.song_name=} {self.artists=} {self.album_id=} {self.local_path=}"
