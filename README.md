<h1 align="center">
  git-tools
</h1>

<h4 align="center">
  CLI tools that help you to automate some routine operations
</h4>

<p align="center">
  <a href="https://github.com/digitalduke/git-tools/blob/master/LICENSE">
    <img alt="License MIT" src="https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square">
  </a>
  <a href="https://www.python.org/">
    <img alt="Python" src="https://img.shields.io/pypi/pyversions/Django.svg?style=flat-square">
  </a>
  <a href="https://www.debian.org/">
    <img alt="Best distro ever" src="https://img.shields.io/badge/platform-linux-yellow.svg?style=flat-square">
  </a>
</p>

#### Install

.deb package will be coming soon, sorry, for now, you may just clone this repository. 

#### Config

1. Go to your profile [settings](https://github.com/settings/tokens) and create [new access token](https://github.com/settings/tokens/new) with repo scope.

2. Then store this token to config file:
```bash
python3 daily-report.py --store-token <token>
```

3. and add repositories names, for which you will need reports, into config file:
```bash
python3 daily-report.py --store-repository <username/repository>
```

#### Use

##### `daily-report.py`
```bash
# show your daily activity on GitHub for today
python3 daily-report.py

# show activity for the specific date
python3 daily-report.py --date 2018-11-25

```

##### `purge-branches.py`
```bash
# show branches (and doesn't do any changes) that has been merged to master and can be cleaned
python3 purge-branches.py --dry-run

# clear repository from unnecessary branches
python3 purge-branches.py

# exclude branch from purge
python3 purge-branches.py --store-exclusion <branch-name>

# remove branch from exclusion list
python3 purge-branches.py --remove-exclusion <branch-name>

# clear repository from unnecessary branches including those in exclusion list
python3 purge-branches.py --force

# purge branches with no stdout
python3 purge-branches [-q|--quiet]

```

#### Contribute
Contributions are welcome. Have new ideas? please open new [Feature request](https://github.com/digitalduke/git-tools/issues/new?template=feature_request.md). If you find any bugs, please open [Bug report](https://github.com/digitalduke/git-tools/issues/new?template=bug_report.md) in order to report it.

If you consider to contribute, you are awesome! See project [wiki](https://github.com/digitalduke/git-tools/wiki) for instructions. 
