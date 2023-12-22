import musicbrainzngs as mb

def get_album_tracks(artist_name, album_name):
    # Initialise the MusicBrainz client with a user agent
    mb.set_useragent("TracklistGrabber", "0.1")

    try:
        # Search for releases matching the artist's name and the album title
        result = mb.search_releases(artist=artist_name, release=album_name, limit=10)
        if not result['release-list']:
            return "Album not found."

        # Loop through the search results to find an exact match
        for release in result['release-list']:
            if release['title'].lower() == album_name.lower() and any(artist['name'].lower() == artist_name.lower() for artist in release['artist-credit']):
                release_id = release['id']
                break
        else:
            # If no exact match is found, return a message indicating this
            return "Exact album not found."

        # Fetch details of the matched album using its ID incl tracks
        result = mb.get_release_by_id(release_id, includes=['recordings'])
        if not result:
            return "Tracks not found."

        # Extract the track list from the result
        tracks = result['release']['medium-list'][0]['track-list']
        # Format track titles as numbered list
        track_titles = [f"{idx + 1}. {track['recording']['title']}" for idx, track in enumerate(tracks)]

        return track_titles

    except mb.WebServiceError as exc:
        # Print any errors that occur during API request
        return f"Error: {exc}"

# Prompt the user to input the desired artist name and album title
artist = input("Enter the artist name: ")
album = input("Enter the album name: ")
tracks = get_album_tracks(artist, album)

# Display the results - either the track list or an error message
if isinstance(tracks, list):
    print("Tracks found:")
    for track in tracks:
        print(track)
else:
    print(tracks)
