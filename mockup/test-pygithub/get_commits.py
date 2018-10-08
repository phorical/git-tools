from datetime import date, datetime
from github import Github

ACCESS_TOKEN = ""
REPO_NAME = "a-iv/100maketov"

today = datetime.combine(date.today(), datetime.min.time())

github = Github(ACCESS_TOKEN)
user = github.get_user()

repo = github.get_repo(REPO_NAME)

commits = repo.get_commits(since=today, author=user)

for commit in commits:
    print('[%s](%s) %s' % (commit.sha[:7], commit.html_url, commit.commit.message))
