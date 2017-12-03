#!/bin/bash
# to run type source basic_git_push.sh into command line

module load git

echo adding all files to commit
git add *

echo commiting with generic message
git commit -m "cleaning up"

echo pushing commit to master
git push
