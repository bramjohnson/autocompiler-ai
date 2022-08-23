# Autoplaylist
This is a tool to create playlists using AI recommendations.
After a playlist is created it can be saved to .apm (Autoplaylist Maker) or .m3u8

# How does it work?
The tool uses an AI model from [Deej-AI](https://github.com/teticio/Deej-AI) by Robert Smith.
Once a network has been provided, a piece of code provided by Deej-AI finds similar songs if that song is part of the network.

# Installation
Download the [latest release](https://github.com/bramjohnson/autoplaylist-ai/releases/latest).

## Setting up a network
- Go to the [Deej-AI](https://github.com/teticio/Deej-AI) page and scroll down to "Try it out for yourself".
- Follow the instructions to create a network (ensure it is named "Pickles")
- Download the speccy_model file

Once both the Pickles folder and speccy_model file are created, copy them to the ./network folder, next to "deekAI.py"

*WARNING*: Song recommendations will only be applied if that song is in the network you created.
Additionally, only songs in the network will be recommended.

# Usage
## Creating a playlist
A playlist can be created either by importing a new .m3u/.m3u8 file, or loading a previously saved .apm file.
## Saving a playlist
A playlist can be saved to .apm through "File/Save..." or exported to .m3u8 through "File/Export/.m3u8"
## Editing the playlist
The playlist can currently only be editing by choosing what to do with the current song.
The buttons under the album art control this...
- Add Similar: Add up to 10 similar songs to the playlist, including this one
- Keep: Add this song to the playlist
- Remove: Remove this song from the queue, and do not add it to the playlist.
## Filters
Filters can be added to allow only certain songs to be recommended. They can be created through "Edit/Add Filter...".

Filters are currently simple: they check if the song path contains any of the filters entered.
## Renaming Playlist
The current playlist can be renamed through "Edit/Rename Playlist..."
## Hotkeys
- Ctrl+S: Save as .apm
#### Seek
Using numbers 1-9 to skip through the song.
### Volume
Use the left/right arrow keys to decrease/increase the volume.
#### Current song
- A: Add Simliar
- S: Keep
- D: Remove