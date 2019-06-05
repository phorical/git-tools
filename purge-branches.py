#!/usr/bin/python3
import subprocess
import argparse
import os
import json

SCRIPT_FOLDER = "git-tools"
EXCLUSIONS_FILENAME = "purge-branches.json"

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
parser.add_argument(
    "-q","--quiet",
    action="store_true",
    dest="quiet",
    help="quiet mode, do not print"
)
parser.add_argument(
    "--store-exclusion",
    action="store",
    default=None,
    metavar="EXCLUSION",
    type=str,
    dest="store_exclusion",
    help="save exclusion name into configuration file"
)
parser.add_argument(
    "--remove-exclusion",
    action="store",
    default=None,
    metavar="EXCLUSION",
    type=str,
    dest="remove_exclusion",
    help="remove exclusion name from configuration file"
)
parser.add_argument(
    "--list-exclusions",
    action="store_true",
    dest="list_exclusions",
    help="list exclusions stored in configuration file"
)
parser.add_argument(
    "--force",
    action="store_true",
    dest="force",
    help="ignores exclusion configurations, forces prune of all merged branches"
)



def get_config_path():
    xdg_config_home_dir = os.environ.get("XDG_CONFIG_HOME", "")
    home_dir = os.environ.get("HOME", "")
    path = ""
    if xdg_config_home_dir:
        path = os.path.join(xdg_config_home_dir, SCRIPT_FOLDER)
    elif home_dir:
        path = os.path.join(home_dir, ".config", SCRIPT_FOLDER)
    return path

def get_exclusions_file_full_path():
    return os.path.join(get_config_path(), EXCLUSIONS_FILENAME)

def get_options(quiet):
    options = {}
    try:
        with open(get_exclusions_file_full_path()) as config_file:
            options = json.load(config_file)
    except FileNotFoundError:
        if not quiet:
            print("No exclusions file.")
    return options

def save_options(options):
    os.makedirs(get_config_path(), exist_ok=True)

    with open(get_exclusions_file_full_path(), "w") as config_file:
        json.dump(options, config_file)


def run():
    args = parser.parse_args()
    options = get_options(args.quiet)
    
    if args.store_exclusion:
        exclusions = list(options.get("exclusions", ""))
        new_exclusion = args.store_exclusion
        if new_exclusion not in exclusions:
            exclusions.append(new_exclusion)
            options.update(exclusions=exclusions)
            save_options(options)
            if not args.quiet:
                print("Repository %s successfully added to exclusions list." % new_exclusion)
        else:
            if not args.quiet:
                print("Repository %s already in exclusions list." % new_exclusion)
    elif args.remove_exclusion:
        exclusions = list(options.get("exclusions", ""))
        repo = args.remove_exclusion
        if repo in exclusions:
            exclusions.remove(repo)
            options.update(exclusions=exclusions)
            save_options(options)
            if not args.quiet:
                print("Repository %s successfully removed from exclusion list." % repo)
        else:
            if not args.quiet:
                print("Repository %s not in exclusion list." % repo)
    elif args.list_exclusions:
        exclusions = list(options.get("exclusions", ""))
        if not args.quiet:
            for repo in exclusions:
                print(repo)
    else:
        command = ["git", "branch", "--merged"]
        git_process = subprocess.run(
            args=command,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True
        )

        if git_process.returncode != 0:
            if not args.quiet:
                print("something wrong: %s" % git_process.stderr)
        else:
            repositories = [
                repo.replace(" ", "")
                for repo in git_process.stdout.split("\n")
                if repo != "" and repo != "  master" and not repo.startswith("* ")
            ]
            
            if not args.force:
                exclusions = list(options.get("exclusions", ""))
                repositories = [
                    repo
                    for repo in repositories
                    if repo not in exclusions
                ]

            repo_count = len(repositories)
            if repo_count == 0:
                if not args.quiet:
                    print("nothing for purge")
            else:
                if args.dry_run:
                    if not args.quiet:
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
                        if not args.quiet:
                            print("something wrong: %s" % git_process.stderr)
                    else:
                        if not args.quiet:
                            print("all done, purged %d branch(es)" % repo_count)


if __name__ == "__main__":
    run()
