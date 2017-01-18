#!./bin/python
""" Shows a list of all starred items
"""

from github import Github
from argparse import ArgumentParser
from config import GITHUB_USERNAME, GITHUB_PASS


def repo_title(repo):
    return "{} ({}/{})".format(repo.html_url,
                               repo.stargazers_count,
                               repo.raw_data['subscribers_count'])


def main():

    parser = ArgumentParser(description="Show a user's Github stars")
    parser.add_argument('-u',
                        '--username',
                        help='Github Username',
                        type=str,
                        default=GITHUB_USERNAME)
    args = parser.parse_args()
    username = args.username

    gh = Github(GITHUB_USERNAME, GITHUB_PASS)
    usr = gh.get_user(username)
    for repo in usr.get_starred():
        print(u"{} ({}) @ {}".format(
            repo.full_name, repo.description, repo.html_url))


if __name__ == "__main__":
    main()
