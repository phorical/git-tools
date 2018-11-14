import os
import argparse

from dateutil.parser import parse
from datetime import date, datetime, timedelta
from github import Github, BadCredentialsException


SCRIPT_FOLDER = 'daily-report'

parser = argparse.ArgumentParser(description="Show daily activity on GitHub and (optional) send via e-mail.",
                                 epilog="Find more information at https://github.com/digitalduke/github-tools")

parser.add_argument('--date',
                    action='store',
                    default='today',
                    metavar="YYYY-MM-DD",
                    type=str,
                    help='Date in ISO 8601 format, for example: 2018-10-16. Default is today.')

args = parser.parse_args()

if args.date == 'today':
    date_since = datetime.combine(date.today(), datetime.min.time())
    date_until = datetime.combine(date_since.date() + timedelta(days=1), datetime.min.time())
else:
    date_since = parse(args.date)
    date_since = datetime.combine(date_since, datetime.min.time())
    date_until = datetime.combine(date_since.date() + timedelta(days=1), datetime.min.time())


def get_config_path():
    xdg_config_home_dir = os.environ.get('XDG_CONFIG_HOME', '')
    home_dir = os.environ.get('HOME', '')
    path = ""
    if xdg_config_home_dir:
        path = os.path.join(xdg_config_home_dir, SCRIPT_FOLDER)
    elif home_dir:
        path = os.path.join(home_dir, '.config', SCRIPT_FOLDER)
    return path


def get_config_file_full_path():
    return os.path.join(get_config_path(), 'daily-report.conf')


ACCESS_TOKEN = ""
REPO_NAME = "a-iv/100maketov"

github = Github(ACCESS_TOKEN)
user = github.get_user()

try:
    repo = github.get_repo(REPO_NAME)
except (Exception, BadCredentialsException) as error:
    print("Can't get repo %s" % REPO_NAME)


try:
    closed_issues = user.get_issues(state="closed", since=date_since)
    print("List of daily closed issues")
    for issue in closed_issues:
        if date_since <= issue.closed_at <= date_until:
            print(issue.number, issue.html_url, issue.title)
    print()
except (Exception, BadCredentialsException) as error:
    print("Can't get list of closed issues.")


try:
    commits = repo.get_commits(since=date_since, author=user)
    print("List of daily commits in repo \"%s\" in PR which already closed" % REPO_NAME)
    for commit in commits:
        print(commit.sha[:7], commit.html_url, commit.commit.message)
    print()
except (Exception, BadCredentialsException) as error:
    print("Can't get list of commits in PR which already closed.")


try:
    pulls = repo.get_pulls(state="open", base="master")
    if pulls:
        print("List of daily commits in repo \"%s\" in PR which don't closed" % REPO_NAME)

    for pr in pulls:
        commits = pr.get_commits()
        print_pr_number = True

        for commit in commits:

            if not commit.committer.login == user.login:
                continue

            if date_since <= commit.commit.author.date <= date_until:
                if print_pr_number:
                    print("PR#%s %s %s" % (pr.number, pr.html_url, pr.title))
                    print_pr_number = False

                print(commit.sha[:7], commit.html_url, commit.commit.message)

except (Exception, BadCredentialsException) as error:
    print("Can't get list of commits in opened PR.")


print("\r\nDone.")
