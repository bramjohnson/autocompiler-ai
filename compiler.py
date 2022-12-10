import os, time, utils, json, pickle
from network.deejAI import make_playlist, contains_track
from config import OPTIONS_DICT

NETWORK_LOCATION = 'Network/Pickles/mp3tovecs/mp3tovec.p'

class Compiler:
    def __init__(self, playlist = None, queue = [], accepted = [], removed = [], title = None) -> None:
        self.queue = queue.copy()
        self.accepted = accepted.copy()
        self.removed = removed.copy()
        self.title = title
        self.queue_title_cache = []
        self.autosave = AutoSaver(5, self)
        self.filter = [""]
        self.mp3tovec = pickle.load(open(NETWORK_LOCATION, 'rb'))
        if (playlist is not None and os.path.isfile(playlist) and playlist.endswith(".m3u8")):
            songs = open(playlist, 'r', encoding='utf-8-sig')
            for song in songs:
                if (not song.startswith("#")):
                    self.queue.append(song.rstrip())
        for song in self.queue:
            self.queue_title_cache.append(utils.title(song))
        if OPTIONS_DICT["auto_load_songs_on_open"]:
            for song in range(len(self.queue)):
                self.add_similar()
    
    def hasNext(self):
        return len(self.queue) > 0

    def next(self):
        if not self.hasNext():
            return
        return self.queue[0].replace("\\", "/")

    def pop_top(self):
        self.autosave.update()
        self.queue_title_cache.pop(0)
        return self.queue.pop(0)

    def add_similar(self):
        track = self.pop_top()
        if not contains_track(track, self.mp3tovec):
            return
        # if not file_exists(track):
            # return

        negativeTracks = []
        if OPTIONS_DICT["use_negative_weights"]:
            negativeTracks = self.removed

        similar = [x for x in make_playlist([track],
        size=OPTIONS_DICT["amount_similar_tracks"],
        noise=OPTIONS_DICT["random_noise"],
        lookback=OPTIONS_DICT["playlist_lookback"],
        filter=self.filter,
        mp3tovec=self.mp3tovec,
        negative=negativeTracks) if (x not in self.accepted and x not in self.queue and x not in self.removed and not x == track)]
        self.accepted.append(track)
        self.queue.extend(similar)
        for song in similar:
                self.queue_title_cache.append(utils.title(song))
    
    def delete(self):
        self.removed.append(self.pop_top())

    def keep(self):
        self.accepted.append(self.pop_top())

    def tracks_to_m3u(self, fileout):
        with open(fileout, 'w', encoding='utf-8') as f:
            for item in self.accepted:
                f.write(item + "\n")

    def save(self, fileout):
        with open(fileout, 'w', encoding='utf-8') as f:
            data = {
                "title": self.title,
                "queue": self.queue,
                "accepted": self.accepted,
                "removed": self.removed
            }
            json.dump(data, f)

    def set_filter(self, filter):
        if filter == "":
            self.filter = [""]
            return
        self.filter = filter.split(";")
        print(self.filter)

    def get_title(self):
        if self.title == None:
            return "New Playlist"
        return self.title

class CompilerLoad:
    def __init__(self, file) -> None:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.title = data["title"]
            self.queue = data["queue"]
            self.accepted = data["accepted"]
            self.removed = data["removed"]
            
    def load(self):
        return Compiler(queue = self.queue, accepted = self.accepted, removed = self.removed, title = self.title)

class CompilerLoadList:
    def __init__(self, file) -> None:
        with open(file, 'r', encoding='utf-8') as f:
            info = f.readlines()
            def populate():
                list = []
                while True:
                    track = info.pop(0)
                    if track == "\n":
                        return list
                    else: list.append(track.rstrip())
            self.queue = populate()
            self.accepted = populate()
            self.removed = populate()
            self.title = os.path.basename(file)

    def load(self):
        return Compiler(queue = self.queue, accepted = self.accepted, removed = self.removed, title = self.title)

class AutoSaver:
    def __init__(self, increment, compiler):
        self.increment = increment
        self.compiler = compiler
        self.cur = 0
        if (not os.path.exists('./backup/')): os.mkdir('./backup/')
        if (not os.path.exists('./backup/auto')): os.mkdir('./backup/auto')

    def update(self):
        self.cur += 1
        if self.cur >= self.increment:
            self.autosave()
            self.cur = 0

    def autosave(self):
        self.compiler.save('./backup/auto/' + str(time.time()))