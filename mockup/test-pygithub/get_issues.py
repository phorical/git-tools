from datetime import date, datetime
from github import Github

ACCESS_TOKEN = ""

today = datetime.combine(date.today(), datetime.min.time())

github = Github(ACCESS_TOKEN)
user = github.get_user()

closed_issues = user.get_issues(state="closed", since=today)
print('daily closed issues:', closed_issues.totalCount)

for issue in closed_issues:
    print('[%s](%s) %s' % (issue.number, issue.html_url, issue.title))
