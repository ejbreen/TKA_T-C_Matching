#!/bin/bash
module load git

echo adding all files to commit
git add *

echo commiting with generic message
git commit -m "generic commit from flux"

echo pushing commit to master
git push
