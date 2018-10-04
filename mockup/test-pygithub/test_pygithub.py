from github import Github

ACCESS_TOKEN = ""
g = Github(ACCESS_TOKEN)

for repo in g.get_user().get_repos():
    print(repo.name)
