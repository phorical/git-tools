#!/bin/bash
# Удалить все ветки, кроме master и которые, не смержены в текущую ветку.

git branch --merged | grep -v "\*" | grep -v master | xargs -n 1 git branch -d

