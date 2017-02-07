#!/usr/bin/env python

from __future__ import print_function
from datetime import datetime, timedelta
from gmusicapi import Mobileclient
from argparse import ArgumentParser
from tabulate import tabulate
from config import GOOGLE_EMAIL, GOOGLE_MUSIC_PASS
import os.path
import pprint
import json

pp = pprint.PrettyPrinter(indent=2)


def resort_by_added(lib):
    return sorted(lib, key=lambda x: x['creationTimestamp'])


def get_datetime(ts):

    d = datetime.fromtimestamp(float(ts[:10]))
    return d


def get_songs(sync=False):
    if os.path.isfile('songs.json') and not sync:
        f = open('songs.json', 'r')
        songs = f.read()
        songs = json.loads(songs)
    else:
        api = Mobileclient()
        api.login(GOOGLE_EMAIL,
                  GOOGLE_MUSIC_PASS,
                  Mobileclient.FROM_MAC_ADDRESS)

        songs_gen = api.get_all_songs(True)

        print("Loading library songs:")

        songs = []
        for part in songs_gen:
            songs = songs + part
            print("%s songs loaded" % len(songs))

            str(len(songs)) + " songs loaded."

        songs = list(reversed(resort_by_added(songs)))

        f = open('songs.json', 'w')
        f.write(json.dumps(songs, indent=4, separators=(',', ': ')))
        f.close()

    return songs


def main():

    parser = ArgumentParser(description="Show last added music")
    parser.add_argument('-d',
                        '--days',
                        help='Number of days in history',
                        type=int,
                        default=30)
    parser.add_argument('-s',
                        '--sync',
                        help='Synchronise library with the latest songs',
                        action="store_true")

    args = parser.parse_args()

    days = int(args.days)
    sync = args.sync

    result = []
    back = timedelta(days=days)
    now = datetime.now()

    songs = get_songs(sync)

    for track in songs:
        d = get_datetime(track['creationTimestamp'])
        if (now - d) < back:
            result.append([track['title'], d.strftime("%a %d-%m-%Y %H:%M")])

    print(tabulate(result, headers=['Song', 'Date']))

if __name__ == "__main__":
    main()
