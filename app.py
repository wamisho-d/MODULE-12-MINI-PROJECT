from flask import Flask, request, jsonify
app = Flask(__name__)

# In-memory storage for playlist and songs
playlists = {}
songs = {}

# Helper function to sort songs and based on a key (name, artist, or genre)
def sort_songs(songs, key):
    return sorted(songs, key=lambda song: song.get(key))

# Helper function to search for a song in a list by an attribute
def search_songs(songs, key, value):
    return [song for song in songs if song.get(key) == value]

# Song Endpoints

@app.route('/songs', methods=['POST'])
def create_song():
    song = request.json
    song_id = str(len(songs) + 1)
    songs[song_id] = song
    return jsonify({"message": "Song created", "song": song, "song_id": song_id})

@app.route('/songs/<song_id>', methods=['PUT'])
def update_song(song_id):
    if song_id not in songs:
        return jsonify({"message": "Song not found"}), 404
    song_data = request.json
    songs[song_id].update(song_data)
    return jsonify({"message": "Song updated", "song": songs[song_id]})

@app.route('/songs/<song_id>', methods=['DELETE'])
def delete_song(song_id):
    if song_id in songs:
        del songs[song_id]
        return jsonify({"message": "Song deleted"})
    return jsonify({"message": "Song not found"}), 404

@app.route('/songs', methods=['GET'])
def get_song():
    query_param = request.args
    search_key = query_param.get('key')
    search_value = query_param.get('value')

    if search_key and search_value:
        results = search_songs(songs.values(), search_key, search_value)
        return jsonify(results)
    return jsonify(list(songs.values()))

# playlist Endpoints

@app.route('/playlists', methods=['POST'])
def create_playlist():
    playlist = request.json
    playlist_id = str(len(playlists) + 1)
    playlist[playlist_id] = {
        "name": playlist.get("name", f"playlist {playlist_id}"),
        "songs": []
    }
    return jsonify({"message": "playlist created", "playlist_id": playlist_id})

@app.route('/playlists/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    playlist = playlists.get(playlist_id)
    if playlist:
        return jsonify(playlist)
    return jsonify({"message": "playlist not found"}), 404


@app.route('/playlists/<playlist_id>', methods=['PUT'])
def update_playlist(playlist_id):
    if playlist_id not in playlists:
        return jsonify({"message": "playlist not found"}), 404
    playlist_data = request.json
    playlists[playlist_id].update(playlist_data)
    return jsonify({"message": "playlist updated", "playlist": playlists[playlist_id]})

@app.route('/playlists/<playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    if playlist_id in playlists:
        del playlists[playlist_id]
        return jsonify({"message": "playlist deleted"})
    return jsonify({"message": "playlist not found"}), 404


# Additional Endpoints

@app.route('/playlists/<playlist_id>/add_song', methods=['POST'])
def add_song_to_playlsit(playlist_id):
    playlist = playlists.get(playlist_id)
    if not playlist:
        return jsonify({"message": "Playlist not found"}), 404
    
    song_id = request.json.get("song_id")
    song = songs.get(song_id)

    if song:
        playlist['songs'].append(song)
        return jsonify({"message": "Song added to playlist", "playlist": playlist})
    return jsonify({"message": "Song not found"}), 404

@app.route('/playlists/<playlist_id>/remove_song', methods=['POST'])
def remove_song_from_playlist(playlist_id):
    playlist = playlists.get(playlist_id)
    if not playlist:
        return jsonify({"message": "Playlist not found"}), 404
    song_id = request.json.get("song_id")
    song = songs.get(song_id)

    if song in playlist['songs']:
        playlist['songs'].remove(song)
        return jsonify({"message": "Song removed from playlist", "playlist": playlist})
    return jsonify({"message": "Song not found in playlist"}), 404

@app.route('/playlists/<playlist_id>/sort_songs', methods=['GET'])
def sort_songs_in_playlist(playlist_id):
    playlist = playlists.get(playlist_id)
    if not playlist:
        return jsonify({"message": "Playlist not found "}), 404
    
    sort_key = request.args.get('key', 'name')
    sorted_songs = sort_songs(playlist['songs'], key=sort_key)
    return jsonify({"sorted_songs": sorted_songs})

if __name__ == '__main__':
    app.run(debug=True)

