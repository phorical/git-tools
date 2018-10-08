from datetime import date, datetime
from github import Github, BadCredentialsException

ACCESS_TOKEN = ""
REPO_NAME = "a-iv/100maketov"

today = datetime.combine(date.today(), datetime.min.time())

github = Github(ACCESS_TOKEN)
user = github.get_user()

try:
    repo = github.get_repo(REPO_NAME)
except (Exception, BadCredentialsException) as error:
    print("Can't get repo %s" % REPO_NAME)

try:
    closed_issues = user.get_issues(state="closed", since=today)
    print('Daily closed issues:', closed_issues.totalCount)
    for issue in closed_issues:
        print('[%s](%s) %s' % (issue.number, issue.html_url, issue.title))
    print()
except (Exception, BadCredentialsException) as error:
    print("Can't get list of issues.")

try:
    commits = repo.get_commits(since=today, author=user)
    print('Daily commits in repo "%s" total: %s' % (REPO_NAME, commits.totalCount))
    for commit in commits:
        if not commit.commit.message.startswith("Merge"):
            print('[%s](%s) %s' % (commit.sha[:7], commit.html_url, commit.commit.message))
except (Exception, BadCredentialsException) as error:
    print("Can't get list of commits.")

