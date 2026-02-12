#!/bin/bash
set -e
NEW_TOKEN=$(gh auth token)
VAULT=~/api-keys

# Update vault
sed -i "s/^GITHUB_TOKEN=.*/GITHUB_TOKEN=$NEW_TOKEN/" $VAULT/github.env

# Commit and push
cd $VAULT
git add github.env
git commit -m "Rotate GitHub CLI token"
git push

# Update Netlify and other CI envs
netlify env:set GITHUB_TOKEN "$NEW_TOKEN" --context production
