#!/usr/bin/python3
import subprocess
import argparse

parser = argparse.ArgumentParser(
    description="Clear repository from unnecessary branches.",
    epilog="Find more information at https://digitalduke.github.io/git-tools/"
)

parser.add_argument(
    "--version",
    action="version",
    version="purge branches version 1.0"
)
parser.add_argument(
    "--dry-run",
    action="store_true",
    dest="dry_run",
    help="only report, doesn't do any real changes"
)


def run():
    args = parser.parse_args()

    command = ["git", "branch", "--merged"]
    git_process = subprocess.run(
        args=command,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    if git_process.returncode != 0:
        print("something wrong: %s" % git_process.stderr)
    else:
        repositories = [
            repo.replace(" ", "")
            for repo in git_process.stdout.split("\n")
            if repo != "" and repo != "  master" and not repo.startswith("* ")
        ]

        repo_count = len(repositories)
        if repo_count == 0:
            print("nothing for purge")
        else:
            if args.dry_run:
                print("can purge this branches:")
                for repo in repositories:
                    print(" %s" % repo)
            else:
                command = ["git", "branch", "-d"]
                for repo in repositories:
                    command.append(repo)
                git_process = subprocess.run(
                    args=command,
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    universal_newlines=True
                )
                if git_process.returncode != 0:
                    print("something wrong: %s" % git_process.stderr)
                else:
                    print("all done, purged %d branch(es)" % repo_count)


if __name__ == "__main__":
    run()
