#!./bin/python


# install https://github.com/PyGithub/PyGithub
from github import Github
from datetime import datetime, date
from argparse import ArgumentParser
from config import GITHUB_USERNAME, GITHUB_PASS, GITHUB_AUTHOR, GITHUB_ORGS


def is_work_repo(url):
    for org in GITHUB_ORGS:
        if '/{}/'.format(org) in url:
            return True
    return False


def main():

    parser = ArgumentParser(description="Retrieve Github activity")
    parser.add_argument('month', type=int, help='Month for activity log')
    args = parser.parse_args()
    month = args.month
    g = Github(GITHUB_USERNAME, GITHUB_PASS)
    usr = g.get_user(GITHUB_USERNAME)

    year = datetime.now().year

    start = date(year=year, month=month, day=1)

    for event in usr.get_public_events():
        # go back in history until the start date is reached
        if event.type != u"PushEvent":
            continue
        if event.created_at.date() <= start:
            break
        repo_url = event._repo.value.html_url
        if not is_work_repo(repo_url):
            continue
        repo = repo_url.split('/')[-1]
        commits = event.payload['commits']
        for commit in commits:
            if GITHUB_AUTHOR not in commit['author']['name'].lower():
                continue
            print(event.created_at.date(), " - ", repo, ": ",
                  commit['message'])


if __name__ == "__main__":
    main()
