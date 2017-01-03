#!./bin/python

from datetime import datetime
from gmusicapi import Mobileclient
from config import GOOGLE_EMAIL, GOOGLE_MUSIC_PASS


def resort_by_added(lib):
    # for track in lib:
    #     track['creationTimestamp'] = int(track['creationTimestamp'])

    return sorted(lib, key=lambda x: x['creationTimestamp'])


def format_ts(ts):
    d = datetime.fromtimestamp(float(ts[:10]))
    return d.strftime("%a %d-%m-%Y %H:%M")


def main():
    api = Mobileclient()
    api.login(GOOGLE_EMAIL,
              GOOGLE_MUSIC_PASS,
              Mobileclient.FROM_MAC_ADDRESS)

    library = api.get_all_songs()

    library = reversed(resort_by_added(library))

    i = 0
    for track in library:
        i += 1
        print track['title'], ' / ', format_ts(track['creationTimestamp'])
        if i > 20:
            break


if __name__ == "__main__":
    main()
