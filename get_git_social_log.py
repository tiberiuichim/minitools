#!./bin/python
""" Shows interesting activity from followed users of Github
"""

from github import Github
from datetime import datetime, timedelta
from argparse import ArgumentParser
from config import GITHUB_USERNAME, GITHUB_PASS


def repo_title(repo):
    return "{} ({}/{})".format(repo.full_name,
                               repo.stargazers_count,
                               repo.raw_data['subscribers_count'])


def main():

    parser = ArgumentParser(description="Show Github social log")
    parser.add_argument('-u',
                        '--username',
                        help='Github Username',
                        type=str,
                        default=GITHUB_USERNAME)
    parser.add_argument('-d',
                        '--days',
                        help='Max age of events (in days)',
                        type=int,
                        default=2, )
    args = parser.parse_args()
    username = args.username
    days = args.days

    gh = Github(GITHUB_USERNAME, GITHUB_PASS)
    usr = gh.get_user(username)
    d = datetime.now().date() - timedelta(days=days)
    events = usr.get_received_events()

    watched = {
        'CreateEvent': 'created',
        'ForkEvent': 'forked',
        'WatchEvent': 'starred'
    }

    for ev in events:
        if not (ev.created_at.date() >= d):
            break
        if ev.type not in watched:
            continue
        actor = ev.actor
        print("{} {} {}".format(
            actor.name or actor.login,
            watched[ev.type],
            repo_title(ev.repo))
        )


if __name__ == "__main__":
    main()
