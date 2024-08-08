from config.app import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "spotify_username",
            "profile_image",
            "name",
            "bio",
            "banner",
            "created_at",
            "friend_count",
            "country",
            "email"
        )

class UserTopArtistsSchema(ma.Schema):
    class Meta:
        fields = (
            "artists",
            "next_update"
        )

class UserTopTracksSchema(ma.Schema):
    class Meta:
        fields = (
            "tracks",
            "next_update"
        )

class UserTopGenresSchema(ma.Schema):
    class Meta:
        fields = (
            "genres",
            "next_update"
        )


user_schema = UserSchema()
user_top_artists_schema = UserTopArtistsSchema()
user_top_tracks_schema = UserTopTracksSchema()
user_top_genres_schema = UserTopGenresSchema()