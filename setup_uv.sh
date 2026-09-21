#!/bin/bash

# For this to work, uv has to be installed, either through
# your linux package manager or from uv directly like so :
#
# curl -LsSf https://astral.sh/uv/install.sh | sh
# source $HOME/.local/bin/env

# Check if uv is installed, exit if not.
which uv &> /dev/null
status="$?"
if [ "$status" -ne 0 ]
then
 echo uv is not installed, exiting
 exit -1
fi

# Initialize a bare bones uv project.
uv init --name get_dp_health --description "API to see if a data provider is behaving" --bare .

# Install Packages
uv add -r requirements.txt

# Append the footer to pyproject.toml we just generated
cat pyproject.toml pyproject.footer > pyproject.tmp
mv pyproject.tmp pyproject.toml

# Install the hook according to .pre-commit-config.yaml
uv run pre-commit install

