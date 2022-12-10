import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import pickle
import argparse

default_lookback = 3 # number of previous tracks to take into account
default_noise = 0    # amount of randomness to throw in the mix
default_playlist_size = 10
NETWORK_LOCATION = 'Network/Pickles/mp3tovecs/mp3tovec.p'

def most_similar(mp3tovec, positive=[], negative=[], topn=5, noise=0, filter=[""]):
    if isinstance(positive, str):
        positive = [positive] # broadcast to list
    if isinstance(negative, str):
        negative = [negative] # broadcast to list
    if len(negative) > 0:
        print("Using negative weights")
    mp3_vec_i = np.sum([mp3tovec[i] for i in positive] + [-mp3tovec[i] for i in negative], axis=0)
    mp3_vec_i += np.random.normal(0, noise * np.linalg.norm(mp3_vec_i), len(mp3_vec_i))
    similar = []
    for track_j in mp3tovec:
        if (track_j in positive or track_j in negative) or (all(x not in track_j for x in filter)):
            continue
        mp3_vec_j = mp3tovec[track_j]
        cos_proximity = np.dot(mp3_vec_i, mp3_vec_j) / (np.linalg.norm(mp3_vec_i) * np.linalg.norm(mp3_vec_j))
        similar.append((track_j, cos_proximity))
    return sorted(similar, key=lambda x:-x[1])[:topn]

def make_playlist(seed_tracks, size=10, lookback=3, noise=0, filter=[""], negative=[], mp3tovec=None):
    if mp3tovec == None:
        mp3tovec = pickle.load(open(NETWORK_LOCATION, 'rb'))
    max_tries = 20
    playlist = seed_tracks
    while len(playlist) < size:
        similar = most_similar(mp3tovec, positive=playlist[-lookback:], negative=negative, topn=max_tries, noise=noise, filter=filter)
        # print(playlist[-lookback:])
        candidates = [candidate[0] for candidate in similar if candidate[0] != playlist[-1]]
        for candidate in candidates:
            if (not candidate in playlist):
                break
        playlist.append(candidate)
    return playlist

def tracks_to_m3u(fileout, tracks):
    # using absolute path

    with open(fileout, 'w', encoding='utf-8') as f:
        for item in tracks:
            f.write(item + "\n")

def contains_track(track, mp3tovec=None):
    if mp3tovec == None:
        mp3tovec = pickle.load(open(NETWORK_LOCATION, 'rb'))
    return track in mp3tovec

def main():
    mp3tovec = pickle.load(open(dump_directory + '/mp3tovecs/' + mp3tovec_file + '.p', 'rb'))
    print(f'{len(mp3tovec)} MP3s')
    if input_song != None:
        print("Outfile playlist: {}".format(playlist_outfile))
        print("Input song selected: {}".format(input_song))
        print("Requested {} songs".format(n_songs))

        if n_songs == None:
            n_songs = default_playlist_size
        if noise == None:
            noise = default_noise
        if lookback == None:
            lookback = default_lookback

        tracks = make_playlist(mp3tovec, [input_song], size=n_songs + 1, noise=noise, lookback=lookback, filter=filter)
        tracks_to_m3u(playlist_outfile, tracks)
    else:
        print("[ERR] Argument --inputsong is required")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pickles', type=str, help='Directory of pickled TrackToVecs')
    parser.add_argument('mp3tovec', type=str, help='Filename (without extension) of pickled MP3ToVecs')
    parser.add_argument('--playlist', type=str, help='Write playlist file without starting interface')
    parser.add_argument('--inputsong', type=str, help="Requires --playlist option\nSelects a song to start the playlist with.")
    parser.add_argument("--nsongs", type=int, help="Requires --playlist option\nNumber of songs in the playlist")
    parser.add_argument("--noise", type=float, help="Requires --playlist option\nAmount of noise in the playlist (default 0)")
    parser.add_argument("--lookback", type=int, help="Requires --playlist option\nAmount of lookback in the playlist (default 3)")
    parser.add_argument("--filter", type=str, help="Requires --playlist option\nOnly include files with this string in their path")

    args = parser.parse_args()
    dump_directory = args.pickles
    mp3tovec_file = args.mp3tovec
    playlist_outfile = args.playlist
    input_song = args.inputsong
    n_songs = args.nsongs
    noise = args.noise
    lookback = args.lookback
    filter = args.filter

    if filter == None:
        filter = ""
    
    main(dump_directory, mp3tovec_file, playlist_outfile, input_song, n_songs, noise)

# Code written by Robert Smith at https://github.com/teticio/Deej-AI